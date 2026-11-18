import json
import os
import re

import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(directorio, "..", "data", "ventas.csv.gz")
ruta_submission = os.path.join(directorio, "..", "submission")

COLUMNAS_REQUERIDAS = [
    "supplier_id",
    "supplier",
    "country",
    "city",
    "purchase_date",
    "amount",
    "discount",
    "weight",
    "units",
    "unit_price",
    "contact_email",
]

PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")


def normalizar_encabezado(nombre):
    """minúsculas, sin BOM, sin espacios externos, espacios internos como _."""
    limpio = nombre.replace("\ufeff", "").strip().lower()
    return re.sub(r"\s+", "_", limpio)


def es_faltante(valor):
    """Celda vacía o con `N/A`."""
    texto = str(valor).strip()
    return texto == "" or texto.upper() == "N/A"


def es_unidad_invalida(valor):
    """Valor numérico que no es un entero positivo."""
    if es_faltante(valor):
        return False

    try:
        numero = float(str(valor).strip())
    except ValueError:
        return False  # no es numérico, no aplica esta regla

    return not (numero > 0 and numero.is_integer())


def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """
    # dtype=str y keep_default_na=False preservan los valores tal cual
    df = pd.read_csv(ruta_archivo, dtype=str, keep_default_na=False)
    df.columns = [normalizar_encabezado(columna) for columna in df.columns]

    columnas = list(df.columns)

    reporte = {
        "row_count": int(len(df)),
        "column_count": int(len(columnas)),
        "missing_required_columns": sorted(
            c for c in COLUMNAS_REQUERIDAS if c not in columnas
        ),
        "unexpected_columns": sorted(
            c for c in columnas if c not in COLUMNAS_REQUERIDAS
        ),
        "duplicate_row_count": int(df.duplicated().sum()),
        "duplicate_supplier_id_row_count": (
            int(df.duplicated(subset=["supplier_id"], keep=False).sum())
            if "supplier_id" in columnas
            else 0
        ),
        "missing_value_count_by_column": {
            columna: int(df[columna].map(es_faltante).sum()) for columna in columnas
        },
        "invalid_email_count": (
            int(
                (
                    ~df["contact_email"].map(
                        lambda v: bool(PATRON_EMAIL.match(str(v).strip()))
                    )
                ).sum()
            )
            if "contact_email" in columnas
            else 0
        ),
        "invalid_unit_count": (
            int(df["units"].map(es_unidad_invalida).sum()) if "units" in columnas else 0
        ),
        "country_values": (
            sorted(df["country"].unique().tolist()) if "country" in columnas else []
        ),
    }

    os.makedirs(ruta_submission, exist_ok=True)
    with open(
        os.path.join(ruta_submission, "data_quality_report.json"),
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(reporte, archivo, indent=2, ensure_ascii=False)

    return reporte


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))