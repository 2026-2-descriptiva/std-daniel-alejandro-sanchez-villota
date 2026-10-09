def pregunta_04():

    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.

    Ejemplo del formato de la respuesta:

        [("01", 3), ("02", 4), ("03", 2), ...]
    """
    with open("LAB_01_python_basico/data/data.csv", "r") as f:
      
       data = f.readlines()

    month_counts = {}
    for line in data:
        parts = line.strip().split("\t")
        date = parts[2]
        month = date.split("-")[1]
        if month in month_counts:
            month_counts[month] += 1
        else:
            month_counts[month] = 1

    result = sorted((month, month_counts[month]) for month in sorted(month_counts))
    return result

print(pregunta_04())  