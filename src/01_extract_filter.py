# src/01_extract_filter.py
# revisado, CONFIRMADO!!! TIENE TODAS LAS VARIABLES

import sys
from pathlib import Path

import pandas as pd
import pyreadstat


def mb(n_bytes: int) -> float:
    return n_bytes / (1024 * 1024)


def main():
    # =========================
    # Rutas
    # =========================
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "data" / "raw" / "PISA_2022_STU_QQQ.SAV"
    output_dir = project_root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "pisa_usa_age15to16_ict_filtered.csv"

    if not input_path.exists():
        print(f"[ERROR] No existe el archivo: {input_path}")
        sys.exit(1)

    # =========================
    # Columnas requeridas
    # =========================
    cols_needed = [
        "CNT",
        "Option_ICTQ",
        "AGE",
        "ST004D01T",
    ]

    # PVs
    cols_needed += [f"PV{i}MATH" for i in range(1, 11)]
    cols_needed += [f"PV{i}READ" for i in range(1, 11)]
    cols_needed += [f"PV{i}SCIE" for i in range(1, 11)]

    # Horas generales de uso digital (ST326 subpreguntas)
    cols_needed += [
        "ST326Q01JA",
        "ST326Q02JA",
        "ST326Q03JA",
        "ST326Q04JA",
        "ST326Q05JA",
        "ST326Q06JA",
    ]

    # IC170 (aprendizaje dentro de la escuela, frecuencia) 1..7
    cols_needed += [f"IC170Q0{i}JA" for i in range(1, 8)]

    # IC171 (aprendizaje fuera de la escuela, frecuencia) 1..7  ✅ corregido
    cols_needed += [f"IC171Q0{i}JA" for i in range(1, 7)]

    # IC177 (recreativo entre semana, horas) 1..7  ✅ añadido
    cols_needed += [f"IC177Q0{i}JA" for i in range(1, 8)]

    # IC178 (recreativo fines de semana, horas) 1..7 ✅ añadido
    cols_needed += [f"IC178Q0{i}JA" for i in range(1, 8)]

    # Quitar duplicados
    cols_needed = list(dict.fromkeys(cols_needed))

    # =========================
    # Validación de columnas
    # =========================
    _, meta = pyreadstat.read_sav(str(input_path), metadataonly=True)
    all_cols = set(meta.column_names)

    missing = [c for c in cols_needed if c not in all_cols]
    if missing:
        print("[ERROR] Faltan estas columnas en tu .SAV:")
        for c in missing:
            print(" -", c)
        sys.exit(1)

    # =========================
    # Lectura eficiente
    # =========================
    print("[INFO] Leyendo .SAV con solo las columnas necesarias...")
    df, _ = pyreadstat.read_sav(str(input_path), usecols=cols_needed)
    print(f"[INFO] Cargado inicial: {df.shape[0]:,} filas x {df.shape[1]:,} columnas")

    # =========================
    # Filtros: USA + ICTQ
    # =========================
    df = df[df["CNT"] == "USA"].copy()
    df = df[df["Option_ICTQ"] == 1].copy()

    # =========================
    # Filtro de edad: 15 hasta <17 (incluye 15.xx y 16.xx)
    # =========================
    df["AGE"] = pd.to_numeric(df["AGE"], errors="coerce")

    print("\n===== EDADES ANTES DEL FILTRO (USA + ICTQ) =====")
    print("Rango:", df["AGE"].min(), "a", df["AGE"].max())
    print("================================================\n")

    df = df[(df["AGE"] >= 15) & (df["AGE"] < 17)].copy()

    print("===== EDADES DESPUÉS DEL FILTRO (15 <= AGE < 17) =====")
    print("Rango:", df["AGE"].min(), "a", df["AGE"].max())
    print("Registros:", f"{df.shape[0]:,}")
    print("======================================================\n")

    # Eliminar columnas usadas solo para filtrar
    df.drop(columns=["CNT", "Option_ICTQ"], inplace=True)

    print(f"[INFO] Dataset final: {df.shape[0]:,} filas x {df.shape[1]:,} columnas")

    # =========================
    # Exportar a CSV
    # =========================
    print(f"[INFO] Exportando a CSV: {output_csv}")
    df.to_csv(output_csv, index=False)

    file_size_bytes = output_csv.stat().st_size
    print("\n===== RESUMEN FINAL =====")
    print(f"Archivo generado: {output_csv}")
    print(f"Dimensiones: {df.shape[0]:,} filas x {df.shape[1]:,} columnas")
    print(f"Tamaño CSV: {mb(file_size_bytes):.2f} MB")
    print("=========================")


if __name__ == "__main__":
    main()