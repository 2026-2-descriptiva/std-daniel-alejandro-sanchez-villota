import gzip
import os

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "data.csv.gz"
)


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    conteo = {}
    with gzip.open(ruta_archivo, "rt") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")
            if columnas and columnas[0]:
                letra = columnas[0]
                # Si la letra no existe en el diccionario, arranca en 0
                conteo[letra] = conteo.get(letra, 0) + 1

    # dict.items() da tuplas (letra, cantidad); sorted las ordena por la letra
    return sorted(conteo.items())


if __name__ == "__main__":
    print(pregunta_02())