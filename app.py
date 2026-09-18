import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

# Configuración de página para que ocupe toda la pantalla (tipo Dashboard)
st.set_page_config(page_title="Presupuesto Rápido", layout="wide", initial_sidebar_state="expanded")

# --- CSS PERSONALIZADO PARA MODO OSCURO Y ESTILOS ---
st.markdown("""
    <style>
    /* Ocultar elementos predeterminados de Streamlit para aspecto de Web App */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Estilo para las tarjetas de resumen */
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- MENÚ LATERAL (Replicando la imagen) ---
with st.sidebar:
    st.markdown("### 🎯 Mi Presupuesto")
    seleccion = option_menu(
        menu_title=None,
        options=["Vista General", "Transacciones", "Cuentas", "Deudas", "Objetivos", "Gráficos"],
        icons=["grid", "list-check", "bank", "credit-card", "bullseye", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#4fc3f7", "font-size": "18px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#333"},
            "nav-link-selected": {"background-color": "#1976d2"},
        }
    )

# ==========================================
# VISTA GENERAL (DASHBOARD principal)
# ==========================================
if seleccion == "Vista General":
    
    # Fila 1: Resumen y Gráficos de Anillo
    col_resumen, col_mes_actual, col_mes_pasado = st.columns([1.5, 1, 1])
    
    with col_resumen:
        st.markdown("#### Resumen")
        # Datos simulados basados en tu contexto para mostrar la UI
        st.metric("Balance Total (Liquidez)", "$1.071.000 COP")
        st.metric("Deudas Pendientes", "-$2.964.602 COP", delta_color="inverse")
        st.metric("Salario Domo (Proyectado)", "$2.740.238 COP")

    with col_mes_actual:
        st.markdown("<p style='text-align: center;'>Este mes</p>", unsafe_allow_html=True)
        # Gráfico de anillo tipo Fast Budget
        fig_actual = go.Figure(data=[go.Pie(labels=['Ingresos', 'Gastos'], values=[2740238, 1669238], hole=.7, 
                                            marker_colors=['#43a047', '#e53935'])])
        fig_actual.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), 
                                 paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150)
        st.plotly_chart(fig_actual, use_container_width=True)
        
    with col_mes_pasado:
        st.markdown("<p style='text-align: center;'>Mes pasado</p>", unsafe_allow_html=True)
        fig_pasado = go.Figure(data=[go.Pie(labels=['Ingresos', 'Gastos'], values=[2740238, 2000000], hole=.7, 
                                            marker_colors=['#43a047', '#e53935'])])
        fig_pasado.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), 
                                 paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150)
        st.plotly_chart(fig_pasado, use_container_width=True)

    st.markdown("---")
    
    # Fila 2: Cuentas y Gráfico de Líneas de Balance
    col_cuentas, col_grafico_balance = st.columns([1, 2])
    
    with col_cuentas:
        st.markdown("#### Cuentas")
        st.markdown("**Efectivo / Cartera** <br> <span style='color:#e53935'>-$354.600 COP</span>", unsafe_allow_html=True)
        st.markdown("**Cuenta Bancaria** <br> <span style='color:#43a047'>$1.425.600 COP</span>", unsafe_allow_html=True)
        st.markdown("<br>#### Próximos Pagos", unsafe_allow_html=True)
        st.markdown("🔴 **Cuota Papá:** $82.750")
        st.markdown("🔴 **UdeA (Quincena):** $25.000")

    with col_grafico_balance:
        st.markdown("#### Evolución del Balance")
        # Generar datos dummy de los últimos días simulando acumulación de liquidez
        fechas = [datetime.today() - timedelta(days=x) for x in range(10, 0, -1)]
        balances = [500000, 480000, 450000, 1800000, 1750000, 1700000, 1680000, 1500000, 1200000, 1071000]
        
        fig_linea = px.area(x=fechas, y=balances, color_discrete_sequence=['#1976d2'])
        fig_linea.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', 
                                plot_bgcolor='rgba(0,0,0,0)', xaxis_title="", yaxis_title="COP $", height=250)
        fig_linea.update_xaxes(showgrid=False)
        fig_linea.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#333')
        st.plotly_chart(fig_linea, use_container_width=True)

    st.markdown("---")
    
    # Fila 3: Barras de últimos 7 días y Presupuestos (Progreso)
    col_barras, col_presupuestos = st.columns([2, 1])
    
    with col_barras:
        st.markdown("#### Últimos 7 días")
        dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        ingresos_d = [0, 0, 0, 1370119, 0, 0, 0] # Simulando pago quincenal
        gastos_d = [18860, 18860, 50000, 18860, 600000, 0, 0] # Pasajes diarios (4715x4) y mercado
        
        fig_barras = go.Figure()
        fig_barras.add_trace(go.Bar(x=dias, y=gastos_d, name='Gastos', marker_color='#e53935'))
        fig_barras.add_trace(go.Bar(x=dias, y=ingresos_d, name='Ingresos', marker_color='#43a047'))
        fig_barras.update_layout(barmode='group', margin=dict(t=10, b=10, l=10, r=10), 
                                 paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250,
                                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_barras, use_container_width=True)

    with col_presupuestos:
        st.markdown("#### Presupuestos")
        
        st.markdown("<small>Mercado mensual (Ejecutado: 60%)</small>", unsafe_allow_html=True)
        st.progress(0.60)
        st.markdown("<div style='text-align: right; font-size: 12px'>360.000 / 600.000 COP</div>", unsafe_allow_html=True)
        
        st.markdown("<small>Pasajes (Ejecutado: 25%)</small>", unsafe_allow_html=True)
        st.progress(0.25)
        st.markdown("<div style='text-align: right; font-size: 12px'>62.500 / 250.000 COP</div>", unsafe_allow_html=True)
        
        st.markdown("<small>UdeA (Ejecutado: 100%)</small>", unsafe_allow_html=True)
        st.progress(1.0)
        st.markdown("<div style='text-align: right; font-size: 12px'>50.000 / 50.000 COP</div>", unsafe_allow_html=True)

# ==========================================
# PESTAÑA: TRANSACCIONES (Para el registro diario)
# ==========================================
elif seleccion == "Transacciones":
    st.header("📝 Registro de Gastos")
    # Aquí puedes mover el formulario st.form que tenías en la versión anterior para guardar en Google Sheets.
    st.info("Aquí integraremos la conexión a Google Sheets para que los gastos alimenten los gráficos de la Vista General.")
