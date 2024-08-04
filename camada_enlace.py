# Error Detection using Parity
def generate_parity(data):
    return data + str(data.count('1') % 2)

def check_parity(data):
    return data[:-1], data[-1] == str(data[:-1].count('1') % 2)