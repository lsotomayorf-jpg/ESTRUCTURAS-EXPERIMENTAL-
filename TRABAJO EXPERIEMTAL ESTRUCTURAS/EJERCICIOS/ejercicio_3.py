"""Ejercicio 3 · Conjuntos en acción"""

inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}

ambas = inscritos_matematica & inscritos_ingles                # intersección
solo_mate = inscritos_matematica - inscritos_ingles            # diferencia
total = len(inscritos_matematica | inscritos_ingles)           # unión

print("¿Quiénes están en las dos?      ", sorted(ambas))       # ['Luis', 'Marco']
print("¿Quiénes solo en matemática?    ", sorted(solo_mate))   # ['Ana', 'Sol']
print("¿Cuántos estudiantes distintos? ", total)               # 5
