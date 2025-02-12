from flask import Flask, jsonify
from flask_restful import Api
from resources.site import Sites, Site # resources
from config.blacklist import BLACKLIST # config (invalidar determinados tokens JWT)
from resources.hotel import Hoteis, Hotel # resources
from resources.usuario import Usuario, Usuarios, CadastroUsuario, UsuarioLogin, UsuarioLogout, UsuarioAtivacao # resources
from config.config_DB import Config # config
from flask_jwt_extended import JWTManager # autenticação e criptografia

# sintaxe do Flask
app = Flask(__name__)
app.config.from_object(Config) # configuração do banco
api = Api(app)

jwt = JWTManager(app)

# executada antes de cada solicitação do aplicativo Flask
@app.before_request 
def cria_banco():
    banco.create_all()

# Verificar token na BLACKLIST (autenticação token)
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

# Resposta de BLACKLIST caso conste na lista (autenticação token)
@jwt.revoked_token_loader
def token_de_acesso_invalido(jwt_header, jwt_payload):
    return jsonify({'message': 'Sem acesso ao login.'}), 401

@app.route('/')
def index():
    return '<h1> Hotel </h1>'

# rotas
api.add_resource(Hoteis, '/hoteis') # acessar cadastro do hoteis 
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') # cadastro do hoteis
api.add_resource(CadastroUsuario, '/usuarios/cadastro') # cadastrar usuário
api.add_resource(Usuarios, '/usuarios') # cadastro do usuário
api.add_resource(Usuario, '/usuarios/<int:usuario_id>') # cadastro do usuário
api.add_resource(UsuarioLogin, '/usuarios/login') # acessar cadastro do usuário
api.add_resource(UsuarioLogout, '/usuarios/logout') # sair cadastro do usuário
api.add_resource(UsuarioAtivacao, '/usuarios/ativacao/<int:usuario_id>') # ativar usuário cadastrado (método envio de email em models)
api.add_resource(Sites, '/sites') # acessar cadastro do site
api.add_resource(Site, '/sites/<string:url>') # cadastrar site

# execução arquivo principal
if __name__ == '__main__':
    # instanciar banco
    from config.sql_alchemy import banco # config
    banco.init_app(app)

    app.run(debug=True) # instanciar api

# Seção 14