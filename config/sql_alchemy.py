from flask_sqlalchemy import SQLAlchemy # ORM (Object-Relational Mapping)

'''
SQLAlchemy é uma biblioteca em Python que facilita a interação com 
bancos de dados relacionais de uma maneira mais orientada a objetos. 
Em vez de escrever SQL diretamente, SQLAlchemy permite que você defina 
objetos Python que representam tabelas em seu banco de dados.

pip install Flask-SQLAlchemy
'''
banco = SQLAlchemy() # ORM criando uma engine para um banco


