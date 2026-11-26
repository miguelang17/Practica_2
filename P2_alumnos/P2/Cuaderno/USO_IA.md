# Declaración de uso de IA — Práctica 2

**Grupo:** *(número)* · **Integrantes:** *(apellido 1)*, *(apellido 2)*, *(apellido 3)*, *(apellido 4)*
**Fecha:** *(fecha de entrega)*

---

## Para qué sirve este fichero

En esta asignatura el uso de IA generativa está **permitido, con declaración**, y este fichero es
esa declaración. Es un **entregable de la Práctica 2**: si falta o está vacío, resta puntos.

Rellenarlo con sinceridad no os cuesta nada. Lo que se evalúa es vuestra comprensión, y se os
preguntará por vuestro propio cuaderno.

## Qué hay que escribir

Para la Práctica 2, indicad:

* **la herramienta o el servicio**, con su nombre: «un LLM» no es una declaración;
* **el propósito**, por ejemplo ideas, explicaciones, depuración, sugerencias de código o
  revisión de redacción;
* **los ficheros o secciones afectados**, con precisión: «Ejercicio 4(b), el método `predict`
  de nuestro KNN», no «parte del código»;
* **cómo comprobasteis el resultado**. Esta es la parte que más importa: decid qué hicisteis
  para aseguraros de que era correcto.

**No hace falta adjuntar conversaciones completas ni registros de instrucciones.**

**Si no usasteis IA generativa, basta una frase que lo diga.** En ese caso, borrad la tabla y
escribid esa frase.

## Declaración

| Herramienta o servicio | Propósito | Ficheros o secciones afectados | Cómo se comprobó el resultado |
|---|---|---|---|
| Herramienta o servicio | Propósito | Ficheros o secciones afectados | Cómo se comprobó el resultado |
|---|---|---|---|
| Claude | Sugerencia de trabajar en escala logarítmica en el KNN de regresión local: ajustar la recta sobre log10(latencia) y deshacer con 10^ẑ, para que las predicciones sean positivas y coherentes con la métrica MAE_log.  | Ejercicio 5(a): texto con z_c = log10(ỹ_c) y ŷ = 10^ẑ. Celda final: definición de `modelo_final_latencia`. | Validamos el modelo final con la latencia en nanosegundos y la métrica oficial (`scorer_log`), y comprobamos que daba el mismo MAE_log que la validación en escala log (≈0.112 con K=30). Comprobamos que el `assert` de predicciones positivas pasa y que `comprobar_estimador` sigue dando "TODO CORRECTO". |
| *(p. ej. Claude)* | *(p. ej. depurar un error de matplotlib)* | *(p. ej. Ejercicio 5(b), el método `fit`)* | *(p. ej. volvimos a ejecutar la celda y comprobamos que el caso particular coincide con `KNeighborsRegressor`)* |
| | | | |



| Herramienta o servicio | Propósito | Ficheros o secciones afectados | Cómo se comprobó el resultado |
|---|---|---|---|
| ChatGPT | Explicación del uso de `clone` de scikit-learn para crear una copia independiente de cada estimador en cada partición de la validación cruzada, evitando reutilizar modelos ya entrenados. | Ejercicio 5(a): código de comparación entre `KNNRegresionLocal` y `KNeighborsRegressor` mediante `GroupKFold`. | Comprobamos que en cada partición se creaba un estimador nuevo, que se entrenaba exclusivamente con los datos de entrenamiento correspondientes y que ambos modelos se evaluaban sobre las mismas particiones. |
| ChatGPT | Ayuda para elaborar un código que permitiera identificar qué característica selecciona OneR en cada partición de la validación cruzada y comprobar si la selección cambia al modificar el número de intervalos (`n_bins`). |Ejercicio 2(b): código de evaluación con `GroupKFold` y tabla resumen de las características seleccionadas para cada valor de `n_bins`. | Ejecutamos el código para los distintos valores de `n_bins` y comprobamos que la tabla mostraba correctamente la característica seleccionada en cada una de las cinco particiones. |
| Gemini | Asesoramiento para comprobar si existía solapamiento de configuraciones entre los conjuntos de entrenamiento y validación en los dos esquemas de partición, `GroupKFold` y `KFold`. | Ejercicio 1(b): código de validación cruzada y comprobación del solapamiento de configuraciones mediante `grupos_latencia`. | Calculamos el número de configuraciones compartidas entre entrenamiento y validación en cada partición. Comprobamos que `GroupKFold` no presentaba solapamientos, mientras que `KFold` sí podía incluir configuraciones repetidas en ambos conjuntos. |
| Claude | Sugerencia de trabajar en escala logarítmica en el KNN de regresión local: ajustar la recta sobre log10(latencia) y deshacer con 10^ẑ, para que las predicciones sean positivas y coherentes con la métrica MAE_log. | Ejercicio 5(a): texto con z_c = log10(ỹ_c) y ŷ = 10^ẑ. Celda final: definición de `modelo_final_latencia`. | Validamos el modelo final con la latencia en nanosegundos y la métrica oficial (`scorer_log`), y comprobamos que daba el mismo MAE_log que la validación en escala log (≈0.112 con K=30). Comprobamos que el `assert` de predicciones positivas pasa y que `comprobar_estimador` sigue dando "TODO CORRECTO". |
| ChatGPT | Asesoramiento sobre la construcción de la matriz de diseño de la regresión lineal local mediante `np.column_stack`, incorporando una columna de unos para estimar el término independiente. | Ejercicio 5(a): método `predict` de la clase `KNNRegresionLocal`, construcción de la matriz `A`. | Comprobamos las dimensiones de la matriz construida y verificamos que permitía ajustar correctamente la regresión con los vecinos seleccionados. |
| ChatGPT | Explicación del uso de `np.linalg.lstsq` para obtener los coeficientes de la regresión lineal mediante mínimos cuadrados ordinarios, sin recurrir a un estimador de regresión de scikit-learn. | Ejercicio 5(a): método `predict` de la clase `KNNRegresionLocal`, cálculo de los coeficientes. | Comprobamos que las predicciones se ejecutaban correctamente y evaluamos el error mediante validación cruzada agrupada (`GroupKFold`), comparándolo con el KNN convencional. |
| ChatGPT | Asesoramiento sobre el tratamiento de las cinco ejecuciones de cada configuración, agrupándolas mediante la mediana para evitar que las repeticiones se considerasen configuraciones independientes. | Ejercicio 5(a): método `fit` de la clase `KNNRegresionLocal` y explicación del diseño del modelo. | Comprobamos que el estimador agrupaba las observaciones en 1000 configuraciones y que las medianas calculadas coincidían con las obtenidas directamente a partir de los datos. |
| ChatGPT | Asesoramiento sobre la transformación logarítmica de la variable objetivo y la recuperación de las predicciones a la escala original mediante una potencia de diez. | Ejercicio 5(a): parámetro `log_objetivo` de la clase `KNNRegresionLocal`. | Evaluamos el modelo con la métrica MAE_log y comprobamos que las predicciones devueltas estaban expresadas en nanosegundos y eran positivas. |

## Lo que sigue siendo vuestro

El grupo es **plenamente responsable** de que todo lo entregado sea correcto: cada resultado,
el código, la interpretación, las referencias y la reproducibilidad del cuaderno. También de
**entender todo lo que entrega**.

Hay dos límites que no se negocian:

* **No se permite ninguna ayuda de IA generativa durante las preguntas individuales.**
* Si vuestra propia explicación de vuestro trabajo contradice esta declaración, el asunto es de
  **integridad académica**, no de calificación.

Las normas de integridad académica de la universidad se siguen aplicando en su totalidad.
