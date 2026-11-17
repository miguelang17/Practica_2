"""OneR para clasificación y para regresión, compatible con scikit-learn.

Código proporcionado por el curso para la Práctica 2 (Machine Learning, MUIA 2026/2027).
No hace falta modificarlo: se usa como cualquier otro estimador de scikit-learn, dentro de un
``Pipeline``, con ``cross_val_score``, con ``GridSearchCV``, etc.

Cómo funciona
-------------
OneR (*One Rule*) construye una regla para **cada** característica y se queda con la que menos
se equivoca en el conjunto de entrenamiento.

* Una característica **nominal** (texto) define un grupo por cada valor.
* Una característica **numérica** se discretiza antes en ``n_bins`` intervalos, con cortes
  calculados **solo con los datos de entrenamiento**: por cuantiles (``strategy="quantile"``, cada
  intervalo con un número parecido de patrones) o de igual anchura (``strategy="uniform"``).
  Si la característica tiene pocos valores distintos, salen menos intervalos.
* En clasificación, cada grupo predice su **clase mayoritaria** y el error es la tasa de fallos.
* En regresión, cada grupo predice la **media** (``aggregate="mean"``, error cuadrático medio) o
  la **mediana** (``aggregate="median"``, error absoluto medio) de la variable objetivo.
* Un valor nominal que no apareció en el entrenamiento recibe la predicción por defecto: la clase
  mayoritaria o la media/mediana global.

Atributos útiles tras ``fit``
-----------------------------
``feature_name_``   la característica elegida
``errors_``         error de entrenamiento de la regla de **cada** característica (``pandas.Series``)
``describe()``      la regla elegida, escrita en texto
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.utils.multiclass import check_classification_targets
from sklearn.utils.validation import check_is_fitted, column_or_1d

__all__ = ["OneRClassifier", "OneRRegressor"]


class _OneRBase(BaseEstimator):
    """Lógica común a los dos OneR. No se usa directamente."""

    # ------------------------------------------------------------------ etiquetas de sklearn
    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.input_tags.string = True
        return tags

    # ------------------------------------------------------------------ validación de X
    def _validar_X(self, X, reset: bool):
        nombre = type(self).__name__
        if sparse.issparse(X):
            raise TypeError(f"{nombre} no admite datos dispersos (sparse); conviértelos a denso.")
        if isinstance(X, pd.DataFrame):
            df = X
            nombres = np.asarray([str(c) for c in X.columns], dtype=object)
        else:
            arr = np.asarray(X)
            if np.iscomplexobj(arr):
                raise ValueError("Complex data not supported")
            if arr.ndim == 1:
                raise ValueError(
                    "Expected 2D array, got 1D array instead. Reshape your data either using "
                    "array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) "
                    "if it contains a single sample.")
            if arr.ndim != 2:
                raise ValueError(f"Se esperaba una matriz bidimensional y se recibió una de {arr.ndim} dimensiones.")
            df = pd.DataFrame(arr)
            nombres = None
        n, k = df.shape
        if n == 0:
            raise ValueError(f"Found array with 0 sample(s) (shape={df.shape}) while a minimum of 1 is required.")
        if k == 0:
            raise ValueError(f"Found array with 0 feature(s) (shape={df.shape}) while a minimum of 1 is required.")

        if reset:
            self.n_features_in_ = k
            if nombres is not None:
                self.feature_names_in_ = nombres
            elif hasattr(self, "feature_names_in_"):
                del self.feature_names_in_
        else:
            ajustado_con_nombres = hasattr(self, "feature_names_in_")
            if nombres is not None and not ajustado_con_nombres:
                warnings.warn(f"X has feature names, but {nombre} was fitted without feature names", UserWarning)
            if nombres is None and ajustado_con_nombres:
                warnings.warn(f"X does not have valid feature names, but {nombre} was fitted with feature names",
                              UserWarning)
            if nombres is not None and ajustado_con_nombres and list(nombres) != list(self.feature_names_in_):
                raise ValueError("The feature names should match those that were passed during fit.")
            if k != self.n_features_in_:
                raise ValueError(f"X has {k} features, but {nombre} is expecting {self.n_features_in_} "
                                 "features as input.")

        columnas = []
        for j in range(k):
            col = df.iloc[:, j]
            if reset:
                tipo = "numerica" if self._es_numerica(col) else "nominal"
            else:
                tipo = self.feature_types_[j]
            if tipo == "numerica":
                try:
                    v = np.asarray(col, dtype=float)
                except (TypeError, ValueError) as err:
                    raise ValueError(f"La característica {j} era numérica en el entrenamiento y ahora "
                                     f"no lo es: {err}") from err
                if not np.all(np.isfinite(v)):
                    raise ValueError("Input X contains NaN or infinity.")
            else:
                v = np.asarray(col.astype(str), dtype=object)
            columnas.append((tipo, v))
        if reset:
            self.feature_types_ = [t for t, _ in columnas]
        return columnas

    @staticmethod
    def _es_numerica(col: pd.Series) -> bool:
        if pd.api.types.is_bool_dtype(col):
            return False
        if pd.api.types.is_numeric_dtype(col):
            return True
        try:
            np.asarray(col, dtype=float)
            return True
        except (TypeError, ValueError):
            return False

    # ------------------------------------------------------------------ discretización
    def _cortes(self, v: np.ndarray) -> np.ndarray:
        if not isinstance(self.n_bins, (int, np.integer)) or self.n_bins < 1:
            raise ValueError(f"n_bins debe ser un entero mayor o igual que 1; se recibió {self.n_bins!r}.")
        if self.strategy not in ("quantile", "uniform"):
            raise ValueError(f"strategy debe ser 'quantile' o 'uniform'; se recibió {self.strategy!r}.")
        if self.n_bins == 1:
            return np.array([], dtype=float)
        if self.strategy == "quantile":
            cortes = np.quantile(v, np.linspace(0, 1, self.n_bins + 1)[1:-1])
        else:
            cortes = np.linspace(v.min(), v.max(), self.n_bins + 1)[1:-1]
        return np.unique(cortes)

    @staticmethod
    def _grupo(v: np.ndarray, tipo: str, cortes) -> np.ndarray:
        if tipo == "numerica":
            return np.searchsorted(cortes, v, side="right")
        return v

    # ------------------------------------------------------------------ ajuste genérico
    def _ajustar(self, columnas, y):
        errores, reglas, cortes_por_car = [], [], []
        for tipo, v in columnas:
            cortes = self._cortes(v) if tipo == "numerica" else None
            g = self._grupo(v, tipo, cortes)
            regla = self._regla(g, y)
            pred = np.array([regla[x] for x in g], dtype=object if self._es_clasificador() else float)
            errores.append(self._error(y, pred))
            reglas.append(regla)
            cortes_por_car.append(cortes)
        errores = np.asarray(errores, dtype=float)
        mejor = int(np.argmin(errores))            # empate: la primera característica
        nombres = (list(self.feature_names_in_) if hasattr(self, "feature_names_in_")
                   else [f"x{j}" for j in range(len(columnas))])
        self.feature_ = mejor
        self.feature_name_ = nombres[mejor]
        self.errors_ = pd.Series(errores, index=nombres, name="error_entrenamiento")
        self.rule_ = reglas[mejor]
        self.bin_edges_ = cortes_por_car[mejor]
        return self

    def _predecir(self, X):
        check_is_fitted(self)
        columnas = self._validar_X(X, reset=False)
        tipo, v = columnas[self.feature_]
        g = self._grupo(v, tipo, self.bin_edges_)
        salida = [self.rule_.get(x, self.default_) for x in g]
        return np.asarray(salida, dtype=self._tipo_salida())

    # ------------------------------------------------------------------ descripción en texto
    def describe(self) -> str:
        """Devuelve la regla elegida, escrita en texto."""
        check_is_fitted(self)
        lineas = [f"OneR eligió la característica «{self.feature_name_}» "
                  f"(error de entrenamiento {self.errors_.iloc[self.feature_]:.4f})."]
        if self.feature_types_[self.feature_] == "numerica":
            c = self.bin_edges_
            for b in sorted(self.rule_):
                if len(c) == 0:
                    tramo = "cualquier valor"
                elif b == 0:
                    tramo = f"< {c[0]:.6g}"
                elif b == len(c):
                    tramo = f">= {c[-1]:.6g}"
                else:
                    tramo = f"[{c[b - 1]:.6g}, {c[b]:.6g})"
                lineas.append(f"  {self.feature_name_} {tramo}  ->  {self._formato(self.rule_[b])}")
        else:
            for valor in sorted(self.rule_, key=str):
                lineas.append(f"  {self.feature_name_} = {valor}  ->  {self._formato(self.rule_[valor])}")
        lineas.append(f"  cualquier otro valor  ->  {self._formato(self.default_)}")
        return "\n".join(lineas)

    @staticmethod
    def _formato(valor) -> str:
        return f"{valor:.6g}" if isinstance(valor, (float, np.floating)) else str(valor)


class OneRClassifier(ClassifierMixin, _OneRBase):
    """OneR para clasificación.

    Parámetros
    ----------
    n_bins : int, por defecto 10
        Número de intervalos en que se discretiza cada característica numérica.
    strategy : {"quantile", "uniform"}, por defecto "quantile"
        Cortes por cuantiles o de igual anchura, calculados con el conjunto de entrenamiento.
    """

    def __init__(self, n_bins: int = 10, strategy: str = "quantile"):
        self.n_bins = n_bins
        self.strategy = strategy

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.classifier_tags.poor_score = True
        return tags

    def _es_clasificador(self) -> bool:
        return True

    def _tipo_salida(self):
        return self.classes_.dtype

    def fit(self, X, y):
        if y is None:
            raise ValueError(f"{type(self).__name__} requires y to be passed, but the target y is None.")
        y = column_or_1d(y, warn=True)
        if y.dtype.kind in "fc" and not np.all(np.isfinite(y)):
            raise ValueError("Input y contains NaN or infinity.")
        check_classification_targets(y)
        columnas = self._validar_X(X, reset=True)
        if len(y) != len(columnas[0][1]):
            raise ValueError(f"X e y tienen distinto número de patrones: {len(columnas[0][1])} y {len(y)}.")
        self.classes_, cuentas = np.unique(y, return_counts=True)
        self._orden = {c: i for i, c in enumerate(self.classes_[np.argsort(-cuentas, kind="stable")])}
        self.default_ = self.classes_[int(np.argmax(cuentas))]
        self._ajustar(columnas, y)
        del self._orden
        return self

    def _regla(self, g, y):
        df = pd.DataFrame({"g": g, "y": y})
        regla = {}
        for clave, sub in df.groupby("g", sort=False)["y"]:
            vc = sub.value_counts()
            maximo = vc.max()
            empatadas = [c for c in vc.index[vc == maximo]]
            # empate: la clase más frecuente en todo el entrenamiento
            regla[clave] = min(empatadas, key=lambda c: self._orden[c])
        return regla

    @staticmethod
    def _error(y, pred) -> float:
        return float(np.mean(np.asarray(y, dtype=object) != pred))

    def predict(self, X):
        return self._predecir(X)


class OneRRegressor(RegressorMixin, _OneRBase):
    """OneR para regresión.

    Parámetros
    ----------
    n_bins : int, por defecto 10
        Número de intervalos en que se discretiza cada característica numérica.
    strategy : {"quantile", "uniform"}, por defecto "quantile"
        Cortes por cuantiles o de igual anchura, calculados con el conjunto de entrenamiento.
    aggregate : {"mean", "median"}, por defecto "mean"
        Qué predice cada grupo. Con ``"mean"`` la característica se elige por el error cuadrático
        medio; con ``"median"``, por el error absoluto medio.
    """

    def __init__(self, n_bins: int = 10, strategy: str = "quantile", aggregate: str = "mean"):
        self.n_bins = n_bins
        self.strategy = strategy
        self.aggregate = aggregate

    def __sklearn_tags__(self):
        tags = super().__sklearn_tags__()
        tags.regressor_tags.poor_score = True
        return tags

    def _es_clasificador(self) -> bool:
        return False

    def _tipo_salida(self):
        return float

    def fit(self, X, y):
        if y is None:
            raise ValueError(f"{type(self).__name__} requires y to be passed, but the target y is None.")
        if self.aggregate not in ("mean", "median"):
            raise ValueError(f"aggregate debe ser 'mean' o 'median'; se recibió {self.aggregate!r}.")
        y = column_or_1d(y, warn=True)
        try:
            y = np.asarray(y, dtype=float)
        except (TypeError, ValueError) as err:
            raise ValueError(f"La variable objetivo debe ser numérica: {err}") from err
        if not np.all(np.isfinite(y)):
            raise ValueError("Input y contains NaN or infinity.")
        columnas = self._validar_X(X, reset=True)
        if len(y) != len(columnas[0][1]):
            raise ValueError(f"X e y tienen distinto número de patrones: {len(columnas[0][1])} y {len(y)}.")
        self.default_ = float(np.mean(y) if self.aggregate == "mean" else np.median(y))
        self._ajustar(columnas, y)
        return self

    def _regla(self, g, y):
        df = pd.DataFrame({"g": g, "y": y})
        agr = df.groupby("g", sort=False)["y"].agg(self.aggregate)
        return {k: float(v) for k, v in agr.items()}

    def _error(self, y, pred) -> float:
        if self.aggregate == "mean":
            return float(np.mean((y - pred) ** 2))
        return float(np.mean(np.abs(y - pred)))

    def predict(self, X):
        return self._predecir(X)
