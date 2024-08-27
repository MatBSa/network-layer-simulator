import socket
from camada_enlace import *
from camada_fisica import *
import streamlit as st
import pickle


def transmissor(texto, codificacao, enquadramento, erro, modulacao):
    print('Transmissor iniciando...')
    
    # converte o texto para lista de bits
    binary_message = binary_conversor(texto)
    
    # codificacao
    if codificacao == 'nrz': 
        bits_codificados = polar_nrz(binary_message)
        bits_10 = [0 if bits != 1 else 1 for bits in bits_codificados]
    elif codificacao == 'bipolar':
        bits_codificados = bipolar_nrz(binary_message)
        bits_10 = [0 if bits == 0 else 1 for bits in bits_codificados]
    elif codificacao == 'manchester':
        bits_codificados = manchester(binary_message)
        bits_10 = bits_codificados
    else:
        print('Nenhum método de codificação escolhido')
        st.markdown('Nenhum método de codificação escolhido')
    
    # enquadramento
    if enquadramento == 'contagem de caracteres':
        quadros = char_count(8, bits_10)
    elif enquadramento == 'insercao de bytes':
        quadros = byte_insert(8, bits_10)
    elif enquadramento == 'insercao de bits':
        quadros = bit_insert(64, bits_10)
    else:
        print('Nenhum método de enquadramento escolhido')
        st.markdown('Nenhum método de enquadramento escolhido')
        
    # deteccao e correcao de erros
    if erro == 'paridade':
        quadros_pos_erro = generate_parity(quadros)
    elif erro == 'crc32':
        quadros_pos_erro = generate_crc(quadros)
    elif erro == 'hamming':
        quadros_pos_erro = hamming(quadros)
    else:
        print('Nenhum método de detecção/correção de erros  escolhido')
        st.markdown('Nenhum método de detecção/correção de erros escolhido')

    #NOTE quadros_pos_erro momentaneo -> testar recebimento correto de 'ZZZ' no receptor. Aqui vamos mandar zzz em binario
    sinal = binary_message

    # 'quadros' e uma lista de quadros
    # mensagem binaria unica
    #final_binary_msg = [bit for quadro in quadros_pos_erro for bit in quadro]    
    final_binary_msg = []
    
    # modulacao
    if modulacao == 'ask':
        sinal = ask(final_binary_msg)
    elif modulacao == 'fsk':
        sinal = fsk(final_binary_msg)
    elif modulacao == '8qam':
        sinal = qam8(final_binary_msg)
    else:
        print('Nenhum método de modulação escolhido')
        st.markdown('Nenhum método de modulação escolhido')

    print(sinal, 'ZZZ em binario')
    st.markdown(f'ZZZ em binario SINAL ENVIADO: {sinal}')
    
    # enviar para o receptor apenas o sinal
    transmitir_dados(sinal)
    
    #return binary_message, bits_codificados, sinal
    return sinal


def transmitir_dados(dados):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 65432))
        dados = pickle.dumps(dados)
        client_socket.send(dados)
        dados_recebidos = client_socket.recv(4096)
        client_socket.close()

        return dados_recebidos
