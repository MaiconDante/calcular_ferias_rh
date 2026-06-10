# Importando Bibliotecas
import streamlit as st
from fpdf import FPDF
import locale, time, io, datetime

st.set_page_config(layout="centered", initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    [data-testid="stToolbar"] { 
        display: none !important; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://png.pngtree.com/thumb_back/fh260/background/20210915/pngtree-geometric-line-pattern-white-gold-gradient-minimalist-background-image_879490.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
label,
p,
h1,
h2,
h3,
h4,
h5,
h6,
span {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* TextInput */
div[data-baseweb="input"]{
    border: none !important;
    box-shadow: none !important;
}

/* NumberInput */
div[data-baseweb="base-input"]{
    border: none !important;
    box-shadow: none !important;
}

/* Remove borda ao focar */
div[data-baseweb="input"]:focus-within{
    box-shadow: none !important;
}

div[data-baseweb="base-input"]:focus-within{
    box-shadow: none !important;
}

</style>
""", unsafe_allow_html=True)

date_today = datetime.date.today()
formatted_date = date_today.strftime("%d de %B de %Y")

# Configurando o locale com fallback
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Define o formato para o Brasil
except locale.Error:
    locale.setlocale(locale.LC_ALL, '') # Usa o padrão do sistema se o locale não estiver disponível

# Inicializa a sessão de estado para controle do pop-up
if "popup_open" not in st.session_state:
    st.session_state.popup_open = False

# Funções calcular férias
def days_vacation():
    return 30 - days_monetary

def value_vacation():
    return days_vacation() * salary_day

def one_third_vacation():
    return value_vacation() / 3

def abono_value():
    return days_monetary * salary_day if abono_option == "Sim" else 0.0

def one_third_abono():
    return abono_value() / 3 if abono_option == "Sim" else 0.0

def decimo_value():
    return salary / 2 if decimo_option == "Sim" else 0.0

def calcule_inss():
    value1 = value_vacation()
    value2 = one_third_vacation()
    totalizer = value1 + value2
    range_1 = 0
    range_2 = 0
    range_3 = 0
    if salary <= salary_min:
        range_1 = totalizer * 0.075
        
    elif salary >= salary_min+0.01 and salary <= 2666.68:
        range_1 = (salary_min) * 0.075
        range_2 = (totalizer - salary_min) * 0.09
       
    elif salary >= 2666.69 and salary <= 4000.03:
        range_1 = (salary_min) * 0.075
        range_2 = (totalizer - salary_min) * 0.09
        range_3 = (totalizer - 4000.03) * 0.12
       
    elif salary >= 4000.04:
        range_1 = (salary_min) * 0.075
        range_2 = (totalizer - salary_min) * 0.09
        range_3 = (totalizer- 4000.04) * 0.14
        
    total_inss = range_1 + range_2 + range_3
    return total_inss

# Função para a barra de progresso
def progress_calcule():
    progresso = st.progress(0, text="Aguarde será realizado os cálculos") 
    time.sleep(1) # Inicializa a barra de progresso
    for i in range(1, 11):
        time.sleep(0.2)  # Simula o tempo de processamento (0,2 segundos por etapa)
        progresso.progress(i * 10, text="Realizando processamento de cálculos")  # Atualiza a barra de progresso
    time.sleep(0.5)    
    st.success("Cálculos realizados com SUCESSO")

# Função imprimir recibo férias
def vacation_receipt():
    value_1 = value_vacation()
    value_2 = one_third_vacation()
    value_desconto = calcule_inss()
    value_abono = abono_value()
    value_one_third_abono = one_third_abono()
    value_decimo = decimo_value()
    total_value = value_1 + value_2 + value_abono + value_one_third_abono + value_decimo - value_desconto

    st.info(f"""| RECIBO DE FÉRIAS |
    
    | ---------------------------------------------------------------------|
    | Empresa: {company}           
    | Colaborador: {colaborater}               
    | {days_vacation()} dias de Férias                    
    | Salário R$ {salary}                   
    | Férias R$ {value_1:.2f}                    
    | 1/3 de Férias R$ {value_2:.2f}              
    | Abono Pecuniário R$ {value_abono:.2f}           
    | 1/3 Abono Pecuniário R$ {value_one_third_abono:.2f}       
    | Parcela 1 - Décimo Terceiro R$ {value_decimo:.2f} 
    | Desconto INSS - R$ {value_desconto:.2f}
    | ---------------------------------------------------------------------|
    | TOTAL | R$ {total_value:.2f}
    | ---------------------------------------------------------------------|
    """)

# Função para validar os campos
def click_calcular():
    valid = True

    if company.isdigit() or len(company) < 6:
        st.error("O nome da [EMPRESA] deve conter letras e ter mais de 4 caracteres !!!")
        valid = False
        
    if colaborater.isdigit() or len(colaborater) < 6:
        st.error("O nome do [COLABORADOR] deve conter letras e ter mais de 6 caracteres !!!")
        valid = False
        
    # Validação para o Abono Pecuniário
    if abono_option == "Sim" and days_monetary == 0:
        st.error("Ao selecionar 'Abono Pecuniário: Sim', é obrigatório informar a quantidade de dias!")
        valid = False
    
    return valid

# Função para criar o PDF
def criar_pdf():
    # Criando uma instância da classe FPDF
    pdf = FPDF()

    # Adicionando uma página
    pdf.add_page()

    # Adicionando a imagem de fundo
    pdf.image('./assets/receipt.jpg', 0, 0, 210, 297)  # Para cobrir toda a página A4 (210x297mm)

    # Definindo a fonte para o texto
    pdf.set_font("Arial", "B", 12)

    # Recuperando os valores calculados
    value_1 = value_vacation()
    value_2 = one_third_vacation()
    value_desconto = calcule_inss()
    value_abono = abono_value()
    value_one_third_abono = one_third_abono()
    value_decimo = decimo_value()
    total_value = value_1 + value_2 + value_abono + value_one_third_abono + value_decimo - value_desconto

    # Adicionando texto no PDF
    pdf.ln(49)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(165, 10, f"{formatted_date}", ln=True, align="R")
    pdf.ln(1)
    pdf.set_font("Arial", "B", 17)
    pdf.cell(0, 10, "| RECIBO DE FÉRIAS |", ln=True, align='C')
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Empresa: {company}", ln=True, align="C")
    pdf.cell(0, 10, f"Colaborador: {colaborater}", ln=True, align="C")
    pdf.cell(0, 10, f"{days_vacation()} dias de Férias", ln=True, align="C")
    pdf.cell(0, 10, f"Salário R$ {salary:.2f}", ln=True, align="C")
    pdf.cell(0, 10, f"Férias R$ {value_1:.2f}", ln=True, align="C")
    pdf.cell(0, 10, f"1/3 de Férias R$ {value_2:.2f}", ln=True, align="C")
    pdf.cell(0, 10, f"Abono Pecuniário R$ {value_abono:.2f}", ln=True, align="C")
    pdf.cell(0, 10, f"1/3 Abono Pecuniário R$ {value_one_third_abono:.2f}", ln=True, align="C")
    pdf.cell(0, 10, f"Parcela 1 - Décimo Terceiro R$ {value_decimo:.2f}", ln=True, align="C")
    pdf.cell(0, 10, f"Desconto INSS - R$ {value_desconto:.2f}", ln=True, align="C")
    pdf.ln(25)
    pdf.set_font("Arial", "B", 28)
    pdf.cell(0, 5, f"R$ {total_value:.2f}", ln=True, align='C')

    # Retornando o PDF como bytes
    return pdf

# Caminho para o logotipo e rodapé
image_path = "./assets/rh_logo.jpg"
image_end = "./assets/rodape.png" 

# CSS para centralizar o título
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 40px;  
        font-weight: bold;
        color: black;
    }
    .centered-rodape {
        text-align: center;
        font-size: 12px;  
        font-weight: bold;
        color: darkblue;
    }
    .dados{
    color: black;
    }
    .stNumberInput > {
            color: red !important;
    }
    .stButton > button {
            color: white !important;
            cursor: pointer;
    }
    .stTextInput > label {
        color: black;
    }
    .stRadio > label {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .custom-info {
        background-color: #1e71a8; /* Cor de fundo semelhante ao st.info */
        padding: 10px;
        border-radius: 5px;
        color: white; /* Cor do texto */
        font-weight: bold;
        font-family: "Arial", sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para abrir o sidebar com informações de ajuda
def open_help_sidebar():
    # Estilo CSS para justificar completamente o texto
    st.sidebar.markdown(
        """
        <style>
            .justified-text {
                color: red ;
                text-align: justify;
                text-justify: inter-word;
            }
            .red-text {
            color: red;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.write("---------------------------")
    st.sidebar.markdown('<div class="red-text">Como funciona o sistema?</div>', unsafe_allow_html=True)
    st.sidebar.write("---------------------------")
    st.sidebar.markdown("""
                <div class="justified-text">
                    Sistema web para cálculo de férias, no qual
                    você pode inserir o nome da empresa, o nome
                    do colaborador, o salário mínimo vigente e o
                    salário do funcionário. Com base nessas informações,
                    o sistema calcula automaticamente o valor diário do
                    serviço e exibe o resultado na tela. Após preencher
                    todos os campos corretamente, o usuário terá duas opções:
                    clicar em "Calcular" para visualizar o resultado em um popup
                    no próprio sistema ou selecionar "Gerar PDF" para criar um
                    documento pronto para impressão e visualização.
                </div>
                """,
                unsafe_allow_html=True)

# Criação do container título e logotipo
frame_title = st.container()
with frame_title:
    col1, col2 = st.columns([1, 3]) 
    col1.image(image_path)
    col2.markdown('<div class="centered-title">| Cálculo de Férias RH |</div>', unsafe_allow_html=True)

# Criação do container empresa e colaborador
frame_company = st.container(border=True)
with frame_company:
    col1, col2, col3 = st.columns([3, 5, 5])
    with col1:
        st.markdown('<p class="dados"> Dados a seguir :</p>', unsafe_allow_html=True)
    with col2:
        salary_min = st.number_input("Digite o salário mínimo VIGENTE do ANO: ", min_value=1412.00, format="%.2f", key="salariominimo")
    with col3:
        if st.button("Informações do Sistema   CLIQUE AQUI  "):
            open_help_sidebar()

    company = st.text_input("Empresa :", max_chars=50, placeholder="Digite aqui o nome da empresa!!!", key="empresa")
    colaborater = st.text_input("Colaborador :", max_chars=50, placeholder="Digite aqui o nome do colaborador!!!", key="colaborador")

# Criação do container salário e opções
frame_salary = st.container(border=True)
with frame_salary:
    col1, col2 = st.columns([8, 2])
    with col1:
        salary = st.number_input("Salário:", min_value=0.0, format="%.2f", key="salario", placeholder="0.00", value=None)
        if salary:
            salary_day = salary / 30 if salary > 0 else 0
    with col2:
        if salary:
            st.markdown(
            f"""
            <div class="custom-info">
            Salário/Dia: R$ {salary_day:.2f}
            </div>
            """,
            unsafe_allow_html=True
            )
        else:
            st.markdown(
            """
            <div class="custom-info">
            Salário/Dia: R$ 0,00
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2, col3 = st.columns([2, 3, 3])
    with col1:
        abono_option = st.radio("Abono Pecuniário:", ["Sim", "Não"], key="abono_option")
    with col2:
        decimo_option = st.radio("Adiantamento Décimo:", ["Sim", "Não"], key="decimo_option")
    with col3:
        days_monetary = st.number_input("Dias de Abono:", min_value=0, max_value=10, key="DiasAbono")

# CSS para estilizar o botão
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #89caf5; /* Cor de fundo */
        color: black; /* Cor do texto */
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #1198d6; /* Cor ao passar o mouse */
        color: black; /* Cor do texto */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Criação do container dos botões
frame_buttons = st.container(border=True)
with frame_buttons:
    col1, col2, col3 = st.columns([15, 55, 18])
    with col1:
        calculation = st.button("Calcular", key="calcular")
    with col2:
        if calculation:
            valid = click_calcular()
            if valid:
                progress_calcule()
                st.session_state.popup_open = True  # Definindo o estado como True após o cálculo
    with col3:
         # O botão "Gerar PDF" só aparece se o popup for aberto
        if st.session_state.popup_open:
            generator_pdf = st.button(label="Gerar PDF", key="gerarpdf")
            if generator_pdf:
                # Criar o PDF
                pdf = criar_pdf()
                # Criando um buffer de memória para o PDF
                pdf_buffer = io.BytesIO()
                pdf.output(pdf_buffer)
                pdf_buffer.seek(0)

                # Gerando o download do arquivo PDF
                st.download_button(
                    label="Salvar Recibo",
                    data=pdf_buffer,
                    file_name="Recibo_Férias_Gerado.pdf",
                    mime="application/pdf"
                )

    if st.session_state.popup_open:
        vacation_receipt()
        col1, col2, col3 = st.columns([20, 20, 10])
        with col2:
            st.button("Fechar Pop-up", on_click=lambda: setattr(st.session_state, "popup_open", False), key="fechar")

# Criação do container rodapé
frame_end = st.container(border=True)
with frame_end:
    st.image(image_end)

frame_dev = st.container(border=True)
with frame_end:
    st.markdown('<div class="centered-rodape">Sistema web desenvolvido por Maicon Dante™</div>', unsafe_allow_html=True)