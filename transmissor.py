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
    
    print(f"1. codificacao: {bits_10}")
    
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
        
    print(f"2. enquadramento: {quadros}")
    
    # deteccao e correcao de erros
    if erro == 'paridade':
        quadros_pos_erro = aplicar_paridade_quadros(enquadramento, quadros)
    elif erro == 'crc32':
        quadros_pos_erro = aplicar_crc_quadros(enquadramento, quadros)
    elif erro == 'hamming':
        quadros_pos_erro = hamming(quadros)
    else:
        print('Nenhum método de detecção/correção de erros  escolhido')
        st.markdown('Nenhum método de detecção/correção de erros escolhido')
        
    print(f"3. erros: {quadros_pos_erro}")

    # mensagem binaria unica
    final_binary_msg = [bit for quadro in quadros_pos_erro for bit in quadro]    
    
    # modulacao
    if modulacao == 'ask':
        sinal = ask(1, 1, final_binary_msg)
    elif modulacao == 'fsk':
        sinal = fsk(1, 2, 1, final_binary_msg)
    elif modulacao == '8qam':
        sinal = qam8(final_binary_msg)
    else:
        print('Nenhum método de modulação escolhido')
        st.markdown('Nenhum método de modulação escolhido')

    # mensagem binaria unica str
    final_binary_msg_str = ''.join(map(str, final_binary_msg))
    
    # enviar para o receptor a msg
    transmitir_dados(final_binary_msg_str)
    
    st.markdown(f'MSG ENVIADA: {final_binary_msg_str}')
    print(f'MSG ENVIADA: {final_binary_msg_str}')
    
    return binary_message, bits_codificados, sinal


def transmitir_dados(dados):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 65432))
        dados = pickle.dumps(dados)
        client_socket.send(dados)
        dados_recebidos = client_socket.recv(8192)
        client_socket.close()

        return dados_recebidos
