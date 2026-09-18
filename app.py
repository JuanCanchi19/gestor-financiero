import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Presupuesto Rápido", layout="wide", initial_sidebar_state="expanded")

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# --- MENÚ LATERAL ---
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
# VISTA GENERAL
# ==========================================
if seleccion == "Vista General":
    col_resumen, col_mes_actual, col_mes_pasado = st.columns([1.5, 1, 1])
    
    with col_resumen:
        st.markdown("#### Resumen")
        st.metric("Balance Total (Liquidez)", "$1.071.000 COP")
        st.metric("Deudas Pendientes", "-$2.964.602 COP", delta_color="inverse")
        st.metric("Salario Domo (Proyectado)", "$2.740.238 COP")

    with col_mes_actual:
        st.markdown("<p style='text-align: center;'>Este mes</p>", unsafe_allow_html=True)
        fig_actual = go.Figure(data=[go.Pie(labels=['Ingresos', 'Gastos'], values=[2740238, 1669238], hole=.7, 
                                            marker_colors=['#43a047', '#e53935'],
                                            textinfo='value', texttemplate='$%{value:,.0f}')])
        fig_actual.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), 
                                 paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150)
        st.plotly_chart(fig_actual, use_container_width=True)
        
    with col_mes_pasado:
        st.markdown("<p style='text-align: center;'>Mes pasado</p>", unsafe_allow_html=True)
        fig_pasado = go.Figure(data=[go.Pie(labels=['Ingresos', 'Gastos'], values=[2740238, 2000000], hole=.7, 
                                            marker_colors=['#43a047', '#e53935'],
                                            textinfo='value', texttemplate='$%{value:,.0f}')])
        fig_pasado.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), 
                                 paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=150)
        st.plotly_chart(fig_pasado, use_container_width=True)

    st.markdown("---")
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
        fechas = [(datetime.today() - timedelta(days=x)).strftime("%d %b") for x in range(10, 0, -1)]
        balances = [500000, 480000, 450000, 1800000, 1750000, 1700000, 1680000, 1500000, 1200000, 1071000]
        
        # Usamos Scatter en lugar de area para poder mostrar los textos encima de los puntos
        fig_linea = go.Figure()
        fig_linea.add_trace(go.Scatter(x=fechas, y=balances, fill='tozeroy', mode='lines+markers+text',
                                       text=[f"${v:,.0f}" for v in balances], textposition="top center",
                                       line=dict(color='#1976d2')))
        fig_linea.update_layout(margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', 
                                plot_bgcolor='rgba(0,0,0,0)', xaxis_title="", yaxis_title="COP $", height=250)
        st.plotly_chart(fig_linea, use_container_width=True)

    st.markdown("---")
    col_barras, col_presupuestos = st.columns([2, 1])
    
    with col_barras:
        st.markdown("#### Últimos 7 días")
        dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        ingresos_d = [0, 0, 0, 1370119, 0, 0, 0] 
        gastos_d = [18860, 18860, 50000, 18860, 600000, 0, 0] 
        
        fig_barras = go.Figure()
        fig_barras.add_trace(go.Bar(x=dias, y=gastos_d, name='Gastos', marker_color='#e53935',
                                    text=[f"${v:,.0f}" if v > 0 else "" for v in gastos_d], textposition='auto'))
        fig_barras.add_trace(go.Bar(x=dias, y=ingresos_d, name='Ingresos', marker_color='#43a047',
                                    text=[f"${v:,.0f}" if v > 0 else "" for v in ingresos_d], textposition='auto'))
        
        fig_barras.update_layout(barmode='group', margin=dict(t=10, b=10, l=10, r=10), 
                                 paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250,
                                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_barras, use_container_width=True)

    with col_presupuestos:
        st.markdown("#### Presupuestos")
        st.markdown("<small>Mercado mensual</small>", unsafe_allow_html=True)
        st.progress(0.60)
        st.markdown("<div style='text-align: right; font-size: 12px'>360.000 / 600.000 COP</div>", unsafe_allow_html=True)
        
        st.markdown("<small>Pasajes</small>", unsafe_allow_html=True)
        st.progress(0.25)
        st.markdown("<div style='text-align: right; font-size: 12px'>62.500 / 250.000 COP</div>", unsafe_allow_html=True)

# ==========================================
# TRANSACCIONES (Agregar info sin salir de la app)
# ==========================================
elif seleccion == "Transacciones":
    st.header("📝 Registro Rápido de Gastos")
    st.write("Agrega tus compras diarias aquí. Se guardarán automáticamente en tu base de datos en la nube.")
    
    with st.form("form_gastos", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            f_fecha = st.date_input("Fecha de transacción", datetime.now())
            f_categoria = st.selectbox("Categoría", ["Mercado", "Transporte", "Universidad", "Deudas", "Otros"])
        with col2:
            f_monto = st.number_input("Valor ($)", min_value=0, step=1000)
            f_concepto = st.text_input("Concepto / Descripción")
            
        submit_btn = st.form_submit_button("Guardar Transacción", use_container_width=True)
        
        if submit_btn:
            try:
                # Conecta en silencio a GSheets para guardar el dato
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_diarios = conn.read(worksheet="Gastos Diarios")
                nuevo_gasto = pd.DataFrame([{
                    "Fecha": f_fecha.strftime("%Y-%m-%d"), 
                    "Concepto": f_concepto, 
                    "Categoría": f_categoria, 
                    "Monto": f_monto
                }])
                df_actual = pd.concat([df_diarios, nuevo_gasto], ignore_index=True).dropna(how="all")
                conn.update(worksheet="Gastos Diarios", data=df_actual)
                st.success(f"✅ ¡Gasto de ${f_monto:,.0f} registrado con éxito!")
            except Exception as e:
                st.error(f"Error al guardar. Verifica tu conexión de GSheets. Detalle: {e}")
