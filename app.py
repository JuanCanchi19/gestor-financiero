from streamlit_gsheets import GSheetsConnection
from datetime import datetime

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor Financiero Personal", layout="wide")

st.title("📊 Gestor Financiero Personal")
st.markdown("Control de liquidez y pago de deudas pre-noviembre")

st.sidebar.header("1. Ingresos Mensuales")
salario = st.sidebar.number_input("Salario Mensual (Domo)", value=2740238, step=10000)

def calcular_cuota(principal, tasa_mensual, meses):
    if tasa_mensual == 0: return principal / meses
    return principal * (tasa_mensual * (1 + tasa_mensual)**meses) / ((1 + tasa_mensual)**meses - 1)

cuota_papa = calcular_cuota(2285510, 0.015, 36)

st.sidebar.header("2. Gastos Fijos")
mercado = st.sidebar.number_input("Mercado", value=600000, step=10000)
pasajes = st.sidebar.number_input("Pasajes", value=250000, step=5000)
udea = st.sidebar.number_input("UdeA", value=50000, step=5000)
yt = st.sidebar.number_input("Youtube Premium", value=20900, step=1000)

st.sidebar.header("3. Variables y Obligaciones")
st.sidebar.info(f"Cuota Papá calculada aut: ${cuota_papa:,.0f}")
lavadora = st.sidebar.number_input("Lavadora Fer", value=354600, step=10000)
jean = st.sidebar.number_input("Deuda Jean", value=127252, step=1000)
regalo = st.sidebar.number_input("Regalo Eli", value=133000, step=5000)
compartir = st.sidebar.number_input("Compartir 25 Sept", value=50000, step=5000)

total_fijos = mercado + pasajes + udea + yt
total_variables = cuota_papa + lavadora + jean + regalo + compartir
gastos_totales_obligatorios = total_fijos + total_variables
remanente = salario - gastos_totales_obligatorios

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos", f"${salario:,.0f}")
col2.metric("Obligaciones", f"${gastos_totales_obligatorios:,.0f}")
col3.metric("Disponible", f"${remanente:,.0f}", delta="Liquidez a asignar")

st.markdown("---")
st.header("⚖️ Distribución del Remanente")

col_a, col_b = st.columns(2)
with col_a:
    abono_fer = st.slider("Abono Viaje Fer ($1.3M)", 0, int(remanente) if remanente > 0 else 0, 50000, step=10000)
    abono_jheferson = st.slider("Abono PC Jheferson ($900k)", 0, int(remanente - abono_fer) if (remanente - abono_fer) > 0 else 0, 50000, step=10000)

colchon = remanente - abono_fer - abono_jheferson

with col_b:
    st.success(f"🛡️ Colchón de Seguridad: **${colchon:,.0f}**")
    st.progress(colchon / remanente if remanente > 0 else 0)

st.markdown("### Resumen de Movimientos")
datos = {
    "Categoría": ["Ingreso", "Fijos", "Obligaciones Variables", "Abono Fer", "Abono Jheferson", "Colchón Emergencia"],
    "Monto": [salario, -total_fijos, -total_variables, -abono_fer, -abono_jheferson, colchon]
}
df = pd.DataFrame(datos)
st.dataframe(df.style.format({"Monto": "${:,.0f}"}), use_container_width=True)

st.markdown("---")
st.header("💾 Guardar Registro Mensual")

if st.button("Guardar en Google Sheets"):
    try:
        # 1. Establecer conexión
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # 2. Leer los datos históricos (Hoja 1 por defecto)
        df_existente = conn.read(worksheet="Hoja 1")
        
        # 3. Empaquetar los datos del mes actual
        nuevo_registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%Y-%m-%d"),
            "Salario": salario,
            "Gastos Fijos": total_fijos,
            "Gastos Variables": total_variables,
            "Abono Fer": abono_fer,
            "Abono Jheferson": abono_jheferson,
            "Colchón": colchon
        }])
        
        # 4. Concatenar y limpiar filas vacías
        df_actualizado = pd.concat([df_existente, nuevo_registro], ignore_index=True).dropna(how="all")
        
        # 5. Sobrescribir la base de datos
        conn.update(worksheet="Hoja 1", data=df_actualizado)
        
        st.success("¡Registro guardado exitosamente en la nube!")
    except Exception as e:
        st.error(f"Ocurrió un error al guardar: {e}")
