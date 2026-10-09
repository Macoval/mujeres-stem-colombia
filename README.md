# Mujeres STEM en Colombia

Proyecto de gestión, integración y análisis de datos sobre la participación de mujeres en programas STEM en Colombia, utilizando información del Sistema Nacional de Información de la Educación Superior (SNIES).

## Objetivo

Analizar la evolución de la participación femenina en programas STEM en Colombia a partir de datos de matriculados y graduados, con énfasis en tendencias por año, categoría STEM, programa académico, institución y territorio.

## Fuentes de datos

- SNIES - Matriculados
- SNIES - Graduados
- Catálogo propio de programas clasificados como STEM

## Arquitectura de datos

El proyecto utiliza una arquitectura Medallion:

### Bronze
Contiene los archivos originales provenientes de SNIES, sin transformación.

### Plata
Contiene las bases limpias, homologadas, tipadas y unificadas.

Ejemplos:
- `SNIES_Graduados_Unificado_2001_2025.parquet`
- `SNIES_Matriculados_Unificado_2014_2025.parquet`

### Oro
Contiene tablas integradas y preparadas para análisis, visualización y consumo analítico.

Ejemplos previstos:
- graduados STEM
- matriculados STEM
- panel integrado de matriculados y graduados
- indicadores de participación femenina

## Flujo general

1. Carga de archivos SNIES.
2. Diagnóstico de estructura y variables.
3. Homologación de nombres de columnas.
4. Limpieza y transformación de variables.
5. Conversión de tipos de datos.
6. Unificación de archivos históricos.
7. Clasificación de programas STEM.
8. Integración de matriculados y graduados.
9. Análisis exploratorio de datos.
10. Visualización en Power BI.

## Clasificación STEM

Los programas se agrupan en cuatro grandes categorías:

- Ciencias
- Tecnología
- Ingeniería
- Matemáticas

La clasificación se realiza a partir del código SNIES y el nombre del programa, utilizando un catálogo depurado de programas STEM.

## Tecnologías utilizadas

- Python
- pandas
- NumPy
- openpyxl
- pyarrow
- PostgreSQL
- DataGrip
- Power BI
- Git
- GitHub

## Estructura del repositorio

```text
Proyecto_STEM/
├── Data/
│   ├── Bronze/
│   ├── Plata/
│   └── Oro/
├── Graduados/
├── Matriculados/
├── Scripts/
├── SQL/
├── Presentacion_STEM.pptx
├── Stem Final.pbix
├── README.md
└── .gitignore
```

## Datos incluidos en GitHub

Se incluyen principalmente:

- scripts de transformación y análisis;
- archivos `.parquet` de la capa Plata;
- consultas SQL;
- archivos de Power BI;
- presentación del proyecto;
- documentación.

No se incluyen:

- archivos originales de SNIES;
- archivos CSV de gran tamaño;
- entornos virtuales;
- archivos temporales.

## Nota metodológica

La comparación entre matriculados y graduados por año permite analizar volúmenes y participación relativa, pero no debe interpretarse directamente como una tasa de graduación de cohorte, ya que los graduados de un año no corresponden necesariamente a los matriculados de ese mismo año.

## Estado del proyecto

En desarrollo.

Actualmente se cuenta con:

- base de graduados unificada;
- base de matriculados unificada;
- catálogo de programas STEM;
- clasificación por categoría STEM;
- integración analítica en construcción;
- visualizaciones en Power BI en desarrollo.
