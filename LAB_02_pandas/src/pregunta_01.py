import os

import pandas as pd

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "tbl0.tsv"
)


def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """
    df = pd.read_csv(ruta_archivo, sep="\t")

    return len(df)


if __name__ == "__main__":
    print(pregunta_01())