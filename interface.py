import streamlit as st
import numpy as np
import os
from camada_fisica import (qam8, bipolar_nrz, polar_nrz, ask, fsk, plot_signal, manchester, binary_conversor, plot_signal_8qam, plot_signal_bip)
from camada_enlace import (char_count, byte_insert, bit_insert, check_crc, generate_parity, generate_crc, check_parity)

# Função para carregar e exibir a imagem
def exibir_imagem(caminho):
    st.image(caminho, use_column_width=True)

# Título da aplicação
st.title("Simulador Camada Física e de Enlace")

# Barra lateral (Esquerda) - Transmissor e Modulador
message = st.text_input("Digite a mensagem a ser transmitida:")

# Escolha da codificação de linha
line_code = st.selectbox("Escolha o tipo de codificação:", ["NRZ", "Manchester", "Bipolar"])

# Seção Modulador
modulacao = st.selectbox("Escolha o tipo de Modulação:", ["ASK", "FSK", "8-QAM"])

# Botão para criar o sinal
if st.button("Criar Sinal"):
    # Converte a mensagem em binário
    binary_message = binary_conversor(message)
    binary_message_str = ''.join(map(str, binary_message))

    # Aplicando a codificação
    if line_code == "NRZ":
        coded_signal = polar_nrz(binary_message)
    elif line_code == "Manchester":
        coded_signal = manchester(binary_message)
    elif line_code == "Bipolar":
        coded_signal = bipolar_nrz(binary_message_str)

    st.write(f"Sinal codificado ({line_code})")

    # Aplicando a modulação
    if modulacao == "ASK":
        modulated_signal = ask(coded_signal)
    elif modulacao == "FSK":
        modulated_signal = fsk(coded_signal)
    elif modulacao == "8QAM":
        modulated_signal = qam8(coded_signal)

    st.write(f"Sinal modulado ({modulacao})")

    # Plotando o gráfico do sinal modulado
    if modulacao == "8QAM":
        plot_signal_8qam(binary_message_str, modulated_signal, title=f"Sinal modulado - {modulacao}")
    elif modulacao == "ASK":
        plot_signal(binary_message_str, modulated_signal, title=f"Sinal modulado - {modulacao}")
    elif modulacao == "FSK":
        plot_signal(binary_message_str, coded_signal, title=f"Sinal modulado - {modulacao}")

    # Exibindo a imagem gerada
    exibir_imagem("signal.png")