import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. CARGA DE DATOS
# ============================================================

archivo = (
    r"C:\Proyecto_STEM\Graduados\Plata"
    r"\SNIES_Graduados_Unificado_2001_2025.parquet"
)

df = pd.read_parquet(archivo)

print("=" * 70)
print("CARGA DE DATOS")
print("=" * 70)

print(f"Filas: {df.shape[0]:,}")
print(f"Columnas: {df.shape[1]}")

# ============================================================
# 2. PREPARACIÓN DE VARIABLES
# ============================================================

df["anio"] = pd.to_numeric(
    df["anio"],
    errors="coerce"
)

df["graduados"] = pd.to_numeric(
    df["graduados"],
    errors="coerce"
)

df["sexo"] = (
    df["sexo"]
    .astype(str)
    .str.strip()
    .str.upper()
)

print("\nTipos principales:")
print(df[["anio", "sexo", "graduados"]].dtypes)

print("\nValores de sexo:")
print(df["sexo"].value_counts(dropna=False))

# ============================================================
# 3. CALIDAD DE DATOS
# ============================================================

print("\n" + "=" * 70)
print("CALIDAD DE DATOS")
print("=" * 70)

print("\nValores nulos:")
print(
    df.isna()
    .sum()
    .sort_values(ascending=False)
)

print("\nFilas duplicadas:")
print(df.duplicated().sum())

print("\nRango de años:")
print(
    int(df["anio"].min()),
    "-",
    int(df["anio"].max())
)

print("\nGraduados totales:")
print(
    f"{df['graduados'].sum():,.0f}"
)