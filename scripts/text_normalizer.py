import unicodedata
import os

def limpar_arquivo(input_file, output_file):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"O arquivo {input_file} não foi encontrado!")

    with open(input_file, 'r', encoding='utf-8') as f:
        texto = f.read()
    
    texto_normalizado = unicodedata.normalize('NFD', texto)
    texto_ascii = "".join([c for c in texto_normalizado if not unicodedata.combining(c)])
    texto_final = texto_ascii.encode('ascii', 'ignore').decode('ascii')
    
    with open(output_file, 'w', encoding='ascii') as f:
        f.write(texto_final)

input_path = os.path.join('data', 'input_raw.txt')
output_path = os.path.join('data', 'input_clean.txt')

limpar_arquivo(input_path, output_path)
print("Arquivo convertido com sucesso para ASCII puro!")