from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.action_chains import ActionChains
import time


def iniciar_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver


def configuracao_inicial(driver):
    try:
        # Acessar a página de login do pfSense
        driver.get("http://192.168.0.111/index.php")

        # Esperar que o campo de username esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "usernamefld"))
        )

        # Fazer login
        driver.find_element(By.ID, "usernamefld").send_keys("admin")
        driver.find_element(By.ID, "passwordfld").send_keys("67yuhjnm")
        driver.find_element(By.NAME, "login").click()

        # Esperar que a página principal seja carregada
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "widget-system_information-0_panel-body"))
        )
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erro ao tentar fazer login: {e}")
        driver.quit()
        return False
    return True


def usuario_existe(driver, user_name):
    try:
        # Navegar até a seção de Usuários
        driver.get("http://192.168.0.111/system_usermanager.php")

        # Esperar até que a tabela esteja presente na página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "panel-body"))
        )

        # Encontrar todos os elementos <td> na segunda coluna onde os usernames estão
        usernames = driver.find_elements(By.XPATH, "//table/tbody/tr/td[2]")

        # Verificar se algum <td> contém exatamente o username desejado
        for username in usernames:
            if username.text.strip() == user_name:
                print(f"Username '{user_name}' encontrado na página.")
                return True

        print(f"Username '{user_name}' não encontrado na página.")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erro ao verificar existência do usuário: {e}")

    return False


def verifica_certificado_valido(driver, user_name):
    try:
        # Acessar a página de gerenciamento de certificados
        driver.get("http://192.168.0.111/system_certmanager.php")

        # Localizar o campo de pesquisa e inserir o nome do usuário
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchstr"))
        )
        search_field.send_keys(user_name)

        # Clicar no botão de pesquisa
        search_button = driver.find_element(By.ID, "btnsearch")
        search_button.click()

        # Esperar que a tabela seja carregada
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )

        # Buscar os certificados do usuário
        certificates = table.find_elements(By.TAG_NAME, "tr")

        time.sleep(2)

        # Variáveis para verificar se o certificado foi encontrado e é válido
        found_any = False
        cert_valido = False

        for certificate in certificates:
            # Encontrar o nome do usuário na linha específica
            username = certificate.find_element(By.XPATH, ".//td[1]").text.split('\n')[0]

            if username == user_name:
                found_any = True

                # Verificar o status do certificado
                validade_elemento = certificate.find_element(By.XPATH, ".//small/span[@data-toggle='tooltip']")
                validade_texto = validade_elemento.text.strip()
                status = "Expirado" if "text-danger" in validade_elemento.get_attribute("class") else "Válido"

                if status == "Válido":
                    cert_valido = True

                # # Verificar se o certificado está vencido
                # if "text-danger" in validade_elemento.get_attribute("class"):
                #     status = "Expirado"
                # else:
                #     status = "Válido"
                #     cert_valido = True

                print(f"Certificado: {username}, Validade: {validade_texto}, Status: {status}")

        if not found_any:
            print(f"Certificado '{user_name}' não encontrado na página.")

        return cert_valido

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Erro ao verificar certificado: {e}")
        return False


def desvincular_certificado(driver):
    # Esperar até que a tabela esteja presente na página
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ipsecpsk"))
    )
    try:
        # Localiza o elemento pelo ID e clica nele
        botao_delcert0 = driver.find_element(By.ID, "delcert0")
        botao_delcert0.click()

        # Aguardar brevemente para o alert aparecer
        time.sleep(2)  # Ajuste conforme necessário

        # Interage com o alerta de confirmação se ele aparecer
        try:
            alert = Alert(driver)
            alert.accept()  # Confirma a exclusão
            print("Alerta de confirmação aceito.")
        except Exception as e:
            print("Nenhum alerta de confirmação foi encontrado.")

        print("Clique realizado com sucesso no botão delcert0.")

    except Exception as e:
        print(f"Erro ao clicar no botão delcert0: {e}")


def criar_certificado(driver, user_name):
    try:
        # Localizar e clicar no botão "Add"
        button_add = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/form/div[3]/div[2]/div/div/nav/a"))
        )
        button_add.click()

        time.sleep(5)

        # Esperar até que o formulário de certificado esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "lifetime"))
        )

        # Preencher o tempo de vida do certificado
        lifetime = driver.find_element(By.ID, "lifetime")
        lifetime.clear()
        lifetime.send_keys("365")

        # Esperar até que o formulário de certificado esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dn_commonname"))
        )

        # Preencher o nome comum (Common Name)
        common_name = driver.find_element(By.ID, "dn_commonname")
        common_name.send_keys(user_name)

        # Localizar e clicar no botão "Save"
        button_save = driver.find_element(By.ID, "save")
        button_save.click()

        print("Certificado criado com sucesso para o usuário:", user_name)

    except TimeoutException:
        print("O tempo de espera foi excedido ao tentar criar o certificado.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar o certificado: {e}")


def encontrar_user_and_editar(driver, user_name):
    try:
        # Navegar até a seção de Usuários
        driver.get("http://192.168.0.111/system_usermanager.php")

        # Esperar até que a tabela esteja presente na página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )

        # Encontrar todas as linhas da tabela
        linhas = driver.find_elements(By.XPATH, "//table/tbody/tr")

        # Iterar sobre cada linha para verificar o username
        for linha in linhas:
            # Selecionar o <td> que contém o username (segunda coluna)
            username = linha.find_element(By.XPATH, "./td[2]").text.strip()

            if username == user_name:
                # Encontrar o link "Edit user" na mesma linha e clicar
                edit_link = linha.find_element(By.XPATH, "./td[6]/a[@title='Edit user']")
                edit_link.click()
                print(f"Username '{user_name}' encontrado e botão 'Edit user' clicado.")
                return True

        print(f"Username '{user_name}' não encontrado na página.")
        return False

    except TimeoutException:
        print("A página demorou muito para carregar ou a tabela de usuários não foi encontrada.")
    except NoSuchElementException as e:
        print(f"Elemento não encontrado: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    return False


def deletar_certificado(driver, user_name):
        # Acessar a página de gerenciamento de certificados
        driver.get("http://192.168.0.111/system_certmanager.php")

        # Localizar o campo de pesquisa e inserir o nome do usuário
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchstr"))
        )
        search_field.send_keys(user_name)
        time.sleep(2)
        # Clicar no botão de pesquisa
        search_button = driver.find_element(By.ID, "btnsearch")
        search_button.click()
        time.sleep(2)
        # Esperar que a tabela seja carregada
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
        time.sleep(5)

        try:
            # Encontra a linha que contém o nome de usuário
            user_row = driver.find_element(By.XPATH, f"//tr[td[contains(text(), '{user_name}')]]")

            # Tenta encontrar o ícone de deletar na linha do usuário
            try:
                delete_icon = user_row.find_element(By.CSS_SELECTOR, "a.fa.fa-trash")
            except NoSuchElementException:
                print(f"Ícone de deletar não encontrado para o usuário '{user_name}'.")
                return

            # Se o ícone for encontrado, clica nele
            ActionChains(driver).move_to_element(delete_icon).click().perform()

            # Confirma a exclusão, caso apareça um popup de confirmação
            try:
                driver.switch_to.alert.accept()
                print(f"Usuário '{user_name}' deletado com sucesso.")
            except NoSuchElementException:
                print("Nenhum popup de confirmação encontrado.")

        except NoSuchElementException:
            print(f"Usuário '{user_name}' não encontrado.")


def criar_user_and_vpn(driver, user_name, password, cargo, nome_guerra, om):
    try:
        # Navegar até a seção de Usuários
        driver.get("http://192.168.0.111/system_usermanager.php")

        # Esperar e clicar no botão para adicionar um novo usuário
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-sm.btn-success"))
        )
        add_button.click()

        # Preencher os campos de criação de usuário
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "usernamefld"))
        ).send_keys(user_name)

        driver.find_element(By.ID, "passwordfld1").send_keys(password)
        driver.find_element(By.ID, "passwordfld2").send_keys(password)

        # Preencher o campo de Full Name
        driver.find_element(By.ID, "descr").send_keys(f"{cargo} {nome_guerra} - {om}")

        # Marcar a opção para gerar o certificado VPN
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "showcert"))
        ).click()

        # Preencher os campos de geração do certificado
        driver.find_element(By.ID, "name").send_keys(user_name)

        lifetime = driver.find_element(By.ID, "lifetime")
        lifetime.clear()
        lifetime.send_keys("365")

        # Clicar no botão para salvar o novo usuário e o certificado
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "save"))
        ).click()

        print(f"Usuário '{user_name}' criado com sucesso e certificado VPN gerado.")

    except TimeoutException:
        print("Erro: O tempo de espera foi excedido para um ou mais elementos.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def exportar_certificado(driver, user_name, download_folder):
    try:
        # Configurar o Chrome para salvar arquivos automaticamente
        driver.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow',
            'downloadPath': download_folder
        })

        # Navegar até a seção de importar certificados
        driver.get("http://192.168.0.111/vpn_openvpn_export.php")

        # Esperar o campo de busca estar visível e buscar pelo usuário
        search_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "searchstr"))
        )
        search_box.send_keys(user_name)

        # Clicar no botão para buscar o certificado do usuário
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnsearch"))
        )
        search_button.click()

        # Esperar até que o botão "Most Clients" esteja presente e clicável
        botao_download = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Most Clients')]"))
        )
        botao_download.click()

        # Esperar um tempo para garantir que o download seja iniciado
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'fa-download')]"))
        )

        print("Download iniciado com sucesso.")

    except TimeoutException:
        print("Erro: O tempo de espera foi excedido para um ou mais elementos.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
