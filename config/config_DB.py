from dotenv import load_dotenv 
from pathlib import Path
import os

load_dotenv()

nome_do_banco_de_dados = os.getenv('NOME_DO_BANCO')

# endereço da pasta atual
caminho_do_arquivo = Path(__file__).parent.parent

# configuração do Banco de Dados
class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{caminho_do_arquivo}\\{nome_do_banco_de_dados}' # 
    SQLALCHEMY_TRACK_MODIFICATIONS = False # rastrear modificações em objetos
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret") # criptografia (token)
    JWT_BLACKLIST_ENABLED  = True # lista negra de token

'''
Outras configurações:
    'sqlite:///nome_do_banco'
    'mysql://username:password@localhost:3306/nome_do_banco'
    'postgresql://username:password@localhost:5432/nome_do_banco'
'''