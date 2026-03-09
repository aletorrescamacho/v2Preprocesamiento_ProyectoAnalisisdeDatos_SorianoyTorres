# Proyecto Final – Análisis de Datos  
## Uso recreativo digital y desempeño académico en PISA 2022 (Argentina)

### Autores
Luis Soriano  
Alessandra Torres

---

## Descripción del Proyecto

Este proyecto analiza la relación entre el uso recreativo de recursos digitales y el desempeño académico general en estudiantes argentinos de 15 y 16 años evaluados en PISA 2022.

La pregunta de investigación es:

> En estudiantes argentinos de 15 y 16 años evaluados en PISA 2022, ¿los estudiantes que reportan un uso recreativo alto de recursos digitales (evaluados mediante un puntaje de intensidad) presentan un promedio más bajo en el desempeño académico general, medido a través del puntaje combinado de matemáticas, lectura y ciencias, en comparación con aquellos que reportan menor frecuencia de uso?

El análisis se enmarca en el estudio del impacto del uso digital recreativo sobre el rendimiento académico.

---

## Fuente de Datos

- **PISA 2022 – Student Questionnaire Data File**
- Fuente oficial: OECD PISA 2022 Database

El archivo original en formato `.SAV` no se incluye en este repositorio debido a su tamaño.  
Debe descargarse desde el sitio oficial de la OECD.

## **Nota sobre la Integración de Fuentes**
Es importante destacar que, aunque los datos se extrajeron de un único archivo consolidado por la OECD, la investigación integra dos fuentes de información distintas diseñadas de manera independiente:

1. Cuestionario General del Estudiante: De donde se obtienen los resultados de desempeño académico (Valores Plausibles) y datos demográficos.
2. Cuestionario de Familiaridad con las TIC (ICT Questionnaire): Un módulo opcional que profundiza en las conductas digitales.

De acuerdo con lo consultado y aprobado por la profesora, el uso de este dataset cumple con el requisito de integración de múltiples fuentes, ya que el archivo oficial de PISA 2022 actúa como el punto de unión de dos encuestas con objetivos y estructuras diferentes. El proceso de limpieza realizado en este proyecto se encargó de extraer y vincular estas dos dimensiones para permitir el análisis de la relación entre el entorno digital y el rendimiento escolar.

---

## Preprocesamiento de Datos

El preprocesamiento inicial se realizó en Python (VSCode) con el objetivo de reducir el tamaño del dataset y trabajar únicamente con las variables relevantes para el análisis.

### Filtrado de la muestra

Se aplicaron los siguientes criterios de filtrado:

- `CNT = ARG` → Selección de estudiantes argentinos.
- `Option_ICTQ = 1` → Garantiza que al estudiante se le aplicó el módulo de conductas digitales.
- Se excluyeron los registros que no tenían respuesta en ninguna de las 14 variables de las secciones IC177 e IC178 del cuestionario de conductas digitales.
- Edad entre 15 y 16 años → Calculada a partir de `AGE`.

Estas variables fueron utilizadas para filtrar la muestra y posteriormente eliminadas del dataset final cuando ya no eran necesarias.

---

## Variables Utilizadas

### 1. Datos Generales del Encuestado

- `AGE` → Edad.
- `ST004Q01TA` → Género/Sexo.

---

### 2. Puntajes en Exámenes de Desempeño (Plausible Values)

PISA no proporciona un único puntaje directo por estudiante. En su lugar, utiliza diez valores plausibles (PV), que son estimaciones del nivel académico del estudiante basadas en modelos estadísticos aplicados a sus respuestas.

Se utilizaron estas columnas:

- Matemáticas: `PV1MATH` – `PV10MATH`
- Lectura: `PV1READ` – `PV10READ`
- Ciencias: `PV1SCIE` – `PV10SCIE`


---

### 3. Uso de Recursos Digitales para Actividades Recreativas ENTRE SEMANA 

Bloque `IC177`:

- `IC177Q01JA` – Play video-game  
- `IC177Q02JA` – Browse social networks  
- `IC177Q03JA` – Browse the Internet (excluding social networks) for fun (e.g. reading news, listening to podcasts and music or watching videos)  
- `IC177Q04JA` – Look for practical information online (e.g. find a place, book a train ticket, buy a product)  
- `IC177Q05JA` – Communicate and share digital content on social networks or any communication platform  
- `IC177Q06JA` – Read, listen to or view informational materials to learn how to do something (e.g. tutorial, podcast)  
- `IC177Q07JA` – Create or edit my own digital content (pictures, videos, music, computer programs)

---

### 4. Uso de Recursos Digitales para Actividades Recreativas FINES DE SEMANA 

Bloque `IC178`:

- `IC178Q01JA` – Play video-game  
- `IC178Q02JA` – Browse social networks  
- `IC178Q03JA` – Browse the Internet (excluding social networks) for fun (e.g. reading news, listening to podcasts and music or watching videos)  
- `IC178Q04JA` – Look for practical information online (e.g. find a place, book a train ticket, buy a product)  
- `IC178Q05JA` – Communicate and share digital content on social networks or any communication platform  
- `IC178Q06JA` – Read, listen to or view informational materials to learn how to do something (e.g. tutorial, podcast)  
- `IC178Q07JA` – Create or edit my own digital content (pictures, videos, music, computer programs)

## Estructura del Proyecto

```
ProyectoAnalisisDeDatos_SorianoTorres/
│
├── data/
│   ├── raw/               # Archivo original .SAV (no incluido en el repositorio)
│   └── processed/         # Dataset filtrado (ARG, 15–16 años, ICT aplicado)
│
├── src/
│   └── 01_extract_filter.py   # Script de selección de columnas y filtrado
│
└── notebooks/
    └── ProyectoAnalisisdeDatos_SorianoyTorres.ipynb    # Limpieza final, construcción de variables, EDA, visualizaciones y análisis principal
```

---

## Reproducibilidad

Para reproducir el preprocesamiento:

1. Descargar el archivo `.SAV` oficial de PISA 2022.
2. Colocarlo en `data/raw/`.
3. Ejecutar: python src/01_extract_filter.py

El dataset filtrado se generará en `data/processed/`.

El análisis completo se encuentra en el siguiente notebook de Google Colab:

https://colab.research.google.com/drive/1sEwLajSE5JSwh22egYIzalhyiDZfinOk#scrollTo=yekO6jYO5mSm

---

## Limitaciones

- Los puntajes académicos se basan en valores plausibles (estimaciones estadísticas).
- El estudio identifica asociaciones, no relaciones causales.
- Parte del uso digital es información autodeclarada por los estudiantes.
- El archivo original en formato .SAV correspondiente a la base completa de PISA 2022 no se incluye en el repositorio debido a limitaciones de tamaño en la plataforma (aproximadamente 2 GB). Sin embargo, el repositorio contiene el script reproducible que permite generar el dataset filtrado utilizado en el análisis, siempre que el archivo original sea descargado previamente desde la fuente oficial de la OECD y colocado en la ruta indicada dentro del proyecto.

---

## Licencia

Este proyecto utiliza datos públicos de la OECD bajo sus términos oficiales de uso.
