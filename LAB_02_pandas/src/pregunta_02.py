import os

import pandas as pd

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "tbl0.tsv"
)


def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """
    df = pd.read_csv(ruta_archivo, sep="\t")

    return len(df.columns)


if __name__ == "__main__":
    print(pregunta_02())