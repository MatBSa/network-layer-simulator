

class Transmissor:
    def __init__(self, received_text: str, host="localhost", port=8888):
        self.host = host
        self.port = port
        self.received_text = received_text
        self.bit_arrray = self.__text_2_binary(received_text) 
    def __text_2_binary(self,text): # converter para binário
        bits_str = ''
        for byte in text.encode('utf8'):
            byte = f'{byte:08b}' # converte o byte para uma string
            bits_str += byte
        return[int(bit) for bit in bits_str] #retorna uma lista de bits
    def run(self, encoding_method, framing_method, error_correction_or_detection_method,  modulation_method):
        self.encoded_bits = self.coder(encoding_method)
        match encoding_method.lower():
            case "bipolar": # 0 -> 0; -1 ou 1 -> 1
                self.encoded_bits_cleaned = [0 if (b == 0) else 1 for b in self.encoded_bits]
                
        match framing_method.lower():
            case "character_count":
                self.frames = self.character_count_framing(
                    self.encoded_bits_cleaned, 8)
            case "byte_insertion":
                self.frames = self.bytes_insertion_framing(
                    self.encoded_bits_cleaned, 8)
            case "bits_insertion":
                self.frames = self.bits_insertion_framing(
                    self.encoded_bits_cleaned, 8)

        match error_correction_or_detection_method.lower():
            case "even_parity":
                self.frames_final = self.adjust_frames_even_parity(
                    self.frames, framing_method)
            case "crc":
                self.frames_final = self.adjust_frames_crc(
                    self.frames, framing_method)
            case "hamming":
                self.frames_final = self.adjust_frames_hamming(
                    self.frames, framing_method)

    # convert the frames matrix to a big bit vector
        bits_vector = [bit for frame in self.frames_final for bit in frame]
        match modulation_method.lower():
            case "ask":
                self.sinal = self.ASK(1, 1, bits_vector)
            case "fsk":
                self.sinal = self.FSK(1, 1, 2, bits_vector)
            case "8qam":
                self.sinal = self.QAM(1, 1, 2, bits_vector)
        self.send_message(self.sinal)
        return self.bit_arrray, self.encoded_bits, self.sinal
    def coder(self, encoding_method):
        match encoding_method.lower():
            case "bipolar":
                return self.polar_nrz_coder(self.bit_arrray)
    
    # Bipolar METHOD
    def metodo_bipolar(self, bit_array):
        output = bit_array.copy()
        flip = False
        for i, bit in enumerate(output):
            if bit == 1 and not flip:
                output[i] = 1
                flip = not flip
            elif bit == 1 and flip:
                output[i] = -1
                flip = not flip
        return output
    
    # 8QAM METHOD
    
