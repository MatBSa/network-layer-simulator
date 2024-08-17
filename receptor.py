import socket
from camada_enlace import check_parity, check_crc

def receptor():
    # Configurando o socket do servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8002))
    server_socket.listen(1)

    print("Aguardando conexão...")
    connection, address = server_socket.accept()
    print(f"Conexão estabelecida com {address}")

    try:
        data = connection.recv(1024).decode()
        print(f"Dados recebidos: {data}")

        # Verificando CRC
        polynomial = "1101"  # Exemplo de polinômio
        crc_valid = check_crc(data, polynomial)
        print(f"CRC Valid: {crc_valid}")

        # Verificando Paridade
        if crc_valid:
            data_without_crc = data[:-len(polynomial) + 1]
            checked_data, parity_valid = check_parity(data_without_crc)
            print(f"Checked Data: {checked_data}, Parity Valid: {parity_valid}")

            if parity_valid:
                response = "Dados recebidos corretamente"
            else:
                response = "Erro na paridade"
        else:
            response = "Erro no CRC"

        connection.sendall(response.encode())

    finally:
        connection.close()
        server_socket.close()

if __name__ == "__main__":
    receptor()
