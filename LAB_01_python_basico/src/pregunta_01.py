def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.

    Ejemplo del formato de la respuesta:

        214
    """
    suma = 0

    with open('files/input/data.csv', 'r') as data:

        for linea in data:
            columnas = linea.strip().split('\t')
            suma += int(columnas[1])
            
    return suma
    print(pregunta_01())