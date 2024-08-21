import numpy as np
from camada_fisica import binary_conversor, text_conversor

# camada de enlace:
#   1. permitir a comunicação eficiente transmissor-receptor
#   2. recebe os pacotes da camada de rede -> encapsula em quadros para transmissão
#   3. transferir dados da camada de rede origem - destino
#   4. dividir o fluxo de bits em quadros distintos
#   5. calcula o checksum p cada quadro
#   6. incluir o checksum no quadro enviado
# meio de comunicação possui empecilhos que tornam a comunicação mais complexa que enviar-receber
# quadros:
#   1. unidades de informação inteiras
#   2. cabeçalho, campo de carga útil, final

# contagem de caracteres:
#   1. campo no cabeçalho especifica número de bytes no quadro (tamanho do quadro)
#   2. camada de destino sabe quantos bytes o quadro contém - onde está o seu fim
 
# divide a lista de bits em bytes 
# loop continua até que bytes_list esteja vazio
# calcula em cada loop o tamanho do quadro = min(n_bytes_restantes, tam_max_quadro - 1)
# cria um quadro -> cabeçalho (tamanho do quadro em binario) e os bytes no quadro
# quadro adicionada a uma matriz que os guarda - lista de quadros, cada quadro eh uma lista de str8bits
def char_count(n_bytes_per_frame, binary_message):
    binary_message = ''.join(str(bit) for bit in binary_message)
    bytes = [int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8)]
    frames = []
    
    for i in range(0, len(bytes), n_bytes_per_frame - 1):
        len_frame = min(len(bytes) - i, n_bytes_per_frame - 1)
        # adds 1 to consider the header (character count method)
        frame = [f"{format(len_frame + 1, '08b')}"] + [f"{format(byte, '08b')}" for byte in bytes[i:i + len_frame]]  # +1 for the header
        frames.append(frame)
        
    return frames

# BITS DE PREENCHIMENTO:
# para evitar que a sequencia '0111110' seja confundida com uma flag, um bit extra (0) e inserido automaticamente apos uma sequencia de 5 1s consecutivos,
# garantindo que a flag nunca apareca no quadro (carga util)
# esses bits de preenchimento sao removidos no receptor para restaurar a mensagem original

# inserção de bytes:
#   0. contornar o problema de ressincronização após um erro de bit
#   1. cada quadro começa e termina com um byte de flag
#   2. ex: flag 1 2 3 flag flag 4 5 6 flag
#   3. dois bytes de flag consecutivos indicam fim-inicio
#   4. caso o receptor perca a sincronização basta procurar 
#      dois bytes de flag consecutivos para encontrar o final 
#      do quadro atual e o início do seguinte
#   5. caso ocorra uma flag no campo de carga util (meio do quadro, bytes arm.)
#      incluir caractere especial esc antes de cada byte de flag acidental
#   6. caso ocorra esc no campo de carga util
#      incluir caractere especial esc antes de cada esc acidental


def byte_insert(n_bytes_per_frame, binary_message, flag='01111110'):
    binary_message = ''.join(str(bit) for bit in binary_message)
    bytes = [int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8)]
    frames = []
    
    for i in range(0, len(bytes), n_bytes_per_frame - 2):
        # calcula o tamanho de cada quadro
        # o minimo garante que o tamanho maximo de cada quadro nao sera excedido
        # o numero de bytes remanescentes no minimo garante que, mesmo que haja uma
        # quantidade de bytes menor que a definida por quadro, eles sejam enquadrados
        if (n_bytes_per_frame - 2) < (len(bytes) - i):
            len_frame = n_bytes_per_frame - 2
        else:
            len_frame = len(bytes) - i
        # adds 1 to consider the header (character count method)
        frame = [flag] + [f"{format(byte, '08b')}" for byte in bytes[i:i + len_frame]]  + [flag] # +1 for the header
        frames.append(frame)
        
    return frames


# inserção de bits:
#   1. contorna limitação da inserção de bytes (fato de usar 8 bits)
#   2. enquadramento pode ser feito a nível de bits - quadros de qualquer tamanho
#   3. cada quadro começa e termina com um padrão de bits especial 01111110
#   4. essa sequência de bit especial é um byte de flag
#   5. evitar a ocorrência da sequência de bits especiais na carga útil
#   sempre que ocorre sequência de 5 bits '1', é inserido um bit '0' após ela
def bit_insert(n_bits_per_frame, binary_message, flag='01111110'):
    frames = []
    # percorre toda a binary_message, de n em n bits por quadro que queremos
    for i in range(0, len(binary_message), n_bits_per_frame):
        # constroi o quadro transformando os n bits atuais que queremos (binary_message[i:i+n_bits_per_frame]) no quadro em uma string 
        # ja adiciona a flag no comeco e no fim do quadro
        frame = flag + ''.join(str(bit) for bit in binary_message[i:i+n_bits_per_frame]) + flag
        frames.append(frame)
        
    return frames


# receptor -> receives from the transmitter a binary message to be decoded into text
# in each function below, one per framing method, we remove the 'additional info' that are not part of the message itself, like flags and character counts
# filter only the message of each frame


# obtains each frame separately, removing their headers (which contains the number of bytes in the frame)
# obtains a list containing the bits of each frame (concatenated in str, removing header - number of bytes in the frame) and the additional bits
def get_char_count_frames_bits(binary_message):
    byte_units = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    bytes = [''.join(str(bit) for bit in byte) for byte in byte_units]
    str_frames_without_headers, additional_bits = list(), list()

    i = 0
    for _ in range(len(bytes)):
        if i >= len(bytes):
            break
        
        # obtain integer (from base 2) number of bytes in current frame (header info)
        len_frame = int(bytes[i], 2)
        add_bits = int(bytes[i + 1], 2)
        additional_bits.append(add_bits)
        
        # add frame without header to the final list of frames (already in str format, each frame)
        str_frame_without_header = ''.join(bytes[i + 2:i + len_frame])
        str_frames_without_headers.append(str_frame_without_header)
        
        # move to the next frame
        i += len_frame

    return str_frames_without_headers, additional_bits

# obtain frames (without flags) and additional bits information
# obtains a list containing the bits of each frame (concatenated in str, removing the flag delimiting each frame) and the additional bits
def get_byte_insert_frames_bits(binary_message, flag='01111110'):
    str_frames_without_flags, additional_bits, frame = list(), list()
    byte_units = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    bytes = [''.join(str(bit) for bit in byte) for byte in byte_units]

    for byte in bytes:
        if byte != flag:
            frame.append(byte)
        else:
            if frame:  
                add_bits = int(frame[0], 2) # first byte of the frame (not being flag) will be the additional bits
                additional_bits.append(add_bits)
                
                str_frame_without_flag = ''.join(frame[1:]) # then, we will have the frame bytes, converted into a unique string
                str_frames_without_flags.append(str_frame_without_flag)
                frame.clear()        

    return str_frames_without_flags, additional_bits


# obtain frames (without flags) and additional bits information
# obtains a list containing the bits of each frame (concatenated in str, removing the flag in each frame) and the additional bits
def get_bit_insert_frames_bits(binary_message, flag='01111110', crc=True):
    str_frames_without_flags, additional_bits, frame_bits = list(), list(), list()
    str_bits = [str(bit) for bit in binary_message]
    bits = ''.join(str_bits)
    
    i = 0                                           # para ir selecionando partes mais à frente na mensagem binária
    while i < len(bits):  
        
        if bits[i:i+len(flag)] == flag:             # é flag?
            i += len(flag)                          # selecionar os bits depois da flag (remover flag)
            
            if frame_bits:                          # se o frame não estiver vazio (fim de quadro), adiciona ele na lista de frames
                str_frames_without_flags.append(''.join(frame_bits))
                frame_bits = list()
                
            # verificar se frame está vazio (início de quadro, com flag)
            else:
                if not crc:                         # se não tiver correção CRC, adic"iona zero
                    additional_bits.append(0)
                else:                               # se tiver CRC, remove os 8 bits de preenchimento logo após uma flag de início de quadro
                    add_bits = bits[i:i+8]          # pegar os próximos 8 bits de preenchimento
                    add_bits = int(add_bits, 2)     # converte de binário para inteiro
                    additional_bits.append(add_bits)
                    i += 8                          # avançar 8 bits após os bits de preenchimento
        else:                      
            frame_bits.append(bits[i])
            i += 1                                  # avançar 1 bit
    
    return str_frames_without_flags, additional_bits
    
######################### Parity Bit #########################
def generate_parity(data):
    return data + str(data.count('1') % 2)

def check_parity(data):
    return data[:-1], data[-1] == str(data[:-1].count('1') % 2)

########################### CRC-32 ###########################
def crc_remainder(data, polynomial):
    data = data + '0' * (len(polynomial) - 1)
    data = list(data)
    polynomial = list(polynomial)
    for i in range(len(data) - len(polynomial) + 1):
        if data[i] == '1':
            for j in range(len(polynomial)):
                data[i + j] = str(int(data[i + j]) ^ int(polynomial[j]))
    return ''.join(data[-(len(polynomial) - 1):])

def generate_crc(data, polynomial):
    remainder = crc_remainder(data, polynomial)
    return data + remainder

def check_crc(data, polynomial):
    remainder = crc_remainder(data, polynomial)
    return remainder == '0' * (len(polynomial) - 1)
