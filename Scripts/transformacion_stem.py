from pathlib import Path
import re
import unicodedata
import pandas as pd

carpeta = Path(__file__).resolve().parent
archivo = carpeta / "SNIES_Matriculados_2025.xlsx"
salida = carpeta / "datos_transformados"
salida.mkdir(exist_ok=True)

# 1. Extraer los datos y retirar espacios estructurales vacíos
df = pd.read_excel(archivo, sheet_name="1.", header=5)
df = df.dropna(how="all").dropna(axis=1, how="all")

# 2. Normalizar nombres de columnas
def normalizar_nombre(nombre):
    nombre = unicodedata.normalize("NFKD", str(nombre))
    nombre = "".join(c for c in nombre if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "_", nombre.lower()).strip("_")

df.columns = [normalizar_nombre(c) for c in df.columns]

# 3. Separar las notas finales, sin confundirlas con datos nulos
es_nota = (
    df["codigo_snies_del_programa"].isna()
    & df["matriculados"].isna()
    & df["codigo_de_la_institucion"].notna()
)
notas = df.loc[es_nota].copy()
df = df.loc[~es_nota].copy()

# 4. Limpiar espacios y convertir cadenas vacías en nulos
for c in df.select_dtypes(include=["object", "string"]).columns:
    df[c] = (
        df[c].astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .replace("", pd.NA)
    )

# 5. Eliminar únicamente duplicados exactos
duplicados = df.loc[df.duplicated()].copy()
df = df.drop_duplicates().copy()

# 6. Convertir y validar variables numéricas esenciales
numericas = ["ano", "semestre", "matriculados"]
for c in numericas:
    df[c] = pd.to_numeric(df[c], errors="coerce")

esenciales = [
    "codigo_de_la_institucion",
    "codigo_snies_del_programa",
    "codigo_del_municipio_programa",
    "id_sexo", "sexo", "ano", "semestre", "matriculados"
]

invalidos = df[esenciales].isna().any(axis=1)
invalidos |= ~df["semestre"].isin([1, 2])
invalidos |= df["matriculados"].lt(0)
for c in numericas:
    invalidos |= df[c].mod(1).ne(0)

revision = df.loc[invalidos].copy()
df = df.loc[~invalidos].copy()

for c in numericas:
    df[c] = df[c].astype("Int64")

# Los identificadores se conservan como texto
codigos = [
    c for c in df.columns
    if c.startswith(("codigo_", "id_")) or c == "ies_padre"
]
for c in codigos:
    df[c] = df[c].astype("string").str.replace(
        r"^(\d+)\.0$", r"\1", regex=True
    )

# Campo amplio CINE: códigos de dos caracteres
df["id_cine_campo_amplio"] = (
    df["id_cine_campo_amplio"].str.zfill(2)
)

# 7. Detectar registros con igual clave, pero información distinta
clave = [
    "codigo_de_la_institucion",
    "codigo_snies_del_programa",
    "codigo_del_municipio_programa",
    "id_sexo", "ano", "semestre"
]
conflictos = df.loc[df.duplicated(clave, keep=False)].copy()
if not conflictos.empty:
    conflictos.to_csv(salida / "conflictos.csv", index=False)
    raise ValueError("Hay claves repetidas. Revisar antes de agregar.")

# 8. Clasificar STEM sin convertir una clasificación ausente en 'No STEM'
df["es_stem"] = df["id_cine_campo_amplio"].isin(
    ["05", "06", "07"]
).astype("boolean")
df.loc[df["id_cine_campo_amplio"].isna(), "es_stem"] = pd.NA

stem = df.loc[df["es_stem"].fillna(False)].copy()

# 9. Resumir por semestre y campo, conservando todos los sexos
grupos = ["ano", "semestre", "id_cine_campo_amplio"]
stem["matriculados_femeninos"] = stem["matriculados"].where(
    stem["sexo"].eq("Femenino"), 0
)

resumen = stem.groupby(grupos, as_index=False).agg(
    total_matriculados=("matriculados", "sum"),
    mujeres_matriculadas=("matriculados_femeninos", "sum")
)
resumen["participacion_femenina_pct"] = (
    100 * resumen["mujeres_matriculadas"]
    / resumen["total_matriculados"].replace(0, pd.NA)
)

# 10. Exportar datos, resultados y registros de revisión
df.to_csv(salida / "matriculados_limpios.csv",
          index=False, encoding="utf-8-sig")
df.to_parquet(salida / "matriculados_limpios.parquet", index=False)
resumen.to_csv(salida / "resumen_stem.csv",
               index=False, encoding="utf-8-sig")

for nombre, tabla in {
    "notas_fuente": notas,
    "duplicados_exactos": duplicados,
    "registros_para_revision": revision
}.items():
    tabla.to_csv(salida / f"{nombre}.csv",
                 index=False, encoding="utf-8-sig")

print("Registros válidos:", len(df))
print("Duplicados retirados:", len(duplicados))
print("Registros para revisión:", len(revision))
print(resumen)