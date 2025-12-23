import streamlit as st

# Configuração da página
st.set_page_config(page_title="Minha Medida, Meu Estilo", page_icon="🧵")

def identificar_biotipo(ombro, busto, cintura, quadril):
    superior = max(ombro, busto)
    
    # Lógica de classificação
    if (0.95 <= superior / quadril <= 1.05) and (cintura <= superior * 0.75):
        return "Ampulheta", "O equilíbrio perfeito! Na costura, valorize sua cintura com pences e evite esconder suas formas em roupas muito largas."
    elif quadril > (superior * 1.05):
        return "Pera", "Seu quadril é sua força. Use a costura para criar golas trabalhadas, babados ou mangas bufantes que equilibram o visual."
    elif superior > (quadril * 1.05):
        return "Triângulo Invertido", "Ombros marcantes pedem saias com volume, bolsos laterais e tecidos encorpados na parte de baixo. Crie o equilíbrio você mesma!"
    elif cintura >= superior and cintura >= quadril:
        return "Oval", "Conforto é a palavra-chave. Aposte em linhas verticais, decotes em V e tecidos com bom caimento que não marcam, mas valorizam seu colo."
    else:
        return "Retângulo", "Sua silhueta é moderna. Use a costura para 'inventar' curvas com cintos do próprio tecido, recortes laterais e pences estratégicas."

# Interface do Usuário
st.title("🧵 Descubra seu Biotipo e Liberte sua Costura")
st.write("O primeiro passo para parar de brigar com o provador e começar a criar roupas que te amam.")

col1, col2 = st.columns(2)

with col1:
    o = st.number_input("Medida do Ombro (cm)", min_value=1.0, step=0.5)
    b = st.number_input("Medida do Busto (cm)", min_value=1.0, step=0.5)

with col2:
    c = st.number_input("Medida da Cintura (cm)", min_value=1.0, step=0.5)
    q = st.number_input("Medida do Quadril (cm)", min_value=1.0, step=0.5)

if st.button("Descobrir meu Biotipo ✨"):
    if o and b and c and q:
        resultado, conselho = identificar_biotipo(o, b, c, q)
        
        st.success(f"Seu biotipo é: **{resultado}**")
        
        # Exibindo o guia visual para o usuário
        st.info(f"**Dica de Costura para você:** {conselho}")
        
        st.write("---")
        st.write("### Por onde começar do zero?")
        st.write("Agora que você conhece seu corpo, que tal aprender a costurar sua primeira peça pensada exatamente para essas medidas?")
    else:
        st.warning("Por favor, preencha todas as medidas para o cálculo.")

st.sidebar.header("Sobre o Projeto")
st.sidebar.write("A costura não é apenas técnica, é uma ferramenta de autoestima. Ao entender suas medidas, você para de tentar caber no padrão e faz o padrão caber em você.")