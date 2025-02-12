# HOTEL  
 
 **API de cadastramento de hotel e usuário on-line com autenticação via e-mail**

 Este projeto consiste em uma API back-end feita com Flask para consulta e cadastramento de hotéis e usuário em endereços de WEB, em sites previamente cadastrados armazenados em __Banco de Dados MySQL__.

 Segue arquivo em word com documentação de uso da API HOTEL: __Documentação REST API Hoteis.docx__

- Principais ações:
    - Cadastramento de sites;
    - Cadastramento de hotéis;
    - Cadastramento de usuário;
    - Consulta via id de usuário;
    - Autenticação de usuário via e-mail;
    - Consulta personalizadas de hotéis apos autenticação;
    - Relacionamento sites e hotéis cadastrado por usuário autenticado.

- Principais tecnologias:
    - __Flask__ é um microframework para desenvolvimento web escrito em Python.

    - __SQLAlchemy__ é uma biblioteca de ORM (Object-Relational Mapping) em Python que permite manipulação e troca simplificada diferentes bancos de dados relacionais com mudança em uma única linha de comando.

    - __Autenticação JWT (JSON Web Token)__ (JSON Web Token) é uma técnica amplamente usada para autenticar usuários em aplicações web, incluindo APIs construídas com Flask.

    - __O Mailgun__ é um serviço de API de e-mail transacional projetado para desenvolvedores. Em termos mais simples, é uma ferramenta que permite que seus aplicativos enviem, recebam e rastreiem e-mails de forma eficiente e confiável.
