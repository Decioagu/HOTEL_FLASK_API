from flask_restful import Resource # acesso ao (GET, POST, PUT, DELETE)
from models.site import SiteModel # models
from models.hotel import HotelModel # models
from config.sql_alchemy import banco # ORM (Object-Relational Mapping)
from flask_jwt_extended import jwt_required # criptografia (token)

# rota visualizar Sites
class Sites(Resource):
    # método de (Leitura)
    def get(self):
        # {'sites': [(MÉTODO AUXILIAR JSON) for sites in (ESCOPO BANCO DE DADOS.filtra_todos)]}
        return {'sites': [site.json() for site in SiteModel.query.all()]}

# rota CRUD
class Site(Resource):
    # Solicitar (leitura) por "url"
    def get(self, url):
        # site = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por "url")).(retornar 1º resultado)
        site = SiteModel.query.filter_by(url=url).first()
        if site:
            # (ESCOPO BANCO DE DADOS).(MÉTODO AUXILIAR JSON)
            return site.json()
        else:
            return {'mensagem': 'Site não existe'}, 404
        
    # Enviar (criar)
    @jwt_required() # necessário token de acesso
    def post(self, url):
        # site = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por "url")).(retornar 1º resultado)
        site = SiteModel.query.filter_by(url=url).first()

        if site:
            return {'mensagem': 'Site já existe'}, 400
        
        if not 'www.' in url:
            return {'mensagem': "Favor inserir endereço valido iniciando com (www.)"}, 400
        else:
            # acesso ao banco de dados com "url"
            novo_site = SiteModel(url) # >>>>> preencher dados no Banco de Dabos => (MÉTODO AUXILIAR CONSTRUTOR) <<<<<
            try:
                # (ESCOPO BANCO DE DADOS).(método salvar dados)
                banco.session.add(novo_site)
                banco.session.commit()
                # (ESCOPO BANCO DE DADOS).(MÉTODO AUXILIAR JSON)
                return novo_site.json()
            except:
                return {'mensagem': 'Ocorreu um erro interno'}, 500

    # Excluir
    @jwt_required() # necessário token de acesso
    def delete(self, url):
        # site = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por "url")).(retornar 1º resultado)
        site = SiteModel.query.filter_by(url=url).first()
      
        if site:
            # Busca todos os hotéis associados ao site pelo 'site_id'
            # lista_de_hoteis_com_site_id = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por "site_id")).(filtra_todos)
            lista_de_hoteis_com_site_id = HotelModel.query.filter_by(site_id=site.site_id).all()

            try:
                # Deleta todos os hotéis associados ao site
                for hotel_id in lista_de_hoteis_com_site_id:
                    # (ESCOPO BANCO DE DADOS).(método delete)
                    banco.session.delete(hotel_id)

                # (ESCOPO BANCO DE DADOS).(método delete)
                banco.session.delete(site)
                banco.session.commit()
                return {'mensagem': 'Site deletado'}, 200
            except:
                return {'mensagem': 'Ocorreu um erro interno ao deletar o site'}, 500
        else:
            return {'mensagem': 'Site não existe'}, 404