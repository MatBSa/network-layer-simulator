import socket
from threading import Thread
from camada_enlace import *
from camada_fisica import *
import pickle
import streamlit as st

binary_message = None

# socket -> soquetes de rede -> comunicacao em rede -> endpoints de uma conexao
# thread -> fluxos de execucao separados -> fazer coisas simultaneas

############################## receptor - ouvir canal (sockets) e receber dados em global 'binary_message' ##############################

def ouvir_canal():
    global binary_message
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # cria soquete
    server_socket.bind(('127.0.0.1', 65432))                            # associa o soquete ao endereco e porta                               
    server_socket.listen(1)                                             # coloca em modo de escuta
    print(f"Ouvindo canal, porta 65432")
    
    while True:
        conexao_socket, endpoint = server_socket.accept()               # aceita conexoes de entrada do transmissor e recebe os dados
        print(f'Conexão estabelecida em: {endpoint}')                   # dados recebidos -> binary message em receptor(...) global
        
        dados = conexao_socket.recv(8192)                               # recebe os dados em stream de bits pickle
        binary_message = pickle.loads(dados)                            # sockets lida com bytes, desserializa 
        print(f'Mensagem recebida: {binary_message}')

        conexao_socket.send(pickle.dumps(binary_message))               # envia novamente para transmissor e fecha conexao
        conexao_socket.close()
        
        
# iniciar servidor -> cria instancia de thread e inicia ela (realizar multiplas tarefas ao mesmo tempo)
# passa o ouvir canal para conexao sockets e inicia
def inicia_servidor():            
    thread = Thread(target=ouvir_canal)
    thread.daemon = True
    thread.start()
        

# 1. global binary_message -> mensagem recebida do transmissor (codificada)
# 2. obtem os quadros removendo bits adicionais (para garantir multiplicidade por 8 na carga util em insercao de bytes e contagem de caracteres) e as flags/tamanho_quadro
# 3. remove bits de paridade e crc de acordo com o metodo de deteccao de erros escolhido, ja retornando listas indicativas de erro, (bits_10 sao os bits originais da mensagem, sem nada adicional, o que interessa)
# 4. caso a codificacao seja do tipo manchester, converte os pares de bits usados na codificacao para bits 1 e 0 novasmente
# 5. converte bits_10 (mensagem original em binario) para texto e retorna:
#   5.1 mensagem binaria recebida inicialmente do transmissor
#   5.2 mensagem decodificada em texto 
#   5.3 mensagem decodificada em binario
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
        quadros = remover_frames_hamming(enquadramento, quadros)
        bits_10, erros = checar_paridade(quadros, bits_adicionais)
        
    print(f'2. Erros: {bits_10, erros}')
        
    # codificacao
    if codificacao == 'manchester':
        bits_2_a_2 = [bits_10[i:i+2] for i in range(0, len(bits_10), 2)]
        bits_10 = [0 if bits == [0, 1] else 1 for bits in bits_2_a_2]
    
    print(f'3. bits decodificados: {bits_10} e msg final a ser convert a texto')
    
    # erros
    mensagem_recebida = text_conversor(bits_10)
    
    return binary_message, mensagem_recebida, ''.join(map(str, bits_10))