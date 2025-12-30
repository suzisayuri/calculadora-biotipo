import streamlit as st
from PIL import Image
import pandas as pd
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Configuração da página
st.set_page_config(page_title="Minha Medida, Meu Estilo", page_icon="🧵")

# 2. CSS (ESTILOS - FIX PARA CELULAR)
st.markdown(
    """
    <style>
    /* --- 1. ESCONDER O CABEÇALHO/RODAPÉ DO STREAMLIT --- */
    footer {visibility: hidden; display: none !important;}
    .stFooter {display: none !important;}
    header {visibility: hidden; display: none !important;}
    #MainMenu {visibility: hidden; display: none !important;}

    /* --- 2. AJUSTES DE ESPAÇAMENTO (MOBILE) --- */
    .block-container {
        padding-top: 1rem !important; 
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* --- 3. CORES E FONTES --- */
    .stApp {background-color: #bdfff8;}

    html, body, p, li, label, .stTextInput label, .stNumberInput label, .stCheckbox label, div[data-testid="stMarkdownContainer"] p {
        font-family: 'Helvetica', sans-serif;
        font-size: 18px; 
        color: #3c857e !important;
    }

    /* Títulos centralizados para ficar bonito no celular */
    h1, h2, h3 {
        color: #E91E63 !important;
        text-align: center !important; 
        padding-top: 0px !important;
    }
    
    /* Legendas */
    .stCaption, div[data-testid="stCaptionContainer"] {
        font-family: 'Helvetica', sans-serif;
        font-size: 12px !important; 
        color: #3c857e !important;
        line-height: 1.2 !important;
        text-align: justify;
    }

    /* --- 4. CENTRALIZAR IMAGENS AUTOMATICAMENTE --- */
    div[data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    div[data-testid="stImage"] > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- FUNÇÕES ---

def salvar_lead(email, nome, biotipo_resultado, genero):
    try:
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        
        if "gsheets" in st.secrets:
            creds_dict = dict(st.secrets["gsheets"])
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
            caminho_arquivo = os.path.join(os.path.dirname(__file__), "credentials.json")
            creds = ServiceAccountCredentials.from_json_keyfile_name(caminho_arquivo, scope)
        
        client = gspread.authorize(creds)
        sheet = client.open("Leads Costura que Cura").sheet1 
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([data_hora, nome, email, biotipo_resultado, genero])
        return True
    except Exception as e:
        # Em produção, você pode querer silenciar o erro visualmente ou logar
        return False

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

# Dicionário de Traduções (Mantido o Persuasivo)
traducoes = {
    "Português": {
        "titulo": "🧵 Descubra seu Biotipo Real",
        "subtitulo": "Chega de culpar seu corpo porque a roupa não serve. Descubra a matemática das suas curvas.",
        "ombro": "Medida do Ombro (cm)",
        "busto": "Medida do Busto/Tórax (cm)",
        "cintura": "Medida da Cintura (cm)",
        "quadril": "Medida do Quadril (cm)",
        "botao": "Revelar meu Biotipo 🚀",
        "aviso_preencher": "Preencha tudo para uma análise precisa.",
        "resultado_titulo": "A verdade sobre seu corpo:",
        "dica_titulo": "Por que as roupas não te servem:",
        "extra_titulo": "Cansada de se sentir errada no provador?",
        "extra_texto": "O problema não é você, é o padrão industrial. No curso 'Costura que Cura', eu te entrego o método para ajustar qualquer peça ao SEU corpo, não o contrário.",
        "botao_compra": "👉 QUERO APRENDER A AJUSTAR MINHAS ROUPAS AGORA",
        "biotipos": {
            "Ampulheta": {"nome": "Ampulheta", "conselho": "Cintura fina e curvas acentuadas. O drama: calça que serve no quadril fica um saco na cintura. Pare de usar cintos feios! No curso, te ensino o 'Ajuste Invisível'."},
            "Pera": {"nome": "Pera / Triângulo", "conselho": "Quadril poderoso. Você vive comprando roupa maior para passar na coxa e manda apertar tudo em cima? Chega de gambiarras. Aprenda a remodelar a peça."},
            "Triangulo": {"nome": "Triângulo Invertido", "conselho": "Presença marcante nos ombros. Camisas travam nas costas e sobram no quadril? Não aceite isso. No curso, revelo como aliviar a tensão superior e equilibrar o visual."},
            "Oval": {"nome": "Oval", "conselho": "Volume centralizado. A indústria te obriga a usar 'sacos'? Recuse. O segredo é o conforto com estrutura. Te ensino a soltar a roupa nos pontos certos."},
            "Retangulo": {"nome": "Retângulo", "conselho": "Linhas retas. Roupas comuns te deixam sem forma? A costura é sua mágica. Aprenda a criar curvas visuais com pences estratégicas."}
        }
    },
    "English": {
        "titulo": "🧵 Discover Your True Body Type",
        "subtitulo": "Stop blaming your body. Understand your curves' math and take control of your style today.",
        "ombro": "Shoulder Measurement (cm)",
        "busto": "Chest/Bust Measurement (cm)",
        "cintura": "Waist Measurement (cm)",
        "quadril": "Hip Measurement (cm)",
        "botao": "Reveal My Body Type 🚀",
        "aviso_preencher": "Fill in all fields for accurate analysis.",
        "resultado_titulo": "The truth about your body:",
        "dica_titulo": "Why clothes don't fit you:",
        "extra_titulo": "Tired of fitting rooms?",
        "extra_texto": "The problem isn't you, it's the industry standard. In the 'Costura que Cura' course, I give you the method to make any garment fit YOUR body.",
        "botao_compra": "👉 I WANT TO MASTER SEWING NOW",
        "biotipos": {
            "Ampulheta": {"nome": "Hourglass", "conselho": "Small waist, curvy hips. Pants fit hips but gap at the waist? I teach the 'Invisible Adjustment' to honor your silhouette."},
            "Pera": {"nome": "Pear / Triangle", "conselho": "Powerful hips. Buying bigger sizes for thighs leaving the top baggy? Learn to reshape the garment to respect your strong base."},
            "Triangulo": {"nome": "Inverted Triangle", "conselho": "Strong shoulders. Shirts pull at the back? Don't settle. I'll show you how to release upper tension and balance your look."},
            "Oval": {"nome": "Apple (Oval)", "conselho": "Central volume. Forced into 'sacks'? The secret is comfort with structure. I teach where to loosen the fit so you can breathe."},
            "Retangulo": {"nome": "Rectangle", "conselho": "Straight lines. Standard clothes look boxy? Sewing is magic. Learn to create visual curves with strategic darts."}
        }
    },
    "Español": {
        "titulo": "🧵 Descubre tu Biotipo Real",
        "subtitulo": "Basta de culpar a tu cuerpo. Entiende la matemática de tus curvas y toma el control.",
        "ombro": "Medida de Hombros (cm)",
        "busto": "Medida de Pecho/Busto (cm)",
        "cintura": "Medida de Cintura (cm)",
        "quadril": "Medida de Cadera (cm)",
        "botao": "Revelar mi Biotipo 🚀",
        "aviso_preencher": "Completa todo para un análisis preciso.",
        "resultado_titulo": "La verdad sobre tu cuerpo:",
        "dica_titulo": "Por qué la ropa no te queda:",
        "extra_titulo": "¿Cansada del probador?",
        "extra_texto": "El problema no eres tú, es el estándar industrial. En el curso 'Costura que Cura', te doy el método para ajustar cualquier prenda a TU cuerpo.",
        "botao_compra": "👉 QUIERO APRENDER A AJUSTAR MI ROPA AHORA",
        "biotipos": {
            "Ampulheta": {"nome": "Reloj de Arena", "conselho": "Cintura fina y curvas. ¿El pantalón sobra en la cintura? En el curso, te enseño el 'Ajuste Invisible' para valorar tu silueta."},
            "Pera": {"nome": "Pera / Triángulo", "conselho": "Caderas poderosas. ¿Compras tallas grandes para los muslos y sobra arriba? Aprende a remodelar la prenda para respetar tu base."},
            "Triangulo": {"nome": "Triángulo Invertido", "conselho": "Hombros marcados. ¿Las camisas tiran en la espalda? En el curso, revelo cómo aliviar la tensión superior y equilibrar tu look."},
            "Oval": {"nome": "Óvalo", "conselho": "Volumen central. ¿Te obligan a usar 'sacos'? El secreto es confort. Te enseño a soltar la ropa en los puntos justos."},
            "Retangulo": {"nome": "Rectángulo", "conselho": "Líneas rectas. ¿La ropa te deja 'cuadrada'? La costura es magia. Aprende a crear curvas visuales con pinzas estratégicas."}
        }
    }
}

# --- INÍCIO DO APP ---

# 1. SELETOR DE IDIOMA NO TOPO (MUDANÇA CRÍTICA PARA CELULAR)
# Usamos colunas para deixar pequeno no canto, ou centralizado
col_lang1, col_lang2, col_lang3 = st.columns([1, 2, 1])
with col_lang2:
    idioma = st.selectbox("🌎 Language / Idioma", ["Português", "English", "Español"], label_visibility="collapsed")

t = traducoes[idioma]

# 2. LOGO CENTRALIZADA (SEM COLUNAS = SEM ERRO NO CELULAR)
try:
    imagem = Image.open('Logo-costura-que-cura.jpg')
    # O CSS já vai centralizar isso automaticamente
    st.image(imagem, width=280) 
except:
    pass

# Título Principal
st.title(t["titulo"])
st.write(f"<div style='text-align: center'>{t['subtitulo']}</div>", unsafe_allow_html=True)
st.write("---")

# Inputs das Medidas
col1, col2 = st.columns(2)

with col1:
    # Adicionei value=None e placeholder="0.00"
    o_input = st.number_input(t["ombro"], min_value=0.0, step=0.5, value=None, placeholder="0.00")
    b_input = st.number_input(t["busto"], min_value=0.0, step=0.5, value=None, placeholder="0.00")

with col2:
    c_input = st.number_input(t["cintura"], min_value=0.0, step=0.5, value=None, placeholder="0.00")
    q_input = st.number_input(t["quadril"], min_value=0.0, step=0.5, value=None, placeholder="0.00")

st.write("---")

# --- TRATAMENTO DE DADOS ---
# Como iniciamos com None (vazio), precisamos converter para 0.0 se a pessoa não digitar nada
# para não dar erro de cálculo lá na frente.
o = o_input if o_input is not None else 0.0
b = b_input if b_input is not None else 0.0
c = c_input if c_input is not None else 0.0
q = q_input if q_input is not None else 0.0

# --- ÁREA DO FORMULÁRIO ---
st.markdown(f"""
    <h3 style="padding-top: 0px; margin-bottom: 0px; text-align: center;">
        📧 Receba seu resultado completo
    </h3>
    """, unsafe_allow_html=True)

# Inputs de Cadastro
nome_usuario = st.text_input("Seu primeiro nome")
email_usuario = st.text_input("Seu melhor e-mail")
genero_usuario = st.selectbox("Gênero", ["Feminino", "Masculino", "Outro"])

# --- LGPD ---
st.markdown("<br>", unsafe_allow_html=True)
aceite_lgpd = st.checkbox("✅ Li e concordo com o uso dos meus dados para receber o resultado e dicas.")

# --- BOTÃO E LÓGICA ---
# Vamos centralizar o botão de ação também
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    botao_clicado = st.button(t["botao"], use_container_width=True)

if botao_clicado:
    if not aceite_lgpd:
        st.warning("⚠️ Marque a caixinha de concordância para ver o resultado.")
    elif not email_usuario or not nome_usuario:
        st.error("⚠️ Preencha seu nome e e-mail.")
    elif o > 0 and b > 0 and c > 0 and q > 0:
        
        # 1. Calcula
        chave = identificar_biotipo_chave(o, b, c, q)
        dados = t["biotipos"][chave]
        
        # 2. Salva
        salvar_lead(email_usuario, nome_usuario, dados['nome'], genero_usuario)
        
        # 3. Mostra o Resultado
        st.markdown(f"<h2 style='text-align: center; color: #E91E63'>{t['resultado_titulo']} <br>{dados['nome']}</h2>", unsafe_allow_html=True)
        st.info(f"**{t['dica_titulo']}** {dados['conselho']}")
        
        st.write("---")
        st.markdown(f"<h3 style='text-align: center'>{t['extra_titulo']}</h3>", unsafe_allow_html=True)
        st.write(t["extra_texto"])
        
        # --- BOTÃO DE COMPRA ---
        link_compra = "https://SEU_LINK_DE_COMPRA_AQUI.com"
        
        st.markdown(f"""
            <a href="{link_compra}" target="_blank" style="text-decoration: none;">
                <div style="
                    background-color: #E91E63; 
                    color: white; 
                    padding: 15px; 
                    border-radius: 30px; 
                    text-align: center; 
                    font-weight: bold; 
                    font-size: 18px; 
                    margin-top: 20px; 
                    margin-bottom: 20px; 
                    box-shadow: 0px 4px 15px rgba(233, 30, 99, 0.4);
                ">
                    {t['botao_compra']}
                </div>
            </a>
            """, unsafe_allow_html=True)
        
    else:
        st.warning(t["aviso_preencher"])

# --- RODAPÉ ---
st.write("---")
try:
    imagem_rodape = Image.open('logo-seampoint.jpg') 
    st.image(imagem_rodape, width=100) # CSS vai centralizar automático
except:
    pass