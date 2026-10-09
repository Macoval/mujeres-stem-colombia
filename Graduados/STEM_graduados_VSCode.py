# Proyecto Mujeres STEM - SNIES Graduados
# Ruta base esperada: C:\Proyecto_STEM\Graduados

# ============================================================
# VERIFICACIÓN DEL ENTORNO
# ============================================================

import sys
import os
import glob
import re
import time
import unicodedata
import pandas as pd
from IPython.display import display

_inicio_proceso_1 = time.perf_counter()

# ============================================================
# PROCESO 1. DEFINIR RUTAS LOCALES Y LIBRERÍAS
# ============================================================

# Carpeta local del proyecto.
# El notebook y los archivos Excel están en esta misma carpeta.
BASE_PROYECTO = r"C:\Proyecto_STEM\Graduados"

# Los archivos fuente están directamente en BASE_PROYECTO.
CARPETA_BRONZE = BASE_PROYECTO

# Los resultados procesados se guardarán en una subcarpeta "Plata".
CARPETA_PLATA = os.path.join(
    BASE_PROYECTO,
    "Plata"
)

os.makedirs(
    CARPETA_PLATA,
    exist_ok=True
)

print("=" * 70)
print("RUTAS DEL PROYECTO")
print("=" * 70)
print("Proyecto:", BASE_PROYECTO)
print("Bronze:", CARPETA_BRONZE)
print("Plata:", CARPETA_PLATA)

_tiempo_proceso_1 = time.perf_counter() - _inicio_proceso_1
print(f"\nTiempo PROCESO 1: {_tiempo_proceso_1:.2f} segundos")

_inicio_proceso_2 = time.perf_counter()

# ============================================================
# PROCESO 2. IDENTIFICAR ARCHIVOS DE GRADUADOS
# ============================================================

archivos = [
    archivo
    for archivo in glob.glob(
        os.path.join(CARPETA_BRONZE, "*.xlsx")
    )
    if not os.path.basename(archivo).startswith("~$")
]

archivos = sorted(archivos)

print("\n" + "=" * 70)
print("ARCHIVOS DE GRADUADOS")
print("=" * 70)

print("Número de archivos:", len(archivos))

for i, archivo in enumerate(archivos, 1):
    print(
        f"{i:02d}. {os.path.basename(archivo)}"
    )

_tiempo_proceso_2 = time.perf_counter() - _inicio_proceso_2
print(f"\nTiempo PROCESO 2: {_tiempo_proceso_2:.2f} segundos")

_inicio_proceso_3 = time.perf_counter()

# ============================================================
# PROCESO 3. DIAGNÓSTICO GENERAL DE LOS ARCHIVOS
# ============================================================

diagnostico = []

for archivo in archivos:

    df = pd.read_excel(
        archivo,
        dtype=str
    )

    diagnostico.append({
        "archivo": os.path.basename(archivo),
        "filas": len(df),
        "columnas": len(df.columns),
        "codigo_institucion":
            "SI" if "Código de la Institución" in df.columns
            else "NO",
        "institucion":
            "SI"
            if "Institución de Educación Superior (IES)"
            in df.columns
            else "NO",
        "ies_padre":
            "SI" if "IES_PADRE" in df.columns
            else "NO"
    })


diagnostico_df = pd.DataFrame(
    diagnostico
)

display(diagnostico_df)

_tiempo_proceso_3 = time.perf_counter() - _inicio_proceso_3
print(f"\nTiempo PROCESO 3: {_tiempo_proceso_3:.2f} segundos")

_inicio_proceso_4 = time.perf_counter()

# ============================================================
# PROCESO 4. REVISAR COLUMNAS DE CADA ARCHIVO
# ============================================================

for archivo in archivos:

    df = pd.read_excel(
        archivo,
        dtype=str
    )

    print("\n" + "=" * 80)
    print(
        "ARCHIVO:",
        os.path.basename(archivo)
    )
    print(
        "FILAS:",
        f"{len(df):,}"
    )
    print(
        "COLUMNAS:",
        len(df.columns)
    )
    print("=" * 80)

    for i, columna in enumerate(
        df.columns,
        1
    ):
        print(
            f"{i:02d}. {columna}"
        )

_tiempo_proceso_4 = time.perf_counter() - _inicio_proceso_4
print(f"\nTiempo PROCESO 4: {_tiempo_proceso_4:.2f} segundos")

_inicio_proceso_5 = time.perf_counter()

# ============================================================
# PROCESO 5. DEFINIR ESTRUCTURA MAESTRA
# ============================================================

COLUMNAS_MAESTRAS = [

    # --------------------------------------------------------
    # IDENTIFICACIÓN DE LA IES
    # --------------------------------------------------------

    "codigo_institucion",
    "institucion",
    "ies_padre",
    "principal_seccional",
    "tipo_ies",

    # --------------------------------------------------------
    # SECTOR
    # --------------------------------------------------------

    "id_sector",
    "sector",

    # --------------------------------------------------------
    # CARÁCTER Y ACREDITACIÓN
    # --------------------------------------------------------

    "ies_acreditada",
    "id_caracter",
    "caracter",
    "programa_acreditado",

    # --------------------------------------------------------
    # UBICACIÓN DE LA IES
    # --------------------------------------------------------

    "codigo_departamento_ies",
    "departamento_ies",
    "codigo_municipio_ies",
    "municipio_ies",

    # --------------------------------------------------------
    # PROGRAMA
    # --------------------------------------------------------

    "codigo_snies",
    "programa",

    # --------------------------------------------------------
    # NIVEL
    # --------------------------------------------------------

    "id_nivel_academico",
    "nivel_academico",
    "id_nivel_formacion",
    "nivel_formacion",

    # --------------------------------------------------------
    # METODOLOGÍA Y MODALIDAD
    # --------------------------------------------------------

    "id_metodologia",
    "metodologia",
    "id_modalidad",
    "modalidad",

    # --------------------------------------------------------
    # ÁREA
    # --------------------------------------------------------

    "id_area",
    "area_conocimiento",

    # --------------------------------------------------------
    # NBC
    # --------------------------------------------------------

    "id_nucleo",
    "nbc",

    # --------------------------------------------------------
    # UBICACIÓN DEL PROGRAMA
    # --------------------------------------------------------

    "codigo_departamento_programa",
    "departamento_programa",
    "codigo_municipio_programa",
    "municipio_programa",

    # --------------------------------------------------------
    # SEXO Y TIEMPO
    # --------------------------------------------------------

    "id_sexo",
    "sexo",
    "anio",
    "semestre",

    # --------------------------------------------------------
    # VARIABLE OBJETIVO
    # --------------------------------------------------------

    "graduados",

    # --------------------------------------------------------
    # TRAZABILIDAD
    # --------------------------------------------------------

    "archivo_origen"
]

_tiempo_proceso_5 = time.perf_counter() - _inicio_proceso_5
print(f"\nTiempo PROCESO 5: {_tiempo_proceso_5:.2f} segundos")

_inicio_proceso_6 = time.perf_counter()

# ============================================================
# PROCESO 6. NORMALIZAR NOMBRES DE COLUMNAS
# ============================================================

def normalizar_nombre_columna(nombre):

    nombre = str(
        nombre
    ).strip().upper()

    nombre = unicodedata.normalize(
        "NFKD",
        nombre
    )

    nombre = "".join(
        c
        for c in nombre
        if not unicodedata.combining(c)
    )

    nombre = re.sub(
        r"\s+",
        " ",
        nombre
    )

    return nombre

_tiempo_proceso_6 = time.perf_counter() - _inicio_proceso_6
print(f"\nTiempo PROCESO 6: {_tiempo_proceso_6:.2f} segundos")

_inicio_proceso_7 = time.perf_counter()

# ============================================================
# PROCESO 7. DEFINIR HOMOLOGACIÓN DE COLUMNAS
# ============================================================

HOMOLOGACION = {

    # --------------------------------------------------------
    # INSTITUCIÓN
    # --------------------------------------------------------

    "CODIGO DE LA INSTITUCION":
        "codigo_institucion",

    "IES_PADRE":
        "ies_padre",

    "INSTITUCION DE EDUCACION SUPERIOR (IES)":
        "institucion",

    "PRINCIPAL O SECCIONAL":
        "principal_seccional",

    "TIPO IES":
        "tipo_ies",

    # --------------------------------------------------------
    # SECTOR
    # --------------------------------------------------------

    "ID_SECTOR":
        "id_sector",

    "ID SECTOR IES":
        "id_sector",

    "SECTOR IES":
        "sector",

    # --------------------------------------------------------
    # CARÁCTER
    # --------------------------------------------------------

    "ID_CARACTER":
        "id_caracter",

    "ID CARACTER":
        "id_caracter",

    "ID CARACTER IES":
        "id_caracter",

    "CARACTER IES":
        "caracter",

    # --------------------------------------------------------
    # ACREDITACIÓN
    # --------------------------------------------------------

    "IES ACREDITADA":
        "ies_acreditada",

    "PROGRAMA ACREDITADO":
        "programa_acreditado",

    # --------------------------------------------------------
    # UBICACIÓN IES
    # --------------------------------------------------------

    "CODIGO DEL DEPARTAMENTO (IES)":
        "codigo_departamento_ies",

    "CODIGO DEL DEPARTAMENTO IES":
        "codigo_departamento_ies",

    "DEPARTAMENTO DE DOMICILIO DE LA IES":
        "departamento_ies",

    "CODIGO DEL MUNICIPIO (IES)":
        "codigo_municipio_ies",

    "CODIGO DEL MUNICIPIO IES":
        "codigo_municipio_ies",

    "MUNICIPIO DE DOMICILIO DE LA IES":
        "municipio_ies",

    # --------------------------------------------------------
    # PROGRAMA
    # --------------------------------------------------------

    "CODIGO SNIES DEL PROGRAMA":
        "codigo_snies",

    "PROGRAMA ACADEMICO":
        "programa",

    # --------------------------------------------------------
    # NIVEL
    # --------------------------------------------------------

    "ID NIVEL":
        "id_nivel_academico",

    "ID NIVEL ACADEMICO":
        "id_nivel_academico",

    "NIVEL ACADEMICO":
        "nivel_academico",

    "ID NIVEL FORMACION":
        "id_nivel_formacion",

    "ID NIVEL DE FORMACION":
        "id_nivel_formacion",

    "NIVEL DE FORMACION":
        "nivel_formacion",

    # --------------------------------------------------------
    # METODOLOGÍA
    # --------------------------------------------------------

    "ID METODOLOGIA":
        "id_metodologia",

    "METODOLOGIA":
        "metodologia",

    # --------------------------------------------------------
    # MODALIDAD
    # --------------------------------------------------------

    "ID MODALIDAD":
        "id_modalidad",

    "MODALIDAD":
        "modalidad",

    # --------------------------------------------------------
    # ÁREA
    # --------------------------------------------------------

    "ID AREA":
        "id_area",

    "ID AREA DE CONOCIMIENTO":
        "id_area",

    "AREA DE CONOCIMIENTO":
        "area_conocimiento",

    # --------------------------------------------------------
    # NBC
    # --------------------------------------------------------

    "ID NUCLEO":
        "id_nucleo",

    "ID_NUCLEO":
        "id_nucleo",

    "NUCLEO BASICO DEL CONOCIMIENTO (NBC)":
        "nbc",

    # --------------------------------------------------------
    # UBICACIÓN DEL PROGRAMA
    # --------------------------------------------------------

    "CODIGO DEL DEPARTAMENTO (PROGRAMA)":
        "codigo_departamento_programa",

    "DEPARTAMENTO DE OFERTA DEL PROGRAMA":
        "departamento_programa",

    "CODIGO DEL MUNICIPIO (PROGRAMA)":
        "codigo_municipio_programa",

    "MUNICIPIO DE OFERTA DEL PROGRAMA":
        "municipio_programa",

    # --------------------------------------------------------
    # SEXO
    # --------------------------------------------------------

    "ID GENERO":
        "id_sexo",

    "ID SEXO":
        "id_sexo",

    "GENERO":
        "sexo",

    "SEXO":
        "sexo",

    # --------------------------------------------------------
    # TIEMPO
    # --------------------------------------------------------

    "ANO":
        "anio",

    "AÑO":
        "anio",

    "SEMESTRE":
        "semestre",

    # --------------------------------------------------------
    # MATRÍCULADOS
    # --------------------------------------------------------

    "GRADUADOS":
        "graduados"
}

_tiempo_proceso_7 = time.perf_counter() - _inicio_proceso_7
print(f"\nTiempo PROCESO 7: {_tiempo_proceso_7:.2f} segundos")

_inicio_proceso_8 = time.perf_counter()

# ============================================================
# PROCESO 8. PROCESAR Y HOMOLOGAR CADA ARCHIVO
# ============================================================

def procesar_archivo(archivo):

    nombre_archivo = os.path.basename(
        archivo
    )

    print("\n" + "=" * 70)
    print(
        "PROCESANDO:",
        nombre_archivo
    )
    print("=" * 70)

    # --------------------------------------------------------
    # 8.1 LEER ARCHIVO
    # --------------------------------------------------------

    df = pd.read_excel(
        archivo,
        dtype=str
    )

    filas_originales = len(df)
    columnas_originales = len(df.columns)

    # --------------------------------------------------------
    # 8.2 NORMALIZAR NOMBRES
    # --------------------------------------------------------

    df.columns = [
        normalizar_nombre_columna(c)
        for c in df.columns
    ]

    # --------------------------------------------------------
    # 8.3 ELIMINAR VARIABLES CINE
    # --------------------------------------------------------

    columnas_cine = [
        c
        for c in df.columns
        if "CINE" in c
    ]

    if columnas_cine:

        df = df.drop(
            columns=columnas_cine
        )

    # --------------------------------------------------------
    # 8.4 HOMOLOGAR COLUMNAS
    # --------------------------------------------------------

    nuevas_columnas = {}

    for columna in df.columns:

        if columna in HOMOLOGACION:

            nuevas_columnas[
                columna
            ] = HOMOLOGACION[
                columna
            ]

        elif re.match(
            r"^GRADUADOS\s*\d{4}$",
            columna
        ):

            nuevas_columnas[
                columna
            ] = "graduados"

    df = df.rename(
        columns=nuevas_columnas
    )

    # --------------------------------------------------------
    # 8.5 VALIDAR VARIABLE GRADUADOS
    # --------------------------------------------------------

    if "graduados" not in df.columns:

        raise ValueError(
            f"No se encontró la variable "
            f"GRADUADOS en "
            f"{nombre_archivo}\n\n"
            f"Columnas encontradas:\n"
            f"{list(df.columns)}"
        )

    # --------------------------------------------------------
    # 8.6 DIAGNÓSTICO DE VARIABLES INSTITUCIONALES
    # --------------------------------------------------------

    print("\nVARIABLES DE IDENTIFICACIÓN INSTITUCIONAL")

    variables_ies = [
        "codigo_institucion",
        "institucion",
        "ies_padre"
    ]

    for variable in variables_ies:

        if variable in df.columns:

            faltantes = (
                df[variable]
                .isna()
                .sum()
            )

            distintos = (
                df[variable]
                .nunique(
                    dropna=True
                )
            )

            print(
                f"✓ {variable}: "
                f"PRESENTE | "
                f"distintos: {distintos:,} | "
                f"faltantes: {faltantes:,}"
            )

        else:

            print(
                f"⚠ {variable}: "
                f"NO EXISTE EN EL ARCHIVO"
            )

    # --------------------------------------------------------
    # 8.7 DETECTAR COLUMNAS DUPLICADAS
    # --------------------------------------------------------

    duplicadas = (
        df.columns[
            df.columns.duplicated()
        ].tolist()
    )

    if duplicadas:

        raise ValueError(
            f"Columnas duplicadas después "
            f"de homologar en "
            f"{nombre_archivo}: "
            f"{duplicadas}"
        )

    # --------------------------------------------------------
    # 8.8 TRAZABILIDAD
    # --------------------------------------------------------

    df["archivo_origen"] = (
        nombre_archivo
    )

    # --------------------------------------------------------
    # 8.9 CONSERVAR COLUMNAS MAESTRAS
    # --------------------------------------------------------

    columnas_presentes = [
        c
        for c in COLUMNAS_MAESTRAS
        if c in df.columns
    ]

    df = df[
        columnas_presentes
    ]

    # --------------------------------------------------------
    # 8.10 INFORME
    # --------------------------------------------------------

    print("\nRESUMEN DEL ARCHIVO")

    print(
        "Filas:",
        f"{filas_originales:,}"
    )

    print(
        "Columnas originales:",
        columnas_originales
    )

    print(
        "Columnas CINE eliminadas:",
        len(columnas_cine)
    )

    print(
        "Columnas finales:",
        len(df.columns)
    )

    return df

_tiempo_proceso_8 = time.perf_counter() - _inicio_proceso_8
print(f"\nTiempo PROCESO 8: {_tiempo_proceso_8:.2f} segundos")

_inicio_proceso_9 = time.perf_counter()

# ============================================================
# PROCESO 9. UNIFICAR TODOS LOS ARCHIVOS
# ============================================================

bases = []

for archivo in archivos:

    df_temp = procesar_archivo(
        archivo
    )

    bases.append(
        df_temp
    )


graduados_unificado = pd.concat(
    bases,
    ignore_index=True,
    sort=False
)


print("\n" + "=" * 70)
print("BASE UNIFICADA DE GRADUADOS")
print("=" * 70)

print(
    "Número total de registros:",
    f"{len(graduados_unificado):,}"
)

print(
    "Número total de columnas:",
    len(graduados_unificado.columns)
)

_tiempo_proceso_9 = time.perf_counter() - _inicio_proceso_9
print(f"\nTiempo PROCESO 9: {_tiempo_proceso_9:.2f} segundos")

_inicio_proceso_10 = time.perf_counter()

# ============================================================
# PROCESO 10. VALIDACIÓN DE LA BASE UNIFICADA
# ============================================================

TOTAL_ESPERADO = 846018

print("=" * 70)
print("VALIDACIÓN DE GRADUADOS UNIFICADOS")
print("=" * 70)


# ------------------------------------------------------------
# 10.1 TOTAL DE REGISTROS
# ------------------------------------------------------------

total_registros = (
    len(graduados_unificado)
)

print("\nTOTAL DE REGISTROS")
print("-" * 40)

print(
    "Total obtenido:",
    f"{total_registros:,}"
)

print(
    "Total esperado:",
    f"{TOTAL_ESPERADO:,}"
)

if total_registros == TOTAL_ESPERADO:

    print("✓ CORRECTO")

else:

    print("⚠ REVISAR")


# ------------------------------------------------------------
# 10.2 AÑOS
# ------------------------------------------------------------

print("\nAÑOS")
print("-" * 40)

print(
    sorted(
        graduados_unificado[
            "anio"
        ]
        .dropna()
        .unique()
        .tolist()
    )
)


# ------------------------------------------------------------
# 10.3 REGISTROS POR AÑO
# ------------------------------------------------------------

print("\nREGISTROS POR AÑO")
print("-" * 40)

registros_anio = (
    graduados_unificado
    .groupby("anio")
    .size()
    .reset_index(
        name="registros"
    )
)

display(
    registros_anio
)


# ------------------------------------------------------------
# 10.4 VARIABLES CINE
# ------------------------------------------------------------

print("\nVARIABLES CINE")
print("-" * 40)

columnas_cine = [
    c
    for c in graduados_unificado.columns
    if "CINE" in c.upper()
]

if len(columnas_cine) == 0:

    print(
        "✓ No existen variables CINE."
    )

else:

    print(
        "⚠ Se encontraron:",
        columnas_cine
    )


# ------------------------------------------------------------
# 10.5 VALORES NULOS
# ------------------------------------------------------------

print("\nVALORES NULOS")
print("-" * 40)

nulos = (
    graduados_unificado
    .isna()
    .sum()
    .sort_values(
        ascending=False
    )
)

display(
    nulos[
        nulos > 0
    ].to_frame(
        "faltantes"
    )
)


# ------------------------------------------------------------
# 10.6 DUPLICADOS EXACTOS
# ------------------------------------------------------------

print("\nDUPLICADOS EXACTOS")
print("-" * 40)

print(
    "Filas duplicadas:",
    graduados_unificado
    .duplicated()
    .sum()
)

_tiempo_proceso_10 = time.perf_counter() - _inicio_proceso_10
print(f"\nTiempo PROCESO 10: {_tiempo_proceso_10:.2f} segundos")

_inicio_proceso_11 = time.perf_counter()

# ============================================================
# PROCESO 11. DEFINIR LAS VARIABLES FINALES
# ============================================================

COLUMNAS_DEFINITIVAS = [

    # IDENTIFICACIÓN INSTITUCIONAL
    "codigo_institucion",
    "institucion",
    "ies_padre",

    # CARACTERÍSTICAS IES
    "sector",
    "caracter",

    # UBICACIÓN IES
    "departamento_ies",

    # PROGRAMA
    "codigo_snies",
    "programa",

    # NIVEL
    "nivel_academico",

    # ÁREA
    "id_area",
    "area_conocimiento",

    # NBC
    "id_nucleo",
    "nbc",

    # SEXO
    "sexo",

    # TIEMPO
    "anio",
    "semestre",

    # GRADUADOS
    "graduados"
]


# ------------------------------------------------------------
# VALIDAR QUE TODAS LAS VARIABLES EXISTAN
# ------------------------------------------------------------

faltantes_columnas = [
    c
    for c in COLUMNAS_DEFINITIVAS
    if c not in graduados_unificado.columns
]

if faltantes_columnas:

    raise ValueError(
        "Faltan columnas definitivas: "
        f"{faltantes_columnas}"
    )


graduados_unificado = (
    graduados_unificado[
        COLUMNAS_DEFINITIVAS
    ].copy()
)


print("=" * 70)
print("VARIABLES DEFINITIVAS")
print("=" * 70)

print(
    "Número de registros:",
    f"{len(graduados_unificado):,}"
)

print(
    "Número de variables:",
    len(graduados_unificado.columns)
)

for i, columna in enumerate(
    graduados_unificado.columns,
    1
):

    print(
        f"{i:02d}. {columna}"
    )

_tiempo_proceso_11 = time.perf_counter() - _inicio_proceso_11
print(f"\nTiempo PROCESO 11: {_tiempo_proceso_11:.2f} segundos")

_inicio_proceso_12 = time.perf_counter()

# ============================================================
# PROCESO 12. CONVERSIÓN DE TIPOS DE DATOS
# ============================================================

# ------------------------------------------------------------
# 12.1 CÓDIGO DE INSTITUCIÓN
# ------------------------------------------------------------

graduados_unificado[
    "codigo_institucion"
] = (
    pd.to_numeric(
        graduados_unificado[
            "codigo_institucion"
        ],
        errors="coerce"
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 12.2 IES PADRE
# ------------------------------------------------------------

graduados_unificado[
    "ies_padre"
] = (
    pd.to_numeric(
        graduados_unificado[
            "ies_padre"
        ],
        errors="coerce"
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 12.3 CÓDIGO SNIES
# ------------------------------------------------------------

snies_no_numericos = (
    graduados_unificado
    .loc[
        ~graduados_unificado[
            "codigo_snies"
        ]
        .astype("string")
        .str.fullmatch(
            r"\d+"
        ),
        "codigo_snies"
    ]
    .drop_duplicates()
)


print(
    "Valores SNIES no numéricos:",
    len(snies_no_numericos)
)

if len(snies_no_numericos) > 0:

    display(
        snies_no_numericos.head(50)
    )

    raise ValueError(
        "Existen códigos SNIES no numéricos."
    )


graduados_unificado[
    "codigo_snies"
] = (
    pd.to_numeric(
        graduados_unificado[
            "codigo_snies"
        ],
        errors="raise"
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 12.4 ID ÁREA
# ------------------------------------------------------------

graduados_unificado[
    "id_area"
] = (
    graduados_unificado[
        "id_area"
    ]
    .astype("string")
)


# ------------------------------------------------------------
# 12.5 AÑO
# ------------------------------------------------------------

graduados_unificado[
    "anio"
] = (
    pd.to_numeric(
        graduados_unificado[
            "anio"
        ],
        errors="coerce"
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 12.6 SEMESTRE
# ------------------------------------------------------------

graduados_unificado[
    "semestre"
] = (
    pd.to_numeric(
        graduados_unificado[
            "semestre"
        ],
        errors="coerce"
    )
    .astype("Int64")
)


# ------------------------------------------------------------
# 12.7 GRADUADOS
# ------------------------------------------------------------

graduados_unificado[
    "graduados"
] = (
    pd.to_numeric(
        graduados_unificado[
            "graduados"
        ],
        errors="coerce"
    )
    .astype("Int64")
)


print("=" * 70)
print("TIPOS DE DATOS")
print("=" * 70)

display(
    graduados_unificado
    .dtypes
    .to_frame("tipo")
)

_tiempo_proceso_12 = time.perf_counter() - _inicio_proceso_12
print(f"\nTiempo PROCESO 12: {_tiempo_proceso_12:.2f} segundos")

_inicio_proceso_13 = time.perf_counter()

# ============================================================
# PROCESO 13. HOMOLOGACIÓN DE VARIABLES CATEGÓRICAS
# ============================================================


# ------------------------------------------------------------
# 13.1 SECTOR
# ------------------------------------------------------------

graduados_unificado[
    "sector"
] = (
    graduados_unificado[
        "sector"
    ]
    .astype("string")
    .str.strip()
    .replace({
        "OFICIAL": "Oficial",
        "Oficial": "Oficial",
        "PRIVADA": "Privada",
        "Privado": "Privada"
    })
)


# ------------------------------------------------------------
# 13.2 CARÁCTER
# ------------------------------------------------------------

graduados_unificado[
    "caracter"
] = (
    graduados_unificado[
        "caracter"
    ]
    .astype("string")
    .str.strip()
    .str.upper()
    .replace({

        "UNIVERSIDAD":
            "Universidad",

        "INSTITUCIÓN UNIVERSITARIA/ESCUELA TECNOLÓGICA":
            "Institución Universitaria/Escuela Tecnológica",

        "INSTITUCION UNIVERSITARIA/ESCUELA TECNOLOGICA":
            "Institución Universitaria/Escuela Tecnológica",

        "INSTITUCIÓN TECNOLÓGICA":
            "Institución Tecnológica",

        "INSTITUCION TECNOLOGICA":
            "Institución Tecnológica",

        "INSTITUCIÓN TÉCNICA PROFESIONAL":
            "Institución Técnica Profesional",

        "INSTITUCION TECNICA PROFESIONAL":
            "Institución Técnica Profesional"
    })
)


# ------------------------------------------------------------
# 13.3 NIVEL ACADÉMICO
# ------------------------------------------------------------

graduados_unificado[
    "nivel_academico"
] = (
    graduados_unificado[
        "nivel_academico"
    ]
    .astype("string")
    .str.strip()
    .str.upper()
    .replace({
        "PREGRADO": "Pregrado",
        "POSGRADO": "Posgrado"
    })
)


# ------------------------------------------------------------
# 13.4 SEXO
# ------------------------------------------------------------

graduados_unificado[
    "sexo"
] = (
    graduados_unificado[
        "sexo"
    ]
    .astype("string")
    .str.strip()
    .str.upper()
    .replace({

        "FEMENINO": "Mujer",
        "MUJER": "Mujer",

        "MASCULINO": "Hombre",
        "HOMBRE": "Hombre",

        "NO BINARIO": "No binario",
        "TRANS": "Trans"
    })
)

print(
    "✓ Homologación categórica realizada."
)

_tiempo_proceso_13 = time.perf_counter() - _inicio_proceso_13
print(f"\nTiempo PROCESO 13: {_tiempo_proceso_13:.2f} segundos")

_inicio_proceso_14 = time.perf_counter()

# ============================================================
# PROCESO 14. HOMOLOGACIÓN DE DEPARTAMENTO DE LA IES
# ============================================================

def normalizar_texto(valor):

    if pd.isna(valor):

        return pd.NA

    valor = (
        str(valor)
        .strip()
        .upper()
    )

    valor = unicodedata.normalize(
        "NFKD",
        valor
    )

    valor = "".join(
        c
        for c in valor
        if not unicodedata.combining(c)
    )

    valor = re.sub(
        r"\s+",
        " ",
        valor
    )

    return valor


graduados_unificado[
    "departamento_ies"
] = (
    graduados_unificado[
        "departamento_ies"
    ]
    .apply(normalizar_texto)
)


MAPA_DEPARTAMENTOS = {

    "BOGOTA D.C":
        "BOGOTA D.C.",

    "BOGOTA D.C.":
        "BOGOTA D.C.",

    "NARINIO":
        "NARINO",

    "GUAJIRA":
        "LA GUAJIRA",

    "SAN ANDRES Y PROVIDENCIA":
        "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA",

    "SAN ANDRES Y PROVI":
        "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA",

    "ARCHIPIELAGO DE SA":
        "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA",

    "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA":
        "ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA"
}


graduados_unificado[
    "departamento_ies"
] = (
    graduados_unificado[
        "departamento_ies"
    ]
    .replace(
        MAPA_DEPARTAMENTOS
    )
)


print("=" * 70)
print("DEPARTAMENTOS HOMOLOGADOS")
print("=" * 70)

display(
    graduados_unificado[
        "departamento_ies"
    ]
    .value_counts(
        dropna=False
    )
    .to_frame(
        "frecuencia"
    )
)

print(
    "Número de categorías:",
    graduados_unificado[
        "departamento_ies"
    ].nunique(
        dropna=True
    )
)

_tiempo_proceso_14 = time.perf_counter() - _inicio_proceso_14
print(f"\nTiempo PROCESO 14: {_tiempo_proceso_14:.2f} segundos")

_inicio_proceso_15 = time.perf_counter()

# ============================================================
# PROCESO 15. HOMOLOGACIÓN DE ÁREA DE CONOCIMIENTO
# ============================================================

area_normalizada = (
    graduados_unificado[
        "area_conocimiento"
    ]
    .apply(normalizar_texto)
)


MAPA_AREA_CONOCIMIENTO = {

    "ECONOMIA ADMINISTRACION CONTADURIA Y AFINES":
        "Economía, administración, contaduría y afines",

    "ECONOMIA, ADMINISTRACION, CONTADURIA Y AFINES":
        "Economía, administración, contaduría y afines",

    "INGENIERIA ARQUITECTURA URBANISMO Y AFINES":
        "Ingeniería, arquitectura, urbanismo y afines",

    "INGENIERIA, ARQUITECTURA, URBANISMO Y AFINES":
        "Ingeniería, arquitectura, urbanismo y afines",

    "CIENCIAS DE LA EDUCACION":
        "Ciencias de la educación",

    "CIENCIAS DE LA SALUD":
        "Ciencias de la salud",

    "CIENCIAS SOCIALES Y HUMANAS":
        "Ciencias sociales y humanas",

    "BELLAS ARTES":
        "Bellas artes",

    "AGRONOMIA VETERINARIA Y AFINES":
        "Agronomía, veterinaria y afines",

    "AGRONOMIA, VETERINARIA Y AFINES":
        "Agronomía, veterinaria y afines",

    "MATEMATICAS Y CIENCIAS NATURALES":
        "Matemáticas y ciencias naturales",

    "SIN INFORMACION":
        "Sin información",

    "SIN CLASIFICAR":
        "Sin clasificar"
}


graduados_unificado[
    "area_conocimiento"
] = (
    area_normalizada
    .replace(
        MAPA_AREA_CONOCIMIENTO
    )
)


resultado_area = (
    graduados_unificado[
        "area_conocimiento"
    ]
    .value_counts(
        dropna=False
    )
    .rename_axis(
        "area_conocimiento"
    )
    .reset_index(
        name="frecuencia"
    )
)

display(
    resultado_area
)

print(
    "Categorías:",
    graduados_unificado[
        "area_conocimiento"
    ].nunique(
        dropna=True
    )
)

_tiempo_proceso_15 = time.perf_counter() - _inicio_proceso_15
print(f"\nTiempo PROCESO 15: {_tiempo_proceso_15:.2f} segundos")

_inicio_proceso_16 = time.perf_counter()

# ============================================================
# PROCESO 16. HOMOLOGACIÓN DE NBC
# ============================================================

nbc_diagnostico = (
    graduados_unificado[
        "nbc"
    ]
    .value_counts(
        dropna=False
    )
    .rename_axis(
        "valor_original"
    )
    .reset_index(
        name="frecuencia"
    )
)


nbc_diagnostico[
    "valor_normalizado"
] = (
    nbc_diagnostico[
        "valor_original"
    ]
    .apply(normalizar_texto)
)


MAPA_NBC = dict(
    zip(
        nbc_diagnostico[
            "valor_original"
        ],
        nbc_diagnostico[
            "valor_normalizado"
        ]
    )
)


graduados_unificado[
    "nbc_normalizado"
] = (
    graduados_unificado[
        "nbc"
    ]
    .map(
        MAPA_NBC
    )
)


# ------------------------------------------------------------
# VALIDAR RELACIÓN ID_NUCLEO - NBC
# ------------------------------------------------------------

relacion_nucleo_nbc = (
    graduados_unificado
    .groupby(
        "id_nucleo",
        dropna=False
    )[
        "nbc_normalizado"
    ]
    .nunique(
        dropna=True
    )
    .reset_index(
        name="numero_nbc"
    )
)


casos_multiples_nbc = (
    relacion_nucleo_nbc[
        relacion_nucleo_nbc[
            "numero_nbc"
        ] > 1
    ]
)

print(
    "ID_NUCLEO con más de un NBC:",
    len(casos_multiples_nbc)
)


# ------------------------------------------------------------
# APLICAR NBC NORMALIZADO
# ------------------------------------------------------------

graduados_unificado[
    "nbc"
] = (
    graduados_unificado[
        "nbc_normalizado"
    ]
)


graduados_unificado.drop(
    columns=[
        "nbc_normalizado"
    ],
    inplace=True
)


print(
    "Categorías NBC:",
    graduados_unificado[
        "nbc"
    ].nunique(
        dropna=True
    )
)

_tiempo_proceso_16 = time.perf_counter() - _inicio_proceso_16
print(f"\nTiempo PROCESO 16: {_tiempo_proceso_16:.2f} segundos")

_inicio_proceso_17 = time.perf_counter()

# ============================================================
# PROCESO 17. VALIDACIÓN DE IDENTIFICACIÓN INSTITUCIONAL
# ============================================================

print("=" * 70)
print("VALIDACIÓN DE IDENTIFICACIÓN INSTITUCIONAL")
print("=" * 70)


# ------------------------------------------------------------
# 17.1 CÓDIGOS DE INSTITUCIÓN
# ------------------------------------------------------------

print(
    "\nCódigos de institución:",
    graduados_unificado[
        "codigo_institucion"
    ].nunique(
        dropna=True
    )
)


# ------------------------------------------------------------
# 17.2 INSTITUCIONES
# ------------------------------------------------------------

print(
    "Instituciones:",
    graduados_unificado[
        "institucion"
    ].nunique(
        dropna=True
    )
)


# ------------------------------------------------------------
# 17.3 IES PADRE
# ------------------------------------------------------------

print(
    "IES padre:",
    graduados_unificado[
        "ies_padre"
    ].nunique(
        dropna=True
    )
)


# ------------------------------------------------------------
# 17.4 FALTANTES
# ------------------------------------------------------------

print("\nFALTANTES")
print("-" * 50)

faltantes_ies = (
    graduados_unificado[
        [
            "codigo_institucion",
            "institucion",
            "ies_padre"
        ]
    ]
    .isna()
    .sum()
)

display(
    faltantes_ies.to_frame(
        "cantidad_faltantes"
    )
)


# ------------------------------------------------------------
# 17.5 CÓDIGO → INSTITUCIÓN
# ------------------------------------------------------------

relacion_codigo_institucion = (
    graduados_unificado
    .groupby(
        "codigo_institucion",
        dropna=False
    )[
        "institucion"
    ]
    .nunique(
        dropna=True
    )
)


inconsistencias_institucion = (
    relacion_codigo_institucion > 1
).sum()


print(
    "\nCódigos con más de un nombre "
    "de institución:",
    inconsistencias_institucion
)


# ------------------------------------------------------------
# 17.6 CÓDIGO → IES PADRE
# ------------------------------------------------------------

relacion_codigo_padre = (
    graduados_unificado
    .groupby(
        "codigo_institucion",
        dropna=False
    )[
        "ies_padre"
    ]
    .nunique(
        dropna=True
    )
)


inconsistencias_padre = (
    relacion_codigo_padre > 1
).sum()


print(
    "Códigos con más de un IES_PADRE:",
    inconsistencias_padre
)

_tiempo_proceso_17 = time.perf_counter() - _inicio_proceso_17
print(f"\nTiempo PROCESO 17: {_tiempo_proceso_17:.2f} segundos")

_inicio_proceso_18 = time.perf_counter()

# ============================================================
# PROCESO 18. NORMALIZACIÓN Y DEPURACIÓN DE PROGRAMAS
# ============================================================

def normalizar_programa(texto):

    if pd.isna(texto):

        return pd.NA

    texto = (
        str(texto)
        .strip()
        .upper()
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        c
        for c in texto
        if not unicodedata.combining(c)
    )

    return texto


graduados_unificado[
    "programa_normalizado"
] = (
    graduados_unificado[
        "programa"
    ]
    .apply(
        normalizar_programa
    )
)


# ------------------------------------------------------------
# RELACIÓN SNIES - PROGRAMA
# ------------------------------------------------------------

programas_por_snies_normalizados = (
    graduados_unificado
    .groupby(
        "codigo_snies"
    )[
        "programa_normalizado"
    ]
    .nunique()
)


print(
    "SNIES con un solo nombre:",
    (
        programas_por_snies_normalizados
        == 1
    ).sum()
)


print(
    "SNIES con múltiples nombres:",
    (
        programas_por_snies_normalizados
        > 1
    ).sum()
)


print(
    "Máximo de nombres por SNIES:",
    programas_por_snies_normalizados.max()
)


# ------------------------------------------------------------
# IDENTIFICAR SNIES A EXCLUIR
# ------------------------------------------------------------

snies_excluir = (
    programas_por_snies_normalizados[
        programas_por_snies_normalizados
        > 1
    ]
    .index
)


print(
    "\nSNIES a excluir:",
    len(snies_excluir)
)


# ------------------------------------------------------------
# ELIMINAR REGISTROS PROBLEMÁTICOS
# ------------------------------------------------------------

graduados_unificado = (
    graduados_unificado[
        ~graduados_unificado[
            "codigo_snies"
        ]
        .isin(
            snies_excluir
        )
    ]
    .copy()
)


# ------------------------------------------------------------
# UTILIZAR NOMBRE NORMALIZADO
# ------------------------------------------------------------

graduados_unificado[
    "programa"
] = (
    graduados_unificado[
        "programa_normalizado"
    ]
)


graduados_unificado.drop(
    columns=[
        "programa_normalizado"
    ],
    inplace=True
)


print("\nRESULTADO")
print("-" * 40)

print(
    "Registros:",
    f"{len(graduados_unificado):,}"
)

print(
    "Códigos SNIES:",
    graduados_unificado[
        "codigo_snies"
    ].nunique()
)

print(
    "Programas:",
    graduados_unificado[
        "programa"
    ].nunique()
)

print(
    "Faltantes programa:",
    graduados_unificado[
        "programa"
    ].isna().sum()
)

_tiempo_proceso_18 = time.perf_counter() - _inicio_proceso_18
print(f"\nTiempo PROCESO 18: {_tiempo_proceso_18:.2f} segundos")

_inicio_proceso_19 = time.perf_counter()

# ============================================================
# PROCESO 19. VALIDACIÓN DE LA VARIABLE GRADUADOS
# ============================================================

print("=" * 70)
print("VALIDACIÓN DE GRADUADOS")
print("=" * 70)

print(
    "Tipo:",
    graduados_unificado[
        "graduados"
    ].dtype
)

print(
    "Mínimo:",
    graduados_unificado[
        "graduados"
    ].min()
)

print(
    "Máximo:",
    graduados_unificado[
        "graduados"
    ].max()
)

print(
    "Suma total:",
    graduados_unificado[
        "graduados"
    ].sum()
)

print(
    "Ceros:",
    (
        graduados_unificado[
            "graduados"
        ] == 0
    ).sum()
)

print(
    "Negativos:",
    (
        graduados_unificado[
            "graduados"
        ] < 0
    ).sum()
)

print(
    "Faltantes:",
    graduados_unificado[
        "graduados"
    ].isna().sum()
)

display(
    graduados_unificado[
        "graduados"
    ].describe()
)

_tiempo_proceso_19 = time.perf_counter() - _inicio_proceso_19
print(f"\nTiempo PROCESO 19: {_tiempo_proceso_19:.2f} segundos")

_inicio_proceso_20 = time.perf_counter()

# ============================================================
# PROCESO 20. VALIDACIÓN FINAL DE LA BASE MAESTRA
# ============================================================

print("=" * 70)
print("VALIDACIÓN FINAL — GRADUADOS")
print("=" * 70)


# ------------------------------------------------------------
# 20.1 ESTRUCTURA
# ------------------------------------------------------------

print("\nESTRUCTURA")
print("-" * 40)

print(
    "Registros:",
    f"{len(graduados_unificado):,}"
)

print(
    "Variables:",
    len(graduados_unificado.columns)
)


# ------------------------------------------------------------
# 20.2 COLUMNAS
# ------------------------------------------------------------

print("\nCOLUMNAS")
print("-" * 40)

for i, columna in enumerate(
    graduados_unificado.columns,
    1
):

    print(
        f"{i:02d}. {columna}"
    )


# ------------------------------------------------------------
# 20.3 AÑOS
# ------------------------------------------------------------

print("\nAÑOS")
print("-" * 40)

print(
    sorted(
        graduados_unificado[
            "anio"
        ]
        .dropna()
        .unique()
        .tolist()
    )
)


# ------------------------------------------------------------
# 20.4 REGISTROS POR AÑO
# ------------------------------------------------------------

print("\nREGISTROS POR AÑO")
print("-" * 40)

display(
    graduados_unificado
    .groupby("anio")
    .size()
    .sort_index()
)


# ------------------------------------------------------------
# 20.5 FALTANTES
# ------------------------------------------------------------

print("\nVALORES FALTANTES")
print("-" * 40)

faltantes_final = (
    graduados_unificado
    .isna()
    .sum()
    .sort_values(
        ascending=False
    )
)

display(
    faltantes_final[
        faltantes_final > 0
    ]
    .to_frame(
        "cantidad_faltantes"
    )
)


# ------------------------------------------------------------
# 20.6 DUPLICADOS EXACTOS
# ------------------------------------------------------------

print("\nDUPLICADOS EXACTOS")
print("-" * 40)

print(
    "Duplicados:",
    graduados_unificado
    .duplicated()
    .sum()
)


# ------------------------------------------------------------
# 20.7 TIPOS
# ------------------------------------------------------------

print("\nTIPOS DE DATOS")
print("-" * 40)

display(
    graduados_unificado
    .dtypes
    .to_frame(
        "tipo"
    )
)

_tiempo_proceso_20 = time.perf_counter() - _inicio_proceso_20
print(f"\nTiempo PROCESO 20: {_tiempo_proceso_20:.2f} segundos")

_inicio_proceso_21 = time.perf_counter()

# ============================================================
# PROCESO 21. VALIDACIÓN ESPECÍFICA DE LAS TRES VARIABLES IES
# ============================================================

print("=" * 70)
print("VALIDACIÓN FINAL DE LAS VARIABLES INSTITUCIONALES")
print("=" * 70)

resumen_ies = pd.DataFrame({

    "variable": [
        "codigo_institucion",
        "institucion",
        "ies_padre"
    ],

    "registros": [
        len(graduados_unificado),
        len(graduados_unificado),
        len(graduados_unificado)
    ],

    "con_dato": [
        graduados_unificado[
            "codigo_institucion"
        ].notna().sum(),

        graduados_unificado[
            "institucion"
        ].notna().sum(),

        graduados_unificado[
            "ies_padre"
        ].notna().sum()
    ],

    "faltantes": [
        graduados_unificado[
            "codigo_institucion"
        ].isna().sum(),

        graduados_unificado[
            "institucion"
        ].isna().sum(),

        graduados_unificado[
            "ies_padre"
        ].isna().sum()
    ],

    "valores_distintos": [
        graduados_unificado[
            "codigo_institucion"
        ].nunique(dropna=True),

        graduados_unificado[
            "institucion"
        ].nunique(dropna=True),

        graduados_unificado[
            "ies_padre"
        ].nunique(dropna=True)
    ]
})

display(
    resumen_ies
)

_tiempo_proceso_21 = time.perf_counter() - _inicio_proceso_21
print(f"\nTiempo PROCESO 21: {_tiempo_proceso_21:.2f} segundos")

_inicio_proceso_22 = time.perf_counter()

# ============================================================
# PROCESO 22. GUARDAR BASE MAESTRA EN PLATA
# ============================================================

ruta_csv = os.path.join(
    CARPETA_PLATA,
    "SNIES_Graduados_Unificado_2014_2025.csv"
)

ruta_parquet = os.path.join(
    CARPETA_PLATA,
    "SNIES_Graduados_Unificado_2014_2025.parquet"
)


# ------------------------------------------------------------
# GUARDAR CSV
# ------------------------------------------------------------

graduados_unificado.to_csv(
    ruta_csv,
    index=False,
    encoding="utf-8-sig"
)


# ------------------------------------------------------------
# GUARDAR PARQUET
# ------------------------------------------------------------

graduados_unificado.to_parquet(
    ruta_parquet,
    index=False
)


print("=" * 70)
print("BASE MAESTRA DE GRADUADOS GUARDADA")
print("=" * 70)

print(
    "Registros:",
    f"{len(graduados_unificado):,}"
)

print(
    "Variables:",
    len(graduados_unificado.columns)
)

print(
    "Periodo:",
    graduados_unificado[
        "anio"
    ].min(),
    "–",
    graduados_unificado[
        "anio"
    ].max()
)

print("\nCSV:")
print(ruta_csv)

print("\nParquet:")
print(ruta_parquet)

_tiempo_proceso_22 = time.perf_counter() - _inicio_proceso_22
print(f"\nTiempo PROCESO 22: {_tiempo_proceso_22:.2f} segundos")

_inicio_proceso_23 = time.perf_counter()

# ============================================================
# PROCESO 23. VERIFICAR ARCHIVOS DE SALIDA
# ============================================================

print("=" * 70)
print("VERIFICACIÓN DE ARCHIVOS")
print("=" * 70)

for archivo in [
    ruta_csv,
    ruta_parquet
]:

    if os.path.exists(archivo):

        tamano_mb = (
            os.path.getsize(archivo)
            / (1024 ** 2)
        )

        print(
            f"✓ {os.path.basename(archivo)}"
        )

        print(
            f"  Tamaño: {tamano_mb:.2f} MB"
        )

    else:

        print(
            f"✗ NO ENCONTRADO: {archivo}"
        )


print(
    "\nContenido de Plata/Graduados:"
)

print(
    os.listdir(
        CARPETA_PLATA
    )
)

_tiempo_proceso_23 = time.perf_counter() - _inicio_proceso_23
print(f"\nTiempo PROCESO 23: {_tiempo_proceso_23:.2f} segundos")

