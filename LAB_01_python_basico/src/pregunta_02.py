def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    conteo = {}

    with open('files/input/data.csv', 'r') as data:
        
        for line in data:
            letra = line.strip().split('\t')[0]
            conteo[letra] = conteo.get(letra, 0) + 1

    return sorted(conteo.items())

    print(pregunta_02())
