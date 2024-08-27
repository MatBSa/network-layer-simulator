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
    str_frames_without_flags, additional_bits, frame = list(), list(), list()
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
quadros = [['01111110', '01011010', '01111110'], ['01111110', '01011010', '01111110'], ['01111110', '01011010', '01111110']]

def bits_a_adicionar_quadro_div_8(carga_util_c_paridade):
    # garantir que os quadros tenham um tamanho divisivel por 8 -> bits adicionais para completar numero divisivel por 8
    bits_a_adicionar = (8 - (len(carga_util_c_paridade) % 8)) % 8           # 1. calcula quantos bits necessarios adicionar p o quadro ser divisivel por 8 (8 - (len(carga_util_c_paridade) % 8)) 
                                                                            # 2. verifica se o numero necessario para adicionar eh 0 ou 8, nao sendo necessario
    bits_a_adicionar_binario = format(bits_a_adicionar, '08b')
    quadro_adicionado = carga_util_c_paridade + [0] * bits_a_adicionar
    
    return quadro_adicionado, bits_a_adicionar_binario


def forma_carga_util_contagem_char(quadro):
    carga_util = quadro[1:]
    carga_util_joined = ''.join(carga_util)
    carga_util_binary_lst = [int(bit) for bit in carga_util_joined]    
    return carga_util_binary_lst


def forma_quadro_cabecalho_adicionados_contagem_char(quadro_crc, n_bits_adicionados):
    n_bits_adicionados_binary = format(n_bits_adicionados, '08b')
    cabecalho_adicionado = [int(bit) for bit in n_bits_adicionados_binary]
    
    tamanho_do_quadro = len(quadro_crc) // 8
    tamanho_do_quadro_binario = format(tamanho_do_quadro + 2, '08b')
    cabecalho_do_quadro_binary_lst = [int(bit) for bit in tamanho_do_quadro_binario]
    
    return cabecalho_do_quadro_binary_lst + cabecalho_adicionado + quadro_crc


def forma_flag_carga_util_insercao_bytes(quadro):
    flag = quadro[0]
    flag_binary_lst = [int(bit) for bit in flag]  
    carga_util = quadro[1:-1]
    carga_util_joined = ''.join(carga_util)
    carga_util_binary_lst = [int(bit) for bit in carga_util_joined]
    return flag_binary_lst, carga_util_binary_lst


def forma_flag_carga_util_insercao_bits(quadro):
    flag = quadro[:8]
    flag_binary_lst = [int(bit) for bit in flag]
    carga_util = quadro[8:-8]
    carga_util_joined = ''.join(carga_util)
    carga_util_binary_lst = [int(bit) for bit in carga_util_joined]
    return flag_binary_lst, carga_util_binary_lst


def quadros_com_paridade_insercao_bytes(quadros):
    quadros_com_paridade = list()
        
    # cada quadro e uma lista de bytes em str
    for quadro in quadros:
        flag_binary_lst, carga_util_binary_lst = forma_flag_carga_util_insercao_bytes(quadro)
        carga_util_c_paridade = generate_parity(carga_util_binary_lst)
            
        quadro_adicionado, bits_a_adicionar_binario = bits_a_adicionar_quadro_div_8(carga_util_c_paridade)
        cabecalho_adicionado = [int(bit) for bit in bits_a_adicionar_binario]
    
        quadros_com_paridade.append(flag_binary_lst + cabecalho_adicionado + quadro_adicionado + flag_binary_lst)
        
    return quadros_com_paridade


def quadros_com_paridade_insercao_bits(quadros):
    quadros_com_paridade = list()
    
    for quadro in quadros:
        flag_binary_lst, carga_util_binary_lst = forma_flag_carga_util_insercao_bits(quadro)
        carga_util_c_paridade = generate_parity(carga_util_binary_lst)
        quadros_com_paridade.append(flag_binary_lst + carga_util_c_paridade + flag_binary_lst)

    return quadros_com_paridade


def quadros_com_paridade_contagem_char(quadros):        
    quadros_com_paridade = list()
    
    for quadro in quadros:
        carga_util_binary_lst = forma_carga_util_contagem_char(quadro)
        carga_util_c_paridade = generate_parity(carga_util_binary_lst)
        
        quadro_adicionado, bits_a_adicionar_binario = bits_a_adicionar_quadro_div_8(carga_util_c_paridade)
        cabecalho_adicionado = [int(bit) for bit in bits_a_adicionar_binario]
        
        tamanho_do_quadro = len(quadro_adicionado) // 8
        tamanho_do_quadro_binario = format(tamanho_do_quadro + 2, '08b')
        cabecalho_do_quadro_binary_lst = [int(bit) for bit in tamanho_do_quadro_binario]
        
        quadros_com_paridade.append(cabecalho_do_quadro_binary_lst + cabecalho_adicionado + quadro_adicionado)
    
    return quadros_com_paridade
        

def aplicar_paridade_quadros(enquadramento, quadros):
    if enquadramento == 'insercao de bytes':
        return quadros_com_paridade_insercao_bytes(quadros)
            
    elif enquadramento == 'insercao de bits':
        return quadros_com_paridade_insercao_bits(quadros)
    
    elif enquadramento == 'contagem de caracteres':
        return quadros_com_paridade_contagem_char(quadros)


    
def generate_parity(data):
    data = ''.join([str(bit) for bit in data])
    data_w_parity = data + str(data.count('1') % 2)
    return [int(bit) for bit in data_w_parity]


def checar_paridade(quadros, bits_adicionais):
    erros, bits_quadro_carga_util = list(), list()

    if bits_adicionais:
        indice_quadro = 0
        while indice_quadro < len(quadros):
            quadro = quadros[indice_quadro]
            bit_adicional = bits_adicionais[indice_quadro]

            if bit_adicional != 0:
                quadro = quadro[:-bit_adicional] 

            quadro_binary_bits_lst = []
            indice_bit = 0
            while indice_bit < len(quadro):
                quadro_binary_bits_lst.append(int(quadro[indice_bit]))
                indice_bit += 1

            numero_1s = 0
            indice_soma = 0
            while indice_soma < len(quadro_binary_bits_lst) - 1:
                numero_1s += quadro_binary_bits_lst[indice_soma]
                indice_soma += 1

            bit_paridade = quadro_binary_bits_lst[-1]

            if (numero_1s + bit_paridade) % 2 == 0:
                erros.append(False)
            else:
                erros.append(True)

            indice_copia = 0
            while indice_copia < len(quadro_binary_bits_lst) - 1:
                bits_quadro_carga_util.append(quadro_binary_bits_lst[indice_copia])
                indice_copia += 1

            indice_quadro += 1

    else:
        indice_quadro = 0
        while indice_quadro < len(quadros):
            quadro = quadros[indice_quadro]
            
            quadro_binary_bits_lst = []
            indice_bit = 0
            while indice_bit < len(quadro):
                quadro_binary_bits_lst.append(int(quadro[indice_bit]))
                indice_bit += 1

            numero_1s = 0
            indice_soma = 0
            while indice_soma < len(quadro_binary_bits_lst) - 1:
                numero_1s += quadro_binary_bits_lst[indice_soma]
                indice_soma += 1

            bit_paridade = quadro_binary_bits_lst[-1]

            if (numero_1s + bit_paridade) % 2 == 0:
                erros.append(False)
            else:
                erros.append(True)

            indice_copia = 0
            while indice_copia < len(quadro_binary_bits_lst) - 1:
                bits_quadro_carga_util.append(quadro_binary_bits_lst[indice_copia])
                indice_copia += 1

            indice_quadro += 1

    return bits_quadro_carga_util, erros


########################### CRC-32 ###########################
def quadros_com_crc_insercao_bytes(quadros):
    quadros_com_crc = list()
    for quadro in quadros:
        flag_binary_lst, carga_util_binary_lst = forma_flag_carga_util_insercao_bytes(quadro)
        
        quadro_crc, n_bits_adicionados = calcula_crc32(carga_util_binary_lst)
        n_bits_adicionados_binary = format(n_bits_adicionados, '08b')
        cabecalho_adicionado = [int(bit) for bit in n_bits_adicionados_binary]
        
        quadros_com_crc.append(flag_binary_lst + cabecalho_adicionado + quadro_crc + flag_binary_lst)
        
    return quadros_com_crc


def quadros_com_crc_insercao_bits(quadros):
    quadros_com_crc = list()
    
    for quadro in quadros:
        flag_binary_lst, carga_util_binary_lst = forma_flag_carga_util_insercao_bits(quadro)

        quadro_crc, n_bits_adicionados = calcula_crc32(carga_util_binary_lst)
        n_bits_adicionados_binary = format(n_bits_adicionados, '08b')
        cabecalho_adicionado = [int(bit) for bit in n_bits_adicionados_binary]
        
        quadros_com_crc.append(flag_binary_lst + cabecalho_adicionado + quadro_crc + flag_binary_lst)
    
    return quadros_com_crc


def quadros_com_crc_contagem_char(quadros):
    quadros_com_crc = list()
    for quadro in quadros:
        carga_util_binary_lst = forma_carga_util_contagem_char(quadro)
        quadro_crc, n_bits_adicionados = calcula_crc32(carga_util_binary_lst)
    
    quadros_com_crc.append(forma_quadro_cabecalho_adicionados_contagem_char(quadro_crc, n_bits_adicionados))
    
    return quadros_com_crc
    
    
def aplicar_crc_quadros(enquadramento, quadros):
    if enquadramento == 'insercao de bytes':
        return quadros_com_crc_insercao_bytes(quadros)

    elif enquadramento == 'insercao de bits':
        return quadros_com_crc_insercao_bits(quadros)

    elif enquadramento == 'contagem de caracteres':
        return quadros_com_crc_contagem_char(quadros)
    

def calcula_crc32(binary_message, polinomio=format(0x104C11DB7, '033b')):
    tamanho_bits_adicionados = 0

    if len(binary_message) < 64:  # se o array de bits tiver menos de 64 bits, completar com 0's e 1's (para evitar sequências longas de 0's)
        array_bits_complementares = []
        indice_complementar = 0
        while indice_complementar < (64 - len(binary_message)):
            if indice_complementar % 2 == 0:  # se o índice for par, o bit é 0
                array_bits_complementares.append(0)
            else:  # se o índice for ímpar, o bit é 1
                array_bits_complementares.append(1)
            indice_complementar += 1
        binary_message = binary_message + array_bits_complementares
        tamanho_bits_adicionados = len(array_bits_complementares)

    binary_message_joined = ''.join(map(str, binary_message))  # converter o array de bits para uma string de bits
    binary_message_original = binary_message_joined

    binary_message_joined += '0' * 32  # adicionar 32 zeros para completar os 96 bits
    resultado_xor_str = ''
    indice_bit = 0
    while indice_bit < len(binary_message_joined):  # para cada bit na string de bits
        if indice_bit <= 32:  # se o bit estiver nos primeiros 32 bits
            resultado_xor_str += binary_message_joined[indice_bit]
        else:  # se o bit estiver nos últimos 64 bits
            if resultado_xor_str[0] == '1':
                resultado_xor_temp = ''
                indice_temp = 0
                while indice_temp < len(polinomio):
                    if resultado_xor_str[indice_temp] == polinomio[indice_temp]:
                        resultado_xor_temp += '0'
                    else:
                        resultado_xor_temp += '1'
                    indice_temp += 1
                resultado_xor_str = resultado_xor_temp[1:] + binary_message_joined[indice_bit]  # excluir o primeiro bit (0) e incluir o próximo bit
            else:
                resultado_xor_str = resultado_xor_str[1:] + binary_message_joined[indice_bit]  # excluir o primeiro bit (0) e incluir o próximo bit

        if indice_bit == len(binary_message_joined) - 1:  # se for o último bit
            if resultado_xor_str[0] == '1':  # se o primeiro bit for 1, xor com o polinômio
                resultado_xor_temp = ''
                indice_temp = 0
                while indice_temp < len(polinomio):
                    if resultado_xor_str[indice_temp] == polinomio[indice_temp]:
                        resultado_xor_temp += '0'
                    else:
                        resultado_xor_temp += '1'
                    indice_temp += 1
                resultado_xor_str = resultado_xor_temp[1:]  # excluir o primeiro bit (0)
            else:  # se o primeiro bit for 0, xor com 33 zeros
                resultado_xor_str = resultado_xor_str[1:]  # excluir o primeiro bit (0)
        indice_bit += 1

    return list(binary_message_original + resultado_xor_str), tamanho_bits_adicionados


def checar_crc32(quadros, bits_adicionais, polinomio=format(0x104C11DB7, '033b')):
    erros, bits_quadro_carga_util = list(), list()

    for indice_quadro in range(len(quadros)):
        quadro = quadros[indice_quadro]
        bits_padding = bits_adicionais[indice_quadro]

        quadro_binary_bits_lst = []
        indice_bit = 0
        while indice_bit < len(quadro):
            quadro_binary_bits_lst.append(int(quadro[indice_bit]))
            indice_bit += 1

        tamanho_bits_adicionados = 0

        string_bits = ''.join(map(str, quadro_binary_bits_lst))  # converte o array de bits para uma string de bits
        string_bits += '0' * 32  # adiciona 32 zeros para completar os 96 bits
        resultado_xor_str = ''
        indice_bit_str = 0

        while indice_bit_str < len(string_bits):  # para cada bit na string de bits
            if indice_bit_str <= 32:  # se o bit estiver nos primeiros 32 bits
                resultado_xor_str += string_bits[indice_bit_str]
            else:  # se o bit estiver nos últimos 64 bits
                if resultado_xor_str[0] == '1':
                    resultado_xor_temp = ''
                    indice_temp = 0
                    while indice_temp < len(polinomio):
                        if resultado_xor_str[indice_temp] == polinomio[indice_temp]:
                            resultado_xor_temp += '0'
                        else:
                            resultado_xor_temp += '1'
                        indice_temp += 1
                    resultado_xor_str = resultado_xor_temp[1:] + string_bits[indice_bit_str]  # exclui o primeiro bit (0) e inclui o próximo bit
                else:
                    resultado_xor_str = resultado_xor_str[1:] + string_bits[indice_bit_str]  # exclui o primeiro bit (0) e inclui o próximo bit

            if indice_bit_str == len(string_bits) - 1:  # se for o último bit
                if resultado_xor_str[0] == '1':  # se o primeiro bit for 1, xor com o polinômio
                    resultado_xor_temp = ''
                    indice_temp = 0
                    while indice_temp < len(polinomio):
                        if resultado_xor_str[indice_temp] == polinomio[indice_temp]:
                            resultado_xor_temp += '0'
                        else:
                            resultado_xor_temp += '1'
                        indice_temp += 1
                    resultado_xor_str = resultado_xor_temp[1:]  # exclui o primeiro bit (0)
                else:  # se o primeiro bit for 0, xor com 33 zeros
                    resultado_xor_str = resultado_xor_str[1:]  # exclui o primeiro bit (0)
            indice_bit_str += 1

        if resultado_xor_str == '0' * 32:  # se o resultado for 32 zeros, não há erros
            erros.append(False)
        else:  # se o resultado não for 32 zeros, há erros
            erros.append(True)

        if bits_padding != 0:
            indice_limpeza = 0
            while indice_limpeza < len(quadro_binary_bits_lst) - bits_padding - 32:  # remove os bits de padding
                bits_quadro_carga_util.append(quadro_binary_bits_lst[indice_limpeza])
                indice_limpeza += 1
        else:
            indice_limpeza = 0
            while indice_limpeza < len(quadro_binary_bits_lst) - 32:  # remove os 32 bits do CRC
                bits_quadro_carga_util.append(quadro_binary_bits_lst[indice_limpeza])
                indice_limpeza += 1

    return bits_quadro_carga_util, erros



########################## HAMMING #########################


# TRANSMISSOR
# 1. palavra de codigo de n bits -> m bits de dados e r bits de paridade
# 2**r >= m + r + 1 (formula para calcular o numero de bits de paridade r necessarios)
# 2. comeca preenchendo com bits zero as posicoes na mensagem em que temos bits de verificacao (potencias de dois)
# 3. insere 0 nas posicoes dos bits de paridade inicialmente (posicoes que sao potencias de dois)
# 4. para cada uma dessas potencias, calcula o seu bit de paridade (0/1) com base na soma XOR de todas as outras posicoes que influenciam-no

def calcular_bit_paridade(array, potencia_de_dois):
    # verificar todos os bits de dados que contribuem para a paridade dessa potencia_de_dois (posicao da respectiva potencia de dois)
    # lógica do bit de paridade: soma XOR de todos os bits que influenciam
    valor_paridade = 0        # armazenar a soma XOR de todos os bits que influenciam a paridade dessa potencia de dois
    i = potencia_de_dois - 1  # converter para índice baseado em zero
    
    while i < len(array):
        # seleciona blocos de bits que começam na posição 'i' e têm tamanho 'potencia_de_dois'
        bloco = array[i:i + potencia_de_dois]
        valor_paridade ^= sum(bloco)        # soma XOR sobre o bloco
        i += 2 * potencia_de_dois           # pula para o próximo bloco relevante
    
    return valor_paridade % 2               # retorna 0 ou 1


def hamming(binary_message):
    
    # calcula o numero de bits de paridade necessarios: 2**r >= m + r + 1
    num_parity_bits = 0
    while (2 ** num_parity_bits) < (len(binary_message) + num_parity_bits + 1):
        num_parity_bits += 1
    
    # insere zero inicialmente nas posicoes correspondentes a bits de paridade (potencias de dois)
    parity_zero_filled = []
    j = 0  # indice para bits de dados
    k = 1  # posicao no array com bits de paridade
    
    for i in range(1, len(binary_message) + num_parity_bits + 1):
        if i == 2 ** (k - 1):        # verifica se a posicao e uma potencia de dois
            parity_zero_filled.append(0)
            k += 1
        else:
            parity_zero_filled.append(binary_message[j])
            j += 1


    # para cada bit de paridade, calcula o seu valor (1 ou 0) e insere no array final
    for i in range(num_parity_bits):
        potencia_de_dois = 2 ** i           # potencia de dois correspondente à posição (bit de paridade 0 -> 2 ** 0 = 1)
        bit_paridade = calcular_bit_paridade(parity_zero_filled, potencia_de_dois)
        parity_zero_filled[potencia_de_dois - 1] = bit_paridade     # insere na posicao da potencia de dois (-1 para contar desde indice 0) o respectivo bit de paridade dessa potencia
    
    return parity_zero_filled


# RECEPTOR
def receive_hamming(binary_message_with_parity, additional_bits_list):
    # numero de bits de paridade (r): 2**r >= m + r + 1
    num_parity_bits = 0
    while (2 ** num_parity_bits) < (len(binary_message_with_parity)):
        num_parity_bits += 1

    # inicializa a lista para armazenar os bits de paridade extraídos da mensagem
    parity_bits = [0] * num_parity_bits

    # percorre a mensagem, verificando e ajustando os bits de paridade
    for i in range(num_parity_bits):
        potencia_de_dois = 2 ** i           # Calcula a posição da potência de dois (posição do bit de paridade)
        bit_paridade_calculado = calcular_bit_paridade(binary_message_with_parity, potencia_de_dois)
        parity_bits[i] = bit_paridade_calculado

    # verifica se há algum erro na codificação de Hamming
    erro_posicao = sum([bit * (2 ** idx) for idx, bit in enumerate(parity_bits)])

    if erro_posicao == 0:
        print("Sem erros.")
    else:
        print(f"Erro detectado na posição {erro_posicao}.")
        # corrige o erro invertendo o bit na posição identificada
        binary_message_with_parity[erro_posicao - 1] ^= 1
        print(f"Erro corrigido na posição {erro_posicao}.")

    # retorna a mensagem corrigida
    return binary_message_with_parity
