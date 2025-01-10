import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the data (replace 'dados_spotify.csv' with the actual path if needed)
df = pd.read_csv('dados_spotify.csv')

# --- Streamlit Dashboard ---
st.title("Análise de Dados do Spotify")

# Sidebar for navigation
st.sidebar.title("Navegação")
page = st.sidebar.radio("Selecione uma página:", ["Visão Geral", "Popularidade", "Temporal", "Duração"])


# Function to display a DataFrame nicely
def display_df(df_to_display):
    st.dataframe(df_to_display.style.highlight_max(axis=0))


# --- Visão Geral ---
if page == "Visão Geral":
    st.write("## Visão Geral dos Dados")
    st.write("Aqui está um resumo dos dados coletados:")
    st.dataframe(df.head())

    # Add some basic statistics
    st.write("### Estatísticas Descritivas:")
    st.dataframe(df.describe(include='all').T)



# --- Popularidade ---
elif page == "Popularidade":
    st.write("## Análise de Popularidade")
    st.write("### Relação Popularidade do Artista x Música")

    # Calcula a popularidade média das músicas por artista
    pop_media = df.groupby('artista_nome').agg({
        'musica_popularidade': 'mean',
        'artista_popularidade': 'first'
    }).round(2)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=pop_media, x='artista_popularidade', y='musica_popularidade', ax=ax)

    # Add labels and trendline
    for i, artista in enumerate(pop_media.index):
      ax.annotate(artista, (pop_media['artista_popularidade'][i], pop_media['musica_popularidade'][i]), xytext=(5, 5), textcoords='offset points')
    z = np.polyfit(pop_media['artista_popularidade'], pop_media['musica_popularidade'], 1)
    p = np.poly1d(z)
    plt.plot(pop_media['artista_popularidade'], p(pop_media['artista_popularidade']), "r--", alpha=0.8)

    st.pyplot(fig)

    # Show metricas_pop
    st.write("### Métricas de Popularidade:")
    display_df(metricas_pop)


# --- Temporal ---
elif page == "Temporal":
    st.write("## Análise Temporal")
    st.write("### Distribuição da Popularidade por Ano de Lançamento")
    
    # Convertendo a coluna de data (dentro do elif)
    df['data_lancamento'] = pd.to_datetime(df['data_lancamento'], errors='coerce')
    df['ano_lancamento'] = df['data_lancamento'].dt.year

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='ano_lancamento', y='musica_popularidade', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("### Métricas Temporais:")
    display_df(metricas_temp)


# --- Duração ---
elif page == "Duração":
    st.write("## Análise de Duração")

    # Convertendo duração para minutos (dentro do elif)
    df['duracao_min'] = df['duracao_ms'] / (1000 * 60)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='duracao_min', y='musica_popularidade', alpha=0.6, ax=ax)
    st.pyplot(fig)


    st.write("### Métricas de Duração:")
    display_df(metricas_dur)