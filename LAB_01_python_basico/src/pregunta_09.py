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


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """
    conteo = {}
    for _, _, _, _, metricas in leer_registros():
        for par in metricas.split(","):
            clave = par.split(":")[0]
            conteo[clave] = conteo.get(clave, 0) + 1

    return dict(sorted(conteo.items()))


if __name__ == "__main__":
    print(pregunta_09())
