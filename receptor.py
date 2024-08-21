import socket
from camada_enlace import check_parity, check_crc

def receptor(use_crc, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)

    print("Aguardando conexão...")
    connection, address = server_socket.accept()
    print(f"Conexão estabelecida com {address}")

    try:
        data = connection.recv(1024).decode()
        print(f"Dados recebidos: {data}")

        if use_crc:
            crc_valid = check_crc(data, "1101")
            print(f"CRC Valid: {crc_valid}")
            response = "Dados recebidos corretamente" if crc_valid else "Erro no CRC"
        else:
            checked_data, parity_valid = check_parity(data)
            print(f"Checked Data: {checked_data}, Parity Valid: {parity_valid}")
            response = "Dados recebidos corretamente" if parity_valid else "Erro na paridade"

        connection.sendall(response.encode())

    finally:
        connection.close()
        server_socket.close()
