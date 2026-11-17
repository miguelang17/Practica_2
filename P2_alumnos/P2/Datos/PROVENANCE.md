# Procedencia, licencias y referencias de los datos de la Práctica 2

El curso **no ha generado** estos datos. Lo único que ha hecho es construir los conjuntos de la
práctica a partir de ellos: elegir las características, extraer una muestra, separar el
entrenamiento del test y asignar identificadores nuevos.

**En la práctica no se pueden usar las fuentes originales ni ningún otro dato externo.** Se
citan aquí porque sus términos de uso lo exigen.

## Reto de ciberseguridad: TON_IoT

| | |
|---|---|
| Conjunto de datos | **TON_IoT**, subconjunto de red `Train_Test_Network` |
| Autoría | UNSW Canberra (ADFA), Cyber Range and IoT Labs; investigador principal, Dr. Nour Moustafa |
| Página del proyecto | <https://research.unsw.edu.au/projects/toniot-datasets> |
| Términos de uso | Uso libre para investigación académica; el uso comercial requiere permiso de los autores. Quien use los datos debe citar los ocho artículos siguientes |

1. Moustafa, Nour. "A new distributed architecture for evaluating AI-based security systems
   at the edge: Network TON_IoT datasets." *Sustainable Cities and Society* (2021): 102994.
2. Booij, Tim M., Irina Chiscop, Erik Meeuwissen, Nour Moustafa, and Frank T. H. den Hartog.
   "ToN IoT: The role of heterogeneity and the need for standardization of features and
   attack types in IoT network intrusion datasets." *IEEE Internet of Things Journal* (2021).
3. Alsaedi, Abdullah, Nour Moustafa, Zahir Tari, Abdun Mahmood, and Adnan Anwar. "TON_IoT
   telemetry dataset: a new generation dataset of IoT and IIoT for data-driven Intrusion
   Detection Systems." *IEEE Access* 8 (2020): 165130-165150.
4. Moustafa, Nour, M. Keshk, E. Debie and H. Janicke. "Federated TON_IoT Windows Datasets for
   Evaluating AI-Based Security Applications." *2020 IEEE 19th International Conference on
   Trust, Security and Privacy in Computing and Communications (TrustCom)*, 2020, pp. 848-855,
   doi: 10.1109/TrustCom50675.2020.00114.
5. Moustafa, Nour, M. Ahmed and S. Ahmed. "Data Analytics-Enabled Intrusion Detection:
   Evaluations of ToN_IoT Linux Datasets." *2020 IEEE 19th International Conference on Trust,
   Security and Privacy in Computing and Communications (TrustCom)*, 2020, pp. 727-735,
   doi: 10.1109/TrustCom50675.2020.00100.
6. Moustafa, Nour. "New Generations of Internet of Things Datasets for Cybersecurity
   Applications based Machine Learning: TON_IoT Datasets." *Proceedings of the eResearch
   Australasia Conference*, Brisbane, Australia, 2019.
7. Moustafa, Nour. "A systemic IoT-Fog-Cloud architecture for big-data analytics and cyber
   security systems: a review of fog computing." *arXiv preprint* arXiv:1906.01055 (2019).
8. Ashraf, Javed, Marwa Keshk, Nour Moustafa, Mohamed Abdel-Basset, Hasnat Khurshid,
   Asim D. Bakhshi, and Reham R. Mostafa. "IoTBoT-IDS: A Novel Statistical Learning-enabled
   Botnet Detection Framework for Protecting Networks of Smart Cities." *Sustainable Cities
   and Society* (2021): 103041.

**Cómo se construyeron los ficheros.** Se conservan once características de comportamiento de
cada conexión (`proto`, `service`, `conn_state`, `duration`, `src_bytes`, `dst_bytes`,
`missed_bytes`, `src_pkts`, `src_ip_bytes`, `dst_pkts`, `dst_ip_bytes`) y el tipo de tráfico,
`attack_type`. Se quitaron las direcciones, los puertos y la etiqueta binaria, que identifican la
captura en lugar del comportamiento. Se eliminaron las filas repetidas y los vectores de
características que aparecían con etiquetas distintas. De lo que queda se extrajo una muestra de
10 000 conexiones, con un 60 % de tráfico normal, repartida a partes iguales entre el
entrenamiento y el test, sin ningún vector de características en los dos.

Es un banco de pruebas docente construido a partir de una captura de laboratorio: nada de lo
que se calcule en la práctica es una afirmación sobre la detección de intrusiones en redes
reales.

## Reto de latencia: rendimiento de un sistema de almacenamiento

| | |
|---|---|
| Conjunto de datos | Medidas de rendimiento de un sistema de almacenamiento (repositorio `HSE-LAMBDA/digital-twin`) |
| Autoría | A. Al-Maeeni, A. Temirkhanov, A. Ryzhikov y M. Hushchyn, HSE University |
| Licencia | **Apache-2.0**; el texto completo está en `LICENCIA_latencia_Apache-2.0.txt` |

Referencia:

- Al-Maeeni, Abdalaziz Rashid, Aziz Temirkhanov, Artem Ryzhikov, and Mikhail Hushchyn.
  "Performance Modeling of Data Storage Systems Using Generative Models." *IEEE Access* 13
  (2025): 49643-49658, doi: 10.1109/ACCESS.2025.3552409.

**Cómo se construyeron los ficheros (modificaciones respecto al original).** Se conservan las
nueve características de la configuración y de la carga y la latencia en nanosegundos,
`latency_ns`. Se quitaron las IOPS, que son otra salida medida en la misma ejecución, y las
columnas constantes o de identificación. Se descartaron las mediciones con latencia cero. De
cada configuración se conservan cinco mediciones. Se eligieron 1000 configuraciones para el
entrenamiento y otras 600, distintas, para el test.

Es un banco de pruebas docente construido a partir de una campaña de medidas en un hardware
concreto: nada de lo que se calcule en la práctica es una afirmación sobre los sistemas de
almacenamiento en general.
