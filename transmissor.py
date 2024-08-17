import socket
from camada_enlace import generate_parity, generate_crc

def transmissor():
    # Configurando o socket do cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8001))

    try:
        data = "1100101"  # Exemplo de dados binários
        print(f"Original data: {data}")

        # Adicionando Paridade
        data_with_parity = generate_parity(data)
        print(f"Data with Parity: {data_with_parity}")

        # Adicionando CRC
        polynomial = "1101"  # Exemplo de polinômio
        data_with_crc = generate_crc(data_with_parity, polynomial)
        print(f"Data with CRC: {data_with_crc}")

        client_socket.sendall(data_with_crc.encode())

        response = client_socket.recv(1024).decode()
        print(f"Resposta do servidor: {response}")

    finally:
        client_socket.close()  # Fechando o socket do cliente

if __name__ == "__main__":
    transmissor()
