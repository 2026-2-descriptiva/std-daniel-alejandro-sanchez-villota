import os

import pandas as pd

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "tbl2.tsv"
)


def pregunta_12():
    """
    En `data/tbl2.tsv`, cada valor de la columna `c0` aparece en varias
    filas. Construya un DataFrame con una fila por cada valor de `c0`, en
    orden ascendente, y las columnas `c0` y `c5`. En `c5`, forme un texto
    `c5a:c5b` para cada fila de ese `c0`, ordene esos textos alfabéticamente y
    únalos separados por comas.

    Ejemplo del formato de la respuesta:

            c0                             c5
        0    0  bbb:0,ddd:9,ggg:8,hhh:2,jjj:3
        1    1        aaa:3,ccc:2,ddd:0,hhh:9
        2    2        ccc:6,ddd:2,ggg:5,jjj:1
        ...
    """
    df = pd.read_csv(ruta_archivo, sep="\t")

    # Paso 1: el par "clave:valor" de cada fila
    df["c5"] = df["c5a"] + ":" + df["c5b"].astype(str)

    # Paso 2: agrupar por c0 y pegar los pares ordenados
    return (
        df.groupby("c0")["c5"]
        .apply(lambda pares: ",".join(sorted(pares)))
        .reset_index()
    )


if __name__ == "__main__":
    print(pregunta_12())