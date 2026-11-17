"""Comprobaciones mínimas de un estimador propio de scikit-learn (Práctica 2).

Código proporcionado por el curso. No lo modifiquéis. Uso:

    from comprobar_estimador import comprobar_estimador
    comprobar_estimador(MiKNNClasificador(...), X, y)

``X`` es la matriz **numérica** que recibe vuestro modelo (ya preprocesada) e ``y`` la variable
objetivo. Para ir rápido se usan como mucho 800 patrones.

No sustituye a ``sklearn.utils.estimator_checks.check_estimator``, que podéis investigar; aquí se
comprueba lo que pide el enunciado.
"""
from __future__ import annotations

import inspect

import numpy as np
from sklearn.base import (BaseEstimator, ClassifierMixin, RegressorMixin, clone, is_classifier,
                          is_regressor)
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

__all__ = ["comprobar_estimador"]

_CLASES_VECINOS = ("KNeighborsClassifier", "KNeighborsRegressor", "RadiusNeighborsClassifier",
                   "RadiusNeighborsRegressor", "NearestCentroid", "NearestNeighbors")


def comprobar_estimador(est, X, y, max_patrones: int = 800) -> bool:
    """Imprime una lista de comprobaciones y devuelve True si todas se cumplen."""
    res: list[tuple[str, str]] = []           # (estado, texto); estado en {"OK", "FALLA", "INFO"}

    def ok(texto: str, cond: bool) -> None:
        res.append(("OK" if cond else "FALLA", texto))

    def info(texto: str) -> None:
        res.append(("INFO", texto))

    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    if len(X) > max_patrones:
        idx = np.random.default_rng(0).choice(len(X), size=max_patrones, replace=False)
        X, y = X[np.sort(idx)], y[np.sort(idx)]
    clasif = is_classifier(est)
    regr = is_regressor(est)
    mixin = ClassifierMixin if clasif else RegressorMixin
    nombre_mixin = mixin.__name__

    # 1. Herencia
    mro = type(est).__mro__
    ok("es un clasificador o un regresor de scikit-learn", clasif or regr)
    ok("hereda de BaseEstimator", isinstance(est, BaseEstimator))
    if clasif or regr:
        ok(f"hereda de {nombre_mixin} y de BaseEstimator, en ese orden",
           mixin in mro and BaseEstimator in mro and mro.index(mixin) < mro.index(BaseEstimator))
    heredadas = [c.__name__ for c in mro if c.__name__ in _CLASES_VECINOS]
    ok("no hereda de ninguna clase de vecinos de scikit-learn (usadlas dentro, no como clase madre)",
       not heredadas)

    # 2. __init__ sin lógica y parámetros
    params = est.get_params(deep=False)
    firma = [p for p in inspect.signature(type(est).__init__).parameters if p != "self"]
    ok("__init__ guarda cada parámetro con su mismo nombre", set(params) == set(firma))
    ok("__init__ no crea atributos aparte de los parámetros",
       set(k for k in vars(est) if not k.startswith("__")) <= set(params))
    ok("clone() conserva los parámetros", clone(est).get_params(deep=False) == params)

    # 3. fit y predict
    e1 = clone(est)
    antes = set(vars(e1))
    devuelto = e1.fit(X, y)
    ok("fit devuelve el propio estimador", devuelto is e1)
    nuevos = [a for a in set(vars(e1)) - antes if a.endswith("_") and not a.startswith("__")]
    ok("fit guarda lo aprendido en atributos terminados en guion bajo", len(nuevos) > 0)
    pred = np.asarray(e1.predict(X))
    ok("predict devuelve una predicción por patrón", pred.shape == (len(X),))
    if clasif:
        ok("tiene classes_ y predice solo clases de classes_",
           hasattr(e1, "classes_") and np.isin(pred, e1.classes_).all())
    else:
        ok("predice números finitos", np.issubdtype(pred.dtype, np.number) and np.isfinite(pred).all())
    ok("dos ajustes con los mismos parámetros dan las mismas predicciones",
       np.array_equal(np.asarray(clone(est).fit(X, y).predict(X)), pred))
    antes_pred = dict(vars(e1))
    copias = {a: v.copy() for a, v in antes_pred.items() if isinstance(v, np.ndarray)}
    e1.predict(X)
    despues = vars(e1)
    ok("predict no modifica el estimador",
       set(despues) == set(antes_pred) and all(despues[a] is antes_pred[a] for a in antes_pred)
       and all(np.array_equal(despues[a], c) for a, c in copias.items()))

    # 4. Integración con scikit-learn
    cv = StratifiedKFold(3, shuffle=True, random_state=0) if clasif else KFold(3, shuffle=True, random_state=0)
    try:
        punt = cross_val_score(Pipeline([("escalado", StandardScaler()), ("modelo", clone(est))]), X, y, cv=cv)
        ok("funciona dentro de un Pipeline y con cross_val_score", np.isfinite(punt).all())
    except Exception as err:                       # noqa: BLE001
        ok(f"funciona dentro de un Pipeline y con cross_val_score ({type(err).__name__}: {err})", False)

    # 5. Información: ¿en qué se diferencia del KNN de scikit-learn?
    k = params.get("n_neighbors", params.get("K", params.get("k", 5)))
    try:
        k = int(k)
        base = (KNeighborsClassifier if clasif else KNeighborsRegressor)(n_neighbors=k).fit(X, y)
        pb = base.predict(X)
        if clasif:
            info(f"coincide con KNeighborsClassifier(n_neighbors={k}) en el "
                 f"{100 * np.mean(pb == pred):.1f} % de las predicciones sobre estos patrones")
        else:
            info(f"diferencia media con KNeighborsRegressor(n_neighbors={k}): "
                 f"{np.mean(np.abs(pb - pred)):.4g} sobre estos patrones")
    except Exception:                              # noqa: BLE001
        info("no se ha podido comparar con el KNN de scikit-learn")

    for estado, texto in res:
        print(f"  [{estado}] {texto}")
    todo = all(e != "FALLA" for e, _ in res)
    print("TODO CORRECTO" if todo else "HAY COMPROBACIONES QUE FALLAN")
    return todo
