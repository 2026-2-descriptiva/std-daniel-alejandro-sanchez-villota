import gzip
import os

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "data.csv.gz"
)


def leer_registros():
    """Lee el archivo comprimido y retorna una lista de columnas por registro."""
    registros = []
    with gzip.open(ruta_archivo, "rt") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")
            if len(columnas) == 5:
                registros.append(columnas)
    return registros


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """
    valores = {}
    for _, _, _, _, metricas in leer_registros():
        for par in metricas.split(","):
            clave, valor = par.split(":")
            valores.setdefault(clave, []).append(int(valor))

    return [(clave, min(lista), max(lista)) for clave, lista in sorted(valores.items())]


if __name__ == "__main__":
    print(pregunta_06())
