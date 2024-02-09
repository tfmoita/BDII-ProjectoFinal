from pymongo import MongoClient
client = MongoClient('mongodb+srv://luiscunha:qwerty123@cluster0.c8hkvl9.mongodb.net/')
db = client['trabalhoPraticoBDII']
collection = db["equipamentosvenda"]
"""

document = {
    'pgsidequipamento' : 'PC1',
    'pgsnomeequipamento': 'PC2',
    'pgsidcomponente' : [],
    'pgsprecomedio' : '200',
    'especificador': [{'tipo' : 'Gaming'}]

}
componente1 = {'nomecomponente': 'componente 1', 'quantidade':'2', 'id':'1'}
componente2 = {'nomecomponente': 'componente 2', 'quantidade':'10', 'id':'22'}
listcomponents = [componente1, componente2]
document['pgsidcomponente'] = listcomponents 


insert = collection.insert_one(document)

print("inserted id" + str(insert))"""