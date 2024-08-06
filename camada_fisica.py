import numpy as np


# 'transmitter' sends a text message that must be converted into a binary array of bits

# 0) converts a string message to an array of bits 1/0 (based on ascii byte char representation)
def binary_conversor(message):
    binary_message = []
    
    for char in message:                    # each char
        ascii = ord(char)                   # ascii decimal repr
        byte = format(ascii, '08b')         # ascii dec -> binary (byte) repr
        bit_list = [int(bit) for bit in byte]  
        binary_message.extend(bit_list)     # put all in a single list
        
    return binary_message


# 1) polar nrz digital modulation
# 0 becomes -1 (-Voltage) while 1 stands as 1 (+Voltage)
def polar_nrz(binary_message):
    return [1 if bit == 1 else -1 for bit in binary_message]


# 2) manchester digital modulation
# 2-bit signal representation
# 0 -> (-1, 1)
# 1 -> (1, -1)
def manchester(binary_message):
    manchester_code = {0: [0, 1], 1: [1, 0]}
    
    manchester_msg = []
    for bit in binary_message:
        manchester_msg.extend(manchester_code[bit])
    return manchester_msg


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
 
# divide a lista de bits em bytes - bytes_list
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
        frame = [f"{len_frame + 1:08b}"] + [f"{byte:08b}" for byte in bytes[i:i + len_frame]]  # +1 for the header
        frames.append(frame)
        
    return frames


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
        frame = [flag] + [f"{byte:08b}" for byte in bytes[i:i + len_frame]]  + [flag] # +1 for the header
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
        # constroi o quadro transformando os n bits atuais que queremos (bits_array[i:i+n_bits_per_frame]) no quadro em uma string 
        # ja adiciona a flag no comeco e no fim do quadro
        frame = flag + ''.join(str(bit) for bit in bits_array[i:i+n_bits_per_frame]) + flag
        frames.append(frame)
        
    return frames



# 'receptor' receives a binary encoded message from the transmitter
def text_conversor(binary_message):
    binary_message = ''.join(str(bit) for bit in binary_message)
    bytes = [int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8)]  # obtains separate bytes (8 to 8), specifying base 2 integers
    message = bytearray(bytes).decode('utf-8')
    
    return message


if __name__ == '__main__':
    message = "Hello World!"
    binary_msg = binary_conversor(message)
    polar_nrz_msg = polar_nrz(binary_msg)
    manchester_msg = manchester(binary_msg)
    #print(text_conversor(binary_msg))