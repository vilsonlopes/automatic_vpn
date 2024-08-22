import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import mimetypes
from decouple import config

from config import EMAIL
from config import LOGIN


# Configurações do servidor SMTP do Zimbra
smtp_host = 'smtp.fab.mil.br'  # Substitua pelo host SMTP do seu Zimbra
smtp_port = 587  # Porta SMTP
smtp_user = 'vilsonvls@fab.mil.br'  # Substitua pelo seu e-mail
smtp_password = config('EMAIL_PASSWORD')  # Substitua pela sua senha

# Configuração do e-mail
from_email = 'vilsonvls@fab.mil.br'
to_email = EMAIL
subject = 'Certificado VPN'
body = '''
<html>
<head></head>
<body>
    <div style="font-size: 12pt; font-family: &quot;arial&quot;, &quot;helvetica&quot;, sans-serif; color: rgb(0, 0, 0);">
        <div>
            <div style="font-family: &quot;arial&quot;, &quot;helvetica&quot;, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">
                <div>Prezado(a),</div>
                <br>
                <div>Conforme solicitado, segue em anexo o certificado VPN, tutorial para instalação e senha.</div>
            </div>
            <div>
                <span style="color: rgb(255, 0, 0);">OBS: Informo que a instalação do certificado mudou, caso tenha a versão anterior desinstalar e seguir o tutorial.</span>
            </div>
            <div style="font-family: &quot;arial&quot;, &quot;helvetica&quot;, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);"><br></div>
            <div style="font-family: &quot;arial&quot;, &quot;helvetica&quot;, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">Atenciosamente,</div>
            <div style="font-family: &quot;arial&quot;, &quot;helvetica&quot;, sans-serif; font-size: 12pt; color: rgb(0, 0, 0);">&nbsp;</div>
        </div>
        <br>
        <br>
        <div data-safe-id="signature-content-dc2b1fcb-2f48-400a-9914-2ff4e61b166c">
            <table cellpadding="3px" border="1" style="width: 536.219px;">
                <tbody>
                    <tr>
                        <td style="width: 96.125px;">
                            <img data-cid="null" height="113" width="90" src="D:/Desenvolvimento/Testes/brincando_com_python/nccabr.png">
                        </td>
                        <td style="width: 416.094px;">
                            <strong>3º SGT Vilson Lopes da Silva</strong>
                            <br>Centro de Computação da Aeronáutica de Brasília
                            <br>Seção de Serviços Internos
                            <br>(61) 2023-1708
                        </td>
                    </tr>
                </tbody>
            </table><br>
        </div>
    </div><br>

</body>
</html>
'''

# Criação da mensagem MIME
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'html'))  # Usar 'html' ao invés de 'plain'

# Lista de arquivos a serem anexados
file_paths = [
    'C:/Users/vilso/Documents/17-8-2024/3S VILSON - CCA BR/3S VILSON - CCA BR.txt',
    'C:/Users/vilso/Documents/17-8-2024/3S VILSON - CCA BR/Tutorial Linux.pdf',
    'C:/Users/vilso/Documents/17-8-2024/3S VILSON - CCA BR/Tutorial MacOS.pdf',
    'C:/Users/vilso/Documents/17-8-2024/3S VILSON - CCA BR/Tutorial Windows.pdf',
    f'C:/Users/vilso/Documents/17-8-2024/3S VILSON - CCA BR/VPN_CORPORATIVA-UDP4-28391-{LOGIN}-config.ovpn'
]


# Função para adicionar um anexo ao e-mail
def anexar_arquivo(msg, file_path):
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)

    # Se o tipo MIME não puder ser determinado, usar 'application/octet-stream'
    if mime_type is None:
        mime_type = 'application/octet-stream'

    main_type, sub_type = mime_type.split('/', 1)

    try:
        with open(file_path, 'rb') as attachment_file:
            # Cria a parte MIMEBase para o anexo
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(attachment_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f'attachment; filename="{file_name}"')
            msg.attach(attachment)
    except Exception as e:
        print(f"Erro ao anexar o arquivo {file_name}: {e}")


# Adiciona cada arquivo à mensagem
for file_path in file_paths:
    anexar_arquivo(msg, file_path)

try:
    # Conectando ao servidor SMTP
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()  # Inicia a conexão segura
    server.login(smtp_user, smtp_password)

    # Enviando o e-mail
    server.sendmail(from_email, to_email, msg.as_string())
    print("E-mail enviado com sucesso!")

except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")

finally:
    server.quit()  # Fecha a conexão com o servidor
