import streamlit as st
import sqlite3
import pandas as pd

# Función para conectarse a la DB
def get_connection():
    return sqlite3.connect('fiesta.db')

# ----------------------
# TÍTULO
# ----------------------
st.title("Lista de invitados - Fiesta de aniversario")

# ----------------------
# FORMULARIO PARA AGREGAR INVITADOS
# ----------------------
st.subheader("Agregar nuevo invitado")
with st.form("agregar_invitado"):
    nombre = st.text_input("Nombre")
    apellidos = st.text_input("Apellidos")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo electrónico")
    asistira = st.selectbox("Asistirá", ["No ha confirmado", "Si", "No"])
    num_acompanantes = st.number_input("Número de acompañantes", min_value=0, step=1)
    submitted = st.form_submit_button("Agregar invitado")
    
    if submitted:
        conn = get_connection()
        c = conn.cursor()
        c.execute('''
            INSERT INTO invitados (nombre, apellidos, telefono, correo, asistira, num_acompanantes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, apellidos, telefono, correo, asistira, num_acompanantes))
        conn.commit()
        conn.close()
        st.success(f"Invitado {nombre} {apellidos} agregado correctamente")

# ----------------------
# MOSTRAR INVITADOS
# ----------------------
st.subheader("Lista de invitados")
conn = get_connection()
df = pd.read_sql("SELECT * FROM invitados", conn)
conn.close()

st.dataframe(df)

# ----------------------
# EDITAR Y ELIMINAR INVITADOS
# ----------------------
st.subheader("Editar o eliminar invitado")

if not df.empty:
    selected_id = st.selectbox("Selecciona el invitado", df['id'])
    invitado = df[df['id'] == selected_id].iloc[0]

    with st.form("editar_invitado"):
        nombre = st.text_input("Nombre", invitado['nombre'])
        apellidos = st.text_input("Apellidos", invitado['apellidos'])
        telefono = st.text_input("Teléfono", invitado['telefono'])
        correo = st.text_input("Correo electrónico", invitado['correo'])
        asistira = st.selectbox("Asistirá", ["No ha confirmado", "Si", "No"], index=["No ha confirmado", "Si", "No"].index(invitado['asistira']))
        num_acompanantes = st.number_input("Número de acompañantes", min_value=0, value=invitado['num_acompanantes'], step=1)
        submitted_edit = st.form_submit_button("Actualizar invitado")
        submitted_delete = st.form_submit_button("Eliminar invitado")
        
        if submitted_edit:
            conn = get_connection()
            c = conn.cursor()
            c.execute('''
                UPDATE invitados
                SET nombre=?, apellidos=?, telefono=?, correo=?, asistira=?, num_acompanantes=?
                WHERE id=?
            ''', (nombre, apellidos, telefono, correo, asistira, num_acompanantes, selected_id))
            conn.commit()
            conn.close()
            st.success("Invitado actualizado correctamente")
            st.experimental_rerun()

        if submitted_delete:
            conn = get_connection()
            c = conn.cursor()
            c.execute('DELETE FROM invitados WHERE id=?', (selected_id,))
            conn.commit()
            conn.close()
            st.success("Invitado eliminado correctamente")
            st.experimental_rerun()
