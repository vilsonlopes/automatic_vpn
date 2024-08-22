import time

import criar_user_and_vpn
from config import obter_dados_usuario
from dados_pc import criar_dados_pc
from gerador_senha import gerar_senha


# Dados iniciais de entrada
login, cargo, nome_de_guerra, om, email = obter_dados_usuario()

# Senha usada para criar vpn
senha_gerada = gerar_senha()

# Cria pastas e arquivo .txt
criar_dados_pc(login, cargo, nome_de_guerra, om, senha_gerada)

if __name__ == "__main__":
    driver = criar_user_and_vpn.iniciar_driver()
    if criar_user_and_vpn.configuracao_inicial(driver):
        if criar_user_and_vpn.usuario_existe(driver, login):
            if criar_user_and_vpn.verifica_certificado_valido(driver, login):
                print("O usuário tem certificado válido. Verificar manualmente")
                driver.quit()
        else:
            criar_user_and_vpn.criar_user_and_vpn(driver, login, senha_gerada, cargo, nome_de_guerra, om)
            time.sleep(3)
            criar_user_and_vpn.exportar_certificado(driver, login, new_folder)

    driver.quit()
