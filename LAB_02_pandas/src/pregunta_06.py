import os

import pandas as pd

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "tbl1.tsv"
)


def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """
    df = pd.read_csv(ruta_archivo, sep="\t")

    return sorted(df["c4"].str.upper().unique())


if __name__ == "__main__":
    print(pregunta_06())