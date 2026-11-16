import os

import pandas as pd

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "tbl0.tsv"
)


def pregunta_05():
    """
    Usando `data/tbl0.tsv`, encuentre el valor máximo de la columna `c2` para
    cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice
    son las categorías, en orden alfabético, y cuyos valores son los máximos.

    Ejemplo del formato de la respuesta:

        c1
        A    9
        B    9
        C    9
        ...
    """
    df = pd.read_csv(ruta_archivo, sep="\t")

    return df.groupby("c1")["c2"].max()


if __name__ == "__main__":
    print(pregunta_05())