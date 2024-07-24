# Network Layer Simulator

## Descrição

Este projeto é um simulador das camadas de enlace e física de redes, implementado em Python. Ele simula protocolos de modulação digital e por portadora, além de enquadramento, detecção e correção de erros. Este trabalho é para aplicação prática das teorias aprendidas na disciplina de Teleinformática e Redes 1 da Universidade de Brasília - UnB.

## Funcionalidades

### Camada Física
- **Modulação Digital:**
  - NRZ-Polar
  - Manchester
  - Bipolar
- **Modulação por Portadora:**
  - Amplitude Shift Keying (ASK)
  - Frequency Shift Keying (FSK)
  - 8-Quadrature Amplitude Modulation (8-QAM)

### Camada de Enlace
- **Enquadramento de Dados:**
  - Contagem de caracteres
  - Inserção de bytes ou caracteres
- **Detecção de Erros:**
  - Bit de paridade par
  - CRC (polinômio CRC-32, IEEE 802)
- **Correção de Erros:**
  - Hamming