from config.sql_alchemy import banco # ORM (Object-Relational Mapping)
import requests # método envio de email
from flask import request, url_for # método envio de email
from dotenv import load_dotenv # .env
import os # .env

load_dotenv() 

MAILGUN_DOMAIN = os.getenv('DOMINIO') 
MAILGUN_API_KEY = os.getenv('CHAVE') 
FROM_TITLE = os.getenv('TITULO') 
FROM_EMAIL = os.getenv('EMAIL') 

# atributos a ser enviados
class UsuarioModel(banco.Model):
    # ESCOPO BANCO DE DADOS
    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key = True, autoincrement=True) # id auto incrementado
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado =  banco.Column(banco.Boolean, default=False)
    '''banco.Model é equivalente a declarative_base() do SQLAlchemy'''

    # MÉTODO AUXILIAR JSON ( .resources\usuario.py = POST)
    def __init__(self, login, senha, email, ativado): 
        self.login = login
        self.senha = senha
        self.email = email 
        self.ativado = ativado 
       
    # MÉTODO AUXILIAR JSON ( .resources\usuario.py = GET, POST, PUT)
    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
            'email': self.email, ###
            'ativado' : self.ativado ###
        }
    
      # (APENAS PARA FINS DIÁDICO MÉTODO <= EXCLUIR): .resources\usuario.py = GET
    def json_senha(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
            'senha': self.senha,
            'email': self.email, 
            'ativado' : self.ativado 
        }
    
    ### método envio de email: https://login.mailgun.com/login/
    def envio_de_email(self):
        '''
        Construção do link de ativação:
        link = request.url_root[:-1] + url_for('usuarioativacao', usuario_id=self.usuario_id)

            - request.url_root: Obtém a URL base da aplicação (por exemplo, http://127.0.0.1:5000/).
            - [:-1]: Remove o último caractere (/) da URL (por exemplo, http://127.0.0.1:5000).
            - url_for: Gera a URL do endpoint
            - ('usuarioativacao', usuario_id=self.usuario_id): (nome da rota da função associado escrita em minusculo, argumentos)
                
            # Ex: http://127.0.0.1:5000/usuarios/ativacao/<int:usuario_id> #

            Ver rotas em: app.py
        '''
        # print(f'Email enviado com sucesso para {FROM_EMAIL}')
        ### link = http://127.0.0.1:5000/ + endpoint (por padrão digitar em minúsculas nome da sua classe)
        link = request.url_root[:-1] + url_for('usuarioativacao', usuario_id=self.usuario_id)
        return requests.post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to': self.email,
                        'subject': 'Confirmação de Cadastro.',
                        'html': f'<html><p>"Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a></p></html>"'
                        })
        

