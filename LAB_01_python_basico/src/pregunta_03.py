def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """
    with open("files/input/data.csv", "r") as f:

        data = f.readlines()

    sums = {}

    for line in data:
        parts = line.strip().split("\t")
        letter = parts[0]
        number = int(parts[1])
        if letter in sums:
            sums[letter] += number
        else:
            sums[letter] = number

    result = sorted((letter, sums[letter]) for letter in sums)
    return result

print(pregunta_03())
