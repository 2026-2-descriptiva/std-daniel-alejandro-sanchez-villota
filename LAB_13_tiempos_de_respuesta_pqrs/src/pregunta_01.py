import os

import numpy as np
import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_data = os.path.join(directorio, "..", "data")
ruta_submission = os.path.join(directorio, "..", "submission")

PLAZO_HABIL = 15

ARCHIVOS = {
    "letter": "historical_requests_letter.csv.gz",
    "web": "historical_requests_web.csv.gz",
}


def dias_habiles(entrada, salida):
    """Días lunes a viernes posteriores a `entrada`, hasta `salida` incluida."""
    inicio = (entrada + pd.Timedelta(days=1)).to_numpy().astype("datetime64[D]")
    fin = (salida + pd.Timedelta(days=1)).to_numpy().astype("datetime64[D]")
    return np.busday_count(inicio, fin)


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """
    # Cada canal se deduplica por separado, antes de unirlos
    partes = []
    for canal, archivo in ARCHIVOS.items():
        parte = pd.read_csv(
            os.path.join(ruta_data, archivo), parse_dates=["in_date", "out_date"]
        ).drop_duplicates()
        parte["channel"] = canal
        partes.append(parte)

    df = pd.concat(partes, ignore_index=True)

    # Estado y tiempos de respuesta
    respondidas = df["out_date"].notna()

    df["answered"] = respondidas.astype(int)
    df["pending"] = (~respondidas).astype(int)
    df["calendar_days"] = (df["out_date"] - df["in_date"]).dt.days

    df["business_days"] = np.nan
    df.loc[respondidas, "business_days"] = dias_habiles(
        df.loc[respondidas, "in_date"], df.loc[respondidas, "out_date"]
    )

    # Pendiente = no cumplió; el fillna(False) lo deja en 0
    df["on_time"] = (df["business_days"] <= PLAZO_HABIL).fillna(False).astype(int)

    df["year"] = df["in_date"].dt.year

    # ----- 1. Por canal -----
    channel_summary = (
        df.groupby("channel")
        .agg(
            requests=("channel", "size"),
            answered=("answered", "sum"),
            pending=("pending", "sum"),
            median_business_days=("business_days", "median"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
        .sort_values("channel")
    )

    # ----- 2. Por año y canal -----
    yearly_summary = (
        df.groupby(["year", "channel"])
        .agg(
            requests=("channel", "size"),
            pending=("pending", "sum"),
            on_time_rate=("on_time", "mean"),
        )
        .reset_index()
        .sort_values(["year", "channel"])
    )

    # ----- 3. Por día de entrada -----
    entry_day_summary = (
        df.groupby("day_name")
        .agg(
            requests=("day_name", "size"),
            median_calendar_days=("calendar_days", "median"),
            median_business_days=("business_days", "median"),
        )
        .reset_index()
    )

    # El orden lunes-domingo se deduce de las fechas, no de los nombres
    orden = df.drop_duplicates("day_name").set_index("day_name")["in_date"].dt.dayofweek
    entry_day_summary = (
        entry_day_summary.assign(_orden=entry_day_summary["day_name"].map(orden))
        .sort_values("_orden")
        .drop(columns="_orden")
        .reset_index(drop=True)
    )

    os.makedirs(ruta_submission, exist_ok=True)
    tablas = [
        ("channel_summary", channel_summary),
        ("yearly_summary", yearly_summary),
        ("entry_day_summary", entry_day_summary),
    ]
    for nombre, tabla in tablas:
        tabla.to_csv(os.path.join(ruta_submission, f"{nombre}.csv"), index=False)

    return channel_summary, yearly_summary, entry_day_summary


if __name__ == "__main__":
    channel, yearly, entry = pregunta_01()
    print(channel)
    print(yearly.head())
    print(entry)