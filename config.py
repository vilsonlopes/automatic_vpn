
def obter_dados_usuario():
    LOGIN = input("Digite é o login: ").lower()
    CARGO = input("Qual é o cargo: ").upper()
    NOME_DE_GUERRA = input("Digite o nome de guerra: ").upper()
    OM = input("Digite a organização militar (OM): ").upper()
    EMAIL = f"{LOGIN}@fab.mil.br"

    return LOGIN, CARGO, NOME_DE_GUERRA, OM, EMAIL
