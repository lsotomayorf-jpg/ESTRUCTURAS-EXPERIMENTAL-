"""Ejercicio 1 · Quitar duplicados conservando el orden"""

ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()     # SET de control: pregunta rápido si la ciudad ya apareció
unicas = []        # LISTA de resultado: conserva el orden de aparición
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print("Original:", ciudades)
print("Sin repetidos:", unicas)    # ['Quito', 'Guayaquil', 'Cuenca']

