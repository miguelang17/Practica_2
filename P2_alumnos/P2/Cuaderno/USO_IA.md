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

## Lo que sigue siendo vuestro

El grupo es **plenamente responsable** de que todo lo entregado sea correcto: cada resultado,
el código, la interpretación, las referencias y la reproducibilidad del cuaderno. También de
**entender todo lo que entrega**.

Hay dos límites que no se negocian:

* **No se permite ninguna ayuda de IA generativa durante las preguntas individuales.**
* Si vuestra propia explicación de vuestro trabajo contradice esta declaración, el asunto es de
  **integridad académica**, no de calificación.

Las normas de integridad académica de la universidad se siguen aplicando en su totalidad.
