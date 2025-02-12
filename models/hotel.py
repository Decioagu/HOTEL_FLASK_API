from config.sql_alchemy import banco # ORM (Object-Relational Mapping)

# atributos a ser enviados
class HotelModel(banco.Model):
    # ESCOPO BANCO DE DADOS
    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.String, primary_key = True) # id str via Hesders
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('site.site_id'))  # Chave estrangeira
    site = banco.relationship('SiteModel', back_populates='hoteis')  # Relacionamento reverso
    '''
    relationship: é uma função do SQLAlchemy que é usada para definir uma relação entre duas tabelas.
    back_populates='__tablename__': Este parâmetro é usado para definir a relação bidirecional.
    '''

    # MÉTODO AUXILIAR JSON ( .resources\hotel.py = GET)
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id' : self.site_id # Chave estrangeira
        }

    # MÉTODO AUXILIAR CONSTRUTOR (.resources\hotel.py = POST)
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id # Chave estrangeira
    