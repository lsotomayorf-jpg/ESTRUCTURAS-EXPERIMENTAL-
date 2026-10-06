"""Ejercicio 5 · Tuplas como registros inmutables"""

ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]

total = sum(monto for _mes, monto in ventas)                       # desempaquetado
mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])   # desempaquetado

print(f"Total: {total}")                                           # 4500
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")                 # febrero con 1800

print()
for mes, monto in ventas:                                          # desempaquetado en el for
    print(f"{mes:<10} {monto}")
