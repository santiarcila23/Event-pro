"""
models/database.py
Capa de datos — conexión MySQL y llamadas a Stored Procedures
"""
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host":     "localhost",          # nombre del servicio en Docker Compose
    "user":     "root",
    "password": "",
    "database": "eventpro",
    "port":     3306,
}

def get_conn():
    return mysql.connector.connect(**DB_CONFIG)

def call_sp(sp_name, params=()):
    """Ejecuta un SP sin retorno de filas (INSERT, UPDATE, DELETE)"""
    conn = get_conn()
    cur  = conn.cursor()
    cur.callproc(sp_name, params)
    conn.commit()
    cur.close()
    conn.close()

def call_sp_fetch(sp_name, params=()):
    """Ejecuta un SP que retorna filas (SELECT)"""
    conn = get_conn()
    cur  = conn.cursor()
    cur.callproc(sp_name, params)
    rows = []
    for result in cur.stored_results():
        rows = result.fetchall()
    cur.close()
    conn.close()
    return rows
