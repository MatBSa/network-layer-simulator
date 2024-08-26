import streamlit as st
import numpy as np
import os
from camada_fisica import *
from camada_enlace import *
from receptor import *
from transmissor import *


# carregar e exibir imagem
def exibir_imagem(caminho):
    st.image(caminho, use_column_width=True)

st.title("Simulador - Camada Física e de Enlace")

mensagem = st.text_input("Digite a mensagem a ser transmitida:", key='mensagem')

# codificacao
codificacao = st.selectbox("Escolha o tipo de codificação:", ['Escolher', "nrz", "bipolar", "manchester"], key='codificacao')

# enquadramento
enquadramento = st.selectbox("Escolha o tipo de enquadramento:", ['Escolher', "contagem de caracteres", "insercao de bytes", "insercao de bits"], key='enquadramento')

# deteccao e correcao de erros
erro = st.selectbox("Escolha o método de detecção/correção de erros:", ['Escolher', "paridade", "crc32", "hamming"], key='erro')

# modulacao
modulacao = st.selectbox("Escolha o tipo de Modulação:", ['Escolher', "ask", "fsk", "8qam"], key='modulacao')

def reset():
    st.session_state.mensagem = ''
    st.session_state.codificacao = 'Escolher'
    st.session_state.enquadramento = 'Escolher'
    st.session_state.erro = 'Escolher'
    st.session_state.modulacao = 'Escolher'

st.button('Limpar', on_click=reset)

if st.button("Enviar mensagem"):
    st.markdown('1 -> Inicia servidor')
    print(f'Mensagem: {mensagem}, codificação: {codificacao}, enquadramento: {enquadramento}, erro: {erro}, modulação: {modulacao}')
    st.markdown(f'Mensagem: {mensagem}, codificação: {codificacao}, enquadramento: {enquadramento}, erro: {erro}, modulação: {modulacao}')
    
    inicia_servidor()
    
    # text, encoding, modulation, framing, error_detection -> pars
    # transmissor -> run -> result
    
    # aplica os metodos escolhidos e transmite pro receptor os dados
    dados_transmitidos = transmissor(mensagem,
                                     codificacao,
                                     enquadramento,
                                     erro,
                                     modulacao)

    print('Sinal transmitido', dados_transmitidos)

    # receber mensagem do transmissor 
    #msg_rec_orig, msg_rec_bits, msg_rec_rexti = receptor(codificacao, enquadramento, erro)
    msg_binaria, msg_recebida_texto = receptor(codificacao, enquadramento, erro)
    print('Mensagem binaria recebida no receptor: ', msg_binaria)
    print('Msg decodificada pelo receptor: ', msg_recebida_texto)
    print('Sinal transmitido', dados_transmitidos)
    #st.markdown('Msg decodificada pelo receptor: ', msg_recebida_texto)

