import os
import re

import pandas as pd

ruta_archivo = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "clusters_report.txt"
)

# Una línea de registro nuevo luce así:
#    0      105     15,9 %    palabra, otra palabra,
PATRON_REGISTRO = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d.,]+)\s*%\s*(.*)$")


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    registros = []

    for linea in lineas:
        if not linea.strip():
            continue

        coincidencia = PATRON_REGISTRO.match(linea)

        if coincidencia:
            cluster, cantidad, porcentaje, palabras = coincidencia.groups()
            registros.append(
                {
                    "cluster": int(cluster),
                    "cantidad_de_palabras_clave": int(cantidad),
                    "porcentaje_de_palabras_clave": float(porcentaje.replace(",", ".")),
                    "principales_palabras_clave": palabras.strip(),
                }
            )
        elif registros:
            # Línea de continuación: sus palabras pertenecen al último clúster
            registros[-1]["principales_palabras_clave"] += " " + linea.strip()

    df = pd.DataFrame(registros)

    # Deja las palabras como "palabra1, palabra2, palabra3"
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.rstrip(".")
        .apply(
            lambda texto: ", ".join(p.strip() for p in texto.split(",") if p.strip())
        )
    )

    return df


if __name__ == "__main__":
    print(pregunta_01())