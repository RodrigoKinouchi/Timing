from operator import itemgetter
import pandas as pd
import streamlit as st
import plotly.express as px
import re

# Ler arquivo base
# Modo de uso: limpar excel e salvar no caminho abaixo
# Somente necessário trocar o nome do arquivo depois da ultima barra
dados = pd.read_excel("D:/Bkp/Python/ProgramaStock/SP24_3_P2_LAPS.xlsx")

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

# Transformando o dicionário driver_invo em data frame
for driver in driver_info:
    driver_info[driver] = pd.DataFrame(driver_info[driver])

# Criar um dicionário vazio para armenzar informações de piloto e velocidade max respectiva
average_speed = {}

# Loop para pegar velocidade máxima
for driver in driver_info:
    speeds = driver_info[driver]['SPT'].dropna()
    av_speed = speeds.max()
    average_speed[driver] = av_speed.round(2)

# Transformando o dicionário df_speed em um data frame
df_speed = pd.DataFrame(data=average_speed, index=[
                        'Velocidade máxima']).T.reset_index()
# Renomeando coluna
df_speed = df_speed.rename(
    columns={'index': 'Piloto'})

# Ordenando por maior velocidade
df_speed_ord = df_speed.sort_values(by='Velocidade máxima', ascending=False)
# Eliminando as strings Stock Car PRO 2024 dos pilotos
df_speed_ord['Piloto'] = [re.sub(r' - Stock Car PRO 2024', '', string)
                          for string in df_speed_ord['Piloto']]

# Ajuste de escala para eixo y (Velocidade máxima)
y_max = df_speed_ord['Velocidade máxima'].max()*1.01
y_min = df_speed_ord['Velocidade máxima'].min()*0.98

# Criando gráfico
graph = px.bar(df_speed_ord, x='Piloto',
               y='Velocidade máxima',
               title='<b>Velocidade máxima na sessão</b><br><sup> Quantidade de amostras:1 </sup>', range_y=[y_min, y_max],
               text=df_speed_ord['Piloto'], color='Piloto',
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
graph.update_layout(xaxis_title='Pilotos',
                    title_x=0.5)
graph.show()

# spt_ord = sorted(average_speed.items(), key=itemgetter(1), reverse=True)

# for driver in average_speed:
# print('A velocidade máxima do {} foi: {}'.format(
# driver, average_speed[driver]))

# spt = []
# for driver in average_speed:
# spt.append(average_speed[driver])

# spt_ord = sorted(spt, reverse=True)
# print(spt_ord)
