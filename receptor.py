import socket
from threading import Thread
from camada_enlace import *
from camada_fisica import *
import pickle
import streamlit as st

binary_message = None

# socket -> soquetes de rede -> comunicacao em rede -> endpoints de uma conexao
# thread -> fluxos de execucao separados -> fazer coisas simultaneas
def ouvir_canal():
    global binary_message
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # cria soquete
    server_socket.bind(('127.0.0.1', 65432))                            # associa o soquete ao endereco e porta                               # coloca em modo de escuta
    server_socket.listen(1)                                             # coloca em modo de escuta
    print(f"Ouvindo canal, porta 65432")
    
    while True:
        conexao_socket, endpoint = server_socket.accept()               # aceita conexoes de entrada do transmissor e recebe os dados
        print(f'Conexão estabelecida em: {endpoint}')                   # dados recebidos -> binary message em receptor(...)
        
        dados = conexao_socket.recv(8192)  
        binary_message = pickle.loads(dados)                            # sockets lida com bytes, desserializa
        print(f'Mensagem recebida: {binary_message}')

        conexao_socket.send(pickle.dumps(binary_message))          # envia novamente para transmissor e fecha conexao
        conexao_socket.close()
        
        
# iniciar servidor -> cria instancia de thread e inicia ela
def inicia_servidor():            
    thread = Thread(target=ouvir_canal)
    thread.daemon = True
    thread.start()
        
        
def receptor(codificacao, enquadramento, erro):
    global binary_message
    
    print(f'\n\nReceptor...')
    
    # enquadramento
    if enquadramento == 'contagem de caracteres':
        quadros, bits_adicionais = get_char_count_frames_bits(binary_message)
    elif enquadramento == 'insercao de bytes':
        quadros, bits_adicionais = get_byte_insert_frames_bits(binary_message)
    elif enquadramento == 'insercao de bits':
        if erro != 'crc32':
            quadros, bits_adicionais = get_bit_insert_frames_bits(binary_message, crc=False)
        else:
            quadros, bits_adicionais = get_bit_insert_frames_bits(binary_message)
    
    print(f'1. desenquadramento: {quadros, bits_adicionais}')
    
    # deteccao e correcao de erros
    if erro == 'paridade':
        bits_10, erros = checar_paridade(quadros, bits_adicionais)
    elif erro == 'crc32':
        bits_10, erros = checar_crc32(quadros, bits_adicionais)
    elif erro == 'hamming':
        st.markdown('Hamming ainda não disponibilizado')
        
    print(f'2. Erros: {bits_10, erros}')
        
    # codificacao
    if codificacao == 'manchester':
        bits_2_a_2 = [bits_10[i:i+2] for i in range(0, len(bits_10), 2)]
        bits_10 = [0 if bits == [0, 1] else 1 for bits in bits_2_a_2]
    
    print(f'3. bits decodificados: {bits_10} e msg final a ser convert a texto')
    
    # erros
    mensagem_recebida = text_conversor(bits_10)
    
    return binary_message, mensagem_recebida, ''.join(map(str, bits_10))