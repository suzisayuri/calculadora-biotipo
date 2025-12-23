import streamlit as st
from PIL import Image
import pandas as pd
import os
from datetime import datetime

# 1. Configuração da página
st.set_page_config(page_title="Minha Medida, Meu Estilo", page_icon="🧵")

# 2. CSS (ESTILOS)
st.markdown(
    """
    <style>
    /* Ajuste do Topo e Fundo */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    /* REGRA GERAL: TUDO VERDE E GRANDE (#3c857e, 18px) */
    html, body, p, li, label, .stTextInput label, .stNumberInput label, .stCheckbox label, div[data-testid="stMarkdownContainer"] p {
        font-family: 'Helvetica', sans-serif;
        font-size: 18px; 
        color: #3c857e !important;
    }

    /* REGRA TÍTULOS: ROSA (#E91E63) */
    h1, h2, h3, h1 span, h2 span, h3 span {
        color: #E91E63 !important;
        padding-top: 0px !important;
    }
    
    h1, h1 span {
        font-size: 32px !important; 
    }

    /* --- REGRA PARA TEXTO PEQUENO (CAPTION) --- 
       Aqui configuramos o tamanho 10px (perto do 8 que você queria) e a cor verde.
       O st.caption foge da regra de 18px, por isso funciona. */
    .stCaption, div[data-testid="stCaptionContainer"] {
        font-family: 'Helvetica', sans-serif;
        font-size: 10px !important; 
        color: #3c857e !important;
        line-height: 1.2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Funções
def salvar_lead(email, nome, biotipo_resultado):
    arquivo = 'leads_biotipo.csv'
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    novo_dado = pd.DataFrame([{
        "Data": data_hora,
        "Nome": nome,
        "Email": email,
        "Biotipo": biotipo_resultado
    }])
    if not os.path.isfile(arquivo):
        novo_dado.to_csv(arquivo, index=False, sep=';')
    else:
        novo_dado.to_csv(arquivo, mode='a', header=False, index=False, sep=';')

def identificar_biotipo_chave(ombro, busto, cintura, quadril):
    superior = max(ombro, busto)
    if (0.95 <= superior / quadril <= 1.05) and (cintura <= superior * 0.75):
        return "Ampulheta"
    elif quadril > (superior * 1.05):
        return "Pera"
    elif superior > (quadril * 1.05):
        return "Triangulo"
    elif cintura >= superior and cintura >= quadril:
        return "Oval"
    else:
        return "Retangulo"

# Dicionário de Traduções
traducoes = {
    "Português": {
        "titulo": "🧵 Descubra seu Biotipo e Liberte sua Costura",
        "subtitulo": "O primeiro passo para parar de brigar com o provador e começar a criar roupas que te amam.",
        "ombro": "Medida do Ombro (cm)",
        "busto": "Medida do Busto (cm)",
        "cintura": "Medida da Cintura (cm)",
        "quadril": "Medida do Quadril (cm)",
        "botao": "Descobrir meu Biotipo ✨",
        "aviso_preencher": "Por favor, preencha todas as medidas para o cálculo.",
        "resultado_titulo": "Seu biotipo é:",
        "dica_titulo": "Dica de Costura para você:",
        "extra_titulo": "Por onde começar do zero?",
        "extra_texto": "Agora que você conhece seu corpo, que tal aprender a costurar sua primeira peça pensada exatamente para essas medidas?",
        "sidebar_titulo": "Sobre o Projeto",
        "sidebar_texto": "A costura não é apenas técnica, é uma ferramenta de autoestima. Ao entender suas medidas, você para de tentar caber no padrão e faz o padrão caber em você.",
        "biotipos": {
            "Ampulheta": {"nome": "Ampulheta", "conselho": "O equilíbrio perfeito! Na costura, valorize sua cintura com pences e evite esconder suas formas em roupas muito largas."},
            "Pera": {"nome": "Pera", "conselho": "Seu quadril é sua força. Use a costura para criar golas trabalhadas, babados ou mangas bufantes que equilibram o visual."},
            "Triangulo": {"nome": "Triângulo Invertido", "conselho": "Ombros marcantes pedem saias com volume, bolsos laterais e tecidos encorpados na parte de baixo. Crie o equilíbrio você mesma!"},
            "Oval": {"nome": "Oval", "conselho": "Conforto é a palavra-chave. Aposte em linhas verticais, decotes em V e tecidos com bom caimento que não marcam, mas valorizam seu colo."},
            "Retangulo": {"nome": "Retângulo", "conselho": "Sua silhueta é moderna. Use a costura para 'inventar' curvas com cintos do próprio tecido, recortes laterais e pences estratégicas."}
        }
    },
    "English": {
        "titulo": "🧵 Discover Your Body Type & Free Your Sewing",
        "subtitulo": "The first step to stop fighting fitting rooms and start creating clothes that love you back.",
        "ombro": "Shoulder Measurement (cm)",
        "busto": "Bust Measurement (cm)",
        "cintura": "Waist Measurement (cm)",
        "quadril": "Hip Measurement (cm)",
        "botao": "Calculate Body Type ✨",
        "aviso_preencher": "Please fill in all measurements.",
        "resultado_titulo": "Your body type is:",
        "dica_titulo": "Sewing Tip for you:",
        "extra_titulo": "Where to start?",
        "extra_texto": "Now that you know your body, how about learning to sew your first piece designed exactly for these measurements?",
        "sidebar_titulo": "About the Project",
        "sidebar_texto": "Sewing isn't just technique, it's a tool for self-esteem. By understanding your measurements, you stop trying to fit the standard and make the standard fit you.",
        "biotipos": {
            "Ampulheta": {"nome": "Hourglass", "conselho": "Perfect balance! In sewing, highlight your waist with darts."},
            "Pera": {"nome": "Pear", "conselho": "Your hips are your strength. Use sewing to create detailed collars."},
            "Triangulo": {"nome": "Inverted Triangle", "conselho": "Strong shoulders call for skirts with volume."},
            "Oval": {"nome": "Apple (Oval)", "conselho": "Comfort is key. Bet on vertical lines."},
            "Retangulo": {"nome": "Rectangle", "conselho": "Your silhouette is modern. Use sewing to 'invent' curves."}
        }
    },
    "Español": {
        "titulo": "🧵 Descubre tu Tipo de Cuerpo y Libera tu Costura",
        "subtitulo": "El primer paso para dejar de pelear con el probador y comenzar a crear ropa que te ame.",
        "ombro": "Medida de Hombros (cm)",
        "busto": "Medida de Busto (cm)",
        "cintura": "Medida de Cintura (cm)",
        "quadril": "Medida de Cadera (cm)",
        "botao": "Calcular mi Biotipo ✨",
        "aviso_preencher": "Por favor, complete todas las medidas.",
        "resultado_titulo": "Tu tipo de cuerpo es:",
        "dica_titulo": "Consejo de costura para ti:",
        "extra_titulo": "¿Por dónde empezar?",
        "extra_texto": "Ahora que conoces tu cuerpo, ¿qué tal aprender a coser tu primera prenda pensada exactamente para estas medidas?",
        "sidebar_titulo": "Sobre el Proyecto",
        "sidebar_texto": "La costura no es solo técnica, es una herramienta de autoestima. Al entender tus medidas, dejas de intentar encajar en el patrón y haces que el patrón encaje en ti.",
        "biotipos": {
            "Ampulheta": {"nome": "Reloj de Arena", "conselho": "¡El equilibrio perfecto! En la costura, valora tu cintura con pinzas."},
            "Pera": {"nome": "Pera", "conselho": "Tu cadera es tu fuerza. Usa la costura para crear cuellos trabajados."},
            "Triangulo": {"nome": "Triángulo Invertido", "conselho": "Hombros marcados piden faldas con volumen."},
            "Oval": {"nome": "Óvalo", "conselho": "Comodidad es la clave. Apuesta por líneas verticales."},
            "Retangulo": {"nome": "Rectángulo", "conselho": "Tu silueta es moderna. Usa la costura para 'inventar' curvas."}
        }
    }
}

# --- INÍCIO DO APP ---

# Sidebar
idioma = st.sidebar.selectbox("Language / Idioma", ["Português", "English", "Español"])
t = traducoes[idioma]

st.sidebar.header(t["sidebar_titulo"])
st.sidebar.write(t["sidebar_texto"])

# Imagem Topo
try:
    imagem = Image.open('Logo-costura-que-cura.jpg')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(imagem, width=300)
except:
    pass

# Título Principal
st.title(t["titulo"])
st.write(t["subtitulo"])

# Inputs das Medidas
col1, col2 = st.columns(2)
with col1:
    o = st.number_input(t["ombro"], min_value=0.0, step=0.5)
    b = st.number_input(t["busto"], min_value=0.0, step=0.5)
with col2:
    c = st.number_input(t["cintura"], min_value=0.0, step=0.5)
    q = st.number_input(t["quadril"], min_value=0.0, step=0.5)

st.write("---")

# --- ÁREA DO FORMULÁRIO ---

# 1. Título "Receba seu resultado"
st.markdown(f"""
    <h3 style="padding-top: 0px; margin-bottom: 0px;">
        📧 Receba seu resultado completo
    </h3>
    """, unsafe_allow_html=True)

# 2. Texto Explicativo
st.write("Para descobrir seu biotipo e receber um guia exclusivo de costura, preencha abaixo:")

# Inputs de Cadastro
col_form1, col_form2 = st.columns(2)
with col_form1:
    nome_usuario = st.text_input("Seu primeiro nome")
with col_form2:
    email_usuario = st.text_input("Seu melhor e-mail")

# --- LGPD (USANDO ST.CAPTION) ---
# Pulamos linhas para dar espaço
st.markdown("<br><br>", unsafe_allow_html=True)

# Usamos st.caption, que é feito para ser pequeno. O CSS lá em cima garante que ele seja VERDE e tamanho 10.
st.caption("""
    🔒 **Seus dados estão seguros.** Ao clicar abaixo, você concorda que usaremos suas medidas apenas para calcular o biotipo 
    e seu e-mail para enviar o resultado e dicas de costura do projeto 'Costura que Cura'. 
    Você pode pedir para sair da lista a qualquer momento.
""")

aceite_lgpd = st.checkbox("Li e concordo com o uso dos meus dados para essa finalidade.")

# --- BOTÃO E LÓGICA ---
if st.button(t["botao"]):
    if not aceite_lgpd:
        st.warning("⚠️ Para prosseguir, você precisa concordar com o tratamento dos dados marcando a caixinha acima.")
    elif not email_usuario or not nome_usuario:
        st.error("Por favor, preencha seu nome e e-mail.")
    elif o > 0 and b > 0 and c > 0 and q > 0:
        
        # Lógica
        chave = identificar_biotipo_chave(o, b, c, q)
        dados = t["biotipos"][chave]
        
        # Salva o Lead
        salvar_lead(email_usuario, nome_usuario, dados['nome'])
        
        # Resultado
        st.success(f"{t['resultado_titulo']} **{dados['nome']}**")
        st.info(f"**{t['dica_titulo']}** {dados['conselho']}")
        
        st.write("---")
        st.write(f"### {t['extra_titulo']}")
        st.write(t["extra_texto"])
        
    else:
        st.warning(t["aviso_preencher"])

# --- RODAPÉ ---
st.write("---")
try:
    imagem_rodape = Image.open('seam-point-logo.jpg') 
    col_r1, col_r2, col_r3 = st.columns([3, 1, 3]) 
    with col_r2:
        st.image(imagem_rodape, width=100) 
except:
    pass