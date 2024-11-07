import pandas as pd
import streamlit as st
import plotly.express as px
import re
from PIL import Image
import plotly.graph_objs as go


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
st.write("<div align='center'><h2><i>Stock Car Analysis</i></h2></div>",
         unsafe_allow_html=True)
st.write("")

# Ler arquivo base
# Modo de uso: limpar excel e salvar no caminho abaixo
# Somente necessário trocar o nome do arquivo depois da ultima barra
dados = pd.read_excel("D:/Bkp/Python/ProgramaStock/SP24_5_P1_LAPS.xlsx")

# Separar apenas as colunas de interesse
df = dados[['Time of Day', 'Speed', 'Lap',
            'Lap Tm', 'S1 Tm', 'S2 Tm', 'S3 Tm', 'SPT']]

# Criando dicionario para armazenar informações de cada piloto
driver_info = {}
current_driver = None

# Loop para varrer linhas e armanezar em um dicionário como key o nome dos pilotos e values as informações das voltas
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

# Criar um dicionário vazio para armenzar a média das 5 maiores velocidades
average_speed = {}

# Loop para pegar 5 maiores velocidades máximas
for driver in driver_info:
    speeds = driver_info[driver]['SPT'].nlargest(5).dropna()
    av_speed = speeds.mean()
    average_speed[driver] = av_speed.round(2)

# Transformando o dicionário df_speed em um data frame
df_speed = pd.DataFrame(data=top_speed, index=[
    'Velocidade máxima']).T.reset_index()
# Renomeando coluna
df_speed = df_speed.rename(
    columns={'index': 'Piloto'})

# Transformando o dicionário df_speed em um data frame
df_top5 = pd.DataFrame(data=average_speed, index=[
    'Velocidade máxima']).T.reset_index()
# Renomeando coluna
df_top5 = df_top5.rename(
    columns={'index': 'Piloto'})

# Ordenando por maior velocidade
df_speed_ord = df_speed.sort_values(by='Velocidade máxima', ascending=False)
# Eliminando as strings Stock Car PRO 2024 dos pilotos
df_speed_ord['Piloto'] = [re.sub(r' - Stock Car PRO 2024', '', string)
                          for string in df_speed_ord['Piloto']]

# Ordenando por maior velocidade
df_top5_ord = df_top5.sort_values(by='Velocidade máxima', ascending=False)
# Eliminando as strings Stock Car PRO 2024 dos pilotos
df_top5_ord['Piloto'] = [re.sub(r' - Stock Car PRO 2024', '', string)
                         for string in df_top5_ord['Piloto']]

# Ajuste de escala para eixo y (Velocidade máxima)
y_max = df_speed_ord['Velocidade máxima'].max()*1.01
y_min = df_speed_ord['Velocidade máxima'].min()*0.98

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

# Ajuste de escala para eixo y (Velocidade máxima)
y_max5 = df_top5_ord['Velocidade máxima'].max()*1.01
y_min5 = df_top5_ord['Velocidade máxima'].min()*0.98

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

graph_max.update_layout(xaxis_title='Pilotos',
                        title_x=0.5)
graph_top5.update_layout(xaxis_title='Pilotos',
                         title_x=0.5)

# Criando botão para mudar coloração
graph_max.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(
                    args=["type", "scatter"],
                    label="Equipe",
                    method="update"
                ),
                dict(
                    args=[{'title': 'Green'}],
                    label="Montadora",
                    method="update"
                ),
            ]),
            showactive=True,
            x=0.05,
            xanchor="left",
            y=1.06,
            yanchor="top"
        ),
    ]
)

st.plotly_chart(graph_max, use_container_width=True)
st.plotly_chart(graph_top5, use_container_width=True)


cores = st.sidebar.checkbox('Exbir gráfico por montadora')

if cores:
    st.plotly_chart(graph_max_color, use_container_width=True)
