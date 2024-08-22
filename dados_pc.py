from datetime import datetime
from pathlib import Path
import os


def criar_dados_pc(login, cargo, nome_de_guerra, om, senha):
    ano = datetime.now().year
    mes = datetime.now().month
    dia = datetime.now().day

    # Obter o caminho da pasta "Documents"
    documents_path = Path(os.path.expanduser("~/Documents"))

    # Definir o caminho para a nova pasta e o arquivo
    new_folder = documents_path / f"{dia}-{mes}-{ano}/{cargo} {nome_de_guerra} - {om}"
    new_file = new_folder / f"{cargo} {nome_de_guerra} - {om}.txt"

    # Criar a nova pasta (usando exist_ok=True para evitar erros se já existir)
    new_folder.mkdir(parents=True, exist_ok=True)

    # Conteúdo a ser escrito no arquivo
    conteudo = f"\n\nlogin: {login}\nsenha: {senha}"

    # Criar o arquivo .txt (abrir em modo de escrita 'w')
    with new_file.open('w') as file:
        file.write(conteudo)
