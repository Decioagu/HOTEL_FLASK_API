from hmac import compare_digest # comparar senha
from flask_jwt_extended import create_access_token, get_jwt, jwt_required # criptografia (token)
from flask_restful import Resource, reqparse # acesso ao (GET, POST, PUT, DELETE)
from config.blacklist import BLACKLIST # invalidar determinados tokens JWT
from models.usuario import UsuarioModel # models
from config.sql_alchemy import banco # ORM (Object-Relational Mapping)
import traceback # informações detalhadas sobre uma exceção
from flask import make_response, render_template

# PARÂMETRO DO USUÁRIO
atributos = reqparse.RequestParser() # parâmetros pre-definidos (argumentos)
atributos.add_argument('login', type=str, required=True, help='Campo login obrigatório') # argumentos
atributos.add_argument('senha', type=str, required=True, help='Campo senha obrigatório') # argumentos
atributos.add_argument('email', type=str) # argumentos
atributos.add_argument('ativado', type=bool) # argumentos

# rota (APENAS PARA FINS DIÁDICO MÉTODO <= EXCLUIR)
class Usuarios(Resource):
    # método de (Leitura)
    def get(self):
        # {'usuario': [(MÉTODO AUXILIAR JSON) for usuario in (ESCOPO BANCO DE DADOS).(filtra_todos)]}
        return {'usuario': [usuario.json_senha() for usuario in UsuarioModel.query.all()]}

# rota (CRUD)
class Usuario(Resource):    

    # Solicitar (leitura) por "id"
    def get(self, usuario_id):
        # usuario = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por ID)).(retornar 1º resultado)
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()

        if usuario:
            # (ESCOPO BANCO DE DADOS).(MÉTODO AUXILIAR JSON)
            return usuario.json()   
        else:
            return {'mensagem': 'Usuário não existe.'}, 404           

    # Excluir
    @jwt_required() # necessário token de acesso
    def delete(self, usuario_id):

        # usuario = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por ID)).(retornar 1º resultado) 
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first() # retorna alguma coisa ou falso

        # Se ID existir
        if usuario:
            # (ESCOPO BANCO DE DADOS).(método delete)
            banco.session.delete(usuario)
            banco.session.commit()
            return {'mensagem': 'Usuário deletado.'}, 200   
        else:
            return {'mensagem': 'Usuário não existe.'}, 404
        
# rota cadastrar usuário
class CadastroUsuario(Resource):

    def post(self):
        
        # dados = (PARÂMETRO DO USUÁRIO => argumentos).(extrair dados)
        dados = atributos.parse_args()

        # SE emil nao for preenchido, finalize cadastrado 
        # (PARÂMETRO DO USUÁRIO).email
        if not dados.get('email') or dados.get('email') is None:
            return {'mensagem': 'email não pode ser deixado em branco.'}, 400
        
        # SE não existir email, finalize cadastrado 
        # (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por email)).(retornar 1º resultado)
        if UsuarioModel.query.filter_by(email=dados['email']).first():
            return {"mensagem": "E-mail '{}' já existe!!!".format(dados['email'])}, 400

        # SE não existir login, finalize cadastrado
        # (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por login)).(retornar 1º resultado)
        if UsuarioModel.query.filter_by(login=dados['login']).first():
            return {"mensagem": "Login '{}' já existe!!!".format(dados['login'])}, 400
        else: 
            # usuario = (ESCOPO BANCO DE DADOS).(PARÂMETRO DO USUÁRIO)
            usuario = UsuarioModel(**dados) # >>>>> preencher dados no Banco de Dabos <<<<<
            
            usuario.ativado = False # >>>>> preencher dados no Banco de Dabos <<<<<
            try:
                # (ESCOPO BANCO DE DADOS).(método salvar dados)
                banco.session.add(usuario)
                banco.session.commit()

                # (ESCOPO BANCO DE DADOS).(método envio de email)
                usuario.envio_de_email()
            except:
                '''
                traceback.print_exc() é uma função em Python usada para 
                imprimir informações detalhadas sobre uma exceção.
                '''
                traceback.print_exc()
                return {'mensagem': 'Ocorreu erro interno no servidor.'}, 500
            
            # mensagem de sucesso 
            return {f"mensagem": "Usuário criado com sucesso!!!"}, 201

# rota login
class UsuarioLogin(Resource):

    def post(self):
        # dados = (PARÂMETRO DO USUÁRIO => argumentos).(extrair dados)
        dados = atributos.parse_args()
        
        # usuario = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por login)).(retornar 1º resultado)
        usuario = UsuarioModel.query.filter_by(login=dados['login']).first()       

        #  compare_digest() => realizar comparações seguras de strings
        # compare_digest(ESCOPO BANCO DE DADOS.senha , PARÂMETRO DO USUÁRIO.senha)
        if usuario and compare_digest(usuario.senha, dados['senha']):
            
            # (ESCOPO BANCO DE DADOS).ativado
            if usuario.ativado:
                # create_access_token() => usado em sistema de autenticação e autorização
                token_de_acesso = create_access_token(identity=usuario.usuario_id)
                return {'acesso token': token_de_acesso}, 200
            else:
                return {'mensagem': 'Usuário não ativo.'}, 400
        
        # Se usuario não existir
        return {'mensagem': 'Usuário ou senha errado.'}, 401 

# rota logout
class UsuarioLogout(Resource):
    # sai do "login" e bloqueia senha de "token" do usuário na lista "BLACKLIST"
    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id) # lista de token invalido apos "saída de login" 
        return {'mensagem' : 'Saiu do login com sucesso!!!'}, 200
    
# rota ativação de cadastro
class UsuarioAtivacao(Resource):
    
    def get(self, usuario_id):
        # usuario = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por ID)).(retornar 1º resultado) 
        usuario = UsuarioModel.query.filter_by(usuario_id=usuario_id).first()
        
        # Se ID do usuario não existe, finalizar ativação
        if not usuario:
            return{'mensagem': 'Usuário com id:{} não foi encontrado'.format(usuario_id)}, 404
        
        usuario.ativado = True # >>>>> preencher dados no Banco de Dabos <<<<<
        try:
            # (ESCOPO BANCO DE DADOS).(método salvar dados)
            banco.session.add(usuario)
            banco.session.commit()
        except:
            '''
                traceback.print_exc() é uma função em Python usada para 
                imprimir informações detalhadas sobre uma exceção.
            '''
            traceback.print_exc()
            return {'mensagem': 'Ocorreu erro interno no servidor.'}, 500
        
        #============================================================================================================
        # resposta da requisição como JSON
        # return {'mensagem': f'Usuário: ({usuario.login}) de email: ({usuario.email}) encontrado com sucesso!'}, 200
        #============================================================================================================

        # "headers": resposta da requisição como página HTML
        headers = {'Content-Type': 'text/html'}

        '''
        - make_response(...): Esta função cria uma resposta HTTP personalizada.
        - render_template: Esta função renderiza um template HTML
        - parâmetro enviados no corpo do HTML:
            - email=usuario.email
            - usuario=usuario.login
        '''
        return make_response(render_template('user_confirm.html', email=usuario.email, usuario=usuario.login), 200, headers)
    '''
        OBS: o arquivo "user_confirm.html" obrigatoriamente deve ser alocado 
        em uma pasta de nome "templastes", pois o Flask irá procurar este 
        arquivo no diretório de templates da aplicação por padrão.
    ''' 