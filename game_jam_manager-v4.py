import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime, date, timedelta

# Configuración de página
st.set_page_config(
    page_title="Game Jam Hub - Gestor e Evaluador",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .role-badge {
        background-color: #E0E7FF;
        color: #3730A3;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .gold-medal { background-color: #FEF3C7; color: #92400E; padding: 6px 12px; border-radius: 8px; font-weight: bold; }
    .silver-medal { background-color: #F3F4F6; color: #374151; padding: 6px 12px; border-radius: 8px; font-weight: bold; }
    .bronze-medal { background-color: #FFEDD5; color: #9A3412; padding: 6px 12px; border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Inicialización de Session State
if 'step' not in st.session_state:
    st.session_state.step = 1

if 'host_data' not in st.session_state:
    st.session_state.host_data = {
        'host_name': 'Daniel López Salas',
        'host_email': 'daniel@48toplay.com',
        'organization': '48toplay / Teco Studios',
        'usual_venue': 'Tec de Monterrey (Innovaction Gym) / U-ERRE',
        'target_sponsors': 'Logitech G, Unity, EA, MIMEC, Red Bull'
    }

if 'event_data' not in st.session_state:
    st.session_state.event_data = {
        'event_name': 'Global Game Jam Regio 2026',
        'event_date': date.today() + timedelta(days=30),
        'modality': 'Presencial',
        'isPartOfFramework': True,
        'framework_name': 'Congreso de Innovación & Videojuegos',
        'giveFrameworkTickets': True,
        'capacity': 150,
        'duration_hours': 48,
        'has_venue': True,
        'bandwidth_ok': True,
        'has_catering': True,
        'has_streaming': True,
        'budget_level': 'Medio ($20k - $80k MXN)',
        'prizes_enabled': True,
        'jury_weight': 85,
        'public_weight': 15
    }

if 'committee_members' not in st.session_state:
    st.session_state.committee_members = [
        {'Name': 'Daniel López', 'Email': 'dani@48toplay.com', 'Role': '👑 Director General / Líder', 'TaskCount': 5},
        {'Name': 'Christian Rodríguez', 'Email': 'chris@48toplay.com', 'Role': '📡 Director de Streaming & TI', 'TaskCount': 4},
        {'Name': 'Pamela Álvarez', 'Email': 'pam@48toplay.com', 'Role': '📣 Director de Marketing & Prensa', 'TaskCount': 4},
        {'Name': 'Luis Mora', 'Email': 'maot@48toplay.com', 'Role': '📍 Director de Logística & Venue', 'TaskCount': 6},
        {'Name': 'Alder Gutiérrez', 'Email': 'alder@outline.mx', 'Role': '🎨 Director de Imagen & Arte', 'TaskCount': 3},
        {'Name': 'Guillermo Limón', 'Email': 'limon@damedecibel.com', 'Role': '📸 Encargado de Fotografía & Entrevistas', 'TaskCount': 2},
        {'Name': 'Elias Villa', 'Email': 'elias@thunderstruck.mx', 'Role': '🎮 Encargado de Torneos & Recreación', 'TaskCount': 2}
    ]

if 'tasks_status' not in st.session_state:
    st.session_state.tasks_status = {}

if 'judges_list' not in st.session_state:
    st.session_state.judges_list = [
        {'Nombre': 'Dr. Jose Guerra', 'Especialidad': 'Game Design & Programación', 'Empresa': 'CEDIM'},
        {'Nombre': 'Erick Vásquez', 'Especialidad': 'Arte & Visuales', 'Empresa': 'Incisor Studios'},
        {'Nombre': 'Roberto Herrera', 'Especialidad': 'Audio & UX', 'Empresa': 'Psicofonía Studio'}
    ]

if 'teams_list' not in st.session_state:
    st.session_state.teams_list = [
        {'Code': 'E001', 'TeamName': 'Team-O', 'GameName': 'Unmasked', 'PresentTime': '17:00'},
        {'Code': 'E002', 'TeamName': 'Uneek Games', 'GameName': 'Mask Forge', 'PresentTime': '17:05'},
        {'Code': 'E003', 'TeamName': 'Ratas Florales', 'GameName': 'Ruta Equivocada', 'PresentTime': '17:10'},
        {'Code': 'E004', 'TeamName': 'AstroLovers', 'GameName': 'Masked Souls', 'PresentTime': '17:15'},
        {'Code': 'E005', 'TeamName': 'Monstruos', 'GameName': 'I am a Monster', 'PresentTime': '17:20'}
    ]

if 'evaluations' not in st.session_state:
    # Datos semilla basados en GGJ2026_Evaluación
    st.session_state.evaluations = {
        'Dr. Jose Guerra': {
            'E001': {'Orig_Concept': 8, 'Orig_Theme': 8, 'GD_Mech': 3, 'GD_Dyn': 3, 'GD_Esth': 5, 'GD_Lvl': 1, 'Int_UX': 5, 'Int_UI': 5, 'Int_Replay': 10, 'Art_Vis': 5, 'Art_Aud': 3, 'Art_Narr': 2, 'Art_Amb': 5, 'Tech_Prog': 8, 'Tech_Ctrl': 8, 'Inn_Tech': 4, 'Inn_Proc': 4, 'Viab_Econ': 2, 'Viab_Emp': 2, 'Viab_IP': 2, 'Div_Points': 0, 'PublicScore': 70},
            'E002': {'Orig_Concept': 8, 'Orig_Theme': 7, 'GD_Mech': 5, 'GD_Dyn': 5, 'GD_Esth': 5, 'GD_Lvl': 4, 'Int_UX': 5, 'Int_UI': 5, 'Int_Replay': 8, 'Art_Vis': 5, 'Art_Aud': 5, 'Art_Narr': 5, 'Art_Amb': 5, 'Tech_Prog': 9, 'Tech_Ctrl': 7, 'Inn_Tech': 4, 'Inn_Proc': 4, 'Viab_Econ': 1, 'Viab_Emp': 1, 'Viab_IP': 1, 'Div_Points': 0, 'PublicScore': 72},
            'E003': {'Orig_Concept': 8, 'Orig_Theme': 8, 'GD_Mech': 4, 'GD_Dyn': 4, 'GD_Esth': 5, 'GD_Lvl': 4, 'Int_UX': 5, 'Int_UI': 5, 'Int_Replay': 8, 'Art_Vis': 5, 'Art_Aud': 5, 'Art_Narr': 5, 'Art_Amb': 5, 'Tech_Prog': 8, 'Tech_Ctrl': 8, 'Inn_Tech': 4, 'Inn_Proc': 4, 'Viab_Econ': 2, 'Viab_Emp': 2, 'Viab_IP': 2, 'Div_Points': 0, 'PublicScore': 70}
        }
    }

# Sidebar
st.sidebar.title("🎮 Game Jam Hub")
st.sidebar.markdown(f"**Anfitrión:** {st.session_state.host_data['host_name']}")
st.sidebar.markdown(f"**Org:** {st.session_state.host_data['organization']}")
if st.session_state.event_data['event_name']:
    st.sidebar.divider()
    st.sidebar.markdown(f"**Evento:** {st.session_state.event_data['event_name']}")
    st.sidebar.markdown(f"**Fecha:** {st.session_state.event_data['event_date']}")
    st.sidebar.markdown(f"**Modalidad:** {st.session_state.event_data['modality']}")

st.sidebar.divider()
step_options = {1: "1. Onboarding & Anfitrión", 2: "2. Diagnóstico & Alcance", 3: "3. Panel de Control & Evaluador"}
selected_step = st.sidebar.radio("Navegación:", list(step_options.values()), index=st.session_state.step - 1)

if selected_step.startswith("1"):
    st.session_state.step = 1
elif selected_step.startswith("2"):
    st.session_state.step = 2
else:
    st.session_state.step = 3


# ==========================================\n# PASO 1: ONBOARDING & ANFITRIÓN
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='main-header'>👤 Registro de Anfitrión y Evento</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Paso 1 de 3: Registra tus datos de organizador para alimentar la base de datos de anfitriones, venues y patrocinadores.</div>", unsafe_allow_html=True)

    with st.form("host_onboarding_form"):
        st.subheader("1. Datos del Anfitrión (Base de Datos Central)")
        col1, col2 = st.columns(2)
        with col1:
            h_name = st.text_input("Nombre completo del Anfitrión *", value=st.session_state.host_data['host_name'])
            h_email = st.text_input("Correo electrónico de contacto *", value=st.session_state.host_data['host_email'])
        with col2:
            h_org = st.text_input("Organización / Estudio / Colectivo", value=st.session_state.host_data['organization'])
            h_venue = st.text_input("Sede / Venue habitual", value=st.session_state.host_data['usual_venue'])
        
        h_sponsors = st.text_input("Patrocinadores habituales u objetivo", value=st.session_state.host_data['target_sponsors'])

        st.subheader("2. Datos del Próximo Game Jam")
        col3, col4 = st.columns(2)
        with col3:
            e_name = st.text_input("Nombre del Game Jam *", value=st.session_state.event_data['event_name'])
            e_date = st.date_input("Fecha tentativa de inicio *", value=st.session_state.event_data['event_date'])
        with col4:
            e_mod = st.selectbox("Modalidad principal", ["Presencial", "Virtual (Discord / Twitch)", "Híbrido"], index=["Presencial", "Virtual (Discord / Twitch)", "Híbrido"].index(st.session_state.event_data['modality']))
            is_framework = st.checkbox("¿El Game Jam está dentro del marco de un evento mayor (Congreso, Convención, Festival)?", value=st.session_state.event_data['isPartOfFramework'])

        framework_name = ""
        give_tickets = False
        if is_framework:
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                framework_name = st.text_input("Nombre del Evento Marco", value=st.session_state.event_data['framework_name'])
            with col_f2:
                give_tickets = st.checkbox("¿Se entregarán pases VIP / All-Access o booths de exhibición como premio?", value=st.session_state.event_data['giveFrameworkTickets'])

        submit_btn = st.form_submit_button("Guardar Anfitrión y Pasar a Diagnóstico ➡️", use_container_width=True)

        if submit_btn:
            if not h_name or not e_name:
                st.error("Por favor completa los campos obligatorios.")
            else:
                st.session_state.host_data['host_name'] = h_name
                st.session_state.host_data['host_email'] = h_email
                st.session_state.host_data['organization'] = h_org
                st.session_state.host_data['usual_venue'] = h_venue
                st.session_state.host_data['target_sponsors'] = h_sponsors

                st.session_state.event_data['event_name'] = e_name
                st.session_state.event_data['event_date'] = e_date
                st.session_state.event_data['modality'] = e_mod
                st.session_state.event_data['isPartOfFramework'] = is_framework
                st.session_state.event_data['framework_name'] = framework_name
                st.session_state.event_data['giveFrameworkTickets'] = give_tickets

                st.session_state.step = 2
                st.rerun()


# ==========================================\n# PASO 2: DIAGNÓSTICO & ALCANCE
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='main-header'>🎯 Cuestionario de Alcance y Parámetros</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Paso 2 de 3: Define el alcance técnico, logístico y de premiación para personalizar las 31 tareas sugeridas y las notificaciones.</div>", unsafe_allow_html=True)

    with st.form("diag_form_v4"):
        st.subheader("1. Capacidad y Ponderación de Jueceo")
        col1, col2 = st.columns(2)
        with col1:
            capacity = st.number_input("Aforo estimado (Jammers + Mentores + Staff)", min_value=10, max_value=1000, value=st.session_state.event_data['capacity'], step=10)
            duration = st.selectbox("Duración del maratón", [48, 72, 120, 504], format_func=lambda x: f"{x} horas ({x//24} días)" if x>=24 else f"{x} horas")
        with col2:
            prizes_enabled = st.checkbox("¿El evento ofrecerá bolsa de premios / incentivos?", value=st.session_state.event_data['prizes_enabled'])
            jury_weight = st.slider("Porcentaje de peso del Jurado de Expertos", min_value=50, max_value=100, value=st.session_state.event_data['jury_weight'], step=5)
            st.caption(f"Voto del Público asignado automáticamente: **{100 - jury_weight}%**")

        st.subheader("2. Infraestructura y Redes")
        col3, col4 = st.columns(2)
        with col3:
            has_venue = st.checkbox("Recinto físico asegurado con acceso 24/7", value=st.session_state.event_data['has_venue'])
            bandwidth_ok = st.checkbox("Red dedicada de mínimo 20 Mbps simétricos", value=st.session_state.event_data['bandwidth_ok'])
        with col4:
            has_catering = st.checkbox("Servicio de catering e insumos continuos", value=st.session_state.event_data['has_catering'])
            has_streaming = st.checkbox("Transmisión en vivo por Twitch / YouTube", value=st.session_state.event_data['has_streaming'])

        submit_diag = st.form_submit_button("Generar Sistema de Gestión Completo 🚀", use_container_width=True)

        if submit_diag:
            st.session_state.event_data['capacity'] = capacity
            st.session_state.event_data['duration_hours'] = duration
            st.session_state.event_data['prizes_enabled'] = prizes_enabled
            st.session_state.event_data['jury_weight'] = jury_weight
            st.session_state.event_data['public_weight'] = 100 - jury_weight
            st.session_state.event_data['has_venue'] = has_venue
            st.session_state.event_data['bandwidth_ok'] = bandwidth_ok
            st.session_state.event_data['has_catering'] = has_catering
            st.session_state.event_data['has_streaming'] = has_streaming
            st.session_state.step = 3
            st.rerun()


# ==========================================\n# PASO 3: PANEL DE CONTROL & EVALUADOR
# ==========================================
elif st.session_state.step == 3:
    st.markdown(f"<div class='main-header'>🎮 Hub de Gestión: {st.session_state.event_data['event_name']}</div>", unsafe_allow_html=True)
    st.markdown(f"**Anfitrión:** {st.session_state.host_data['host_name']} ({st.session_state.host_data['organization']}) | **Fecha:** {st.session_state.event_data['event_date']} | **Ponderación Jueceo:** {st.session_state.event_data['jury_weight']}% Jurado / {st.session_state.event_data['public_weight']}% Público")

    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Aforo Objetivo", f"{st.session_state.event_data['capacity']} personas")
    with k2: st.metric("Duración", f"{st.session_state.event_data['duration_hours']}h")
    with k3: st.metric("Comité / Staff", f"{len(st.session_state.committee_members)} miembros")
    with k4: st.metric("Equipos Registrados", f"{len(st.session_state.teams_list)} equipos")

    st.divider()

    tabs = st.tabs([
        "📋 Checklist Operativo (31 Tareas)", 
        "👥 Comité y Asignación de Roles",
        "⚖️ Herramienta de Evaluación para Jueces",
        "🏆 Leaderboard & Ganadores",
        "🍕 Catering & Logística",
        "🔔 Push Notifications & Timeline",
        "📥 Exportar Plan"
    ])

    # -------------------------------------------------------------
    # TAB 1: CHECKLIST OPERATIVO COMPLETO (31 TAREAS)
    # -------------------------------------------------------------
    with tabs[0]:
        st.subheader("Desglose Estandarizado de Actividades (Matriz Completa de 31 Tareas)")
        
        filter_member = st.selectbox("Filtrar tareas asignadas a un miembro del equipo:", ["Todos los miembros"] + [m['Name'] for m in st.session_state.committee_members])

        all_31_tasks = [
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Definir objetivo del jam y desarrollar el plan general", "Crítica", "Director General", 60),
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Definir alcance, aforo y contratar ambulancia si aforo >= 100", "Crítica", "Director de Logística", 55),
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Conformar comité organizador de 5 direcciones clave", "Crítica", "Director General", 50),
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Seleccionar plataforma de entrega de juegos (Itch.io)", "Alta", "Director de Streaming & TI", 45),
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Definir panel de jueces y coordinar rúbrica de 100+20 pts", "Alta", "Director General", 40),
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Establecer alianzas con Liga de Streamers / Influencers", "Media", "Director de Marketing", 35),
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Prospección y firma de patrocinadores (Indie/Master/Legendary)", "Alta", "Director de Vinculación", 32),
            ("Fase 1: Pre-Evento - Planeación (T-60d a T-30d)", "Comisionar arte e ilustración del póster oficial del evento", "Media", "Director de Imagen", 30),

            ("Fase 2: Pre-Evento - Ejecución (T-30d a T-24h)", "Lanzar landing page y formulario oficial de registro", "Alta", "Director de Marketing", 28),
            ("Fase 2: Pre-Evento - Ejecución (T-30d a T-24h)", "Configurar servidor de Discord con canales por especialidades", "Alta", "Director de Streaming & TI", 25),
            ("Fase 2: Pre-Evento - Ejecución (T-30d a T-24h)", "Difusión e hipersegmentación en universidades objetivo", "Media", "Director de Marketing", 20),
            ("Fase 2: Pre-Evento - Ejecución (T-30d a T-24h)", "Confirmación formal del venue físico 24/7 y permisos", "Crítica", "Director de Logística", 15),
            ("Fase 2: Pre-Evento - Ejecución (T-30d a T-24h)", "Prueba de carga de red (Mínimo 20 Mbps simétricos)", "Crítica", "Director de Streaming & TI", 10),
            ("Fase 2: Pre-Evento - Ejecución (T-30d a T-24h)", "Confirmar pedido de catering para 150 personas (café, pizzas)", "Alta", "Director de Logística", 7),
            ("Fase 2: Pre-Evento - Ejecución (T-30d a T-24h)", "Coordinar pases VIP y booth con los organizadores del Evento Marco", "Alta", "Director de Vinculación", 5),

            ("Fase 3: Durante el Jam - Inauguración (Día 1)", "Recepcionar espacio y acomodar mobiliario e impresos", "Crítica", "Director de Logística", 2),
            ("Fase 3: Durante el Jam - Inauguración (Día 1)", "Check-in de participantes, entrega de gafetes y t-shirts", "Alta", "Encargado de Entrada", 1),
            ("Fase 3: Durante el Jam - Inauguración (Día 1)", "Iniciar broadcast en vivo de inauguración y bienvenida", "Alta", "Director de Streaming & TI", 0),
            ("Fase 3: Durante el Jam - Inauguración (Día 1)", "REVELACIÓN OFICIAL DEL TEMA SECRETO y Keynote", "Crítica", "Director General", 0),
            ("Fase 3: Durante el Jam - Inauguración (Día 1)", "Coffee break inaugural y dinámica de integración #busca-equipo", "Media", "Director de Logística", -1),

            ("Fase 4: Durante el Jam - Desarrollo (Día 2)", "Bloques de mentoría técnica con expertos de la industria", "Alta", "Director General", -12),
            ("Fase 4: Durante el Jam - Desarrollo (Día 2)", "Cobertura fotográfica y generación de Reels diarios", "Media", "Encargado de Fotografía", -18),
            ("Fase 4: Durante el Jam - Desarrollo (Día 2)", "Transmisión especial 'La Hora de la Comida' y entrevistas", "Media", "Director de Streaming & TI", -24),
            ("Fase 4: Durante el Jam - Desarrollo (Día 2)", "Playtesting en vivo con la Liga de Streamers", "Alta", "Director de Streaming & TI", -28),
            ("Fase 4: Durante el Jam - Desarrollo (Día 2)", "Torneo de Super Smash Bros / Karaoke nocturno para reducir estrés", "Baja", "Encargado de Torneos", -32),

            ("Fase 5: Durante el Jam - Cierre (Día 3)", "Alerta T-2h para subida de ejecutables a Itch.io", "Crítica", "Director de Streaming & TI", -44),
            ("Fase 5: Durante el Jam - Cierre (Día 3)", "Cierre de entregas y preparación de ronda de pitches", "Crítica", "Director General", -46),
            ("Fase 5: Durante el Jam - Cierre (Día 3)", "Presentaciones de 5 min por equipo frente al jurado y público", "Alta", "Director General", -47),
            ("Fase 5: Durante el Jam - Cierre (Día 3)", "Evaluación del Jurado (85%) y conteo de votos del Público (15%)", "Crítica", "Director General", -48),
            ("Fase 5: Durante el Jam - Cierre (Día 3)", "Ceremonia de Clausura, anuncio del Top 3 y entrega de premios", "Alta", "Director General", -48),

            ("Fase 6: Post-Evento (T+24h a T+7d)", "Limpieza, toma de evidencia y devolución del recinto", "Crítica", "Director de Logística", -50)
        ]

        completed_cnt = 0
        total_cnt = len(all_31_tasks)

        for phase, task_name, urgency, assigned_role, offset in all_31_tasks:
            key = f"chk_v4_{task_name}"
            is_checked = st.session_state.tasks_status.get(key, False)
            if is_checked: completed_cnt += 1

            if filter_member == "Todos los miembros" or assigned_role in [m['Role'] for m in st.session_state.committee_members if m['Name'] == filter_member]:
                urg_color = "🔴" if urgency == "Crítica" else ("🟠" if urgency == "Alta" else "🟡")
                col_t1, col_t2, col_t3 = st.columns([0.05, 0.7, 0.25])
                with col_t1:
                    val = st.checkbox("", key=key, value=is_checked)
                    st.session_state.tasks_status[key] = val
                with col_t2:
                    st.write(f"{urg_color} **{task_name}** ({phase.split('-')[0].strip()})")
                with col_t3:
                    st.caption(f"👤 {assigned_role} | {urgency}")

        st.progress(completed_cnt / total_cnt, text=f"Progreso Global del Jam: {completed_cnt}/{total_cnt} tareas completadas ({(completed_cnt/total_cnt)*100:.1f}%)")

    # -------------------------------------------------------------
    # TAB 2: COMITÉ Y ASIGNACIÓN DE ROLES (RESTAURADO & AMPLIADO)
    # -------------------------------------------------------------
    with tabs[1]:
        st.subheader("👥 Estructura del Comité Organizador y Roles de Campo")
        st.markdown("Gestión de integrantes del equipo organizador basados en la metodología oficial de 48toplay / ElGGJRegio.")

        col_c1, col_c2 = st.columns([0.65, 0.35])

        with col_c1:
            st.markdown("#### Directorio de Integrantes Registrados")
            df_committee = pd.DataFrame(st.session_state.committee_members)
            st.dataframe(df_committee, use_container_width=True)

        with col_c2:
            st.markdown("#### ➕ Registrar / Editar Miembro")
            with st.form("add_member_form"):
                m_name = st.text_input("Nombre completo")
                m_email = st.text_input("Correo electrónico")
                m_role = st.selectbox("Rol Asignado", [
                    "👑 Director General / Líder",
                    "📍 Director de Logística & Venue",
                    "📣 Director de Marketing & Prensa",
                    "🎨 Director de Imagen & Arte",
                    "📡 Director de Streaming & TI",
                    "🤝 Director de Vinculación & Patrocinio",
                    "🚪 Host / Coordinador de Entrada",
                    "🎁 Encargado de Premios & Goodies",
                    "🎤 Orador Principal / MC",
                    "📸 Encargado de Fotografía & Entrevistas",
                    "🎮 Encargado de Torneos & Recreación",
                    "💡 Coordinador de Mentores Técnicos"
                ])
                add_m_btn = st.form_submit_button("Guardar en el Comité")
                if add_m_btn and m_name:
                    st.session_state.committee_members.append({
                        'Name': m_name, 'Email': m_email, 'Role': m_role, 'TaskCount': 3
                    })
                    st.success(f"¡{m_name} agregado exitosamente!")
                    st.rerun()

    # -------------------------------------------------------------
    # TAB 3: HERRAMIENTA DE EVALUACIÓN PARA JUECES (EXCEL GGJ2026_EVALUACIÓN)
    # -------------------------------------------------------------
    with tabs[2]:
        st.subheader("⚖️ Sistema Oficial de Evaluaciones para Jueces")
        st.markdown("Basado exactamente en la estructura del Excel **`GGJ2026_Evaluación`** (100 puntos base + 20 puntos extra).")

        col_j1, col_j2 = st.columns([0.3, 0.7])

        with col_j1:
            st.markdown("#### 👨‍⚖️ Selección de Juez y Equipo")
            active_judge = st.selectbox("Evaluar como Juez:", [j['Nombre'] for j in st.session_state.judges_list])
            
            st.markdown("---")
            st.markdown("#### 🏎️ Equipos Participantes")
            for t in st.session_state.teams_list:
                st.caption(f"**[{t['Code']}] {t['TeamName']}** - Juego: *{t['GameName']}* ({t['PresentTime']} hrs)")
            
            with st.expander("➕ Agregar Nuevo Equipo"):
                new_code = st.text_input("Código (ej. E006)")
                new_tname = st.text_input("Nombre de Equipo")
                new_gname = st.text_input("Nombre de Juego")
                if st.button("Guardar Equipo") and new_code:
                    st.session_state.teams_list.append({'Code': new_code, 'TeamName': new_tname, 'GameName': new_gname, 'PresentTime': '17:30'})
                    st.success("Equipo registrado")
                    st.rerun()

        with col_j2:
            active_team_code = st.selectbox("Seleccionar Equipo a Calificar:", [f"{t['Code']} - {t['TeamName']} ({t['GameName']})" for t in st.session_state.teams_list])
            t_code = active_team_code.split(" - ")[0]

            # Inicializar matriz si no existe
            if active_judge not in st.session_state.evaluations:
                st.session_state.evaluations[active_judge] = {}
            if t_code not in st.session_state.evaluations[active_judge]:
                st.session_state.evaluations[active_judge][t_code] = {
                    'Orig_Concept': 5, 'Orig_Theme': 5, 'GD_Mech': 3, 'GD_Dyn': 3, 'GD_Esth': 3, 'GD_Lvl': 3,
                    'Int_UX': 3, 'Int_UI': 3, 'Int_Replay': 5, 'Art_Vis': 3, 'Art_Aud': 3, 'Art_Narr': 3, 'Art_Amb': 3,
                    'Tech_Prog': 5, 'Tech_Ctrl': 5, 'Inn_Tech': 2, 'Inn_Proc': 2, 'Viab_Econ': 1, 'Viab_Emp': 1, 'Viab_IP': 1,
                    'Div_Points': 0, 'PublicScore': 70
                }

            cur_eval = st.session_state.evaluations[active_judge][t_code]

            with st.form("eval_form_ggj2026"):
                st.markdown("### 1. Rubros Generales (Máximo 100 Puntos)")
                c1, c2 = st.columns(2)

                with c1:
                    st.markdown("**Originalidad (20 pts max)**")
                    c_concept = st.slider("Concepto (0-10)", 0, 10, cur_eval['Orig_Concept'])
                    c_theme = st.slider("Uso de temática (0-10)", 0, 10, cur_eval['Orig_Theme'])

                    st.markdown("**Diseño de Juego (20 pts max)**")
                    c_mech = st.slider("Mecánicas (0-5)", 0, 5, cur_eval['GD_Mech'])
                    c_dyn = st.slider("Dinámicas (0-5)", 0, 5, cur_eval['GD_Dyn'])
                    c_esth = st.slider("Estéticas (0-5)", 0, 5, cur_eval['GD_Esth'])
                    c_lvl = st.slider("Diseño de Nivel (0-5)", 0, 5, cur_eval['GD_Lvl'])

                    st.markdown("**Interacciones (20 pts max)**")
                    c_ux = st.slider("UX (0-5)", 0, 5, cur_eval['Int_UX'])
                    c_ui = st.slider("UI (0-5)", 0, 5, cur_eval['Int_UI'])
                    c_replay = st.slider("Rejugabilidad (0-10)", 0, 10, cur_eval['Int_Replay'])

                with c2:
                    st.markdown("**Calidad Artística (20 pts max)**")
                    c_vis = st.slider("Visual (0-5)", 0, 5, cur_eval['Art_Vis'])
                    c_aud = st.slider("Auditiva (0-5)", 0, 5, cur_eval['Art_Aud'])
                    c_narr = st.slider("Narrativa (0-5)", 0, 5, cur_eval['Art_Narr'])
                    c_amb = st.slider("Ambientación (0-5)", 0, 5, cur_eval['Art_Amb'])

                    st.markdown("**Calidad Técnica (20 pts max)**")
                    c_prog = st.slider("Programación (0-10)", 0, 10, cur_eval['Tech_Prog'])
                    c_ctrl = st.slider("Uso de Controles/Periféricos (0-10)", 0, 10, cur_eval['Tech_Ctrl'])

                st.markdown("### 2. Rubros Extra e Innovación (Máximo 20 Puntos)")
                c3, c4 = st.columns(2)
                with c3:
                    c_inntech = st.slider("Nuevas Tecnologías (0-5)", 0, 5, cur_eval['Inn_Tech'])
                    c_innproc = st.slider("Nuevos Procesos (0-5)", 0, 5, cur_eval['Inn_Proc'])
                    c_viabecon = st.slider("Potencial Económico (0-2)", 0, 2, cur_eval['Viab_Econ'])
                with c4:
                    c_viabemp = st.slider("Potencial de Empresa (0-2)", 0, 2, cur_eval['Viab_Emp'])
                    c_viabip = st.slider("Propiedad Intelectual Explotable (0-2)", 0, 2, cur_eval['Viab_IP'])
                    c_divpts = st.slider("Diversificadores / Retos Extra (0-4)", 0, 4, cur_eval['Div_Points'])

                st.markdown("### 3. Voto del Público / Streamers")
                c_public = st.number_input("Puntaje del Público (0-100)", min_value=0, max_value=100, value=cur_eval['PublicScore'])

                save_eval_btn = st.form_submit_button("Guardar Calificación de Juez 💾", use_container_width=True)

                if save_eval_btn:
                    st.session_state.evaluations[active_judge][t_code] = {
                        'Orig_Concept': c_concept, 'Orig_Theme': c_theme,
                        'GD_Mech': c_mech, 'GD_Dyn': c_dyn, 'GD_Esth': c_esth, 'GD_Lvl': c_lvl,
                        'Int_UX': c_ux, 'Int_UI': c_ui, 'Int_Replay': c_replay,
                        'Art_Vis': c_vis, 'Art_Aud': c_aud, 'Art_Narr': c_narr, 'Art_Amb': c_amb,
                        'Tech_Prog': c_prog, 'Tech_Ctrl': c_ctrl,
                        'Inn_Tech': c_inntech, 'Inn_Proc': c_innproc,
                        'Viab_Econ': c_viabecon, 'Viab_Emp': c_viabemp, 'Viab_IP': c_viabip,
                        'Div_Points': c_divpts, 'PublicScore': c_public
                    }
                    st.success(f"¡Calificación de {active_judge} para {t_code} guardada con éxito!")
                    st.rerun()

    # -------------------------------------------------------------
    # TAB 4: LEADERBOARD & GANADORES
    # -------------------------------------------------------------
    with tabs[3]:
        st.subheader("🏆 Tabla de Posiciones Final (Leaderboard GGJ2026)")
        st.markdown(f"Ponderación aplicada: **{st.session_state.event_data['jury_weight']}% Jurado de Expertos** + **{st.session_state.event_data['public_weight']}% Voto del Público**")

        results_data = []

        for team in st.session_state.teams_list:
            code = team['Code']
            judge_totals = []
            public_score = 70

            for judge_name, eval_dict in st.session_state.evaluations.items():
                if code in eval_dict:
                    ev = eval_dict[code]
                    tot = sum([
                        ev['Orig_Concept'], ev['Orig_Theme'], ev['GD_Mech'], ev['GD_Dyn'], ev['GD_Esth'], ev['GD_Lvl'],
                        ev['Int_UX'], ev['Int_UI'], ev['Int_Replay'], ev['Art_Vis'], ev['Art_Aud'], ev['Art_Narr'], ev['Art_Amb'],
                        ev['Tech_Prog'], ev['Tech_Ctrl'], ev['Inn_Tech'], ev['Inn_Proc'], ev['Viab_Econ'], ev['Viab_Emp'],
                        ev['Viab_IP'], ev['Div_Points']
                    ])
                    judge_totals.append(tot)
                    public_score = ev['PublicScore']

            avg_judge = sum(judge_totals) / len(judge_totals) if judge_totals else 0
            j_weight_val = st.session_state.event_data['jury_weight'] / 100.0
            p_weight_val = st.session_state.event_data['public_weight'] / 100.0
            
            final_score = (avg_judge * j_weight_val) + (public_score * p_weight_val)

            results_data.append({
                'Código': code,
                'Equipo': team['TeamName'],
                'Juego': team['GameName'],
                'Promedio Jurado (120p max)': round(avg_judge, 2),
                'Voto Público (100p max)': public_score,
                'Puntaje Final Ponderado': round(final_score, 2)
            })

        df_results = pd.DataFrame(results_data)
        if not df_results.empty:
            df_results = df_results.sort_values(by='Puntaje Final Ponderado', ascending=False).reset_index(drop=True)
            df_results.index += 1

            st.dataframe(df_results, use_container_width=True)

            # Podio
            if len(df_results) >= 3:
                st.markdown("### 🥇 Podio de Ganadores (Top 3)")
                p1, p2, p3 = st.columns(3)
                with p1:
                    st.markdown(f"<div class='gold-medal'>🥇 1ER LUGAR: {df_results.iloc[0]['Equipo']}</div>", unsafe_allow_html=True)
                    st.write(f"**Juego:** {df_results.iloc[0]['Juego']} ({df_results.iloc[0]['Puntaje Final Ponderado']} pts)")
                    if st.session_state.event_data['giveFrameworkTickets']:
                        st.caption("🎟️ Premia: Pases VIP All-Access + Booth de Exhibición + Cash Pool Nivel Legendary")
                with p2:
                    st.markdown(f"<div class='silver-medal'>🥈 2DO LUGAR: {df_results.iloc[1]['Equipo']}</div>", unsafe_allow_html=True)
                    st.write(f"**Juego:** {df_results.iloc[1]['Juego']} ({df_results.iloc[1]['Puntaje Final Ponderado']} pts)")
                    if st.session_state.event_data['giveFrameworkTickets']:
                        st.caption("🎟️ Premia: Pases de Día Completo al Evento + Becas + Hardware")
                with p3:
                    st.markdown(f"<div class='bronze-medal'>🥉 3ER LUGAR: {df_results.iloc[2]['Equipo']}</div>", unsafe_allow_html=True)
                    st.write(f"**Juego:** {df_results.iloc[2]['Juego']} ({df_results.iloc[2]['Puntaje Final Ponderado']} pts)")
                    if st.session_state.event_data['giveFrameworkTickets']:
                        st.caption("🎟️ Premia: Licencias de Software + Diplomas Oficiales")

    # -------------------------------------------------------------
    # TAB 5: CATERING & LOGÍSTICA
    # -------------------------------------------------------------
    with tabs[4]:
        st.subheader("🍕 Calculadora y Logística de Insumos")
        cap = st.session_state.event_data['capacity']
        st.write(f"Estimación de insumos para **{cap} personas** durante **48 horas**:")

        catering_data = [
            {"Insumo": "☕ Café Soluble/Grano", "Cantidad": f"{cap * 2} tazas", "Ratio": "2 tazas/jammer"},
            {"Insumo": "🥤 Refrescos/Agua", "Cantidad": f"{cap * 3} latas", "Ratio": "3 latas/jammer"},
            {"Insumo": "⚡ Energizantes", "Cantidad": f"{cap * 1} latas", "Ratio": "1 lata/jammer"},
            {"Insumo": "🍕 Pizza (Cena Día 1)", "Cantidad": f"{cap} rebanadas ({cap//4} cajas)", "Ratio": "2 rebanadas/jammer"},
            {"Insumo": "🍔 Comida Fuerte (Día 2)", "Cantidad": f"{cap} porciones", "Ratio": "1 comida fuerte"},
            {"Insumo": "🍪 Galletas / Snacks", "Cantidad": f"{cap * 3} paquetes", "Ratio": "3 paquetes/jammer"}
        ]
        st.table(pd.DataFrame(catering_data))

    # -------------------------------------------------------------
    # TAB 6: PUSH NOTIFICATIONS & TIMELINE
    # -------------------------------------------------------------
    with tabs[5]:
        st.subheader("🔔 Sistema de Notificaciones Push Programadas")
        st.markdown("Recordatorios automáticos del Service Worker dirigidos al Anfitrión y miembros del comité:")

        notifications = [
            ("📌 T-60 Días", "Conformación del Comité", "Líder General", "Enviar plantilla de invitación a los 5 Directores."),
            ("📍 T-30 Días", "Confirmación de Venue", "Logística", "Verificar acceso 24/7 y red dedicada de 20+ Mbps."),
            ("🍕 T-7 Días", "Pedido de Catering", "Logística", f"Confirmar orden para {cap} personas (300 cafés, 450 refrescos)."),
            ("📡 T-24 Horas", "Prueba de Broadcast", "Streaming & TI", "Revisar OBS, overlays de patrocinadores y canal #busca-equipo."),
            ("🚨 Hora 46:00", "ALERTA MÁXIMA DE SUBIDA", "Jammers & Staff", "¡Quedan 2 horas para subir juegos a Itch.io!"),
            ("📦 Post-Event", "Reporte Post-Mortem", "Vinculación", "Enviar reporte de resultados a patrocinadores Nivel Legendary.")
        ]
        st.table(pd.DataFrame(notifications, columns=["Trigger", "Evento", "Rol Destino", "Mensaje de la Notificación"]))

        st.markdown("---")
        st.subheader("📊 Diagrama de Gantt del Evento")
        
        gantt_df = pd.DataFrame([
            {"Tarea": "Planeación General", "Inicio": -60, "Fin": -30, "Fase": "Pre-Evento"},
            {"Tarea": "Patrocinios y Venue", "Inicio": -45, "Fin": -15, "Fase": "Pre-Evento"},
            {"Tarea": "Campaña de Difusión", "Inicio": -30, "Fin": -1, "Fase": "Pre-Evento"},
            {"Tarea": "Inauguración y Kickoff", "Inicio": 0, "Fin": 1, "Fase": "Ejecución Jam"},
            {"Tarea": "Maratón 48h y Mentorías", "Inicio": 1, "Fin": 2, "Fase": "Ejecución Jam"},
            {"Tarea": "Presentaciones y Clausura", "Inicio": 2, "Fin": 3, "Fase": "Ejecución Jam"},
            {"Tarea": "Post-Mortem y Reporte", "Inicio": 3, "Fin": 10, "Fase": "Post-Evento"}
        ])

        fig = px.timeline(gantt_df, x_start="Inicio", x_end="Fin", y="Tarea", color="Fase", title="Cronograma General de Gestión")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 7: EXPORTAR PLAN
    # -------------------------------------------------------------
    with tabs[6]:
        st.subheader("📥 Exportar Configuración Completa")
        export_payload = {
            "host": st.session_state.host_data,
            "event": st.session_state.event_data,
            "committee": st.session_state.committee_members,
            "teams": st.session_state.teams_list,
            "evaluations": st.session_state.evaluations,
            "tasks_status": st.session_state.tasks_status,
            "exported_at": str(datetime.now())
        }
        st.download_button("Descargar Plan Completo en JSON", json.dumps(export_payload, indent=4, default=str), f"plan_gamejam_{st.session_state.event_data['event_name'].lower().replace(' ', '_')}.json", "application/json")
