"""Ejercicio 4 · De lista de diccionarios a índice"""

clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]

indice = {cliente["id"]: cliente for cliente in clientes}    # {id: cliente}

print("Índice:", indice)
print("Nombre del id 2:", indice[2]["nombre"])               # Luis

# Diferencia de costo:
#   recorrer la lista -> revisa hasta N registros
#   indice[2]         -> una sola operación, sin importar cuántos haya
# Es lo mismo que hace una base de datos cuando se crea un índice.
