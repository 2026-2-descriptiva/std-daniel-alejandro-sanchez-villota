import os

import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_data = os.path.join(directorio, "..", "data")
ruta_submission = os.path.join(directorio, "..", "submission")


def construir_dataset(division):
    """Recorre `data/<division>/<sentimiento>/*.txt` y arma el DataFrame."""
    ruta_division = os.path.join(ruta_data, division)
    registros = []

    # sorted() garantiza el mismo orden en cualquier sistema operativo
    for sentimiento in sorted(os.listdir(ruta_division)):
        ruta_sentimiento = os.path.join(ruta_division, sentimiento)

        if not os.path.isdir(ruta_sentimiento):
            continue

        for nombre_archivo in sorted(os.listdir(ruta_sentimiento)):
            ruta_frase = os.path.join(ruta_sentimiento, nombre_archivo)

            with open(ruta_frase, "r", encoding="utf-8") as archivo:
                registros.append(
                    {"phrase": archivo.read().strip(), "target": sentimiento}
                )

    return pd.DataFrame(registros)


def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """
    os.makedirs(ruta_submission, exist_ok=True)

    for division in ["train", "test"]:
        dataset = construir_dataset(division)
        dataset.to_csv(
            os.path.join(ruta_submission, f"{division}_dataset.csv"),
            index=False,
        )


if __name__ == "__main__":
    pregunta_01()
    print("Datasets generados en submission/")