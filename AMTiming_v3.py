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
image = Image.open(
    'images/Capa.png')

# Inserindo a imagem na página utilizando os comandos do stremalit
st.image(image, use_column_width=True)
st.write("<div align='center'><h2><i>AMattheis Timing</i></h2></div>",
         unsafe_allow_html=True)
st.write("")

# Ler arquivo base
# Modo de uso: limpar excel e salvar no caminho abaixo
# Somente necessário trocar o nome do arquivo depois da ultima barra
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")


url = "SP24_8_P1_LAPS_CSV.csv"
dados = pd.read_csv(url, sep=',')  # .dropna(how='all', axis=1)

if uploaded_file is not None:
    dados = pd.read_csv(uploaded_file)  # .dropna(how='all', axis=1)

# Criando abas de vizualização
tabs = st.tabs(['Laptimes', 'Manufactures', 'Teams',
               'Speed x GAP', 'GAP Analysis', 'Ranking by lap'])

# Separar apenas as colunas de interesse
df = dados[['Time of Day', 'Speed', 'Lap',
            'Lap Tm', 'S1 Tm', 'S2 Tm', 'S3 Tm', 'SPT']]

df['SPT'] = df['SPT'].astype(str)
df['SPT'] = df['SPT'].fillna(1)
# df['SPT'] = df['SPT'].fillna('').astype(str)  # Preenche NaN com strings vazias


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
    0: ('KTF Sports', 'Chevrolet'),
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


def convert_time_to_seconds(time_str):
    try:
        if ':' in time_str:
            # Formato mm:ss.000
            minutes, seconds = time_str.split(':')
            seconds, milliseconds = seconds.split('.')
            return int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000
        else:
            # Formato ss.000
            seconds, milliseconds = time_str.split('.')
            return int(seconds) + int(milliseconds) / 1000
    except Exception as e:
        # print(f"Erro ao converter {time_str}: {e}")
        return None  # Retorna None em caso de erro


# Aplicar a conversão de Time of Day para segundos
df['Time in Seconds'] = df['Lap Tm'].apply(convert_time_to_seconds)

# Inicializar dicionário para armazenar os tempos de volta dos pilotos
driver_info = {}
current_driver = None
driver_row = df['Time of Day'].str.contains('Stock', na=False)

# Loop para separar os dados por piloto
for i, row in df.iterrows():
    if driver_row[i]:
        current_driver = row['Time of Day']  # Nome do piloto
        team = row['Team']  # Obter a equipe do piloto
        driver_info[current_driver] = {'Team': team, 'Times': []}
    elif current_driver:
        lap_time = str(row['Lap Tm']).strip()  # Tempo de volta (Lap Tm)
        driver_info[current_driver]['Times'].append(lap_time)

# Transformar o dicionário em DataFrame
times_data = []
for driver, info in driver_info.items():
    for time in info['Times']:
        times_data.append(
            {'Piloto': driver, 'Tempo de Volta': time, 'Team': info['Team']})

# Criar um DataFrame com os dados
times_df = pd.DataFrame(times_data)
times_df['Piloto'] = times_df['Piloto'].str.replace(
    ' - Stock Car PRO 2024', '', regex=False)

# Aplicar a conversão
times_df['Tempo de Volta em Segundos'] = times_df['Tempo de Volta'].apply(
    convert_time_to_seconds)

# Remover linhas com tempos de volta inválidos
times_df.dropna(subset=['Tempo de Volta em Segundos'], inplace=True)
best_time = times_df['Tempo de Volta em Segundos'].min()
times_df_limit = best_time * 1.04
times_df = times_df[times_df['Tempo de Volta em Segundos'] < times_df_limit]


# Função para filtrar dados com base no limite e montadora
def filter_data_by_montadora(df, montadora, time_column, limit_factor=1.02):
    data = df[df['Montadora'] == montadora]
    best_time = data[time_column].min()
    limit = best_time * limit_factor
    filtered_data = data[data[time_column] <= limit]
    return filtered_data

# Função para criar o box plot


def create_box_plot(df, x_column, y_column, title, color_map):
    fig = px.box(df, x=x_column, y=y_column, title=title, color=x_column,
                 color_discrete_map=color_map, labels={y_column: title})
    fig.update_layout(title=dict(text=title, font=dict(size=24), x=0.5, xanchor='center'),
                      xaxis_title='Montadora', yaxis_title=title)
    return fig


with tabs[0]:
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
        xaxis_tickangle=-45
    )

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig)

with tabs[1]:

    df['S1 Tm'] = pd.to_numeric(df['S1 Tm'], errors='coerce')
    df['S2 Tm'] = pd.to_numeric(df['S2 Tm'], errors='coerce')
    df['S3 Tm'] = pd.to_numeric(df['S3 Tm'], errors='coerce')

    # Solicitar ao usuário para selecionar o fator de limite
    limit_factor = st.slider(
        'Selecione o fator de limite', 1.01, 1.05, 1.01, 0.01)

    # Garantir que os dados sejam numéricos (após a leitura)
    df['S1 Tm'] = pd.to_numeric(df['S1 Tm'], errors='coerce')
    df['S2 Tm'] = pd.to_numeric(df['S2 Tm'], errors='coerce')
    df['S3 Tm'] = pd.to_numeric(df['S3 Tm'], errors='coerce')

    # Filtrar dados de cada montadora com o limit_factor definido pelo usuário
    chevrolet_filtered = filter_data_by_montadora(
        df, 'Chevrolet', 'Time in Seconds', limit_factor)
    toyota_filtered = filter_data_by_montadora(
        df, 'Toyota', 'Time in Seconds', limit_factor)

    # Criar o box plot para os tempos de volta
    combined_filtered_data = pd.concat([chevrolet_filtered, toyota_filtered])
    fig_laptime = create_box_plot(combined_filtered_data, 'Montadora', 'Time in Seconds', 'Laptime',
                                  {'Chevrolet': 'yellow', 'Toyota': 'red'})

    # Filtrar dados para o Setor 1 com o limit_factor
    chevrolet_filtered_s1 = filter_data_by_montadora(
        df, 'Chevrolet', 'S1 Tm', limit_factor)
    toyota_filtered_s1 = filter_data_by_montadora(
        df, 'Toyota', 'S1 Tm', limit_factor)
    combined_filtered_s1_data = pd.concat(
        [chevrolet_filtered_s1, toyota_filtered_s1])
    fig_s1 = create_box_plot(combined_filtered_s1_data, 'Montadora', 'S1 Tm', 'Setor 1',
                             {'Chevrolet': 'yellow', 'Toyota': 'red'})

    # Filtrar dados para o Setor 2 com o limit_factor
    chevrolet_filtered_s2 = filter_data_by_montadora(
        df, 'Chevrolet', 'S2 Tm', limit_factor)
    toyota_filtered_s2 = filter_data_by_montadora(
        df, 'Toyota', 'S2 Tm', limit_factor)
    combined_filtered_s2_data = pd.concat(
        [chevrolet_filtered_s2, toyota_filtered_s2])
    fig_s2 = create_box_plot(combined_filtered_s2_data, 'Montadora', 'S2 Tm', 'Setor 2',
                             {'Chevrolet': 'yellow', 'Toyota': 'red'})

    # Filtrar dados para o Setor 3 com o limit_factor
    chevrolet_filtered_s3 = filter_data_by_montadora(
        df, 'Chevrolet', 'S3 Tm', limit_factor)
    toyota_filtered_s3 = filter_data_by_montadora(
        df, 'Toyota', 'S3 Tm', limit_factor)
    combined_filtered_s3_data = pd.concat(
        [chevrolet_filtered_s3, toyota_filtered_s3])
    fig_s3 = create_box_plot(combined_filtered_s3_data, 'Montadora', 'S3 Tm', 'Setor 3',
                             {'Chevrolet': 'yellow', 'Toyota': 'red'})

    # Exibir gráficos no Streamlit
    st.plotly_chart(fig_s1)
    st.write('')
    st.plotly_chart(fig_s2)
    st.write('')
    st.plotly_chart(fig_s3)
    st.write('')
    st.plotly_chart(fig_laptime)


with tabs[2]:
    # Criar um DataFrame para os tempos de volta e setores
    times_data = []
    for team in df['Team'].unique():
        team_data = df[df['Team'] == team]

        # Adiciona os dados de tempo de volta
        for _, row in team_data.iterrows():
            times_data.append(
                {'Team': team, 'Value': row['Time in Seconds'], 'Type': 'Tempo de Volta'})
            times_data.append(
                {'Team': team, 'Value': row['S1 Tm'], 'Type': 'Setor 1'})
            times_data.append(
                {'Team': team, 'Value': row['S2 Tm'], 'Type': 'Setor 2'})
            times_data.append(
                {'Team': team, 'Value': row['S3 Tm'], 'Type': 'Setor 3'})

    # Criar um DataFrame com os dados acumulados
    times_df_teams = pd.DataFrame(times_data)

    # Conversão da coluna 'Value' para numérico
    times_df_teams['Value'] = pd.to_numeric(
        times_df_teams['Value'], errors='coerce')

    # Remover NaNs
    times_df_teams = times_df_teams.dropna()

    # Gráficos para Tempo de Volta e Setores
    types = ['Tempo de Volta', 'Setor 1', 'Setor 2', 'Setor 3']

    for type_name in types:
        # Calcular o melhor tempo para o tipo atual
        best_time = times_df_teams[times_df_teams['Type']
                                   == type_name]['Value'].min()
        limit = best_time * 1.02  # 5% acima do melhor tempo

        # Filtrar os dados para não incluir outliers
        filtered_data = times_df_teams[(times_df_teams['Type'] == type_name) &
                                       (times_df_teams['Value'] <= limit)]

        fig_teams = px.box(
            filtered_data,
            x='Team',
            y='Value',
            title=f'Comparação de {
                type_name} por Equipe (até 5% acima do melhor tempo)',
            labels={'Value': 'Tempo (segundos)', 'Team': 'Equipe'},
            color='Team',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )

        # Ajustes de layout
        fig_teams.update_layout(
            title=dict(text=f'Comparação de {type_name} por Equipe', font=dict(
                size=24), x=0.5, xanchor='center'),
            xaxis_title='Equipe',
            yaxis_title='Tempo (segundos)',
        )

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig_teams)

    # Criar gráfico interativo com largura ajustada para tempos de volta dos pilotos
    fig_t1 = px.box(times_df, x='Piloto', y='Tempo de Volta em Segundos',
                    color='Team',
                    title='Tempos de volta dos pilotos por equipe',
                    labels={'Tempo de Volta em Segundos': 'Tempo de Volta (segundos)', 'Piloto': 'Piloto'})

    # Ajustes de layout adicionais
    fig_t1.update_layout(
        xaxis_tickangle=-45,  # Inclinar os rótulos do eixo x
        title=dict(text='Tempo de volta dos pilotos por equipe',
                   font=dict(size=24), x=0.5, xanchor='center'),
    )

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig_t1)

with tabs[3]:
    results = []
    current_pilot = None

    for index, row in df.iterrows():  # Usando iterrows() para acessar as linhas
        if "Stock" in row[0]:  # Se for o nome do piloto (coluna 0)
            current_pilot = row[0]
        elif isinstance(row[0], str) and ':' in row[0]:  # Verifica se é um tempo
            time = pd.to_timedelta(row[0])
            spt = row[7]  # Acessar a coluna SPT (índice 17)
            results.append((current_pilot, time, spt))

    cleaned_df = pd.DataFrame(
        results, columns=['Piloto', 'Time of Day', 'SPT'])
    cleaned_df = cleaned_df.sort_values(
        by='Time of Day').reset_index(drop=True)
    cleaned_df['Piloto'] = cleaned_df['Piloto'].str.replace(
        ' - Stock Car PRO 2024', '', regex=False)
    # GAP para cada carro em relação ao anterior
    cleaned_df['GAP'] = cleaned_df['Time of Day'].diff().dt.total_seconds()
    # Preencher o primeiro GAP como 0
    cleaned_df['GAP'].fillna(0, inplace=True)
    # Selecionar o piloto para análise
    pilotos = cleaned_df['Piloto'].unique().tolist()
    pilotos.insert(0, "")  # Adiciona uma opção vazia no início
    selected_pilot = st.selectbox('Selecione um piloto:', pilotos)
   # Filtrar apenas os dados do piloto selecionado se houver seleção
    if selected_pilot:
        pilot_data = cleaned_df[cleaned_df['Piloto'] == selected_pilot]

        # Filtrar para SPT acima de 200
        filtered_data = pilot_data[(
            pilot_data['SPT'] > 200)]

        # Criar o gráfico interativo usando Plotly
        fig = px.scatter(
            filtered_data,
            x='GAP',
            y='SPT',
            title=f'GAP vs Velocidade (SPT) > 200 km/h para {selected_pilot}',
            labels={'GAP': 'GAP (s)', 'SPT': 'Velocidade (SPT) (km/h)'},
        )

        # Personalizar o layout
        fig.update_traces(marker=dict(size=10, opacity=0.7,
                          line=dict(width=1, color='DarkSlateGrey')))
        fig.update_layout(title_x=0.3)  # Centralizar o título

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
    else:
        st.warning('Por favor, selecione um piloto.')

with tabs[4]:
    results = []
    current_pilot = None

    # Processando os dados como antes
    for index, row in df.iterrows():
        if "Stock" in row[0]:  # Se for o nome do piloto (coluna 0)
            current_pilot = row[0]
        elif isinstance(row[0], str) and ':' in row[0]:  # Verifica se é um tempo
            time = pd.to_timedelta(row[0])
            results.append((current_pilot, time))

    # Cria o DataFrame de resultados
    cleaned_df = pd.DataFrame(
        results, columns=['Piloto', 'Time of Day'])
    cleaned_df = cleaned_df.sort_values(
        by='Time of Day').reset_index(drop=True)

    # Atribuir as voltas (Lap) corretamente, assumindo que as voltas começam de 1
    cleaned_df['Lap'] = cleaned_df.groupby('Piloto').cumcount() + 1
    cleaned_df['Piloto'] = cleaned_df['Piloto'].str.replace(
        ' - Stock Car PRO 2024', '', regex=False)

    # Selecionar o piloto para análise
    pilotos = cleaned_df['Piloto'].unique().tolist()
    pilotos.insert(0, "")  # Adiciona uma opção vazia no início

    # Seleciona o piloto de referência
    reference_pilot = st.selectbox(
        'Selecione o piloto de referência:', pilotos)

    if reference_pilot:
        # Filtra os dados para o piloto de referência
        reference_times = cleaned_df[cleaned_df['Piloto']
                                     == reference_pilot]

        # Verifica se o piloto de referência possui dados suficientes
        if not reference_times.empty:
            # Cria um dicionário de tempos para o piloto de referência com 'Lap' como chave
            reference_time_dict = reference_times.set_index(
                'Lap')['Time of Day'].to_dict()

            # Calcula o GAP em relação ao piloto de referência para todos os pilotos
            cleaned_df['Reference Time'] = cleaned_df['Lap'].map(
                reference_time_dict)
            cleaned_df['GAP to Reference'] = (
                cleaned_df['Time of Day'] - cleaned_df['Reference Time']).dt.total_seconds()

            # Agora, podemos agrupar os dados por piloto e plotar os GAPs ao longo das voltas
            fig = px.line(
                cleaned_df,
                x='Lap',
                y='GAP to Reference',
                color='Piloto',
                title=f'GAP em Relação ao Piloto {
                    reference_pilot}',
                labels={'Lap': 'Volta', 'GAP to Reference': 'GAP (s)'},
                markers=True)

            # Personalizar o gráfico
            fig.update_layout(title_x=0.5)  # Centralizar o título
            fig.update_traces(mode='lines+markers',
                              marker=dict(size=6, opacity=0.7))

            # Exibir o gráfico no Streamlit
            st.plotly_chart(fig)
        else:
            st.warning(
                f'O piloto {reference_pilot} não possui dados suficientes para análise.')
    else:
        st.warning('Por favor, selecione um piloto de referência.')

with tabs[5]:
    results = []
    current_driver = None  # Vai armazenar o nome do piloto atual
    driver_row = df['Time of Day'].str.contains('Stock', na=False)

    # Iterar sobre as linhas do DataFrame
    for i, row in df.iterrows():
        time_of_day = row['Time of Day']

        # Verifique se o 'Time of Day' contém o nome do piloto
        # Verifica se é o nome do piloto
        if isinstance(time_of_day, str) and 'Stock' in time_of_day:
            current_driver = time_of_day  # Atualiza o piloto atual
        elif current_driver:  # Se um piloto estiver definido, significa que estamos na volta dele
            lap_time = row['Time in Seconds']  # Tempo da volta
            lap_number = row['Lap']  # Número da volta

            # Adicionar o resultado (piloto, tempo em segundos e número da volta)
            results.append((current_driver, lap_time, lap_number))

    # Agora criamos um DataFrame com os resultados
    cleaned_df = pd.DataFrame(
        results, columns=['Piloto', 'Time in Seconds', 'Lap'])

    # Ordenar pelo 'Piloto' e 'Lap' para garantir a ordem correta das voltas
    cleaned_df = cleaned_df.sort_values(
        by=['Piloto', 'Lap']).reset_index(drop=True)

    # Remover a string "- Stock Car PRO 2024" dos nomes dos pilotos
    cleaned_df['Piloto'] = cleaned_df['Piloto'].str.replace(
        ' - Stock Car PRO 2024', '', regex=False)

    # Função para gerar o ranking por volta

    def generate_ranking_by_lap(df):
        rankings = []
        for lap in df['Lap'].unique():
            lap_data = df[df['Lap'] == lap]
            lap_data_sorted = lap_data.sort_values(by='Time in Seconds')
            lap_data_sorted['Rank'] = range(1, len(lap_data_sorted) + 1)
            rankings.append(
                lap_data_sorted[['Piloto', 'Time in Seconds', 'Lap', 'Rank']])

        rankings_df = pd.concat(rankings, ignore_index=True)
        rankings_df = rankings_df.sort_values(
            by=['Lap', 'Rank']).reset_index(drop=True)
        return rankings_df

    # Gerar o ranking por volta
    ranked_df = generate_ranking_by_lap(cleaned_df)

    # Streamlit - selecionar o ranking para visualizar
    st.title("Ranking por Volta")

    # Dropdown para selecionar a volta
    selected_lap = st.slider('Selecione a volta:', min_value=int(
        ranked_df['Lap'].min()), max_value=int(ranked_df['Lap'].max()))

    # Filtrar os dados para a volta selecionada
    lap_data = ranked_df[ranked_df['Lap'] == selected_lap]

    # Identificar pilotos do time
    team_pilots = ['21 - Thiago Camilo', '30 - Cesar Ramos']

    # Vamos grifar os pilotos do time no gráfico
    lap_data['Destaque'] = lap_data['Piloto'].apply(
        lambda x: 'Time' if x in team_pilots else 'Outro')

    # Encontrar o melhor tempo de volta (tempo mínimo) para ajustar a escala
    best_time = lap_data['Time in Seconds'].min()

    # Definir o valor mínimo do eixo Y como 0.98% do melhor tempo
    min_y_value = best_time * 0.98

    # Gerar um gráfico de barras
    fig = px.bar(
        lap_data,
        x='Piloto',
        y='Time in Seconds',
        title=f'Ranking por Volta {selected_lap}',
        labels={'Piloto': 'Piloto', 'Time in Seconds': 'Tempo de Volta (s)'},
        text='Rank',  # Mostrar a posição do piloto na barra
    )

    # Customização para destacar os nomes
    fig.update_traces(
        texttemplate='%{text}',  # Exibe o ranking dentro da barra
        textposition='outside',  # Coloca o texto fora da barra
        marker=dict(
            color=lap_data['Destaque'].apply(
                # Cor para destacar
                lambda x: 'rgba(31, 119, 180, 0.7)' if x == 'Outro' else 'rgba(255, 0, 0, 0.7)')
        )
    )

    # Destacar os nomes dos pilotos do time em negrito
    for i in range(len(lap_data)):
        if lap_data.iloc[i]['Destaque'] == 'Time':  # Se for um piloto do time
            fig.add_annotation(
                x=lap_data.iloc[i]['Piloto'],
                y=lap_data.iloc[i]['Time in Seconds'],
                text=lap_data.iloc[i]['Piloto'],
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                ax=0,
                ay=-30,
                # Destaque em negrito e cor
                font=dict(size=12, color='red',
                          family="Arial, sans-serif", weight='bold'),
                align="center"
            )

    # Personalizar o gráfico
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Piloto",
        yaxis_title="Tempo de Volta (s)",
        showlegend=False,
        xaxis_tickangle=-45,  # Melhor visualização dos nomes dos pilotos
        # Definir o valor mínimo da escala Y como 0.98% do melhor tempo
        yaxis=dict(range=[min_y_value, None])
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

    # Exibir a tabela de rankings
    st.write(f"Ranking da Volta {selected_lap}")
    st.dataframe(lap_data[['Piloto', 'Time in Seconds', 'Rank']])

    selected_pilot = st.selectbox(
        "Selecione o piloto para ver o histórico de ranking", ranked_df['Piloto'].unique())

    # Filtrar os dados do piloto selecionado
    pilot_data = ranked_df[ranked_df['Piloto'] == selected_pilot]

    # Gerar gráfico de linha para histórico de ranking
    fig_line = px.line(
        pilot_data,
        x='Lap',
        y='Rank',
        title=f'Histórico de Ranking de {selected_pilot}',
        labels={'Lap': 'Volta', 'Rank': 'Ranking'},
        markers=True
    )

    # Ajustar o eixo Y para garantir que o ranking 1 apareça na parte inferior (melhor ranking)
    fig_line.update_layout(
        xaxis_title="Volta",
        yaxis_title="Ranking",
        title_x=0.5,
    )

    # Exibir o gráfico de histórico de ranking
    st.plotly_chart(fig_line)
