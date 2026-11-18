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


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    conteo = {}
    for _, _, fecha, _, _ in leer_registros():
        mes = fecha.split("-")[1]
        conteo[mes] = conteo.get(mes, 0) + 1

    return sorted(conteo.items())


if __name__ == "__main__":
    print(pregunta_04())
