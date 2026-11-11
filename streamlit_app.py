import streamlit as st
import time
import database as db

st.set_page_config(
    page_title="SBAR Digital Pro", 
    page_icon="🏥", 
    layout="centered"
)

if "autenticado" not in st.session_state: st.session_state.autenticado = False
if "usuario_id" not in st.session_state: st.session_state.usuario_id = ""
if "turno" not in st.session_state: st.session_state.turno = ""
if "mostrar_registro" not in st.session_state: st.session_state.mostrar_registro = False

def evaluar_signo(nombre, valor):
    if nombre == "FC":
        if 51 <= valor <= 90: return "🟢 Normal", "#d4edda", "#155724"
        elif 41 <= valor <= 50 or 91 <= valor <= 110: return "🟡 Alerta Moderada", "#fff3cd", "#856404"
        else: return "🔴 Alerta Crítica", "#f8d7da", "#721c24"
    elif nombre == "SO2":
        if valor >= 96: return "🟢 Normal", "#d4edda", "#155724"
        elif 94 <= valor <= 95: return "🟡 Alerta Moderada", "#fff3cd", "#856404"
        else: return "🔴 Alerta Crítica", "#f8d7da", "#721c24"
    return "🟢 Normal", "#d4edda", "#155724"

def render_badge(titulo, estado, bg, texto_color):
    st.markdown(f"""
        <div style="background-color:{bg}; padding:8px; border-radius:6px; border-left:4px solid {texto_color}; margin-bottom:5px;">
            <span style="color:{texto_color}; font-weight:bold;">{titulo}:</span> <span style="color:{texto_color};">{estado}</span>
        </div>
    """, unsafe_allow_html=True)

col_l1, col_l2 = st.columns(2)
with col_l1: st.markdown("<h4 style='text-align: center; color: #003366;'>🏥 Clínica del Country</h4>", unsafe_allow_html=True)
with col_l2: st.markdown("<h4 style='text-align: center; color: #003366;'>🏥 Clínica La Colina</h4>", unsafe_allow_html=True)
st.markdown("<hr style='margin:10px 0px; border: 1px solid #e6e6e6;'/>", unsafe_allow_html=True)

if not st.session_state.autenticado:
    st.markdown("<h2 style='text-align: center; font-weight: bold; color: #111111;'>FORMATO DE RECIBO Y ENTREGA DE TURNO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555555; font-size: 15px;'>Gestión Clínica Asistencial Digital Sin Papel</p>", unsafe_allow_html=True)
    
    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    
    with col_centro:
        if not st.session_state.mostrar_registro:
            st.markdown("<h4 style='text-align: center; color: #333333;'>🔐 Ingreso al Sistema</h4>", unsafe_allow_html=True)
            u_input = st.text_input("Identificación Institucional", placeholder="Ej: 123456")
            p_input = st.text_input("Contraseña", type="password", placeholder="******")
            t_sel = st.selectbox("Turno a Laborar", ["Mañana (07:00 - 13:00)", "Tarde (13:00 - 19:00)", "Noche (19:00 - 07:00)"])
            
            if st.button("INGRESAR A LA APLICACIÓN ➡️", use_container_width=True):
                if u_input.strip() and p_input.strip():
                    st.session_state.autenticado = True
                    st.session_state.usuario_id = u_input
                    st.session_state.turno = t_sel
                    st.rerun()
                else:
                    st.error("⚠️ Ingresa usuario y contraseña.")
            
            if st.button("¿No tienes usuario? Regístrate aquí 👤", use_container_width=True):
                st.session_state.mostrar_registro = True
                st.rerun()
        else:
            st.markdown("<h4 style='text-align: center; color: #003366;'>📝 Registro de Nuevo Personal</h4>", unsafe_allow_html=True)
            nuevo_id = st.text_input("Número de Identificación (Será tu usuario)", placeholder="Digita tu cédula")
            nueva_pass = st.text_input("Crea tu Contraseña (Mínimo 6 caracteres)", type="password", placeholder="******")
            
            if st.button("Confirmar y Guardar 💾", use_container_width=True):
                if len(nueva_pass) >= 6 and nuevo_id.strip():
                    db.registrar_usuario(nuevo_id.strip(), nueva_pass.strip())
                    st.success("¡Usuario registrado con éxito!")
                    time.sleep(1)
                    st.session_state.mostrar_registro = False
                    st.rerun()
                else:
                    st.error("⚠️ La contraseña debe tener mínimo 6 caracteres.")
                    
            if st.button("🔙 Volver al Inicio de Sesión", use_container_width=True):
                st.session_state.mostrar_registro = False
                st.rerun()

else:
    st.markdown(f"📊 **Sesión:** {st.session_state.usuario_id} | ⏱️ **Turno:** {st.session_state.turno}")
    if st.button("❌ Cerrar Sesión (Salir)"):
        st.session_state.autenticado = False
        st.rerun()
        
    st.markdown("### 🔍 Búsqueda del Paciente")
    criterio = st.text_input("Digita la Identificación o N° de Atención del Paciente:", placeholder="Ej: 10234567").strip()
    
    if criterio:
        paciente = db.buscar_paciente(criterio)
        
        if paciente:
            st.markdown(f"""
                <div style="background-color: #e8f4fd; padding: 12px; border-radius: 8px; border-left: 5px solid #0066cc; margin-bottom: 12px;">
                    <h4 style="margin: 0; color: #003366;">📌 Paciente: <b>{paciente['nombre_paciente']}</b></h4>
                    <p style="margin: 4px 0 0 0; color: #555555;"><b>Ubicación:</b> {paciente['cama']} | <b>Atención:</b> {paciente['num_atencion']} | <b>Edad:</b> {paciente['edad']} años</p>
                </div>
            """, unsafe_allow_html=True)
            
            tab_s, tab_b, tab_a, tab_r = st.tabs(["📋 S - SITUACIÓN", "🧬 B - ANTECEDENTES", "🩺 A - EVALUACIÓN", "📝 R - RECOMENDACIONES"])
            
            with tab_s:
                st.markdown("#### 📌 Datos de la Situación")
                st.text_input("Cama Asignada", value=paciente['cama'], disabled=True)
                st.text_input("Número de Atención", value=paciente['num_atencion'], disabled=True)
                st.text_input("Edad del Paciente", value=f"{paciente['edad']} Años", disabled=True)
                diagnostico_input = st.text_area("💬 Diagnóstico Médico (Comentarios de la Entrega de Turno)", value=paciente['diagnostico'])

            with tab_b:
                st.markdown("#### 🧬 Historial y Dispositivos Clínicos")
                alergia_sel = st.radio("¿Registra Alergias?", ["No", "Sí"], index=1 if paciente['alergia_si_no'] == "Sí" else 0, horizontal=True)
                alergia_det = st.text_input("Especificar Alergia:", value=paciente['alergia_detalle']) if alergia_sel == "Sí" else ""
                
                aisla_index = ["Ninguno", "Protector", "Respiratorio", "Contacto", "Aerosol"].index(paciente['aislamiento']) if paciente['aislamiento'] in ["Ninguno", "Protector", "Respiratorio", "Contacto", "Aerosol"] else 0
                aislamiento_sel = st.selectbox("Seleccione Tipo de Aislamiento:", ["Ninguno", "Protector", "Respiratorio", "Contacto", "Aerosol"], index=aisla_index)
                
                st.markdown("##### 🩹 Conteo Físico de Accesos Vasculares")
                c1, c2 = st.columns(2)
                with c1:
                    c_peri = st.number_input("Acceso Periférico (Cantidad)", min_value=0, value=paciente['cant_periferico'])
                    c_picc = st.number_input("Catéter Periférico PICC", min_value=0, value=paciente['cant_picc'])
                    c_media = st.number_input("Catéter Línea Media", min_value=0, value=paciente['cant_linea_media'])
                with c2:
                    c_cvc = st.number_input("Catéter Venoso Central (CVC)", min_value=0, value=paciente['cant_cvc'])
                    c_art = st.number_input("Catéter Línea Arterial", min_value=0, value=paciente['cant_linea_arterial'])
                    c_alto = st.number_input("Catéter Alto Flujo", min_value=0, value=paciente['cant_alto_flujo'])
                    
                medico_input = st.text_input("👨‍⚕️ Médico Tratante Asignado", value=paciente['medico_tratante'])

            with tab_a:
                st.markdown("#### 🩺 Evaluación y Monitoreo")
                col_in1, col_in2 = st.columns(2)
                with col_in1:
                    ta_s = st.number_input("Tensión Arterial Sistólica (mmHg)", value=120)
                    ta_d = st.number_input("Tensión Arterial Diastólica (mmHg)", value=80)
                    fc = st.number_input("Frecuencia Cardíaca (FC)", value=80)
                with col_in2:
                    fr = st.number_input("Frecuencia Respiratoria (FR)", value=16)
                    temp = st.number_input("Temperatura Corporal (°C)", value=36.5, format="%.1f")
                    so2 = st.number_input("Saturación de Oxígeno (SO2 %)", value=98)
                    
                dolor_sel = st.slider("Escala del Dolor", 0, 10, value=0)
                
                st.markdown("##### 🚨 Semáforo de Alertas Clínicas (NEWS2)")
                est_fc, bg_fc, tx_fc = evaluar_signo("FC", fc)
                est_so2, bg_so2, tx_so2 = evaluar_signo("SO2", so2)
                render_badge("Frecuencia Cardíaca", est_fc, bg_fc, tx_fc)
                render_badge("Saturación de Oxígeno", est_so2, bg_so2, tx_so2)

                st.markdown("##### 🫁 Soporte Oxigenoterapia")
                oxigeno_sel = st.radio("¿Tiene soporte de Oxígeno?", ["No", "Sí"], horizontal=True)
                oxigeno_det = st.text_input("Dispositivo y Flujo:") if oxigeno_sel == "Sí" else ""

                st.markdown("##### ⚠️ Escalas Clínicas de Riesgo")
                braden_sel = st.selectbox("Escala de Riesgo de Piel (Braden)", ["Riesgo Bajo", "Riesgo Medio", "Riesgo Alto"])
                morse_sel = st.selectbox("Escala de Riesgo de Caídas (Morse)", ["Riesgo Bajo", "Riesgo Medio", "Riesgo Alto"])
                
                heridas_input = st.text_area("🩹 Heridas, Drenes, Piel u Otros:")
                via_oral_input = st.text_area("🍽️ Estado de la Vía Oral:")
                
                               st.markdown("##### 💧 Eliminación")
                tipo_orina = st.radio("Eliminación Urinaria:", ["Espontáneo", "Sonda Vesical"], horizontal=True)
                gasto_urinario = st.text_input("Gasto Urinario:", placeholder="Ej: 450 cc en el turno / 0.8 cc/kg/h")
                deposicion_sel = st.radio("Deposición:", ["Sí", "No"], horizontal=True)

            with tab_r:
                st.markdown("#### 📋 Recomendaciones de Entrega de Turno")
                recomendaciones_turno = st.text_area("💬 Recomendaciones y Novedades del Turno:", placeholder="Escribe aquí las recomendaciones que se comentan durante la entrega de turno...", height=120)
                plan_input = st.text_area("📝 Plan de Cuidados de Enfermería y Pendientes:", placeholder="Laboratorios, imágenes diagnósticas, valoraciones o procedimientos pendientes...")
                alerta_input = st.text_input("🚨 Escala de Alerta Temprana (Observaciones NEWS2):", placeholder="Puntaje u observaciones de seguimiento...")
                recibe_input = st.text_input("👤 Identificación del Auxiliar o Jefe que Recibe:")
                
                if st.button("💾 FINALIZAR Y GUARDAR ENTREGA DE TURNO", use_container_width=True):
                    st.success("¡Entrega de turno guardada con éxito en la nube!")
        else:
            st.error("❌ Paciente no registrado. Prueba con 10234567.")

