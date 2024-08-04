# Error Detection using Parity
def generate_parity(data):
    return data + str(data.count('1') % 2)

def check_parity(data):
    return data[:-1], data[-1] == str(data[:-1].count('1') % 2)

# Error Detection using CRC
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