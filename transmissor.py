import socket
from camada_enlace import generate_parity, generate_crc

def transmissor(data, use_crc, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))

    try:
        print(f"Original data: {data}")

        if use_crc:
            data_with_crc = generate_crc(data, "1101")
            print(f"Data with CRC: {data_with_crc}")
            client_socket.sendall(data_with_crc.encode())
        else:
            data_with_parity = generate_parity(data)
            print(f"Data with Parity: {data_with_parity}")
            client_socket.sendall(data_with_parity.encode())

        response = client_socket.recv(1024).decode()
        print(f"Resposta do servidor: {response}")

    finally:
        client_socket.close()
