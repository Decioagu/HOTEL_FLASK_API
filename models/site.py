from config.sql_alchemy import banco # ORM (Object-Relational Mapping)

# atributos a ser enviados
class SiteModel(banco.Model):
    # ESCOPO BANCO DE DADOS
    __tablename__ = 'site'
    site_id = banco.Column(banco.Integer, primary_key = True) # id auto incrementado
    url = banco.Column(banco.String(80), nullable=False) # endereço
    hoteis = banco.relationship('HotelModel', back_populates='site', lazy='dynamic') # Relacionamento reverso
    '''
    relationship: é uma função do SQLAlchemy que é usada para definir uma relação entre duas tabelas.
    back_populates='__tablename__': Este parâmetro é usado para definir a relação bidirecional.
    lazy='dynamic': Este parâmetro define como a carga dos dados relacionados será tratada. (não obrigatório)
    '''

    # MÉTODO AUXILIAR CONSTRUTOR (.resources\site.py = POST)
    def __init__(self, url):
        self.url = url

    # MÉTODO AUXILIAR JSON ( .resources\hotel.py = GET, POST, PUT)
    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis] # Chamada lista hotéis associadas no site
        }
    