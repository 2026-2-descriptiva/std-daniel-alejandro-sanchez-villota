import glob
import os

import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_data = os.path.join(directorio, "..", "data")
ruta_submission = os.path.join(directorio, "..", "submission")

MESES = {
    "jan": "01",
    "feb": "02",
    "mar": "03",
    "apr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "aug": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dec": "12",
}


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Los datos de una campaña de mercadeo bancario llegaron repartidos en diez
    archivos comprimidos, `data/bank-marketing-campaing-*.csv.gz`, con
    información mezclada del cliente, de la campaña y del contexto económico.
    Su tarea es leerlos directamente desde los archivos comprimidos, sin
    descomprimirlos a mano, y separarlos en tres tablas limpias.

    Guarde cada tabla como un CSV sin comprimir en `submission/`, sin el índice
    de Pandas y con las columnas en el orden indicado:

    1. `client.csv`: `client_id`, `age`, `job`, `marital`, `education`,
       `credit_default` y `mortgage`.
       - En `job`, elimine los puntos y cambie los guiones por guiones bajos.
       - En `education`, cambie los puntos por guiones bajos y deje el valor
         `unknown` como faltante.
       - En `credit_default` y `mortgage`, escriba 1 si el valor es `yes` y 0
         en cualquier otro caso.

    2. `campaign.csv`: `client_id`, `number_contacts`, `contact_duration`,
       `previous_campaign_contacts`, `previous_outcome`, `campaign_outcome` y
       `last_contact_date`.
       - En `previous_outcome`, escriba 1 si el valor es `success` y 0 en
         cualquier otro caso.
       - En `campaign_outcome`, escriba 1 si el valor es `yes` y 0 en
         cualquier otro caso.
       - Construya `last_contact_date` a partir de las columnas `month` y
         `day`, usando el año 2022 y el formato `AAAA-MM-DD`.

    3. `economics.csv`: `client_id`, `cons_price_idx` y
       `euribor_three_months`.

    La función también debe retornar las tres tablas, en el orden `client`,
    `campaign` y `economics`.

    Ejemplo del formato de `campaign.csv`:

        client_id,number_contacts,contact_duration,...,last_contact_date
        0,1,261,...,2022-05-13
        ...
    """
    # pandas descomprime el .gz solo, por la extensión
    archivos = sorted(
        glob.glob(os.path.join(ruta_data, "bank-marketing-campaing-*.csv.gz"))
    )
    df = pd.concat([pd.read_csv(archivo) for archivo in archivos], ignore_index=True)

    # Descarta la columna de índice si los archivos la traen
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

    # ----- client -----
    client = df[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )
    client["education"] = (
        client["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    )
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # ----- campaign -----
    campaign = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
        ]
    ].copy()

    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(
        int
    )
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)
    campaign["last_contact_date"] = (
        "2022-"
        + df["month"].str.lower().map(MESES)
        + "-"
        + df["day"].astype(str).str.zfill(2)
    )

    # ----- economics -----
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    os.makedirs(ruta_submission, exist_ok=True)
    for nombre, tabla in [
        ("client", client),
        ("campaign", campaign),
        ("economics", economics),
    ]:
        tabla.to_csv(os.path.join(ruta_submission, f"{nombre}.csv"), index=False)

    return client, campaign, economics


if __name__ == "__main__":
    client, campaign, economics = clean_campaign_data()
    print(client.head())
    print(campaign.head())
    print(economics.head())