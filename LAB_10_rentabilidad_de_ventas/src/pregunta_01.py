import os

import numpy as np
import pandas as pd

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(directorio, "..", "data", "superstore_orders.csv.gz")
ruta_submission = os.path.join(directorio, "..", "submission")

BANDAS = ["0%", "1%-5%", "6%-10%", "más de 10%"]


def resumir(grupo):
    """Métricas de rentabilidad de un conjunto de líneas de pedido."""
    return grupo.agg(
        lines=("Sales", "size"),
        sales=("Sales", "sum"),
        profit=("Profit", "sum"),
        loss_lines=("is_loss", "sum"),
        loss_line_rate=("is_loss", "mean"),
        lost_profit=("loss_amount", "sum"),
    )


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """
    df = pd.read_csv(ruta_archivo, sep=";", decimal=",")

    # Columnas auxiliares que hacen triviales todas las métricas
    df["is_loss"] = (df["Profit"] < 0).astype(int)
    df["loss_amount"] = -df["Profit"].clip(upper=0)

    df["discount_band"] = pd.cut(
        df["Discount"],
        bins=[-np.inf, 0, 0.05, 0.10, np.inf],
        labels=BANDAS,
    )

    # ----- 1. Resumen general -----
    sales = df["Sales"].sum()
    profit = df["Profit"].sum()

    summary = pd.DataFrame(
        [
            {
                "lines": len(df),
                "orders": df["Order ID"].nunique(),
                "sales": sales,
                "profit": profit,
                "profit_margin": profit / sales,
                "loss_lines": int(df["is_loss"].sum()),
                "loss_line_rate": df["is_loss"].mean(),
                "lost_profit": df["loss_amount"].sum(),
            }
        ]
    )

    # ----- 2. Resumen por rango de descuento -----
    discount = resumir(df.groupby("discount_band", observed=False)).reset_index()
    discount["profit_margin"] = discount["profit"] / discount["sales"]
    discount = discount[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit",
        ]
    ]

    # ----- 3. Segmentos prioritarios -----
    priority = resumir(
        df.groupby(["Customer Segment", "Product Category"])
    ).reset_index()
    priority["profit_margin"] = priority["profit"] / priority["sales"]
    priority = (
        priority[priority["lines"] >= 100]
        .sort_values("lost_profit", ascending=False)
        .head(5)
        .reset_index(drop=True)[
            [
                "Customer Segment",
                "Product Category",
                "lines",
                "sales",
                "profit",
                "profit_margin",
                "lost_profit",
            ]
        ]
    )

    os.makedirs(ruta_submission, exist_ok=True)
    tablas = [
        ("profitability_summary", summary),
        ("discount_summary", discount),
        ("priority_segments", priority),
    ]

    resultados = []
    for nombre, tabla in tablas:
        tabla = tabla.round(4)
        tabla.to_csv(os.path.join(ruta_submission, f"{nombre}.csv"), index=False)
        resultados.append(tabla)

    return tuple(resultados)


if __name__ == "__main__":
    summary, discount, priority = pregunta_01()
    print(summary)
    print(discount)
    print(priority)