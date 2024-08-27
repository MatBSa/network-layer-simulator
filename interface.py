import streamlit as st
import numpy as np
import os
from camada_fisica import *
from camada_enlace import *
from receptor import *
from transmissor import *
from plot_functions import *


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
    print(f'Mensagem: {mensagem}, codificação: {codificacao}, enquadramento: {enquadramento}, erro: {erro}, modulação: {modulacao}')
    
    # plota codificacao isoladamente (codificacao -> plot)
    binary_message = binary_conversor(mensagem)
    if codificacao == 'nrz':
        bits_codificados = polar_nrz(binary_message)
        plota_bits_codificados(bits_codificados, codificacao)
    elif codificacao == 'bipolar':
        bits_codificados = bipolar_nrz(binary_message)
        plota_bits_codificados(bits_codificados, codificacao)
    elif codificacao == 'manchester':
        bits_codificados = manchester(binary_message)
        plota_bits_codificados(bits_codificados, codificacao)
    
    # display na pagina
    st.image('images/bits_codificados.png')    
    
    inicia_servidor()
        
    # aplica os metodos escolhidos e transmite pro receptor os dados
    binary_message, bits_codificados, sinal = transmissor(mensagem,
                                                        codificacao,
                                                        enquadramento,
                                                        erro,
                                                        modulacao)
    
    # plota modulacao isoladamente (modulacao -> plot sinal)
    plota_modulacoes(sinal, modulacao)
    # display na pagina
    st.image('images/modulacao.png')

    # receber mensagem do transmissor 
    msg_bruta, msg_rec_text, msg_rec_bits = receptor(codificacao, enquadramento, erro)
    
    print(f'Sequencia de bits original recebida: {msg_bruta}')
    print(f'Mensagem-texto decodificada: {msg_rec_text}')
    print(f'Sequencia de bits decodificada: {msg_rec_bits}')
    st.markdown(f'Sequencia de bits original recebida: {msg_bruta}')
    st.markdown(f'Mensagem-texto decodificada: {msg_rec_text}')
    st.markdown(f'Sequencia de bits decodificada: {msg_rec_bits}')
