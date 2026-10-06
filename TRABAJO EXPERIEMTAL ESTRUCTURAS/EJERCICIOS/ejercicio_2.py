"""Ejercicio 2 · Contar con un diccionario"""

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

conteo = {}
for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1    # .get evita el KeyError la 1.ª vez

print("Conteo:", conteo)    # {'Quito': 2, 'Guayaquil': 2, 'Cuenca': 1}

# El más repetido (en empate devuelve el primero que apareció)
mas_repetida = max(conteo, key=conteo.get)
print(f"Más repetida: {mas_repetida} ({conteo[mas_repetida]} veces)")
