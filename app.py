from flask import Flask, jsonify
from flask_restful import Api
from config.blacklist import BLACKLIST
from resources.site import Sites, Site
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, CadastroUsuario, UsuarioLogin, UsuarioLogout, UsuarioAtivacao, Usuarios_senha ###
from config.config_DB import Config
from flask_jwt_extended import JWTManager # autenticação e criptografia

# instanciar Flask
app = Flask(__name__)
app.config.from_object(Config) # configuração do banco
api = Api(app)

# instanciar JWT (JSON Web Token) 
jwt = JWTManager(app)

# executada antes de cada solicitação do aplicativo Flask
@app.before_request 
def cria_banco():
    banco.create_all()

# --------------------------- BLACKLIST ----------------------------
# pesquisa token em BLACKLIST (autenticação token)
@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

# resposta da BLACKLIST (autenticação token)
@jwt.revoked_token_loader
def token_de_acesso_invalido(jwt_header, jwt_payload):
    return jsonify({'message': 'Sem acesso ao login.'}), 401
# ------------------------------------------------------------------

#rota
@app.route('/')
def index():
    return '<h1> Hotel </h1>'

# rotas
api.add_resource(Hoteis, '/hoteis') # acessar cadastro do hoteis 
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') # cadastro do hoteis
api.add_resource(Usuario, '/usuarios/<int:usuario_id>') # cadastro do usuário
api.add_resource(CadastroUsuario, '/cadastro') # cadastrar usuário
api.add_resource(UsuarioLogin, '/login') # acessar cadastro do usuário
api.add_resource(UsuarioLogout, '/logout') # sair cadastro do usuário
api.add_resource(Sites, '/sites') # acessar cadastro do site
api.add_resource(Site, '/sites/<string:url>') # cadastrar site
# ----------------------------- (p/ fins diádicos) ------------------------------
api.add_resource(Usuarios_senha, '/usuarios_senha/') # cadastro do usuário
api.add_resource(UsuarioAtivacao, '/ativacao/<int:usuario_id>') ### ativar usuário cadastrado
# -------------------------------------------------------------------------------
# execução arquivo principal
if __name__ == '__main__':
    # instanciar banco
    from config.sql_alchemy import banco
    banco.init_app(app)

    app.run(debug=True) # instanciar api

# Seção 10