"""
main.py — EventPro
Sistema de Gestión para Eventos y Convenciones
Arquitectura MVC | MySQL + SP | Excel/PDF | Pillow | tkcalendar | Temas
"""
import os, sys, re, shutil
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk

from models.database   import call_sp, call_sp_fetch, get_conn
from utils.validators  import errores_recinto, errores_cliente, errores_evento, errores_personal
from utils.exportar    import exportar_excel, exportar_pdf
from utils.temas       import get_tema, cambiar_tema, tema_opuesto
from utils.favicon     import generar_favicon

# ════════════════════════════════════════════════════════════════
#  VENTANA PRINCIPAL
# ════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EventPro")
        self.geometry("980x680")
        self.minsize(900, 600)

        # Favicon
        try:
            ico = generar_favicon("assets/favicon.png")
            self.iconphoto(True, ImageTk.PhotoImage(Image.open(ico)))
        except Exception:
            pass

        self._construir_ui()

    def _construir_ui(self):
        t = get_tema()
        self.configure(bg=t["bg"])

        # ── Barra superior ────────────────────────────────────
        top = tk.Frame(self, bg=t["header_bg"], height=46)
        top.pack(fill="x")
        tk.Label(top, text="  🏛  EventPro", font=("Trebuchet MS",14,"bold"),
                 bg=t["header_bg"], fg=t["header_fg"]).pack(side="left", padx=10, pady=8)


        # ── Notebook ──────────────────────────────────────────
        self.nb = ttk.Notebook(self)
        self.nb.pack(expand=True, fill="both", padx=6, pady=6)

        self._tabs = {}
        for nombre, texto in [("recintos","🏛 Recintos"),("clientes","👥 Clientes"),
                               ("eventos","🎪 Eventos"),("personal","👷 Personal")]:
            f = ttk.Frame(self.nb)
            self.nb.add(f, text=f"  {texto}  ")
            self._tabs[nombre] = f

        # Construir módulos
        self.mod_recintos  = ModuloRecintos(self._tabs["recintos"])
        self.mod_clientes  = ModuloClientes(self._tabs["clientes"])
        self.mod_eventos   = ModuloEventos(self._tabs["eventos"])
        self.mod_personal  = ModuloPersonal(self._tabs["personal"])

    def _toggle_tema(self):
        cambiar_tema(tema_opuesto())
        messagebox.showinfo("Tema", f"Tema cambiado a '{get_tema()}'. Reinicia la app para aplicar.")


# ════════════════════════════════════════════════════════════════
#  HELPERS COMPARTIDOS
# ════════════════════════════════════════════════════════════════
def add_ph(e, ph):
    e._ph = ph
    e.insert(0, ph)
    e.config(fg=get_tema()["placeholder"])
    def fi(_):
        if e.get() == ph:
            e.delete(0, "end")
            e.config(fg=get_tema()["entry_fg"])
    def fo(_):
        if not e.get():
            e.insert(0, ph)
            e.config(fg=get_tema()["placeholder"])
    e.bind("<FocusIn>",  fi)
    e.bind("<FocusOut>", fo)

def gv(e):
    v = e.get()
    return "" if v == getattr(e, "_ph", None) else v

def sv(e, v):
    e.delete(0, "end")
    if v:
        e.insert(0, str(v))
        e.config(fg=get_tema()["entry_fg"])
    else:
        e.insert(0, getattr(e, "_ph", ""))
        e.config(fg=get_tema()["placeholder"])

def cv(e): sv(e, "")

def mke(parent, ph, row, col=1, w=28):
    t = get_tema()
    e = tk.Entry(parent, width=w, font=("Arial",11),
                 relief="solid", bd=1, bg=t["entry_bg"])
    e.grid(row=row, column=col, sticky="w", pady=6, padx=(0,8))
    add_ph(e, ph)
    return e

def mkl(parent, txt, row, col=0):
    t = get_tema()
    tk.Label(parent, text=txt, font=("Arial",11),
             bg=t["bg"], fg=t["fg"]).grid(row=row, column=col, sticky="w", padx=(0,8), pady=6)

def mkc(parent, vals, row, col=1, w=26):
    cb = ttk.Combobox(parent, values=vals, width=w, font=("Arial",11), state="readonly")
    cb.set(vals[0])
    cb.grid(row=row, column=col, sticky="w", pady=6)
    return cb

def mksearch(parent, color, fn):
    t   = get_tema()
    sf  = tk.Frame(parent, bg=t["search_bg"], relief="groove", bd=1)
    sf.pack(fill="x", padx=40, pady=(6,0))
    tk.Label(sf, text="🔍 Buscar:", font=("Arial",10,"bold"),
             bg=t["search_bg"], fg=color).pack(side="left", padx=(10,4), pady=5)
    se = tk.Entry(sf, width=24, font=("Arial",10), relief="solid", bd=1, bg=t["entry_bg"])
    se.pack(side="left", padx=4, pady=5)
    add_ph(se, "Código o nombre...")
    tk.Button(sf, text="Buscar", font=("Arial",10,"bold"),
              bg=color, fg="white", relief="flat", padx=8, cursor="hand2",
              command=lambda: fn(gv(se))).pack(side="left", padx=6, pady=5)
    tk.Button(sf, text="Limpiar", font=("Arial",10),
              bg="#9E9E9E", fg="white", relief="flat", padx=6, cursor="hand2",
              command=lambda: sv(se,"")).pack(side="left", padx=2, pady=5)

def mkbtns(parent, fs, fu, fd, fc, fe_xls=None, fe_pdf=None):
    t  = get_tema()
    bf = tk.Frame(parent, bg=t["bg"])
    bf.pack(pady=10)
    for txt, col, fn in [("💾 Guardar",   t["btn_guardar"],    fs),
                          ("✏ Actualizar", t["btn_actualizar"], fu),
                          ("🗑 Eliminar",  t["btn_eliminar"],   fd),
                          ("🧹 Limpiar",   t["btn_limpiar"],    fc)]:
        tk.Button(bf, text=txt, font=("Arial",10,"bold"),
                  bg=col, fg="white", activebackground=col,
                  relief="flat", width=11, cursor="hand2",
                  command=fn).pack(side="left", padx=4)

    if fe_xls:
        tk.Button(bf, text="📊 Excel", font=("Arial",10,"bold"),
                  bg=t["btn_excel"], fg="white", relief="flat",
                  width=9, cursor="hand2", command=fe_xls).pack(side="left", padx=4)
    if fe_pdf:
        tk.Button(bf, text="📄 PDF", font=("Arial",10,"bold"),
                  bg=t["btn_pdf"], fg="white", relief="flat",
                  width=9, cursor="hand2", command=fe_pdf).pack(side="left", padx=4)

def confirmar(msg): return messagebox.askyesno("Confirmar", msg)
def ok(msg):        messagebox.showinfo("✔", msg)
def err(msg):       messagebox.showerror("Error", msg)
def warn(errs):     messagebox.showwarning("Validación", "\n".join(errs))


# ════════════════════════════════════════════════════════════════
#  MÓDULO RECINTOS
# ════════════════════════════════════════════════════════════════
class ModuloRecintos:
    ENCABEZADOS = ["Código","Nombre","Tipo","Ubicación","Capacidad","Tarifa","Disponibilidad"]

    def __init__(self, tab):
        t = get_tema()
        tab.configure(style="TFrame")
        tk.Label(tab, text="FORMULARIO DE RECINTOS",
                 font=("Trebuchet MS",15,"bold"), fg=t["titulo_fg"],
                 bg=t["bg"]).pack(pady=(12,4))

        mksearch(tab, "#1565C0", self.buscar)

        ff = tk.Frame(tab, bg=t["bg"])
        ff.pack(pady=6, anchor="w", padx=40)

        mkl(ff,"Código Recinto:",0);    self.cod = mke(ff,"Ej: RC-001",0)
        mkl(ff,"Nombre:",1);            self.nom = mke(ff,"Ej: Salón Imperial",1)
        mkl(ff,"Tipo:",2);              self.tip = mkc(ff,["— Seleccionar —","Salón","Auditorio","Sala de reuniones"],2)
        mkl(ff,"Ubicación:",3);         self.ubi = mke(ff,"Ej: Ala Norte, Piso 2",3)
        mkl(ff,"Capacidad (teatro):",4);self.cap = mke(ff,"Ej: 500",4)
        mkl(ff,"Tarifa:",5);            self.tar = mke(ff,"Ej: $350.000/hora",5)
        mkl(ff,"Disponibilidad:",6);    self.dis = mkc(ff,["— Seleccionar —","Disponible","Reservado","En mantenimiento"],6)

        # Imagen del recinto
        mkl(ff, "Imagen del recinto:", 7)
        img_frame = tk.Frame(ff, bg=t["bg"])
        img_frame.grid(row=7, column=1, sticky="w", pady=6)
        self.lbl_img = tk.Label(img_frame, text="Sin imagen", bg=t["entry_bg"],
                                 width=15, height=4, relief="solid", bd=1)
        self.lbl_img.pack(side="left", padx=(0,6))
        tk.Button(img_frame, text="📷 Cargar", font=("Arial",9),
                  bg="#607D8B", fg="white", relief="flat", cursor="hand2",
                  command=self.cargar_imagen).pack(side="left")
        self.img_path = None

        mkbtns(tab, self.guardar, self.actualizar, self.eliminar, self.limpiar,
               self.exportar_excel, self.exportar_pdf)

    # ── Imagen ────────────────────────────────────────────────
    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen del recinto",
            filetypes=[("Imágenes","*.jpg *.jpeg *.png *.gif"),("Todos","*.*")])
        if not ruta: return
        try:
            img = Image.open(ruta)
            # Validar formato
            if img.format not in ("JPEG","PNG","GIF"):
                err("Formato no soportado. Use JPG, PNG o GIF."); return
            # Validar tamaño (max 5MB)
            if os.path.getsize(ruta) > 5 * 1024 * 1024:
                err("Imagen demasiado grande. Máximo 5MB."); return
            img = img.resize((100, 70), Image.LANCZOS)
            self._photo = ImageTk.PhotoImage(img)
            self.lbl_img.config(image=self._photo, text="", width=100, height=70)
            self.img_path = ruta
        except Exception as ex:
            err(f"No se pudo cargar la imagen:\n{ex}")

    # ── CRUD ─────────────────────────────────────────────────
    def _datos(self):
        return {
            "codigo": gv(self.cod), "nombre": gv(self.nom),
            "tipo":   self.tip.get(), "ubicacion": gv(self.ubi),
            "capacidad": gv(self.cap), "tarifa": gv(self.tar),
            "disponibilidad": self.dis.get()
        }

    def buscar(self, t):
        if not t: return
        try:
            rows = call_sp_fetch("sp_buscar_recinto", (t,))
            if rows:
                r = rows[0]
                sv(self.cod,r[0]); sv(self.nom,r[1])
                self.tip.set(r[2] if r[2] in self.tip["values"] else self.tip["values"][0])
                sv(self.ubi,r[3]); sv(self.cap,str(r[4]) if r[4] else ""); sv(self.tar,r[5])
                self.dis.set(r[6] if r[6] in self.dis["values"] else self.dis["values"][0])
            else: messagebox.showinfo("Buscar","No se encontró ningún recinto.")
        except Exception as ex: err(str(ex))

    def guardar(self):
        d = self._datos()
        errs = errores_recinto(d)
        if errs: warn(errs); return
        if not confirmar(f"¿Guardar recinto {d['codigo']}?"): return
        try:
            call_sp("sp_insertar_recinto",(d["codigo"],d["nombre"],d["tipo"],
                    d["ubicacion"],d["capacidad"] or None,d["tarifa"],d["disponibilidad"]))
            ok("Recinto guardado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def actualizar(self):
        d = self._datos()
        if not d["codigo"]: warn(["Ingresa el código del recinto"]); return
        if not confirmar(f"¿Actualizar recinto {d['codigo']}?"): return
        try:
            call_sp("sp_actualizar_recinto",(d["codigo"],d["nombre"],d["tipo"],
                    d["ubicacion"],d["capacidad"] or None,d["tarifa"],d["disponibilidad"]))
            ok("Recinto actualizado ✔")
        except Exception as ex: err(str(ex))

    def eliminar(self):
        cod = gv(self.cod)
        if not cod: warn(["Ingresa el código del recinto"]); return
        if not confirmar(f"¿ELIMINAR recinto {cod}? Esta acción no se puede deshacer."): return
        try:
            call_sp("sp_eliminar_recinto",(cod,))
            ok("Recinto eliminado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def limpiar(self):
        for e in [self.cod,self.nom,self.ubi,self.cap,self.tar]: cv(e)
        self.tip.set(self.tip["values"][0]); self.dis.set(self.dis["values"][0])
        self.lbl_img.config(image="", text="Sin imagen", width=15, height=4)
        self.img_path = None

    def _filas(self):
        return call_sp_fetch("sp_listar_recintos")

    def exportar_excel(self):
        try:
            ruta = exportar_excel("Recintos EventPro", self.ENCABEZADOS, self._filas())
            ok(f"Excel exportado:\n{ruta}")
        except Exception as ex: err(str(ex))

    def exportar_pdf(self):
        try:
            ruta = exportar_pdf("Recintos EventPro", self.ENCABEZADOS, self._filas())
            ok(f"PDF exportado:\n{ruta}")
        except Exception as ex: err(str(ex))


# ════════════════════════════════════════════════════════════════
#  MÓDULO CLIENTES
# ════════════════════════════════════════════════════════════════
class ModuloClientes:
    ENCABEZADOS = ["Código","Tipo","Razón Social","Doc. Fiscal","Teléfono","Correo","Contacto","Clasificación"]

    def __init__(self, tab):
        t = get_tema()
        tk.Label(tab, text="FORMULARIO DE CLIENTES",
                 font=("Trebuchet MS",15,"bold"), fg="#27AE60",
                 bg=t["bg"]).pack(pady=(12,4))

        mksearch(tab, "#27AE60", self.buscar)

        ff = tk.Frame(tab, bg=t["bg"])
        ff.pack(pady=6, anchor="w", padx=40)

        mkl(ff,"Código Cliente:",0);      self.cod  = mke(ff,"Ej: CL-001",0)
        mkl(ff,"Tipo de Cliente:",1);     self.tip  = mkc(ff,["— Seleccionar —","Corporativo","Agencia","Particular"],1)
        mkl(ff,"Razón Social / Nombre:",2);self.raz = mke(ff,"Ej: Tech Summit S.A.",2, w=32)
        mkl(ff,"Documento Fiscal:",3);    self.doc  = mke(ff,"NIT / RUT / Cédula",3)
        mkl(ff,"Teléfono:",4);            self.tel  = mke(ff,"Ej: +57 300 123 4567",4)
        mkl(ff,"Correo Electrónico:",5);  self.mail = mke(ff,"contacto@empresa.com",5)
        mkl(ff,"Persona de Contacto:",6); self.con  = mke(ff,"Nombre completo",6)
        mkl(ff,"Clasificación:",7);       self.cla  = mkc(ff,["— Seleccionar —","Cliente nuevo","Cliente frecuente","Cliente VIP"],7)

        # Foto de contacto
        mkl(ff, "Foto del contacto:", 8)
        img_frame = tk.Frame(ff, bg=t["bg"])
        img_frame.grid(row=8, column=1, sticky="w", pady=6)
        self.lbl_foto = tk.Label(img_frame, text="Sin foto", bg=t["entry_bg"],
                                  width=15, height=4, relief="solid", bd=1)
        self.lbl_foto.pack(side="left", padx=(0,6))
        tk.Button(img_frame, text="📷 Cargar", font=("Arial",9),
                  bg="#607D8B", fg="white", relief="flat", cursor="hand2",
                  command=self.cargar_foto).pack(side="left")
        self.foto_path = None

        mkbtns(tab, self.guardar, self.actualizar, self.eliminar, self.limpiar,
               self.exportar_excel, self.exportar_pdf)

    def cargar_foto(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto del contacto",
            filetypes=[("Imágenes","*.jpg *.jpeg *.png *.gif"),("Todos","*.*")])
        if not ruta: return
        try:
            img = Image.open(ruta)
            if img.format not in ("JPEG","PNG","GIF"):
                err("Formato no soportado. Use JPG, PNG o GIF."); return
            if os.path.getsize(ruta) > 5 * 1024 * 1024:
                err("Imagen demasiado grande. Máximo 5MB."); return
            img = img.resize((80, 80), Image.LANCZOS)
            self._photo = ImageTk.PhotoImage(img)
            self.lbl_foto.config(image=self._photo, text="", width=80, height=80)
            self.foto_path = ruta
        except Exception as ex:
            err(f"No se pudo cargar la foto:\n{ex}")

    def _datos(self):
        return {
            "codigo": gv(self.cod), "tipo": self.tip.get(),
            "razon": gv(self.raz), "doc": gv(self.doc),
            "telefono": gv(self.tel), "correo": gv(self.mail),
            "contacto": gv(self.con), "clasificacion": self.cla.get()
        }

    def buscar(self, t):
        if not t: return
        try:
            rows = call_sp_fetch("sp_buscar_cliente", (t,))
            if rows:
                r = rows[0]
                sv(self.cod,r[0])
                self.tip.set(r[1] if r[1] in self.tip["values"] else self.tip["values"][0])
                sv(self.raz,r[2]); sv(self.doc,r[3]); sv(self.tel,r[4])
                sv(self.mail,r[5]); sv(self.con,r[6])
                self.cla.set(r[7] if r[7] in self.cla["values"] else self.cla["values"][0])
            else: messagebox.showinfo("Buscar","No se encontró ningún cliente.")
        except Exception as ex: err(str(ex))

    def guardar(self):
        d = self._datos()
        errs = errores_cliente(d)
        if errs: warn(errs); return
        if not confirmar(f"¿Guardar cliente {d['codigo']}?"): return
        try:
            call_sp("sp_insertar_cliente",(d["codigo"],d["tipo"],d["razon"],
                    d["doc"],d["telefono"],d["correo"],d["contacto"],d["clasificacion"]))
            ok("Cliente guardado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def actualizar(self):
        d = self._datos()
        if not d["codigo"]: warn(["Ingresa el código del cliente"]); return
        if not confirmar(f"¿Actualizar cliente {d['codigo']}?"): return
        try:
            call_sp("sp_actualizar_cliente",(d["codigo"],d["tipo"],d["razon"],
                    d["doc"],d["telefono"],d["correo"],d["contacto"],d["clasificacion"]))
            ok("Cliente actualizado ✔")
        except Exception as ex: err(str(ex))

    def eliminar(self):
        cod = gv(self.cod)
        if not cod: warn(["Ingresa el código del cliente"]); return
        if not confirmar(f"¿ELIMINAR cliente {cod}?"): return
        try:
            call_sp("sp_eliminar_cliente",(cod,))
            ok("Cliente eliminado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def limpiar(self):
        for e in [self.cod,self.raz,self.doc,self.tel,self.mail,self.con]: cv(e)
        self.tip.set(self.tip["values"][0]); self.cla.set(self.cla["values"][0])
        self.lbl_foto.config(image="", text="Sin foto", width=15, height=4)
        self.foto_path = None

    def _filas(self):
        return call_sp_fetch("sp_listar_clientes")

    def exportar_excel(self):
        try:
            ruta = exportar_excel("Clientes EventPro", self.ENCABEZADOS, self._filas())
            ok(f"Excel exportado:\n{ruta}")
        except Exception as ex: err(str(ex))

    def exportar_pdf(self):
        try:
            ruta = exportar_pdf("Clientes EventPro", self.ENCABEZADOS, self._filas())
            ok(f"PDF exportado:\n{ruta}")
        except Exception as ex: err(str(ex))


# ════════════════════════════════════════════════════════════════
#  MÓDULO EVENTOS
# ════════════════════════════════════════════════════════════════
class ModuloEventos:
    ENCABEZADOS = ["N° Evento","Título","Tipo","Cliente","Fecha Inicio","Fecha Fin","Asistentes","Estado"]

    def __init__(self, tab):
        t = get_tema()
        tk.Label(tab, text="FORMULARIO DE EVENTOS",
                 font=("Trebuchet MS",15,"bold"), fg="#6C3483",
                 bg=t["bg"]).pack(pady=(12,4))

        mksearch(tab, "#6C3483", self.buscar)

        ff = tk.Frame(tab, bg=t["bg"])
        ff.pack(pady=6, anchor="w", padx=40)

        mkl(ff,"N° Evento:",0);         self.num = mke(ff,"Ej: EV-2026-001",0)
        mkl(ff,"Título:",1);            self.tit = mke(ff,"Ej: Cumbre Tecnológica",1, w=32)
        mkl(ff,"Tipo de Evento:",2);    self.tip = mkc(ff,["— Seleccionar —","Congreso","Boda","Feria","Concierto","Conferencia"],2)
        mkl(ff,"Cliente:",3);           self.cli = mke(ff,"Código o nombre del cliente",3)

        # Fechas con tkcalendar
        mkl(ff,"Fecha Inicio:",4)
        self.fi = DateEntry(ff, width=24, font=("Arial",11), date_pattern="yyyy-mm-dd",
                            background="darkblue", foreground="white",
                            borderwidth=1, relief="solid", locale="es_ES")
        self.fi.grid(row=4, column=1, sticky="w", pady=6)

        mkl(ff,"Fecha Fin:",5)
        self.ff_ent = DateEntry(ff, width=24, font=("Arial",11), date_pattern="yyyy-mm-dd",
                                background="darkblue", foreground="white",
                                borderwidth=1, relief="solid", locale="es_ES")
        self.ff_ent.grid(row=5, column=1, sticky="w", pady=6)

        mkl(ff,"N° Asistentes Est.:",6); self.asi = mke(ff,"Ej: 250",6)
        mkl(ff,"Estado Actual:",7);      self.est = mkc(ff,["— Seleccionar —","Cotización","Confirmado","En curso","Finalizado","Cancelado"],7)

        mkbtns(tab, self.guardar, self.actualizar, self.eliminar, self.limpiar,
               self.exportar_excel, self.exportar_pdf)

    def _datos(self):
        return {
            "num": gv(self.num), "titulo": gv(self.tit),
            "tipo": self.tip.get(), "cliente": gv(self.cli),
            "fi": self.fi.get_date().strftime("%Y-%m-%d"),
            "ff": self.ff_ent.get_date().strftime("%Y-%m-%d"),
            "asistentes": gv(self.asi), "estado": self.est.get()
        }

    def buscar(self, t):
        if not t: return
        try:
            rows = call_sp_fetch("sp_buscar_evento", (t,))
            if rows:
                r = rows[0]
                sv(self.num,r[0]); sv(self.tit,r[1])
                self.tip.set(r[2] if r[2] in self.tip["values"] else self.tip["values"][0])
                sv(self.cli,r[3])
                sv(self.asi,str(r[6]) if r[6] else "")
                self.est.set(r[7] if r[7] in self.est["values"] else self.est["values"][0])
            else: messagebox.showinfo("Buscar","No se encontró ningún evento.")
        except Exception as ex: err(str(ex))

    def guardar(self):
        d = self._datos()
        errs = errores_evento(d)
        if errs: warn(errs); return
        if not confirmar(f"¿Guardar evento {d['num']}?"): return
        try:
            call_sp("sp_insertar_evento",(d["num"],d["titulo"],d["tipo"],d["cliente"],
                    d["fi"],d["ff"],d["asistentes"] or None,d["estado"]))
            ok("Evento guardado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def actualizar(self):
        d = self._datos()
        if not d["num"]: warn(["Ingresa el N° de evento"]); return
        if not confirmar(f"¿Actualizar evento {d['num']}?"): return
        try:
            call_sp("sp_actualizar_evento",(d["num"],d["titulo"],d["tipo"],d["cliente"],
                    d["fi"],d["ff"],d["asistentes"] or None,d["estado"]))
            ok("Evento actualizado ✔")
        except Exception as ex: err(str(ex))

    def eliminar(self):
        num = gv(self.num)
        if not num: warn(["Ingresa el N° de evento"]); return
        if not confirmar(f"¿ELIMINAR evento {num}?"): return
        try:
            call_sp("sp_eliminar_evento",(num,))
            ok("Evento eliminado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def limpiar(self):
        for e in [self.num,self.tit,self.cli,self.asi]: cv(e)
        self.tip.set(self.tip["values"][0]); self.est.set(self.est["values"][0])

    def _filas(self):
        return call_sp_fetch("sp_listar_eventos")

    def exportar_excel(self):
        try:
            ruta = exportar_excel("Eventos EventPro", self.ENCABEZADOS, self._filas())
            ok(f"Excel exportado:\n{ruta}")
        except Exception as ex: err(str(ex))

    def exportar_pdf(self):
        try:
            ruta = exportar_pdf("Eventos EventPro", self.ENCABEZADOS, self._filas())
            ok(f"PDF exportado:\n{ruta}")
        except Exception as ex: err(str(ex))


# ════════════════════════════════════════════════════════════════
#  MÓDULO PERSONAL
# ════════════════════════════════════════════════════════════════
class ModuloPersonal:
    ENCABEZADOS = ["Código","Nombres","Apellidos","Especialidad","Tarifa","Evento","Horario","Disponibilidad"]

    def __init__(self, tab):
        t = get_tema()
        tk.Label(tab, text="FORMULARIO DE PERSONAL",
                 font=("Trebuchet MS",15,"bold"), fg="#C0392B",
                 bg=t["bg"]).pack(pady=(12,4))

        mksearch(tab, "#C0392B", self.buscar)

        ff = tk.Frame(tab, bg=t["bg"])
        ff.pack(pady=6, anchor="w", padx=40)

        mkl(ff,"Código Empleado:",0);   self.cod = mke(ff,"Ej: EP-001",0)
        mkl(ff,"Nombres:",1);           self.nom = mke(ff,"Nombres del empleado",1)
        mkl(ff,"Apellidos:",2);         self.ape = mke(ff,"Apellidos del empleado",2)
        mkl(ff,"Especialidad:",3);      self.esp = mkc(ff,["— Seleccionar —","Coordinador","Técnico audiovisual","Camarero","Seguridad","Decorador","Chef"],3)
        mkl(ff,"Tarifa ($/hora):",4);   self.tar = mke(ff,"Ej: 45000",4)
        mkl(ff,"Evento Asignado:",5);   self.evt = mke(ff,"N° o nombre del evento",5)
        mkl(ff,"Horario Asignado:",6);  self.hor = mke(ff,"Ej: 08:00 – 18:00",6)
        mkl(ff,"Disponibilidad:",7);    self.dis = mkc(ff,["— Seleccionar —","Disponible","Asignado","De vacaciones","Baja médica"],7)

        mkbtns(tab, self.guardar, self.actualizar, self.eliminar, self.limpiar,
               self.exportar_excel, self.exportar_pdf)

    def _datos(self):
        return {
            "codigo": gv(self.cod), "nombres": gv(self.nom),
            "apellidos": gv(self.ape), "especialidad": self.esp.get(),
            "tarifa": gv(self.tar), "evento": gv(self.evt),
            "horario": gv(self.hor), "disponibilidad": self.dis.get()
        }

    def buscar(self, t):
        if not t: return
        try:
            rows = call_sp_fetch("sp_buscar_personal", (t,))
            if rows:
                r = rows[0]
                sv(self.cod,r[0]); sv(self.nom,r[1]); sv(self.ape,r[2])
                self.esp.set(r[3] if r[3] in self.esp["values"] else self.esp["values"][0])
                sv(self.tar,r[4]); sv(self.evt,r[5]); sv(self.hor,r[6])
                self.dis.set(r[7] if r[7] in self.dis["values"] else self.dis["values"][0])
            else: messagebox.showinfo("Buscar","No se encontró ningún empleado.")
        except Exception as ex: err(str(ex))

    def guardar(self):
        d = self._datos()
        errs = errores_personal(d)
        if errs: warn(errs); return
        if not confirmar(f"¿Guardar empleado {d['codigo']}?"): return
        try:
            call_sp("sp_insertar_personal",(d["codigo"],d["nombres"],d["apellidos"],
                    d["especialidad"],d["tarifa"],d["evento"],d["horario"],d["disponibilidad"]))
            ok("Empleado guardado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def actualizar(self):
        d = self._datos()
        if not d["codigo"]: warn(["Ingresa el código del empleado"]); return
        if not confirmar(f"¿Actualizar empleado {d['codigo']}?"): return
        try:
            call_sp("sp_actualizar_personal",(d["codigo"],d["nombres"],d["apellidos"],
                    d["especialidad"],d["tarifa"],d["evento"],d["horario"],d["disponibilidad"]))
            ok("Empleado actualizado ✔")
        except Exception as ex: err(str(ex))

    def eliminar(self):
        cod = gv(self.cod)
        if not cod: warn(["Ingresa el código del empleado"]); return
        if not confirmar(f"¿ELIMINAR empleado {cod}?"): return
        try:
            call_sp("sp_eliminar_personal",(cod,))
            ok("Empleado eliminado ✔"); self.limpiar()
        except Exception as ex: err(str(ex))

    def limpiar(self):
        for e in [self.cod,self.nom,self.ape,self.tar,self.evt,self.hor]: cv(e)
        self.esp.set(self.esp["values"][0]); self.dis.set(self.dis["values"][0])

    def _filas(self):
        return call_sp_fetch("sp_listar_personal")

    def exportar_excel(self):
        try:
            ruta = exportar_excel("Personal EventPro", self.ENCABEZADOS, self._filas())
            ok(f"Excel exportado:\n{ruta}")
        except Exception as ex: err(str(ex))

    def exportar_pdf(self):
        try:
            ruta = exportar_pdf("Personal EventPro", self.ENCABEZADOS, self._filas())
            ok(f"PDF exportado:\n{ruta}")
        except Exception as ex: err(str(ex))


# ════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        get_conn()
    except Exception as e:
        import tkinter as _tk
        r = _tk.Tk(); r.withdraw()
        messagebox.showerror("Error de conexión",
            f"No se pudo conectar a MySQL:\n\n{e}\n\n"
            "Verifica que el contenedor Docker esté corriendo:\n"
            "docker-compose up")
        r.destroy()
    app = App()
    app.mainloop()
