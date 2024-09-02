import numpy as np
from camada_fisica import binary_conversor, text_conversor


############################## camada de enlace ##############################
# fornecer servicos a camada fisica:
#   - recebe pacotes da camada de rede, os encapsula em quadros (cabecalho, carga util, final) para transmissao
#   1. deteccao e correcao de erros
#   2. regulacao do fluxo de dados
#   3. fornecer interface bem definida a camada fisica


############################## transmissor ##############################


############################## enquadramento ##############################
# contagem de caracteres:
#   1. campo no cabeçalho especifica número de bytes no quadro (tamanho do quadro)
#   2. camada de destino sabe quantos bytes o quadro contém - onde está o seu fim
 
# cada metodo abaixo:
#   - realiza o enquadramento de acordo com o metodo e tamanho de quadro escolhido
#   - retorna uma lista de quadros, em que cada quadro e uma lista com os bytes contidos em strings ['cabecalho', 'carga_util', 'final']
# ex: quadros = [['01111110', '01011010', '01111110'], ['01111110', '01011010', '01111110'], ['01111110', '01011010', '01111110']]

# contagem de caracteres 
# adiciona no cabecalho o tamanho do quadro (numero de bytes)
# 0. divide a lista de bits em bytes (ja em decimal)
# 1. ate que a lista esvazie, indo de n_bytes_por_quadro em n_bytes_por_quadro
# 2. calcula tamanho do quadro -> minimo(bytes restantes e n_bytes_por_quadro)
#   - caso esteja restando menos bytes do que o tamanho de quadro definido, adiciona assim mesmo
#   - depois adicionamos bits adicionais para tratar isso e garantir n_bits_totais divisivel por 8 por quadro
def char_count(n_bytes_per_frame, binary_message):
    binary_message = ''.join(str(bit) for bit in binary_message)
    bytes = [int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8)]
    frames = []
    
    for i in range(0, len(bytes), n_bytes_per_frame - 1):
        if i > len(bytes):
            break
        len_frame = min(len(bytes) - i, n_bytes_per_frame - 1)
        frame = [f"{format(len_frame + 1, '08b')}"] + [f"{format(byte, '08b')}" for byte in bytes[i:i + len_frame]]  # +1 contando cabecalho
        frames.append(frame)
        
    return frames


# insercao de bytes
# insere bytes de flag no comeco e no fim de cada quadro - garantir ressincronizacao apos um erro de bit (problema da contagem de char)
# 0. ate que a lista esteja vazia, de tamanho_quadro em tamanho_quadro
# 1. o minimo garante que o tamanho maximo de cada quadro nao sera excedido
#    o numero de bytes remanescentes no minimo garante que, mesmo que haja uma quantidade de bytes menor que a definida por quadro, eles sejam enquadrados
# 2. enquadra bits como flag + bits_dos_bytes_do_quadro + flag 
def byte_insert(n_bytes_per_frame, binary_message, flag='01111110'):
    binary_message = ''.join(str(bit) for bit in binary_message)
    bytes = [int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8)]
    frames = []
    
    for i in range(0, len(bytes), n_bytes_per_frame - 2):
        # calcula o tamanho de cada quadro
        
        if (n_bytes_per_frame - 2) < (len(bytes) - i):
            len_frame = n_bytes_per_frame - 2
        else:
            len_frame = len(bytes) - i

        frame = [flag] + [f"{format(byte, '08b')}" for byte in bytes[i:i + len_frame]]  + [flag] 
        frames.append(frame)
        
    return frames


# inserção de bits:
#   1. contorna limitação da inserção de bytes (fato de usar 8 bits)
#   2. enquadramento pode ser feito a nível de bits - quadros de qualquer tamanho
#   3. cada quadro começa e termina com um padrão de bits especial 01111110
#   4. essa sequência de bit especial é um byte de flag
#   5. evitar a ocorrência da sequência de bits especiais na carga útil
#   sempre que ocorre sequência de 5 bits '1', é inserido um bit '0' após ela

# insercao de bits
# contorna limitacao da insercao de bytes (fato de limitar-se em quadros multiplos de 8 (em numero de bits), com bytes de 8 bits)
# cada quadro comeca e termina com flag
# evitar flag na carga util -> a cada sequencia de 5 1s consecutivos, adiciona um 0
def bit_insert(n_bits_per_frame, binary_message, flag='01111110'):
    frames = []
    # percorre toda a binary_message, de n_bits_por_quadro em n_bits_por_quadro que queremos
    for i in range(0, len(binary_message), n_bits_per_frame):
        # constroi o quadro transformando os n bits atuais que queremos (binary_message[i:i+n_bits_per_frame]) no quadro em uma string 
        # ja adiciona a flag no comeco e no fim do quadro
        frame = flag + ''.join(str(bit) for bit in binary_message[i:i+n_bits_per_frame]) + flag
        frames.append(frame)
        
    return frames


############################## receptor ##############################


############################## desenquadrar ##############################


# cada metodo abaixo:
# 1. apos o enquadramento, obtem apenas a carga util de cada quadro, removendo flags e char counts
# 2. retorna uma lista de quadros, em que cada quadro e uma string de bits (carga util daquele quadro)
# 3. remove os bits adicionados para manter a multiplicidade por 8 e os retorna (em decimal)

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


def get_byte_insert_frames_bits(binary_message, flag='01111110'):
    str_frames_without_flags, additional_bits, frame = list(), list(), list()
    byte_units = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    bytes = [''.join(str(bit) for bit in byte) for byte in byte_units]

    for byte in bytes:
        if byte != flag:
            frame.append(byte)
        else:
            if frame:                       # byte eh flag e frame nao esta vazio -> flag final
                add_bits = int(frame[0], 2) # primeiro byte diferente de flag do quadro -> bits adicionais
                additional_bits.append(add_bits)
                
                str_frame_without_flag = ''.join(frame[1:]) # bytes do quadro -> string unica de bits do quadro
                str_frames_without_flags.append(str_frame_without_flag)
                frame.clear()        

    return str_frames_without_flags, additional_bits


def get_bit_insert_frames_bits(binary_message, flag='01111110', crc=True):
    str_frames_without_flags, additional_bits, frame_bits = list(), list(), list()
    str_bits = [str(bit) for bit in binary_message]
    bits = ''.join(str_bits)
    
    i = 0                                           # para ir selecionando partes mais à frente na mensagem binária
    while i < len(bits):  
        
        if bits[i:i+len(flag)] == flag:             # e flag?
            i += len(flag)                          # selecionar os bits depois da flag (remover flag)
            
            if frame_bits:                          # se o frame não estiver vazio (fim de quadro), adiciona ele na lista de frames (como string de bits)
                str_frames_without_flags.append(''.join(frame_bits))
                frame_bits = list()
                
            # se temos flag e ja tem bytes na lista -> flag no meio 
            else:
                if not crc:                         # se não tiver correção CRC, adiciona zero
                    additional_bits.append(0)
                else:                               # se tiver CRC, remove os 8 bits adicionais logo após uma flag de início de quadro
                    add_bits = bits[i:i+8]          # pegar os próximos 8 bits de adicionais
                    add_bits = int(add_bits, 2)     # converte de binário para inteiro decimal
                    additional_bits.append(add_bits)
                    i += 8                          # avançar 8 bits após os bits adicionais
        else:                      
            frame_bits.append(bits[i])
            i += 1                                  # avançar 1 bit
    
    return str_frames_without_flags, additional_bits

    
############################## deteccao de erros ##############################

# em cada metodo abaixo:
#   1. garantimos que os quadros tenham tamanho divisivel por 8 na carga util -> lidando com bytes em insercao de bytes (8 em 8) e contagem de caracteres
#       - 1) resto da divisao do num bits da carga util por 8 -> quanto falta pra ser multiplo de 8 o num bits na carga
#       - 2) 8 - quanto falta para ser multiplo de 8 o num bits na carga = num bits a adicionar para tornar multiplo de 8 o num bits na carga
#       - 3) quanto falta % 8 = se for 8 ou 0 (resto 0) nao precisa adicionar nada, caso contrario adiciona no final [0] * quanto_falta (bits adicionais)
#   2. funcoes de forma carga util obtem a carga util de acordo com o metodo e a flag (caso haja) -> 'forma_flag_carga_util_metodo'
#   3. funcoes que adicionam bit de paridade e crc aos quadros ja com os bits adicionados para garantir a condicao acima (quadros_com_paridade_metodo e quadros_com_crc_metodo)
#   4. integra-se tudo em funcoes que, com base no metodo de enquadramento escolhido, adicionam bit de paridade ou crc de acordo (aplicar_paridade_quadros e aplicar_crc_quadros)
#   5. tudo isso usando funcoes menores que calculam paridade (generate_parity) e crc (calcula_crc32)
#   6. por fim, checar_crc32 e checar_paridade retornam os quadros originais, sem bit de paridade e crc, e uma lista de erros booleanos
#   OBS: no caso da insercao de bits apenas adiciona bit de paridade ou crc ao quadro, ja que podemos trabalhar com qualquer numero de bits no quadro

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
        
############################## calcular, aplicar e checar paridade - quadros ##############################

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


############################## aplicar, gerar e checar crc32 - quadros ##############################
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

def gerar_codigo_hamming(bit_array): # Apply the Hamming Code to the provided bit array.
    def find_len_redundant_bits(len_bits): 
        """Find the number of redundant bits required for a message of length len_bits."""
        for i in range(len_bits):
            if(2**i >= len_bits + i + 1):
                return i			
            
    def insert_zeros_parity_position(bit_array): 
        """Insert zeros in the parity positions."""
        len_redudant_bits = find_len_redundant_bits(len(bit_array))

        for i in range(len_redudant_bits):
            bit_array.insert((2**i)-1, 0)

        return bit_array		

    def calculate_parity_bit(bit_array, position): # position must be one of the power of 2 (1, 2, 4, 8, 16, ...)
        """Calculate the parity bit for the given position."""
        temp_bit_array = bit_array[position-1:]
        list_of_bits = []
        jump = False # jump must be started with False to collect the first bits of the bit_array according to the position
        for i in range(0, len(bit_array), position):
            if jump:
                jump = False
                continue

            list_of_bits.extend(temp_bit_array[i:i+position]) # if i+position is greater than the length of the temp_bit_array, it will not be a problem because the slice will be until the end of the list
            jump = True        

        parity = list_of_bits[1] # The first bit is the parity bit itself
        list_of_bits = list_of_bits[2:] # Remove the first bit because it is the 0 that was included

        for bit in list_of_bits:
            parity ^= bit

        return parity				

    def insert_parity_bits(bit_array):
        """Return the bit array with the parity bits."""
        len_redudant_bits = find_len_redundant_bits(len(bit_array))
        bit_array = insert_zeros_parity_position(bit_array)

        for i in range(len_redudant_bits):
            position = (2**i)
            bit_array[position-1] = calculate_parity_bit(bit_array, position) # position-1 because the list starts with index 0

        return bit_array
    
    return insert_parity_bits(bit_array)

def aplicar_frames_hamming(enquadramento, quadros):
    if enquadramento == 'insercao de bytes':
        return quadros_com_hamming_insercao_bytes(quadros)
    elif enquadramento == 'insercao de bits':
        return quadros_com_hamming_insercao_bits(quadros)
    elif enquadramento == 'contagem de caracteres':
        return quadros_com_hamming_contagem_char(quadros)
    else:
        raise ValueError("Método de enquadramento desconhecido")

def quadros_com_hamming_insercao_bytes(quadros):
    quadros_com_hamming = list()
    for quadro in quadros:
        flag_binary_lst, carga_util_binary_lst = forma_flag_carga_util_insercao_bytes(quadro)
        carga_util_c_hamming = gerar_codigo_hamming(carga_util_binary_lst)

        quadro_adicionado, bits_a_adicionar_binario = bits_a_adicionar_quadro_div_8(carga_util_c_hamming)

        quadros_com_hamming.append(flag_binary_lst + quadro_adicionado + flag_binary_lst)
    return quadros_com_hamming

def quadros_com_hamming_insercao_bits(quadros):
    quadros_com_hamming = list()

    for quadro in quadros:
        flag_binary_lst, carga_util_binary_lst = forma_flag_carga_util_insercao_bits(quadro)
        carga_util_c_hamming = gerar_codigo_hamming(carga_util_binary_lst)
        quadros_com_hamming.append(flag_binary_lst + carga_util_c_hamming + flag_binary_lst)
        
    return quadros_com_hamming

def quadros_com_hamming_contagem_char(quadros):
    quadros_com_hamming = list()

    for quadro in quadros:
        carga_util_binary_lst = forma_carga_util_contagem_char(quadro)
        carga_util_c_hamming = gerar_codigo_hamming(carga_util_binary_lst)

        quadro_adicionado, bits_a_adicionar_binario = bits_a_adicionar_quadro_div_8(carga_util_c_hamming)
        cabecalho_adicionado = [int(bit) for bit in bits_a_adicionar_binario]

        tamanho_do_quadro = len(quadro_adicionado) // 8
        tamanho_do_quadro_binario = format(tamanho_do_quadro + 2, '08b')
        cabecalho_do_quadro_binary_lst = [int(bit) for bit in tamanho_do_quadro_binario]

        quadros_com_hamming.append(cabecalho_do_quadro_binary_lst + cabecalho_adicionado + quadro_adicionado)

    return quadros_com_hamming

def checar_hamming(quadros, bits_adicionais):
    def find_len_redundant_bits(bit_array):
        len_bit_array = len(bit_array)
        i = 0
        while (2**i) <= len_bit_array:
            i += 1
        return i

    def calculate_parity_bit(bit_array, position):
        temp_bit_array = bit_array[position-1:]
        list_of_bits = []
        jump = False
        for i in range(0, len(bit_array), position):
            if jump:
                jump = False
                continue
            list_of_bits.extend(temp_bit_array[i:i+position])
            jump = True
        parity = list_of_bits[0]
        list_of_bits = list_of_bits[1:]
        for bit in list_of_bits:
            parity ^= bit
        return parity

    def make_correction(bit_array):
        len_redundant_bits = find_len_redundant_bits(bit_array)
        error_position = 0
        str_bin_correction = ""
        for i in range(len_redundant_bits):
            position = 2**i
            parity = calculate_parity_bit(bit_array, position)
            str_bin_correction += str(parity)
        str_bin_correction = str_bin_correction[::-1]
        try:
            error_position = int(str_bin_correction, 2)
        except ValueError:
            error_position = 0
        if error_position != 0:
            error_position -= 1
            bit_array[error_position] ^= 1
        bit_array_corrected_cleaned = [bit_array[i] for i in range(len(bit_array)) if (i+1) not in [2**i for i in range(len_redundant_bits)]]
        return bit_array_corrected_cleaned

    erros, bits_quadro_carga_util = [], []
    for quadro, bits_padding in zip(quadros, bits_adicionais):
        if bits_padding != 0:
            quadro = quadro[:-bits_padding]
        bits_array = [int(bit) for bit in quadro]
        bits_array_corrected = make_correction(bits_array)
        bits_quadro_carga_util.extend(bits_array_corrected)
        erros.append(False)

    return bits_quadro_carga_util, erros
