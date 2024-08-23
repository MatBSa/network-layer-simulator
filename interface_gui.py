import streamlit as st
import numpy as np
import os
from camada_fisica import qam8, bipolar_nrz, ask, fsk, plot_signal

#Função para plot da imagem
def exibir_imagem(caminho):
    st.image(caminho, use_column_width=True)
    
st.sidebar.title("Simulador de Transmissão de Sinais")

st.sidebar.header("Transmissor")

texto = st.sidebar.text_area("Insira o texto a ser transmitido")

codificacao = st.sidebar.radio(
    "Escolha o tipo de transmissor",
    ("NRZ","Manchester","Bipolar")
)
# Botao para transmissão
if st.sidebar.button("Transmitir"):
    st.sidebar.write(f"Transmitindo o texto: '{texto}' usando {codificacao}")

#Seção Modulador
st.sidebar.header("Modulador")
modulacao = st.sidebar.radio(
    "Escolha o tipo de modulação",
    ("ASK","FSK","8-QAM")
)

# Parte da direita
st.subheader("Receptor")

st.write("Aqui será plotado o sinal recebido") #espaço para o sinal recebido

#enquadramento
st.subheader("Enquadramento")
enquadramento =st.radio(
    "Escolha o tipo de enquadramento:",
    ("Cont. de caracteres", "Inserção de Bits", "Inserção de Bytes")
)

#detecção/correção de erro
st.subheader("Detecção/Correção de Erro")
correcao_de_erro = st.radio(
    "Escolha o método de detecção/correção de erro:",
    ("Bit de Paridade Par","CRC32","Hamming")
)

st.write(f"Texto transmitido: {texto}")
st.write(f"Codificação escolhida: {codificacao}")
st.write(f"Modulação escolhida: {modulacao}")
st.write(f"Enquadramento escolhido: {enquadramento}")
sr.write(f"Detecção/Correção de Erro escolhida: {correcao_de_erro}")