"""
utils/validators.py
Validaciones de campos: email, numérico, longitud, fecha
"""
import re

def validar_email(email: str) -> bool:
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(patron, email.strip()))

def validar_numero(valor: str) -> bool:
    try:
        float(valor.replace(",", ".").replace("$", "").replace(".", "", valor.count(".")-1))
        return True
    except Exception:
        return False

def validar_longitud(texto: str, minimo: int = 2, maximo: int = 100) -> bool:
    return minimo <= len(texto.strip()) <= maximo

def validar_no_vacio(valor: str) -> bool:
    return bool(valor.strip())

def validar_codigo(codigo: str, prefijo: str = "") -> bool:
    if prefijo:
        return codigo.startswith(prefijo) and len(codigo) >= 4
    return len(codigo.strip()) >= 2

def errores_recinto(datos: dict) -> list:
    errs = []
    if not validar_codigo(datos.get("codigo", ""), "RC-"):
        errs.append("Código debe empezar con RC- (ej: RC-001)")
    if not validar_longitud(datos.get("nombre", ""), 3, 100):
        errs.append("Nombre debe tener entre 3 y 100 caracteres")
    if datos.get("capacidad") and not validar_numero(datos["capacidad"]):
        errs.append("Capacidad debe ser un número")
    return errs

def errores_cliente(datos: dict) -> list:
    errs = []
    if not validar_codigo(datos.get("codigo", ""), "CL-"):
        errs.append("Código debe empezar con CL- (ej: CL-001)")
    if not validar_longitud(datos.get("razon", ""), 3, 100):
        errs.append("Razón social debe tener entre 3 y 100 caracteres")
    if datos.get("correo") and not validar_email(datos["correo"]):
        errs.append("Formato de correo inválido (ej: nombre@empresa.com)")
    if datos.get("telefono") and not re.match(r'^[\d\s\+\-\(\)]{7,20}$', datos["telefono"]):
        errs.append("Teléfono debe contener solo dígitos, +, - o paréntesis")
    return errs

def errores_evento(datos: dict) -> list:
    errs = []
    if not validar_codigo(datos.get("num", ""), "EV-"):
        errs.append("N° evento debe empezar con EV- (ej: EV-2026-001)")
    if not validar_longitud(datos.get("titulo", ""), 3, 100):
        errs.append("Título debe tener entre 3 y 100 caracteres")
    if datos.get("asistentes") and not validar_numero(datos["asistentes"]):
        errs.append("N° asistentes debe ser un número")
    return errs

def errores_personal(datos: dict) -> list:
    errs = []
    if not validar_codigo(datos.get("codigo", ""), "EP-"):
        errs.append("Código debe empezar con EP- (ej: EP-001)")
    if not validar_longitud(datos.get("nombres", ""), 2, 60):
        errs.append("Nombres deben tener entre 2 y 60 caracteres")
    if not validar_longitud(datos.get("apellidos", ""), 2, 60):
        errs.append("Apellidos deben tener entre 2 y 60 caracteres")
    if datos.get("tarifa") and not validar_numero(datos["tarifa"].replace("$","").replace(".","").replace("/hora","")):
        errs.append("Tarifa debe contener un valor numérico")
    return errs
