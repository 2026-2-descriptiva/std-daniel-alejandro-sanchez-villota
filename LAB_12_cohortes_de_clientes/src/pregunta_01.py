import os

import matplotlib

matplotlib.use("Agg")  # backend sin ventana, para que corra en cualquier parte

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(directorio, "..", "data", "sales.csv.gz")
ruta_submission = os.path.join(directorio, "..", "submission")


def dibujar_mapa_de_calor(cohortes, ruta_png):
    """Mapa de calor de retención, con las celdas no observadas en blanco."""
    matriz = cohortes.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )

    datos = np.ma.masked_invalid(matriz.to_numpy(dtype=float))

    paleta = plt.get_cmap("Blues").copy()
    paleta.set_bad("white")  # así se ven vacías las celdas sin dato

    alto = 1.5 + 0.45 * len(matriz.index)
    ancho = 2.0 + 0.7 * len(matriz.columns)
    figura, ejes = plt.subplots(figsize=(ancho, alto))

    imagen = ejes.imshow(datos, cmap=paleta, aspect="auto", vmin=0, vmax=1)

    ejes.set_xticks(range(len(matriz.columns)), matriz.columns)
    ejes.set_yticks(range(len(matriz.index)), matriz.index)
    ejes.set_xlabel("Períodos desde la primera compra")
    ejes.set_ylabel("Cohorte")
    ejes.set_title("Retención por cohorte")

    for fila in range(datos.shape[0]):
        for columna in range(datos.shape[1]):
            if datos.mask[fila, columna]:
                continue
            valor = datos[fila, columna]
            ejes.text(
                columna,
                fila,
                f"{valor * 100:.1f}%",
                ha="center",
                va="center",
                fontsize=7,
                color="white" if valor > 0.5 else "black",
            )

    figura.colorbar(imagen, ax=ejes, label="Retención")
    figura.tight_layout()
    figura.savefig(ruta_png, dpi=150)
    plt.close(figura)


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """
    df = pd.read_csv(ruta_archivo, parse_dates=["OrderDate"])

    # Mes de cada orden y mes de la primera compra de cada cliente
    df["order_month"] = df["OrderDate"].dt.to_period("M")
    df["cohort_month"] = df.groupby("CustomerID")["order_month"].transform("min")

    # Meses transcurridos, calculados sobre año y mes para evitar ambigüedades
    df["period_index"] = (
        df["order_month"].dt.year - df["cohort_month"].dt.year
    ) * 12 + (df["order_month"].dt.month - df["cohort_month"].dt.month)

    cohortes = (
        df.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )

    # El tamaño de la cohorte son sus activos en el período 0
    tamanos = cohortes[cohortes["period_index"] == 0].set_index("cohort_month")[
        "active_customers"
    ]
    cohortes["cohort_size"] = cohortes["cohort_month"].map(tamanos)
    cohortes["retention_rate"] = cohortes["active_customers"] / cohortes["cohort_size"]

    cohortes["cohort_month"] = cohortes["cohort_month"].astype(str)
    cohortes = cohortes.sort_values(["cohort_month", "period_index"]).reset_index(
        drop=True
    )

    os.makedirs(ruta_submission, exist_ok=True)
    cohortes.to_csv(os.path.join(ruta_submission, "cohort_retention.csv"), index=False)
    dibujar_mapa_de_calor(
        cohortes, os.path.join(ruta_submission, "cohort_retention_heatmap.png")
    )

    return cohortes


if __name__ == "__main__":
    print(build_cohort_analysis().head(12))