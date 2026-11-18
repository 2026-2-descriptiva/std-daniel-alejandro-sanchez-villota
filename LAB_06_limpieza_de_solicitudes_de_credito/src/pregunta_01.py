import os
import re

import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(directorio, "..", "data", "solicitudes_de_credito.csv.gz")
ruta_submission = os.path.join(directorio, "..", "submission")

COLUMNAS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "estrato",
    "comuna_ciudadano",
    "fecha_de_beneficio",
    "monto_del_credito",
    "línea_credito",
]

COLUMNAS_TEXTO = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "línea_credito",
]


def normalizar_texto(serie):
    """minúsculas y palabras separadas por un solo espacio."""
    return (
        serie.str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def normalizar_fecha(valor):
    """Unifica DD/MM/AAAA y AAAA/MM/DD en AAAA-MM-DD."""
    partes = str(valor).strip().replace("-", "/").split("/")

    if len(partes[0]) == 4:
        anio, mes, dia = partes
    else:
        dia, mes, anio = partes

    return f"{anio}-{mes.zfill(2)}-{dia.zfill(2)}"


def normalizar_monto(valor):
    """Quita $, espacios y separadores de miles; devuelve un entero."""
    texto = re.sub(r"[^\d.]", "", str(valor))

    # Si hay más de un punto, son separadores de miles, no decimales
    if texto.count(".") > 1:
        texto = texto.replace(".", "")

    return int(float(texto))


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """
    # index_col=0 descarta la columna de índice que trae el archivo
    df = pd.read_csv(ruta_archivo, sep=";", index_col=0, dtype=str)

    # Registros incompletos, salvo los de comuna_ciudadano
    obligatorias = [c for c in COLUMNAS if c != "comuna_ciudadano"]
    df = df.dropna(subset=obligatorias)

    # Campos de texto
    for columna in COLUMNAS_TEXTO:
        df[columna] = normalizar_texto(df[columna])

    # Numéricos y fechas
    df["estrato"] = df["estrato"].astype(float).astype(int)
    df["monto_del_credito"] = df["monto_del_credito"].apply(normalizar_monto)
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(normalizar_fecha)

    # Los duplicados solo aparecen una vez todo está normalizado
    df = df[COLUMNAS].drop_duplicates()

    os.makedirs(ruta_submission, exist_ok=True)
    df.to_csv(
        os.path.join(ruta_submission, "solicitudes_de_credito.csv"),
        sep=";",
        index=False,
    )

    return df


if __name__ == "__main__":
    resultado = pregunta_01()
    print(resultado.head())
    print(resultado.shape)