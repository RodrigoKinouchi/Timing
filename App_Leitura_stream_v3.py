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
    page_title="Stock Car Data",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded")

# Carregando uma imagem
image = Image.open('D:\Bkp\Motorsport\Ipiranga 2024\Fotos\CH6_9918.JPG')

# Inserindo a imagem na página utilizando os comandos do stremalit
st.markdown("<h1 style='text-align: center; font-size: 60px ; color: yellow;'>Ipiranga Racing</h1>",
            unsafe_allow_html=True)
st.image(image, use_column_width=True)
st.write("<div align='center'><h2><i>Stock Car Speed Analysis</i></h2></div>",
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
tabs = st.tabs(['Top speed', 'Top 5 average', 'P2P analysis',
               'Cont push', 'Driver analysis', 'Speed x GAP', 'Laptimes pratice'])

# Separar apenas as colunas de interesse
df = dados[['Time of Day', 'Speed', 'Lap',
            'Lap Tm', 'S1 Tm', 'S2 Tm', 'S3 Tm', 'SPT']]

# Trocando virgula por ponto e transformando os tempos de volta em float
df['SPT'] = df['SPT'].str.replace(',', '.').astype(float)

with tabs[0]:
    # Loop para varrer linhas e armanezar em um dicionário como key o nome dos pilotos e values as informações das voltas
    driver_info = {}
    current_driver = None
    driver_row = df['Time of Day'].str.contains('Stock', na=False)
    for i, row in df.iterrows():
        if driver_row[i]:
            current_driver = row['Time of Day']
            driver_info[current_driver] = []
        elif current_driver:
            driver_info[current_driver].append(row)

    # Transformando o dicionário driver_info em data frame
    for driver in driver_info:
        driver_info[driver] = pd.DataFrame(driver_info[driver])

    # Criar um dicionário vazio para armenzar informações de piloto e velocidade max respectiva
    top_speed = {}

    # Loop para pegar velocidade máxima
    for driver in driver_info:
        speeds = driver_info[driver]['SPT'].dropna()
        av_speed = speeds.max()
        top_speed[driver] = av_speed.round(2)

    # Transformando o dicionário top_speed em um data frame
    df_speed = pd.DataFrame(data=top_speed, index=[
        'Velocidade máxima']).T.reset_index()
    # Renomeando coluna
    df_speed = df_speed.rename(
        columns={'index': 'Piloto'})

    # Ordenando por maior velocidade
    df_speed_ord = df_speed.sort_values(
        by='Velocidade máxima', ascending=False)
    # Eliminando as strings Stock Car PRO 2024 dos pilotos
    df_speed_ord['Piloto'] = [re.sub(r' - Stock Car PRO 2024', '', string)
                              for string in df_speed_ord['Piloto']]

    # Ajuste de escala para eixo y (Velocidade máxima)
    y_max = df_speed_ord['Velocidade máxima'].max()*1.01
    y_min = df_speed_ord['Velocidade máxima'].min()*0.99

    # Criando gráfico top speed
    graph_max = px.bar(df_speed_ord, x='Piloto',
                       y='Velocidade máxima',
                       title='<b>Velocidade máxima na sessão</b><br><sup> Quantidade de amostras:1 </sup>', range_y=[y_min, y_max],
                       text=df_speed_ord['Piloto'], color='Piloto',
                       height=700,
                       width=800,
                       color_discrete_map={'0 - Caca Bueno': 'orange',
                                           '4 - Julio Campos': 'black',
                                           '8 - Rafael Suzuki': 'darkgreen',
                                           '10 - Ricardo Zonta': 'crimson',
                                           '11 - Gaetano Di Mauro': 'grey',
                                           '12 - Lucas Foresti': 'lightblue',
                                           '18 - Allam Khodair': 'blue',
                                           '19 - Felipe Massa': 'darkgreen',
                                           '21 - Thiago Camilo': 'yellow',
                                           '28 - Enzo Elias': 'navy',
                                           '29 - Daniel Serra': 'greenyellow',
                                           '30 - Cesar Ramos': 'yellow',
                                           '33 - Nelson Piquet Jr': 'grey',
                                           '35 - Gabriel Robe': 'silver',
                                           '38 - Zezinho Muggiati': 'orange',
                                           '44 - Bruno Baptista': 'crimson',
                                           '51 - Atila Abreu': 'black',
                                           '81 - Arthur Leist': 'seashell',
                                           '83 - Gabriel Casagrande': 'lightblue',
                                           '85 - Guilherme Salas': 'orange',
                                           '88 - Felipe Fraga': 'blue',
                                           '90 - Ricardo Mauricio': 'greenyellow',
                                           '91 - Eduardo Barrichello': 'seashell',
                                           '95 - Lucas Kohl': 'silver',
                                           '101 - Gianluca Petecof': 'seashell',
                                           '111 - Rubens Barrichello': 'seashell',
                                           '121 - Felipe Baptista': 'navy'
                                           })

    graph_max_color = px.bar(df_speed_ord, x='Piloto',
                             y='Velocidade máxima',
                             title='<b>Velocidade máxima na sessão</b><br><sup> Cruze/Corolla </sup>', range_y=[y_min, y_max],
                             text=df_speed_ord['Piloto'], color='Piloto',
                             height=700,
                             width=800,
                             color_discrete_map={'0 - Caca Bueno': 'orange',
                                                 '4 - Julio Campos': 'orange',
                                                 '8 - Rafael Suzuki': 'orange',
                                                 '10 - Ricardo Zonta': 'red',
                                                 '11 - Gaetano Di Mauro': 'orange',
                                                 '12 - Lucas Foresti': 'orange',
                                                 '18 - Allam Khodair': 'orange',
                                                 '19 - Felipe Massa': 'orange',
                                                 '21 - Thiago Camilo': 'red',
                                                 '28 - Enzo Elias': 'red',
                                                 '29 - Daniel Serra': 'orange',
                                                 '30 - Cesar Ramos': 'red',
                                                 '33 - Nelson Piquet Jr': 'orange',
                                                 '35 - Gabriel Robe': 'orange',
                                                 '38 - Zezinho Muggiati': 'orange',
                                                 '44 - Bruno Baptista': 'red',
                                                 '51 - Atila Abreu': 'orange',
                                                 '81 - Arthur Leist': 'red',
                                                 '83 - Gabriel Casagrande': 'orange',
                                                 '85 - Guilherme Salas': 'orange',
                                                 '88 - Felipe Fraga': 'orange',
                                                 '90 - Ricardo Mauricio': 'orange',
                                                 '91 - Eduardo Barrichello': 'red',
                                                 '95 - Lucas Kohl': 'orange',
                                                 '101 - Gianluca Petecof': 'red',
                                                 '111 - Rubens Barrichello': 'red',
                                                 '121 - Felipe Baptista': 'red'
                                                 })

    graph_max.update_layout(xaxis_title='Pilotos',
                            title_x=0.5)

    st.plotly_chart(graph_max, use_container_width=True)

with tabs[1]:
    # Criar um dicionário vazio para armenzar a média das 5 maiores velocidades
    average_speed = {}
    # Loop para pegar 5 maiores velocidades máximas
    for driver in driver_info:
        speeds = driver_info[driver]['SPT'].nlargest(5).dropna()
        av_speed = speeds.mean()
        average_speed[driver] = av_speed.round(2)
    # Transformando o dicionário average_speed em um data frame
    df_top5 = pd.DataFrame(data=average_speed, index=[
        'Velocidade máxima']).T.reset_index()
    # Renomeando coluna
    df_top5 = df_top5.rename(
        columns={'index': 'Piloto'})

    # Ordenando por maior velocidade
    df_top5_ord = df_top5.sort_values(by='Velocidade máxima', ascending=False)
    # Eliminando as strings Stock Car PRO 2024 dos pilotos
    df_top5_ord['Piloto'] = [re.sub(r' - Stock Car PRO 2024', '', string)
                             for string in df_top5_ord['Piloto']]

    # Ajuste de escala para eixo y (Velocidade máxima)
    y_max5 = df_top5_ord['Velocidade máxima'].max()*1.01
    y_min5 = df_top5_ord['Velocidade máxima'].min()*0.99

    # Criando gráfico top 5
    graph_top5 = px.bar(df_top5_ord, x='Piloto',
                        y='Velocidade máxima',
                        title='<b>Média top speed</b><br><sup> Quantidade de amostras:5 </sup>', range_y=[y_min5, y_max5],
                        text=df_top5_ord['Piloto'], color='Piloto',
                        height=700,
                        width=800,
                        color_discrete_map={'0 - Caca Bueno': 'orange',
                                            '4 - Julio Campos': 'black',
                                            '8 - Rafael Suzuki': 'darkgreen',
                                            '10 - Ricardo Zonta': 'crimson',
                                            '11 - Gaetano Di Mauro': 'grey',
                                            '12 - Lucas Foresti': 'lightblue',
                                            '18 - Allam Khodair': 'blue',
                                            '19 - Felipe Massa': 'darkgreen',
                                            '21 - Thiago Camilo': 'yellow',
                                            '28 - Enzo Elias': 'navy',
                                            '29 - Daniel Serra': 'greenyellow',
                                            '30 - Cesar Ramos': 'yellow',
                                            '33 - Nelson Piquet Jr': 'grey',
                                            '35 - Gabriel Robe': 'silver',
                                            '38 - Zezinho Muggiati': 'orange',
                                            '44 - Bruno Baptista': 'crimson',
                                            '51 - Atila Abreu': 'black',
                                            '81 - Arthur Leist': 'seashell',
                                            '83 - Gabriel Casagrande': 'lightblue',
                                            '85 - Guilherme Salas': 'orange',
                                            '88 - Felipe Fraga': 'blue',
                                            '90 - Ricardo Mauricio': 'greenyellow',
                                            '91 - Eduardo Barrichello': 'seashell',
                                            '95 - Lucas Kohl': 'silver',
                                            '101 - Gianluca Petecof': 'seashell',
                                            '111 - Rubens Barrichello': 'seashell',
                                            '121 - Felipe Baptista': 'navy'
                                            })

    graph_top5.update_layout(xaxis_title='Pilotos',
                             title_x=0.5)

    st.plotly_chart(graph_top5, use_container_width=True)

with tabs[2]:
    speed_max = {}
    gat = {}
    speeds_sp = {}
    speeds_cp = {}
    for driver in driver_info:
        speed_max[driver] = driver_info[driver]['SPT'].max()
        gat[driver] = speed_max[driver]*0.95
        speed = driver_info[driver]['SPT'].dropna()
        speeds_sp[driver] = speed[(speed < gat[driver]) & (
            speed > speed_max[driver] * 0.9)]
        speeds_cp[driver] = speed[speed > gat[driver]]

    # Gerando boxplot sem P2P
    fig = go.Figure()
    for driver in speeds_sp:
        x = re.sub('- Stock Car PRO 2024', '', driver)
        fig.add_trace(go.Box(y=speeds_sp[driver], name=x))
    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black',
                      title='Passagens SEM uso do P2P')

    # Gerando boxplot com P2P
    fig2 = go.Figure()
    for driver in speeds_cp:
        x = re.sub('- Stock Car PRO 2024', '', driver)
        fig2.add_trace(go.Box(y=speeds_cp[driver], name=x))
    fig2.update_layout(plot_bgcolor='black',
                       paper_bgcolor='black', title='Passagens COM uso do P2P')

    st.plotly_chart(fig, use_container_width=True)
    st.write('')
    st.plotly_chart(fig2, use_container_width=True)

with tabs[3]:
    # Criando loop para contar quantas passagens acima do gatilho
    speed_max_contpush = {}
    gat_contpush = {}
    cont_push = {}
    for driver in driver_info:
        speed_max_contpush[driver] = driver_info[driver]['SPT'].max()
        gat_contpush[driver] = speed_max_contpush[driver]*0.95
        speed = driver_info[driver]['SPT'].dropna()
        cont_push[driver] = speed[speed > gat_contpush[driver]]

    # Criando uma lista para armazenar quantidades de passagens
    lista_qtd = {}
    for driver in cont_push:
        lista_qtd[driver] = cont_push[driver].count()

    df_contpush = pd.DataFrame(list(lista_qtd.items()), columns=[
                               'Piloto', 'Passagens'])

    df_contpush['Piloto'] = [re.sub(r' - Stock Car PRO 2024', '', string)
                             for string in df_contpush['Piloto']]

    # Adiciona uma classe personalizada ao input
    p2p_etapa = st.number_input(
        "Digite a quantidade de P2P total da etapa:", format="%.0f")

    df_contpush['Remaining'] = p2p_etapa - df_contpush['Passagens']

    # Criar um contêiner para centralizar a tabela
    st.markdown(
        """
    <div style="display: flex; justify-content: center;">
        {}
    </div>
    """.format(df_contpush.to_html(classes='data', index=False)),
        unsafe_allow_html=True
    )

    st.write('')

    st.dataframe(df_contpush, hide_index=True)

with tabs[4]:
    speed_analysis = {}
    for driver in driver_info:
        speed_analysis[driver] = driver_info[driver]['SPT'].dropna()

    for driver in speed_analysis:
        speed_analysis[driver] = pd.DataFrame(speed_analysis[driver])

    selected_driver = st.multiselect(
        'Select Driver:', list(speed_analysis.keys()))

    # Exibir os dados do piloto selecionado
    if len(selected_driver) == 1:
        # Exibe o nome do piloto
        st.markdown(
            f"<h2 style='text-align: center; font-size: 24px;'>Velocidades do: {
                selected_driver[0]}</h2>",
            unsafe_allow_html=True
        )

        # Criar um DataFrame a partir dos dados do piloto selecionado
        df_selected = speed_analysis[selected_driver[0]].reset_index()
        # Renomear as colunas para facilitar a leitura
        df_selected.columns = ['Lap', 'Speed']

        # Ordenar o DataFrame pela velocidade de forma decrescente
        df_sorted = df_selected.sort_values(by='Speed', ascending=False)

        # Criar colunas para exibir as tabelas lado a lado
        col1, col2 = st.columns(2)

        # Exibir o DataFrame ordenado na primeira coluna
        with col1:
            st.subheader("Velocidades Ordenadas")
            st.dataframe(df_sorted['Speed'])

        # Mostrar estatísticas do piloto selecionado na segunda coluna
        with col2:
            st.subheader("Estatísticas")
            stats = speed_analysis[selected_driver[0]].describe()
            st.dataframe(stats)

    elif len(selected_driver) > 1:
        st.write('Por favor, selecione apenas um piloto.')

    # Exibir os dados do piloto selecionado e plotar grafico de linha
    if selected_driver:
        # Criar a figura
        fig = go.Figure()

        # Adicionar cada piloto à figura
        for driver in selected_driver:
            driver_data = speed_analysis[driver].reset_index()
            driver_data.columns = ['Lap', 'Speed']

            # Normalizar a coluna 'Lap' para que comece em 1
            driver_data['Lap'] = driver_data.index + 1

            fig.add_trace(go.Scatter(
                x=driver_data['Lap'], y=driver_data['Speed'], mode='lines+markers', name=driver))

        # Configurar layout do gráfico
        fig.update_layout(
            title='Velocidades dos Pilotos',
            xaxis_title='Volta',
            yaxis_title='Velocidade',
            legend_title='Piloto'
        )

        # Exibir o gráfico
        st.plotly_chart(fig)

    else:
        st.write('Por favor, selecione pelo menos um piloto.')


with tabs[5]:
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
            pilot_data['SPT'] > 200) & (pilot_data['GAP'] < 5)]

        # Criar o gráfico interativo usando Plotly
        fig = px.scatter(
            filtered_data,
            x='GAP',
            y='SPT',
            title=f'GAP vs Velocidade (SPT) > 200 km/h para {selected_pilot}',
            labels={'GAP': 'GAP (s)', 'SPT': 'Velocidade (SPT) (km/h)'},
            hover_data=['Time of Day'],  # Exibir o horário ao passar o mouse
        )

        # Personalizar o layout
        fig.update_traces(marker=dict(size=10, opacity=0.7,
                          line=dict(width=1, color='DarkSlateGrey')))
        fig.update_layout(title_x=0.3)  # Centralizar o título

        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
    else:
        st.warning('Por favor, selecione um piloto.')

with tabs[6]:
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
                 labels={
                     'Tempo de Volta em Segundos': 'Tempo de Volta (segundos)', 'Piloto': 'Piloto'})

    # Ajustes de layout adicionais
    fig.update_layout(
        xaxis_tickangle=-45  # Inclinar os rótulos do eixo x
    )

    # Exibir gráfico no Streamlit
    st.plotly_chart(fig)
