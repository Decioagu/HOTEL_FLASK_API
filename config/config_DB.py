from dotenv import load_dotenv 
from pathlib import Path
import os

load_dotenv()

nome_do_banco_de_dados = os.getenv('NOME_DO_BANCO')

# endereço da pasta atual
# caminho_do_arquivo = Path(__file__) # ver caminho do arquivo executado
# basedir = os.path.abspath(os.path.dirname(caminho_do_arquivo.parent))

# configuração do Banco de Dados
class Config:
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, nome_do_banco_de_dados) # tipo de banco
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost:3306/nome_do_banco'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # rastrear modificações em objetos
    JWT_SECRET_KEY = 'DontTellAnyone' # criptografia (token)
    JWT_BLACKLIST_ENABLED  = True # lista negra de token

'''
"SQLALCHEMY_DATABASE_URI" outras configurações:
    'sqlite:///nome_do_banco'
    'mysql://username:password@localhost:3306/nome_do_banco'
    'postgresql://username:password@localhost:5432/nome_do_banco'
'''
""" 
JWT_BLACKLIST_ENABLED:
Quando essa configuração está ativada, sua aplicação permite adicionar tokens a uma blacklist, 
de forma que, mesmo que o token JWT seja válido (não expirado e corretamente assinado), 
ele será rejeitado se estiver na lista negra. Isso é útil para casos como:

    - Logout: Ao fazer logout, o token do usuário pode ser colocado na blacklist para que ele 
      não possa mais usá-lo.
    - Revogação de privilégios: Se você quiser revogar o acesso de um usuário antes do 
      token expirar, você pode colocá-lo na blacklist.
    - Segurança: Caso um token tenha sido comprometido ou usado de maneira suspeita, 
      ele pode ser invalidado imediatamente.
"""