import json
import os

import numpy as np
import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(directorio, "..", "data", "insurance.csv.gz")
ruta_submission = os.path.join(directorio, "..", "submission")

K = 5

QI_ORIGINALES = ["age", "sex", "bmi", "children", "region"]

ESQUEMAS = {
    "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
    "without_children": ["age_group", "sex", "bmi_group", "region"],
}


def generalizar(df):
    """Agrega las columnas generalizadas al DataFrame."""
    df = df.copy()

    df["age_group"] = pd.cut(
        df["age"],
        bins=[18, 30, 40, 50, 65],
        right=False,
        labels=["18-29", "30-39", "40-49", "50-64"],
    ).astype(str)

    df["bmi_group"] = pd.cut(
        df["bmi"],
        bins=[-np.inf, 18.5, 25, 30, np.inf],
        right=False,
        labels=["bajo peso", "normal", "sobrepeso", "obesidad"],
    ).astype(str)

    df["children_group"] = pd.cut(
        df["children"],
        bins=[0, 1, 3, np.inf],
        right=False,
        labels=["0", "1-2", "3+"],
    ).astype(str)

    return df


def evaluar_esquema(df, quasi_identifiers):
    """Mide un esquema y devuelve su resumen y los registros publicados."""
    tamano_de_clase = df.groupby(quasi_identifiers)["charges"].transform("size")
    publicados = df[tamano_de_clase >= K]

    clases = df.groupby(quasi_identifiers).size()

    # Diversidad del atributo sensible entre las clases publicadas
    diversidad = publicados.groupby(quasi_identifiers)["smoker"].nunique()
    tamanos_publicados = publicados.groupby(quasi_identifiers).size()
    sin_diversidad = diversidad == 1

    resumen = {
        "quasi_identifiers": list(quasi_identifiers),
        "equivalence_classes": int(len(clases)),
        "k_before_suppression": int(clases.min()),
        "suppressed_records": int((tamano_de_clase < K).sum()),
        "published_records": int(len(publicados)),
        "published_classes": int((clases >= K).sum()),
        "classes_without_smoker_diversity": int(sin_diversidad.sum()),
        "records_without_smoker_diversity": int(
            tamanos_publicados[sin_diversidad].sum()
        ),
    }

    return resumen, publicados


def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """
    df = pd.read_csv(ruta_archivo)
    df = generalizar(df)

    # Riesgo sin generalizar
    clases_originales = df.groupby(QI_ORIGINALES).size()

    # Evaluación de los dos esquemas
    resumenes = {}
    publicados_por_esquema = {}

    for nombre, quasi_identifiers in ESQUEMAS.items():
        resumen, publicados = evaluar_esquema(df, quasi_identifiers)
        resumenes[nombre] = resumen
        publicados_por_esquema[nombre] = publicados

    # El esquema que suprime menos registros
    seleccionado = min(
        resumenes, key=lambda nombre: resumenes[nombre]["suppressed_records"]
    )
    publicados = publicados_por_esquema[seleccionado]
    columnas_publicadas = ESQUEMAS[seleccionado] + ["smoker", "charges"]

    reporte = {
        "original_k": int(clases_originales.min()),
        "original_unique_records": int((clases_originales == 1).sum()),
        "schemes": resumenes,
        "selected_scheme": seleccionado,
        "mean_charges_original": float(df["charges"].mean()),
        "mean_charges_published": float(publicados["charges"].mean()),
        "smoker_rate_original": float((df["smoker"] == "yes").mean()),
        "smoker_rate_published": float((publicados["smoker"] == "yes").mean()),
    }

    os.makedirs(ruta_submission, exist_ok=True)

    with open(
        os.path.join(ruta_submission, "privacy_report.json"), "w", encoding="utf-8"
    ) as archivo:
        json.dump(reporte, archivo, indent=2, ensure_ascii=False)

    publicados[columnas_publicadas].to_csv(
        os.path.join(ruta_submission, "insurance_published.csv"), index=False
    )

    return reporte


if __name__ == "__main__":
    print(json.dumps(pregunta_01(), indent=2, ensure_ascii=False))