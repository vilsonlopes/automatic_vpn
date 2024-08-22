import secrets
import string


def gerar_senha(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha
