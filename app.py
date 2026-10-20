import os
import pandas as pd
import streamlit as st

# Configuración de la página web
st.set_page_config(
    page_title="Análisis de Homicidios Intencionales - SZ El Oro", layout="wide"
)

# Estilo institucional oscuro: azul marino, cian y acentos rojos
st.markdown(
    """
    <style>
    :root {
        --fondo: #080F1C;
        --panel: #111D2E;
        --panel-2: #17263B;
        --borde: #2B405B;
        --texto: #E8F0FA;
        --secundario: #9FB2C9;
        --cian: #38BDF8;
        --azul: #2563EB;
        --rojo: #F05252;
    }
    .stApp { background: radial-gradient(circle at 15% 0%, #142943 0%, var(--fondo) 45%, #080D16 100%); color: var(--texto); }
    [data-testid="stHeader"] { background: rgba(8,15,28,.92); }
    [data-testid="stSidebar"] { background: #0D1726; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .titulo-principal {
        font-size: clamp(22px, 2.2vw, 32px); font-weight: 800;
        color: #F4F8FF; text-align: center; margin: 4px 0 22px;
        padding: 18px 14px; border: 1px solid #2B4968; border-radius: 12px;
        background: linear-gradient(110deg, rgba(19,42,68,.98), rgba(12,25,43,.96));
        box-shadow: 0 8px 26px rgba(0,0,0,.22); letter-spacing: .5px;
    }
    .titulo-principal span { color: var(--cian); }
    .seccion-header {
        background: linear-gradient(90deg, #174A78, #176A91); color: #F8FAFC;
        padding: 7px 11px; font-weight: 750; border-left: 3px solid var(--cian);
        border-radius: 5px; font-size: 12px; letter-spacing: .45px;
        margin-top: 12px; margin-bottom: 7px;
    }
    .subseccion-header { background: #1B2B40; color: #DCEBFA; padding: 5px 9px; font-weight: 700; border-radius: 5px; font-size: 12px; }
    [data-testid="stMetric"] { background: linear-gradient(145deg,#14253A,#0E1A2B); border: 1px solid #2A4059; padding: 12px 15px; border-radius: 10px; }
    [data-testid="stMetricLabel"] { color: #A8BCD2 !important; }
    [data-testid="stMetricValue"] { color: #F4F8FF !important; }
    [data-testid="stTextInput"] input, [data-testid="stSelectbox"] div[data-baseweb="select"] > div { background-color: #111D2E; color: #E8F0FA; border-color: #344B66; }
    [data-testid="stExpander"] { background: rgba(17,29,46,.88); border: 1px solid #2B405B; border-radius: 9px; }
    [data-testid="stExpander"] summary, [data-testid="stMarkdownContainer"] p, .stMarkdown, label { color: #DCE7F4; }
    .timeline-heading { color: #EAF4FF; font-size: 20px; font-weight: 800; margin: 18px 0 8px; letter-spacing: .6px; }
    .timeline-date { display:inline-block; background:#173858; color:#BDEBFF; border:1px solid #28618B; padding:5px 10px; border-radius:6px; font-size:12px; font-weight:750; margin-bottom:7px; }
    .timeline-card { border:1px solid #2B405B; border-left:3px solid #38BDF8; border-radius:9px; padding:12px 14px; background:linear-gradient(135deg,#15263B,#0F1B2B); min-height:75px; box-shadow:0 5px 15px rgba(0,0,0,.14); }
    .timeline-card-title { color:#F2F7FF; font-weight:750; font-size:14px; margin-bottom:5px; }
    .timeline-card-detail { color:#AFC1D6; font-size:12px; }
    .timeline-dot { background:#F05252; width:13px; height:13px; border:3px solid #101B2B; outline:2px solid #38BDF8; border-radius:50%; margin:15px auto 0; }
    .timeline-line { background:linear-gradient(#38BDF8,#28527A); width:3px; min-height:100%; border-radius:4px; margin:0 auto; }
    hr { border-color:#293D55 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='titulo-principal'>ANÁLISIS DE <span>HOMICIDIOS INTENCIONALES</span> "
    "EN CONTRA DE ESTUDIANTES</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# BASE DE DATOS COMPLETA DE LOS 11 CASOS
# ---------------------------------------------------------
casos = [
    {
        "Cedula": "0750688731",
        "Nombres": "BRAVO BURGOS JOSTYN JOHAO",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2010-07-13",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/SANTA ROSA/LA AVANZADA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Santa Rosa",
        "Lugar": "Sector San José",
        "Fecha": "2026-06-15",
        "Hora": "13:30",
        "Unidad_Educativa": "Por Determinar (Colegio Jorge Enrique Chávez Celi)",
        "Uniformado": "Si",
        "Presunto_GAO": "Choneros",
        "Tipo_Familia": "Monoparental",
        "Circunstancias": """El estudiante se dirigió hasta una tienda utilizada como paradero de buses, donde esperaba abordar el transporte que lo llevaría a su domicilio. En ese momento, llegaron al lugar dos sujetos a bordo de una motocicleta; el acompañante descendió parcialmente del vehículo y abrió fuego contra el estudiante.""",
        "Analisis": """Se presume que el adolescente habría mantenido vínculos con el Grupo Armado Organizado Los Choneros. En el lugar de los hechos, tras su asesinato, se habría dejado un panfleto en el que se atribuye el ataque al GAO Los Lobos, presuntamente como parte de una acción dirigida contra el adolescente.""",
        "Foto": "fotos/caso1.jpg",
    },
    {
        "Cedula": "0750581258",
        "Nombres": "GARCIA TRUJILLO REYNALDO SEBASTIAN",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2008-07-26",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/MACHALA/MACHALA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Machala",
        "Lugar": "2da Este y Av. Circunvalación Sur",
        "Fecha": "2026-07-13",
        "Hora": "16:10",
        "Unidad_Educativa": "Colegio de Bachillerato República del Perú",
        "Uniformado": "No",
        "Presunto_GAO": "SaoBox",
        "Tipo_Familia": "Disfuncional",
        "Circunstancias": """El ciudadano domiciliado en el Sur de Machala y alumno del colegio Republica del Perú caminaba por el sector cuando sujetos armados lo interceptaron y abrieron fuego contra él. Según información preliminar, los atacantes realizaron varios disparos y luego escaparon del lugar.""",
        "Analisis": """El adolescente provenía de un entorno familiar disfuncional y conflictivo. Asimismo, se identificó que su hermano mayor registra antecedentes por el delito de tráfico ilícito de sustancias sujetas a fiscalización. De acuerdo con la información recopilada, la motivación del asesinato estaría relacionada con la disputa por el control territorial en el sector sur de la ciudad.""",
        "Foto": "fotos/caso2.jpg",
    },
    {
        "Cedula": "0750006413",
        "Nombres": "QUITUISACA CORONEL JEFFERSON JAVIER",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2011-01-10",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "PICHINCHA/QUITO/EL CONDADO",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Machala",
        "Lugar": "Sector Leonor Aguilar",
        "Fecha": "2026-07-24",
        "Hora": "13:45",
        "Unidad_Educativa": "Unidad Educativa 16 de Junio",
        "Uniformado": "Si",
        "Presunto_GAO": "SaoBox",
        "Tipo_Familia": "Monoparental",
        "Circunstancias": """El estudiante había culminado su jornada de clases y esperaba el bus que lo trasladaría a su domicilio cuando fue interceptado por dos sujetos que se movilizaban en una motocicleta, quienes proceden a victimarlo utilizando armas de fuego.""",
        "Analisis": """Se presume que el ciudadano habría estado relacionado con el GDC SaoBox y previamente habría recibido amenazas en un colegio anterior (año lectivo 2025), situación que género un cambio de institución educativa.""",
        "Foto": "fotos/caso3.jpg",
    },
    {
        "Cedula": "0706919933",
        "Nombres": "TORO CEDEÑO FRANCISCO JAVIER",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2009-09-19",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/MACHALA/MACHALA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Machala",
        "Lugar": "Av. Pedro Maridueña y 17ava Oeste",
        "Fecha": "2026-07-30",
        "Hora": "12:21",
        "Unidad_Educativa": "Ismael Pérez Pazmiño",
        "Uniformado": "Si",
        "Presunto_GAO": "Por Determinar",
        "Tipo_Familia": "Disfuncional",
        "Circunstancias": """Un estudiante del colegio Ismael Pérez Pazmiño de Machala, fue asesinado mientras se encontraba en el interior de un taxi amarillo. El hecho se registró en la intersección de la avenida Pedro Maridueña Villena y la carrera 17.ª Oeste, cuando dos sujetos encapuchados que se movilizaban en una motocicleta negra habrían perpetrado el ataque y posteriormente huido del lugar.""",
        "Analisis": """El adolescente provenía de un entorno familiar presuntamente disfuncional y conflictivo. Asimismo, se identificó que su padre registra antecedentes por los delitos de robo y descubrimiento de infracciones. Se presume que el adolescente convivía con su madre y otros hermanos de diferente progenitor.""",
        "Foto": "fotos/caso4.jpg",
    },
    {
        "Cedula": "0750755233",
        "Nombres": "ZAVALA SANCHEZ RICHARD MIGUEL",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2009-08-22",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/MACHALA/MACHALA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Machala",
        "Lugar": "25 de junio y 12ava oeste",
        "Fecha": "2026-08-31",
        "Hora": "12:50",
        "Unidad_Educativa": "Colegio Nueve de Octubre",
        "Uniformado": "Si",
        "Presunto_GAO": "Por Determinar",
        "Tipo_Familia": "Monoparental",
        "Circunstancias": """El ciudadano regresaba caminando a su domicilio cuando fue interceptado en la acera por dos sujetos armados que se movilizaban en una motocicleta, quienes abrieron fuego en su contra. Como consecuencia del ataque, el joven recibió aproximadamente cuatro impactos de bala y falleció en el lugar.""",
        "Analisis": """El adolescente provenía de un entomo familiar monoparental, se presume que el adolescente convivía con su madre y otros hermanos de diferente progenitor. La principal hipótesis es su enrolamiento en grupo de delincuencia organizada.""",
        "Foto": "fotos/caso5.jpg",
    },
    {
        "Cedula": "0707256251",
        "Nombres": "GOMEZ MAZA JAHIR XAVIER",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2008-10-11",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/SANTA ROSA/SANTA ROSA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Santa Rosa",
        "Lugar": "Calles Sin Nombre",
        "Fecha": "2026-09-15",
        "Hora": "13:51",
        "Unidad_Educativa": "Colegio Modesto Chávez Franco",
        "Uniformado": "Si",
        "Presunto_GAO": "Choneros",
        "Tipo_Familia": "Nuclear",
        "Circunstancias": """El ciudadano regresaba a su domicilio después de culminar su jornada académica, aún vestido con su uniforme escolar y portando su mochila, cuando fue interceptado por dos sujetos que se movilizaban en una motocicleta. Los atacantes habrían seguido al adolescente, quien intentó escapar corriendo; sin embargo, fue alcanzado y recibió varios disparos.""",
        "Analisis": """El adolescente provendría de un hogar de tipo nuclear. Asimismo, se presume que habría recibido amenazas por parte del Grupo Armado Organizado (GAO) Los Lobos, posiblemente relacionadas con una retaliación en el contexto de la disputa por el control territorial en el cantón Santa Rosa.""",
        "Foto": "fotos/caso6.jpg",
    },
    {
        "Cedula": "0750056426",
        "Nombres": "MORENO MAYON CRISTOPHER FELIPE",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2009-10-08",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/HUAQUILLAS/HUAQUILLAS",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Huaquillas",
        "Lugar": "José Urbina y Asad Bucaram",
        "Fecha": "2026-09-24",
        "Hora": "18:39",
        "Unidad_Educativa": "Unidad Educativa José Anselmo García Cajamarca",
        "Uniformado": "Si",
        "Presunto_GAO": "Lobos",
        "Tipo_Familia": "Monoparental",
        "Circunstancias": """El adolescente fue víctima de un ataque armado en los exteriores de su institución educativa, ubicada en la ciudadadela José Mayón. Según información preliminar, dos sujetos que se movilizaban en una motocicleta lo interceptaron y abrieron fuego en su contra, para posteriormente huir del sector con rumbo desconocido.""",
        "Analisis": """Se presume que el adolescente habría mantenido vínculos con el Grupo Armado Organizado Los Lobos. En el lugar de los hechos, tras su asesinato, se habría dejado un panfleto en el que se atribuye el ataque al GDC Los Volados, presuntamente como parte de una acción dirigida contra el adolescente.""",
        "Foto": "fotos/caso7.jpg",
    },
    {
        "Cedula": "0750357329",
        "Nombres": "RAMIREZ SOCOLA MICHAEL JARED",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2010-07-23",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/HUAQUILLAS/HUAQUILLAS",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Huaquillas",
        "Lugar": "Exterior de colegio Remigio Geo.",
        "Fecha": "2026-09-29",
        "Hora": "13:15",
        "Unidad_Educativa": "Colegio Remigio Geo Gomez",
        "Uniformado": "Si",
        "Presunto_GAO": "Choneros",
        "Tipo_Familia": "Disfuncional",
        "Circunstancias": """El hecho violento ocurrió sobre la avenida La República, cuando el adolescente se encontraba sentado en una silla metálica y fue sorprendido por un sujeto armado que abrió fuego en su contra. Según información preliminar, el presunto atacante habría vestido el uniforme de la institución educativa. Tras el ataque, los sospechosos habrían huido a bordo de una motocicleta.""",
        "Analisis": """El adolescente provenía de un entorno familiar presuntamente disfuncional y se encontraba bajo el cuidado de su madre. Asimismo, se identificó que su padre registraría antecedentes por el delito de contrabando y habría sido asesinado en el año 2023, en el Distrito Huaquillas.""",
        "Foto": "fotos/caso8.jpg",
    },
    {
        "Cedula": "0706953759",
        "Nombres": "MOTOCHE MENDOZA CRISTHOFER EDUARDO",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2010-03-19",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/MACHALA/MACHALA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "APREHENSION POR DELITO ROBO",
        "Distrito": "Machala",
        "Lugar": "9 de mayo y 11ava norte",
        "Fecha": "2026-10-14",
        "Hora": "12:55",
        "Unidad_Educativa": "Colegio 9 de Octubre",
        "Uniformado": "Si",
        "Presunto_GAO": "Lobos",
        "Tipo_Familia": "Disfuncional",
        "Circunstancias": """El ciudadano fue asesinado con arma de fuego, mientras se movilizaba junto a su prima en un bus urbano de la cooperativa Ciudad de Machala, correspondiente a la línea 10. El hecho ocurrió cuando la unidad recogía pasajeros en la intersección de las calles 9 de Mayo y 11.ª Norte. Según información preliminar, un sujeto habría abordado el bus como un pasajero más y posteriormente abrió fuego contra dos personas, para luego huir del lugar.""",
        "Analisis": """El ciudadano provenía de un entorno familiar presuntamente disfuncional. Asimismo, se identificó que, en agosto de 2026, habría sido aprehendido junto con otro ciudadano por su presunta participación en el delito de robo. De igual manera, en fuentes abiertas se habría identificado información que lo vincularía presuntamente con el Grupo Armado Organizado Los Lobos.""",
        "Foto": "fotos/caso9.jpg",
    },
    {
        "Cedula": "0708842259",
        "Nombres": "GUAMAN LEMA JAIRO STEVEN",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2009-04-14",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/MACHALA/MACHALA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Machala",
        "Lugar": "sector 19 de noviembre",
        "Fecha": "2026-10-15",
        "Hora": "08:19",
        "Unidad_Educativa": "Colegio 9 de Octubre",
        "Uniformado": "No",
        "Presunto_GAO": "Lobos",
        "Tipo_Familia": "Disfuncional",
        "Circunstancias": """El ciudadano se encontraba desaparecido desde el día anterior al hallazgo. Según información preliminar, habría sido presuntamente secuestrado por varios sujetos en el cantón Ponce Enríquez, para posteriormente dejar abandonada su cabeza en el barrio 19 de Noviembre, cantón Machala, junto a un panfleto con leyendas amenazantes.""",
        "Analisis": """El ciudadano provenía de un entorno familiar presuntamente disfuncional. Asimismo, se presume que habría recibido amenazas de muerte días antes del hecho, debido a su presunta vinculación con la GAO Los Lobos, motivo por el cual se habría trasladado al cantón Ponce Enríquez. Según información preliminar, en dicho cantón habría sido secuestrado y posterior asesinado, para finalmente dejar abandonada su cabeza junto a un panfleto con leyendas amenazantes.""",
        "Foto": "fotos/caso10.jpg",
    },
    {
        "Cedula": "0750082844",
        "Nombres": "ALVARADO SARMIENTO DERECK SEBASTIAN",
        "Nacionalidad": "ECUATORIANA",
        "Fecha_Nacimiento": "2011-07-05",
        "Sexo": "HOMBRE",
        "Estado_Civil": "SOLTERO",
        "Direccion": "EL ORO/MACHALA/MACHALA",
        "Actividad": "ESTUDIANTE",
        "Antecedentes": "NO REGISTRA",
        "Distrito": "Machala",
        "Lugar": "Pedro Maridueña y R. Veintimilla",
        "Fecha": "2026-10-16",
        "Hora": "13:10",
        "Unidad_Educativa": "Unidad Educativa Ismael Pérez Pazmiño",
        "Uniformado": "Si",
        "Presunto_GAO": "Por Determinar",
        "Tipo_Familia": "Disfuncional",
        "Circunstancias": """El adolescente se encontraba retomando a su domicilio luego de culminar su jornada académica, cuando fue interceptado por dos sujetos que se movilizaban en una motocicleta. Los individuos descendieron del vehículo y abrieron fuego contra el menor, ocasionándole la muerte en el lugar. Posteriormente, los atacantes huyeron con rumbo desconocido.""",
        "Analisis": """El adolescente provenía de un entorno familiar presuntamente disfuncional. Asimismo, se identificó que uno de sus hermanos registra antecedentes por los presuntos delitos de robo, tráfico ilícito de sustancias sujetas a fiscalización y tráfico ilícito de armas de fuego. De igual manera, se presume que el adolescente habría recibido amenazas de muerte con anterioridad al hecho violento.""",
        "Foto": "fotos/caso11.jpg",
    },
]

# ---------------------------------------------------------
# LÍNEA DE TIEMPO, FILTROS Y FICHAS DE EVENTOS
# ---------------------------------------------------------

from datetime import datetime

# Los estilos de la línea de tiempo y las fichas se definen al inicio de la aplicación.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def resolver_foto(caso):
    """Busca primero una imagen cuyo nombre sea la cédula, en la carpeta de app.py."""
    cedula = str(caso.get("Cedula", "")).strip()
    candidatos = []
    if cedula:
        for extension in (".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG", ".webp", ".WEBP"):
            candidatos.append(os.path.join(BASE_DIR, cedula + extension))
            candidatos.append(os.path.join(BASE_DIR, "fotos", cedula + extension))
    # Compatibilidad con los nombres de imagen definidos en la versión anterior.
    foto_anterior = str(caso.get("Foto", "")).strip()
    if foto_anterior:
        candidatos.append(os.path.join(BASE_DIR, foto_anterior))
    for ruta in candidatos:
        if os.path.isfile(ruta):
            return ruta
    return None


def mostrar_campo(etiqueta, valor):
    valor = str(valor).strip() if valor is not None else ""
    if valor:
        st.markdown(f"**{etiqueta}:** {valor}")


def fecha_orden(caso):
    try:
        return datetime.strptime(str(caso.get("Fecha", "")), "%Y-%m-%d")
    except ValueError:
        return datetime.max


# Orden cronológico: del evento más antiguo al más reciente.
casos_ordenados = sorted(casos, key=fecha_orden)

# Indicadores generales
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Casos registrados", len(casos))
with col2:
    st.metric("Distritos", len({c.get("Distrito", "") for c in casos if c.get("Distrito")}))
with col3:
    st.metric("Unidades educativas", len({c.get("Unidad_Educativa", "") for c in casos if c.get("Unidad_Educativa")}))
with col4:
    st.metric("Casos con uniforme reportado", sum(1 for c in casos if str(c.get("Uniformado", "")).lower() == "si"))

st.markdown("<div class='timeline-heading'>LÍNEA DE TIEMPO DE EVENTOS</div>", unsafe_allow_html=True)
st.caption("Seleccione un evento para desplegar sus datos, circunstancias, análisis y fotografía asociada.")

st.markdown("### Buscar y filtrar eventos")
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    busqueda = st.text_input(
        "Buscar por nombre, cédula, lugar o descripción",
        placeholder="Escriba una palabra clave...",
    )
with f2:
    distritos = sorted({c.get("Distrito", "") for c in casos if c.get("Distrito")})
    distrito_sel = st.selectbox("Distrito", ["Todos"] + distritos)
with f3:
    unidades = sorted({c.get("Unidad_Educativa", "") for c in casos if c.get("Unidad_Educativa")})
    unidad_sel = st.selectbox("Unidad educativa", ["Todas"] + unidades)

filtrados = []
for caso in casos_ordenados:
    if distrito_sel != "Todos" and caso.get("Distrito") != distrito_sel:
        continue
    if unidad_sel != "Todas" and caso.get("Unidad_Educativa") != unidad_sel:
        continue
    texto_busqueda = " ".join(str(v) for v in caso.values()).casefold()
    if busqueda and busqueda.casefold() not in texto_busqueda:
        continue
    filtrados.append(caso)

st.caption(f"Se muestran {len(filtrados)} de {len(casos)} eventos, ordenados por fecha.")

if not filtrados:
    st.info("No se encontraron eventos con los filtros seleccionados.")
else:
    for indice, caso in enumerate(filtrados):
        fecha = caso.get("Fecha", "Fecha no disponible")
        try:
            fecha_visible = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            fecha_visible = fecha

        nombre = caso.get("Nombres", f"Evento {indice + 1}")
        resumen = f"{caso.get('Distrito', 'Distrito no disponible')} · {caso.get('Lugar', 'Lugar no disponible')}"
        izquierda, centro, derecha = st.columns([10, 1, 10], gap="small")

        # Alterna las tarjetas a ambos lados de la línea central.
        tarjeta = izquierda if indice % 2 == 0 else derecha
        with tarjeta:
            st.markdown(
                f"<div class='timeline-date'>{fecha_visible} · {caso.get('Hora', 'Hora no disponible')}</div>"
                f"<div class='timeline-card'><div class='timeline-card-title'>{nombre}</div>"
                f"<div class='timeline-card-detail'>{resumen}</div></div>",
                unsafe_allow_html=True,
            )
            with st.expander("Ver información del evento", expanded=(len(filtrados) == 1)):
                foto = resolver_foto(caso)

                st.markdown("<div class='seccion-header'>DATOS DEL EVENTO</div>", unsafe_allow_html=True)
                mostrar_campo("Fecha del hecho", fecha_visible)
                mostrar_campo("Hora", caso.get("Hora"))
                mostrar_campo("Distrito", caso.get("Distrito"))
                mostrar_campo("Lugar", caso.get("Lugar"))
                mostrar_campo("Unidad educativa", caso.get("Unidad_Educativa"))
                mostrar_campo("Uniformado", caso.get("Uniformado"))
                mostrar_campo("Presunto grupo", caso.get("Presunto_GAO"))

                st.markdown("<div class='seccion-header'>DATOS GENERALES</div>", unsafe_allow_html=True)
                foto_col, datos_col = st.columns([1, 3], gap="medium")
                with foto_col:
                    if foto:
                        # Retrato compacto tipo pasaporte; no ocupa todo el ancho.
                        st.image(foto, caption="Fotografía", width=145)
                    else:
                        st.markdown(
                            "<div style='width:145px;height:175px;border:1px dashed #49627D;"
                            "border-radius:8px;display:flex;align-items:center;justify-content:center;"
                            "text-align:center;color:#9FB2C9;background:#111D2E;font-size:12px;padding:8px'>"
                            "Fotografía no encontrada</div>",
                            unsafe_allow_html=True,
                        )
                        st.caption(f"Archivo esperado: {caso.get('Cedula', 'CEDULA')}.png o el nombre indicado en Foto.")
                with datos_col:
                    mostrar_campo("Nombres", caso.get("Nombres"))
                    mostrar_campo("Cédula", caso.get("Cedula"))
                    mostrar_campo("Nacionalidad", caso.get("Nacionalidad"))
                    mostrar_campo("Fecha de nacimiento", caso.get("Fecha_Nacimiento"))
                    mostrar_campo("Sexo", caso.get("Sexo"))
                    mostrar_campo("Estado civil", caso.get("Estado_Civil"))
                    mostrar_campo("Dirección registrada", caso.get("Direccion"))
                    mostrar_campo("Actividad", caso.get("Actividad"))
                    mostrar_campo("Antecedentes registrados", caso.get("Antecedentes"))
                    mostrar_campo("Tipo de familia reportado", caso.get("Tipo_Familia"))

                st.markdown("<div class='seccion-header'>CIRCUNSTANCIAS DEL HECHO</div>", unsafe_allow_html=True)
                st.write(caso.get("Circunstancias", "Sin información registrada."))
                st.markdown("<div class='seccion-header'>ANÁLISIS</div>", unsafe_allow_html=True)
                st.write(caso.get("Analisis", "Sin análisis registrado."))

        with centro:
            st.markdown("<div class='timeline-dot'></div>", unsafe_allow_html=True)
            if indice < len(filtrados) - 1:
                st.markdown("<div class='timeline-line' style='height: 100px;'></div>", unsafe_allow_html=True)

        # Mantiene vacía la columna opuesta para alternar las tarjetas.
        with (derecha if indice % 2 == 0 else izquierda):
            st.write("")

st.markdown("---")
st.caption(
    "Visualizador local de uso interno. Verifique la exactitud y autorización de los datos antes de utilizarlos o compartirlos."
)
