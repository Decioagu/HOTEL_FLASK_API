from config.sql_alchemy import banco # ORM (Object-Relational Mapping)
from dotenv import load_dotenv 
import os

import requests # método envio de email
from flask import request, url_for # método envio de email

load_dotenv()

MAILGUN_DOMAIN = os.getenv('CODIGO')
MAILGUN_API_KEY = os.getenv('CHAVE')
FROM_TITLE = os.getenv('TITULO')
FROM_EMAIL = os.getenv('ENVIO')

# atributos a ser enviados
class UsuarioModel(banco.Model):
    # ESCOPO BANCO DE DADOS
    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key = True, autoincrement=True) # id auto incrementado
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado =  banco.Column(banco.Boolean, default=False)

     # MÉTODO AUXILIAR JSON ( .resources\usuario.py = GET)
    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
            'email': self.email, 
            'ativado' : self.ativado 
        }
    
    # (APENAS PARA FINS DIÁDICO MÉTODO <= EXCLUIR)
    def json_senha(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
            'senha': self.senha,
            'email': self.email, 
            'ativado' : self.ativado 
        }
     
    # método envio de email: https://login.mailgun.com/login/
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
        # link = http://127.0.0.1:5000/ + endpoint(class UsuarioAtivacao: em minusculo, argumentos)
        link = request.url_root[:-1] + url_for('usuarioativacao', usuario_id=self.usuario_id)
        print(link)
        return requests.post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to': self.email,
                        'subject': 'Confirmação de Cadastro.',
                        'html': f'<html><p>"Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a></p></html>"'
                        })
        '''
        Construção do link de ativação:

            link = request.url_root[:-1] + url_for('usuarioativacao', usuario_id=self.usuario_id)
            - request.url_root: Obtém a URL base da aplicação (por exemplo, http://127.0.0.1:5000/).
            - [:-1]: Remove o último caractere (/) da URL.
            - url_for('usuarioativacao', usuario_id=self.usuario_id): Gera a URL do endpoint usuarioativacao, passando como argumento o usuario_id associado ao usuário.
            Assim, o link de ativação para o usuário é montado combinando a URL base com o endpoint usuarioativacao.
        '''