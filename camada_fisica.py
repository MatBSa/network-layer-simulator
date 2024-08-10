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