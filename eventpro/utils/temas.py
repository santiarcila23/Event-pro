"""
utils/temas.py
Dos temas visuales: claro y oscuro
"""

TEMAS = {
    "claro": {
        "bg":          "#F5F5F5",
        "fg":          "#1A1A1A",
        "entry_bg":    "#FFFFFF",
        "entry_fg":    "#000000",
        "btn_guardar": "#4CAF50",
        "btn_actualizar": "#2196F3",
        "btn_eliminar": "#f44336",
        "btn_limpiar": "#FF9800",
        "btn_excel":   "#1D6F42",
        "btn_pdf":     "#C0392B",
        "search_bg":   "#E8E8E8",
        "tab_bg":      "#FFFFFF",
        "titulo_fg":   "#1B4F72",
        "placeholder": "#AAAAAA",
        "card_bg":     "#FFFFFF",
        "header_bg":   "#1B4F72",
        "header_fg":   "#FFFFFF",
    },
    "oscuro": {
        "bg":          "#1A1A2E",
        "fg":          "#EDF2F4",
        "entry_bg":    "#16213E",
        "entry_fg":    "#FFFFFF",
        "btn_guardar": "#27AE60",
        "btn_actualizar": "#2980B9",
        "btn_eliminar": "#C0392B",
        "btn_limpiar": "#E67E22",
        "btn_excel":   "#1D6F42",
        "btn_pdf":     "#922B21",
        "search_bg":   "#0F3460",
        "tab_bg":      "#16213E",
        "titulo_fg":   "#A8DADC",
        "placeholder": "#6C757D",
        "card_bg":     "#16213E",
        "header_bg":   "#E94560",
        "header_fg":   "#FFFFFF",
    }
}

tema_actual = {"nombre": "claro"}

def get_tema():
    return TEMAS[tema_actual["nombre"]]

def cambiar_tema(nombre: str):
    tema_actual["nombre"] = nombre

def tema_opuesto():
    return "oscuro" if tema_actual["nombre"] == "claro" else "claro"
