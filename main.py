import pdfplumber
import pandas as pd
import zipfile
import os

# Definições
PDF_FILE = "/anexoI.pdf"
CSV_FILE = "Tabela_Procedimentos.csv"
ZIP_FILE = "C:/Estudos/IntuitiveCare/testsPython/Teste_igor_dos_santos_coelho.zip"
ABREVIACOES = {"OD": "Odontológico", "AMB": "Ambulatorial"}  # Substituições

# Função para extrair tabelas do PDF
def extrair_tabela(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                data.extend(tables)
    return data

# Extraindo a tabela
tabela = extrair_tabela(PDF_FILE)

# Criando DataFrame
df = pd.DataFrame(tabela[1:], columns=tabela[0])  # A primeira linha é o cabeçalho

# Substituindo abreviações
df.replace(ABREVIACOES, inplace=True)

# Salvando em CSV
df.to_csv(CSV_FILE, index=False, encoding='utf-8')

# Compactando em ZIP
with zipfile.ZipFile(ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(CSV_FILE)

# Removendo CSV original após compactação
os.remove(CSV_FILE)

print(f"Arquivo {ZIP_FILE} criado com sucesso!")