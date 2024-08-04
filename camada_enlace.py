# Error Detection using Parity
def generate_parity(data):
    return data + str(data.count('1') % 2)