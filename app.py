import streamlit as st
import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Baixar os recursos necessários do nltk
nltk.download('vader_lexicon')

def extrair_texto(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraindo texto do corpo do artigo
        paragrafos = soup.find_all('p')
        texto = ' '.join([paragrafo.get_text() for paragrafo in paragrafos])
        return texto
    except Exception as e:
        st.error(f"Erro ao acessar a URL: {e}")
        return None

def analisar_palavras_chave(texto, palavras_chave):
    palavras_encontradas = {palavra: texto.lower().count(palavra.lower()) for palavra in palavras_chave}
    return palavras_encontradas

def analisar_sentimento(texto):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(texto)
    if sentiment['compound'] >= 0.05:
        return 'Positivo'
    elif sentiment['compound'] <= -0.05:
        return 'Negativo'
    else:
        return 'Neutro'

def main():
    st.title("Análise de Sentimento e Palavras-Chave de Artigos")
    
    # Entrada de múltiplos links
    urls = st.text_area("Digite os links dos sites (um por linha):").splitlines()
    palavras_chave = st.text_input("Digite as palavras-chave separadas por vírgula:").split(',')
    
    if st.button("Analisar"):
        if urls and palavras_chave:
            for url in urls:
                st.subheader(f"Análise do link: {url}")
                texto = extrair_texto(url)
                
                if texto:
                    palavras_encontradas = analisar_palavras_chave(texto, palavras_chave)
                    sentimento = analisar_sentimento(texto)
                    
                    st.write(f"\nAnálise das palavras-chave:")
                    for palavra, contagem in palavras_encontradas.items():
                        st.write(f"'{palavra}': {contagem} ocorrência(s)")
                    
                    st.write(f"\nSentimento do artigo: {sentimento}")
                else:
                    st.write("Não foi possível extrair o texto do site.")
        else:
            st.error("Por favor, insira ao menos um link e uma palavra-chave.")

if __name__ == "__main__":
    main()
