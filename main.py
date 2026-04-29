import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Configuración de la página para móvil
st.set_page_config(page_title="Despacho Salvador Glez", layout="centered")

def conectar_db():
    conn = sqlite3.connect('despacho_juridico.db', check_same_thread=False)
    return conn

# Inicialización de tablas
conn = conectar_db()
conn.execute('CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY, nombre TEXT, rfc TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS expedientes (id INTEGER PRIMARY KEY, num TEXT, cliente_id INTEGER)')

# --- INTERFAZ MÓVIL ---
st.title("⚖️ Gestión Jurídica")
st.sidebar.header(f"Abogado: Salvador Gonzalez\nCédula: [Tu Cédula]")

menu = ["Buscador", "Nuevo Cliente", "Registrar Expediente"]
choice = st.sidebar.selectbox("Menú", menu)

if choice == "Buscador":
    st.subheader("🔍 Buscar Cliente o Caso")
    busqueda = st.text_input("Nombre o RFC")
    if busqueda:
        df = pd.read_sql_query(f"SELECT * FROM clientes WHERE nombre LIKE '%{busqueda}%'", conn)
        st.dataframe(df, use_container_width=True)

elif choice == "Nuevo Cliente":
    st.subheader("➕ Registro de Cliente")
    nombre = st.text_input("Nombre Completo")
    rfc = st.text_input("RFC")
    if st.button("Guardar"):
        conn.execute("INSERT INTO clientes (nombre, rfc) VALUES (?,?)", (nombre, rfc))
        conn.commit()
        st.success("Cliente guardado")
