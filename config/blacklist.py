BLACKLIST = set()

'''
BLACKLIST (lista negra) é uma prática comum usada para invalidar tokens específicos 
antes do seu tempo de expiração natural. O JWT, por padrão, é um token que tem uma 
validade definida, e, até que esse prazo expire, ele é considerado válido. No entanto, 
há casos em que você pode querer invalidar um token antes que sua validade termine, como:

    - Logout de usuário: Quando o usuário faz logout, você pode desejar invalidar o token, 
      mesmo que ele ainda tenha tempo de expiração restante.
    - Revogação de permissões: Caso um usuário perca acesso ou suas permissões sejam revogadas, 
      seria importante invalidar o token para que ele não possa continuar a acessar recursos.
    - Segurança: Se um token foi comprometido ou suspeita-se que está sendo utilizado de 
      maneira mal-intencionada, pode ser necessário invalidá-lo.
'''