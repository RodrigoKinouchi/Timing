import pandas as pd
import streamlit as st
import plotly.express as px
import re
from PIL import Image
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from pandas.plotting import table


# Configurando o título da página URL
st.set_page_config(
    page_title="AMattheis Timing",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded")

# Carregando uma imagem
image = Image.open('D:\Bkp\Python\ProgramaStock\Capa.png')

# Inserindo a imagem na página utilizando os comandos do stremalit
st.image(image, use_column_width=True)
st.write("<div align='center'><h2><i>AMattheis Timing</i></h2></div>",
         unsafe_allow_html=True)
st.write("")

# Ler arquivo base
# Modo de uso: limpar excel e salvar no caminho abaixo
# Somente necessário trocar o nome do arquivo depois da ultima barra
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")


url = "D:\Bkp\Python\ProgramaStock\SP24_8_P1_LAPS_CSV.csv"
dados = pd.read_csv(url, sep=',').dropna(how='all', axis=1)

if uploaded_file is not None:
    dados = pd.read_csv(uploaded_file).dropna(how='all', axis=1)

# Criando abas de vizualização
tabs = st.tabs(['Laptimes', 'Manufactures', 'Teams'])

# Separar apenas as colunas de interesse
df = dados[['Time of Day', 'Speed', 'Lap',
            'Lap Tm', 'S1 Tm', 'S2 Tm', 'S3 Tm', 'SPT']]

# Criando a coluna Team, Montadora e Numeral no DataFrame df
df['Team'] = None
df['Montadora'] = None
df['Numeral'] = None

# Criando um dicionario onde a chave vai ser o numeral de cada carro, a primeira chave é a equipe e a segunda a montadora
team_info = {
    121: ('Crown', 'Toyota'),
    91: ('Mobil Ale', 'Toyota'),
    4: ('Pole', 'Chevrolet'),
    19: ('TMG Racing', 'Chevrolet'),
    10: ('RCM Motorsport', 'Toyota'),
    44: ('RCM Motorsport', 'Toyota'),
    83: ('AMattheis Vogel', 'Chevrolet'),
    8: ('TMG Racing', 'Chevrolet'),
    29: ('Eurofarma', 'Chevrolet'),
    28: ('Crown', 'Toyota'),
    111: ('Mobil Ale', 'Toyota'),
    21: ('Ipiranga Racing', 'Toyota'),
    90: ('Eurofarma', 'Chevrolet'),
    33: ('Cavaleiro', 'Chevrolet'),
    88: ('Blau', 'Chevrolet'),
    30: ('Ipiranga Racing', 'Toyota'),
    85: ('KTF Racing', 'Chevrolet'),
    11: ('Cavaleiro', 'Chevrolet'),
    51: ('Pole', 'Chevrolet'),
    81: ('Full Time', 'Toyota'),
    12: ('AMattheis Vogel', 'Chevrolet'),
    101: ('Full Time', 'Toyota'),
    0: ('KTF Racing', 'Chevrolet'),
    120: ('Scuderia', 'Toyota'),
    38: ('KTF Racing', 'Chevrolet'),
    18: ('Blau', 'Chevrolet'),
    95: ('Garra', 'Chevrolet'),
    35: ('Garra', 'Chevrolet')
}


current_driver = None

for i, row in df.iterrows():
    if 'Stock' in str(row['Time of Day']):
        # Extrair numeral e nome do piloto
        parts = row['Time of Day'].split(' - ')
        if len(parts) > 1:
            numeral = int(parts[0])  # Extrair numeral
            current_driver_info = team_info.get(
                numeral, (None, None))  # Obter time e montadora

            # Atribuir o time e a montadora na linha do piloto
            df.at[i, 'Numeral'] = numeral
            df.at[i, 'Team'] = current_driver_info[0]
            df.at[i, 'Montadora'] = current_driver_info[1]

    # Preencher as colunas adicionais para as linhas seguintes
    if current_driver_info is not None:
        df.at[i, 'Numeral'] = numeral  # Manter o numeral
        df.at[i, 'Team'] = current_driver_info[0]  # Manter o time
        df.at[i, 'Montadora'] = current_driver_info[1]  # Manter a montadora

# Trocando virgula por ponto e transformando os dados de velocidade de volta em float
df['SPT'] = df['SPT'].str.replace(',', '.').astype(float)

with tabs[0]:
    def convert_time_to_seconds(time_str):
        try:
            hours, minutes, seconds = map(float, time_str.split(':'))
            return hours * 3600 + minutes * 60 + seconds
        except Exception as e:
            print(f"Erro ao converter {time_str}: {e}")
            return None  # Retorna None em caso de erro

    # Inicializar dicionário para armazenar os tempos de volta dos pilotos
    driver_info = {}
    current_driver = None
    driver_row = df['Time of Day'].str.contains('Stock', na=False)

    # Loop para separar os dados por piloto
    for i, row in df.iterrows():
        if driver_row[i]:
            current_driver = row['Time of Day']  # Nome do piloto
            driver_info[current_driver] = []
        elif current_driver:
            lap_time = str(row['Lap Tm']).strip()  # Tempo de volta (Lap Tm)
            # print(f"Verificando tempo de volta: {lap_time}")
            driver_info[current_driver].append(lap_time)

    # Transformar o dicionário em DataFrame
    times_data = []
    for driver, times in driver_info.items():
        for time in times:
            times_data.append({'Piloto': driver, 'Tempo de Volta': time})

    # Criar um DataFrame com os dados
    times_df = pd.DataFrame(times_data)
    times_df['Piloto'] = times_df['Piloto'].str.replace(
        ' - Stock Car PRO 2024', '', regex=False)

    # Aplicar a conversão de Time of Day para segundos
    df['Time in Seconds'] = df['Time of Day'].apply(convert_time_to_seconds)

    # Função para converter tempo de volta para segundos
    def convert_lap_time_to_seconds(time_str):
        try:
            minutes, seconds = time_str.split(':')
            seconds, milliseconds = seconds.split('.')
            return int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
        except Exception as e:
            print(f"Erro ao converter {time_str}: {e}")
            return None  # Retorna None em caso de erro

    # Aplicar a conversão
    times_df['Tempo de Volta em Segundos'] = times_df['Tempo de Volta'].apply(
        convert_lap_time_to_seconds)

    # Remover linhas com tempos de volta inválidos
    times_df.dropna(subset=['Tempo de Volta em Segundos'], inplace=True)
    times_df = times_df[times_df['Tempo de Volta em Segundos'] < 92]

    # Streamlit
    st.title("Análise dos Tempos de Volta")

    # Criar gráfico interativo com largura ajustada
    fig = px.box(times_df, x='Piloto', y='Tempo de Volta em Segundos',
                 title='Dispersão dos Tempos de Volta por Piloto',
                 color='Piloto',
                 labels={
                     'Tempo de Volta em Segundos': 'Tempo de Volta (segundos)', 'Piloto': 'Piloto'})

    # Ajustes de layout adicionais
    fig.update_layout(
        xaxis_tickangle=-45  # Inclinar os rótulos do eixo x
    )

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig)

with tabs[1]:
    # Primeiro, garantir que a coluna 'Lap Tm em Segundos' esteja presente
    df['Lap Tm em Segundos'] = df['Lap Tm'].apply(convert_lap_time_to_seconds)

    # Filtrar os dados para cada montadora
    chevrolet_data = df[df['Montadora'] == 'Chevrolet']
    toyota_data = df[df['Montadora'] == 'Toyota']

    # Calcular a melhor volta de cada montadora
    best_chevrolet_time = chevrolet_data['Lap Tm em Segundos'].min()
    best_toyota_time = toyota_data['Lap Tm em Segundos'].min()

    # Definir o limite de 10% acima da melhor volta
    chevrolet_limit = best_chevrolet_time * 1.05
    toyota_limit = best_toyota_time * 1.05

    # Filtrar os dados para remover outliers
    chevrolet_filtered = chevrolet_data[chevrolet_data['Lap Tm em Segundos']
                                        <= chevrolet_limit]
    toyota_filtered = toyota_data[toyota_data['Lap Tm em Segundos']
                                  <= toyota_limit]

    # Criar um DataFrame combinado com a montadora após filtragem
    chevrolet_filtered['Montadora'] = 'Chevrolet'
    toyota_filtered['Montadora'] = 'Toyota'

    combined_filtered_data = pd.concat([chevrolet_filtered, toyota_filtered])

    # Criar o box plot
    fig3 = px.box(
        combined_filtered_data,
        x='Montadora',
        y='Lap Tm em Segundos',
        title='Laptime',
        color='Montadora',
        color_discrete_map={'Chevrolet': 'yellow', 'Toyota': 'red'},
        labels={'Lap Tm em Segundos': 'Tempo de Volta (segundos)'}
    )

    # Ajustes de layout adicionais
    fig3.update_layout(
        title=dict(text='Laptime', font=dict(size=24), x=0.5,
                   xanchor='center'),  # Centraliza e aumenta o título
        xaxis_title='Montadora',
        yaxis_title='Tempo de volta'
    )

    # Melhor tempo do Setor 1 para cada montadora
    best_chevrolet_s1_time = chevrolet_data['S1 Tm'].min()
    best_toyota_s1_time = toyota_data['S1 Tm'].min()

    # Definir o limite de 10% acima da melhor volta do Setor 1
    chevrolet_s1_limit = best_chevrolet_s1_time * 1.03
    toyota_s1_limit = best_toyota_s1_time * 1.03

    # Filtrar os dados para remover outliers do Setor 1
    chevrolet_filtered_s1 = chevrolet_data[chevrolet_data['S1 Tm']
                                           <= chevrolet_s1_limit]
    toyota_filtered_s1 = toyota_data[toyota_data['S1 Tm'] <= toyota_s1_limit]

    # Criar um DataFrame combinado com a montadora após filtragem
    chevrolet_filtered_s1['Montadora'] = 'Chevrolet'
    toyota_filtered_s1['Montadora'] = 'Toyota'

    combined_filtered_s1_data = pd.concat(
        [chevrolet_filtered_s1, toyota_filtered_s1])

    # Criar o box plot para Setor 1
    fig_s1 = px.box(
        combined_filtered_s1_data,
        x='Montadora',
        y='S1 Tm',
        title='Setor 1',
        color='Montadora',
        color_discrete_map={'Chevrolet': 'yellow', 'Toyota': 'red'},
        labels={'S1 Tm': 'Tempo do Setor 1'}
    )

    # Ajustes de layout adicionais
    fig_s1.update_layout(
        title=dict(text='Setor 1', font=dict(size=24), x=0.5,
                   xanchor='center'),  # Centraliza e aumenta o título
        xaxis_title='Montadora',
        yaxis_title='Tempo do Setor 1'
    )

    # Melhor tempo do Setor 1 para cada montadora
    best_chevrolet_s2_time = chevrolet_data['S2 Tm'].min()
    best_toyota_s2_time = toyota_data['S2 Tm'].min()

    # Definir o limite de 10% acima da melhor volta do Setor 1
    chevrolet_s2_limit = best_chevrolet_s2_time * 1.03
    toyota_s2_limit = best_toyota_s2_time * 1.03

    # Filtrar os dados para remover outliers do Setor 1
    chevrolet_filtered_s2 = chevrolet_data[chevrolet_data['S2 Tm']
                                           <= chevrolet_s2_limit]
    toyota_filtered_s2 = toyota_data[toyota_data['S2 Tm'] <= toyota_s2_limit]

    # Criar um DataFrame combinado com a montadora após filtragem
    chevrolet_filtered_s2['Montadora'] = 'Chevrolet'
    toyota_filtered_s2['Montadora'] = 'Toyota'

    combined_filtered_s2_data = pd.concat(
        [chevrolet_filtered_s2, toyota_filtered_s2])

    # Criar o box plot para Setor 1
    fig_s2 = px.box(
        combined_filtered_s2_data,
        x='Montadora',
        y='S2 Tm',
        title='Setor 2',
        color='Montadora',
        color_discrete_map={'Chevrolet': 'yellow', 'Toyota': 'red'},
        labels={'S2 Tm': 'Tempo do Setor 2'}
    )

    # Ajustes de layout adicionais
    fig_s2.update_layout(
        title=dict(text='Setor 2', font=dict(size=24), x=0.5,
                   xanchor='center'),  # Centraliza e aumenta o título
        xaxis_title='Montadora',
        yaxis_title='Tempo do Setor 2'
    )

    # Melhor tempo do Setor 1 para cada montadora
    best_chevrolet_s3_time = chevrolet_data['S3 Tm'].min()
    best_toyota_s3_time = toyota_data['S3 Tm'].min()

    # Definir o limite de 10% acima da melhor volta do Setor 1
    chevrolet_s3_limit = best_chevrolet_s3_time * 1.03
    toyota_s3_limit = best_toyota_s3_time * 1.03

    # Filtrar os dados para remover outliers do Setor 1
    chevrolet_filtered_s3 = chevrolet_data[chevrolet_data['S3 Tm']
                                           <= chevrolet_s3_limit]
    toyota_filtered_s3 = toyota_data[toyota_data['S3 Tm'] <= toyota_s3_limit]

    # Criar um DataFrame combinado com a montadora após filtragem
    chevrolet_filtered_s3['Montadora'] = 'Chevrolet'
    toyota_filtered_s3['Montadora'] = 'Toyota'

    combined_filtered_s3_data = pd.concat(
        [chevrolet_filtered_s3, toyota_filtered_s3])

    # Criar o box plot para Setor 1
    fig_s3 = px.box(
        combined_filtered_s3_data,
        x='Montadora',
        y='S3 Tm',
        title='Setor 3',
        color='Montadora',
        color_discrete_map={'Chevrolet': 'yellow', 'Toyota': 'red'},
        labels={'S3 Tm': 'Tempo do Setor 3'}
    )

    # Ajustes de layout adicionais
    fig_s3.update_layout(
        title=dict(text='Setor 3', font=dict(size=24), x=0.5,
                   xanchor='center'),  # Centraliza e aumenta o título
        xaxis_title='Montadora',
        yaxis_title='Tempo do Setor 3'
    )

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig_s1)
    st.write('')
    st.plotly_chart(fig_s2)
    st.write('')
    st.plotly_chart(fig_s3)
    st.write('')
    st.plotly_chart(fig3)

with tabs[2]:
    # Primeiro, garantir que a coluna 'Lap Tm em Segundos' esteja presente
    df['Lap Tm em Segundos'] = df['Lap Tm'].apply(convert_lap_time_to_seconds)

    # Criar gráfico interativo com largura ajustada
    fig_t1 = px.box(df, x='Numeral', y='Lap Tm em Segundos',
                    title='Tempos de Volta por Piloto coloridos por time',
                    color='Team',
                    labels={
                        'Tempo de Volta em Segundos': 'Tempo de Volta (segundos)', 'Piloto': 'Piloto'})

    st.plotly_chart(fig_t1)
