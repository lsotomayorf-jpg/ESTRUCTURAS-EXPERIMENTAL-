from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

# TUPLAS de configuración (fijas)
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")
NOTA_MIN, NOTA_MAX = 0, 20


# ===================== AYUDAS INTERNAS =====================

def emails_registrados(excepto_id=None):
    """CONJUNTO de emails usados."""
    return {r["email"].lower() for r in gestor.leer() if r["id"] != excepto_id}


def carnets_registrados(excepto_id=None):
    """CONJUNTO de carnets usados: detecta duplicados al instante."""
    return {r["carnet"].upper() for r in gestor.leer() if r["id"] != excepto_id}


def siguiente_id():
    ids = [r["id"] for r in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

def crear_estudiante(datos):
    """Devuelve (exito, mensaje)."""
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

        faltantes = [c for c in CAMPOS_OBLIGATORIOS if not valores[c]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        if valores["email"].lower() in emails_registrados():
            return False, "Ese email ya está registrado"

        if valores["carnet"].upper() in carnets_registrados():
            return False, "Ese carnet ya está registrado"

        estudiante = Estudiante(siguiente_id(), **valores)

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Estudiante {estudiante.obtener_nombre_completo()} creado con id {estudiante.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    return [Estudiante.desde_diccionario(r) for r in gestor.leer()]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for registro in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        if "carnet" in cambios:
            if not cambios["carnet"].strip():
                return False, "El carnet no puede quedar vacío"
            if cambios["carnet"].upper() in carnets_registrados(excepto_id=id_estudiante):
                return False, "Ese carnet ya lo usa otro estudiante"

        registros = gestor.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros[posicion].update(cambios)
        if not gestor.guardar(registros):
            return False, "No se pudo escribir el archivo"
        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    quedan = [r for r in registros if r["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    gestor.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"


# ===================== NOTAS Y MATERIAS =====================

def agregar_nota(id_estudiante, materia, nota):
    """La nota debe ser un número entre 0 y 20."""
    materia = str(materia).strip()
    if not materia:
        return False, "La materia es obligatoria"

    try:
        nota = float(nota)
    except (TypeError, ValueError):
        return False, "La nota debe ser un número"

    if not (NOTA_MIN <= nota <= NOTA_MAX):
        return False, f"La nota debe estar entre {NOTA_MIN} y {NOTA_MAX}"

    if nota == int(nota):
        nota = int(nota)

    registros = gestor.leer()
    for registro in registros:
        if registro["id"] == id_estudiante:
            estudiante = Estudiante.desde_diccionario(registro)
            estudiante.agregar_nota(materia, nota)
            registro.update(estudiante.a_diccionario())
            if not gestor.guardar(registros):
                return False, "No se pudo escribir el archivo"
            return True, f"Nota {nota} agregada en {materia}"

    return False, f"No existe un estudiante con id {id_estudiante}"


def obtener_promedio(id_estudiante):
    """Devuelve (exito, promedio_o_mensaje)."""
    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        return False, f"No existe un estudiante con id {id_estudiante}"
    return True, estudiante.obtener_promedio()


def materias_ofertadas():
    """SET con todas las materias inscritas por todos los estudiantes (UNIÓN)."""
    todas = set()
    for registro in gestor.leer():
        todas |= set(registro.get("materias", []))
    return todas


def estudiantes_en_comun(id_a, id_b):
    """Materias que comparten dos estudiantes (INTERSECCIÓN). Devuelve (exito, set | mensaje)."""
    if id_a == id_b:
        return False, "Elija dos estudiantes distintos"
    a = obtener_por_id(id_a)
    b = obtener_por_id(id_b)
    if not a:
        return False, f"No existe un estudiante con id {id_a}"
    if not b:
        return False, f"No existe un estudiante con id {id_b}"
    return True, a.materias_en_comun(b)
