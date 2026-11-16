import os

import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_tbl0 = os.path.join(directorio, "..", "data", "tbl0.tsv")
ruta_tbl2 = os.path.join(directorio, "..", "data", "tbl2.tsv")


def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """
    tbl0 = pd.read_csv(ruta_tbl0, sep="\t")
    tbl2 = pd.read_csv(ruta_tbl2, sep="\t")

    df = pd.merge(tbl0, tbl2, on="c0")

    return df.groupby("c1")["c5b"].sum()


if __name__ == "__main__":
    print(pregunta_13())