from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import gunicorn
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

## Endereço da database
## Desabilitado para testar conexão com Render
link = 'mysql+pymysql://https://github.com/VittorioUnip/Tcc_BackEnd/blob/master/dbteste.sql/e_commerce_db'

## Conexão para a database pela utilização do SQLAlchemy
## Desabilitado para testar conexão com Render
app.config['SQLALCHEMY_DATABASE_URI'] = link

## Instrução para o jsonify não colocar os itens em ordem alfabética
app.json.sort_keys = False

## Código necessário para identificar que é nessa aplicação que quero rodar o código
app.app_context().push()

db = SQLAlchemy(app)

## Código necessário para retirar os models das tables da database, a alternativa disso seria transporta-las manualmente
Base = automap_base()
Base.prepare(autoload_with = db.engine)

##Models, retiradas do arquivo da database
Categories = Base.classes.products_category
Products = Base.classes.products
Products_Images = Base.classes.products_images
Users = Base.classes.users
Favorites = Base.classes.favorites

### Abaixo, temos todos os endpoints requisitados

## Mostra todas as categorias presentes no banco. Vale constar que esse 'app.route' é literalmente a rota para acessar essa função.
@app.route('/categories', methods = ['GET'])
def get_categories():
    show_categories = db.session.query(Categories).all()
    return jsonify([{'category id': sc.products_category_id,
                     'category name': sc.category_name,
                     'category description': sc.category_description,
                     'category image': sc.category_image} for sc in show_categories])

## Mostra todos os produtos de uma categoria.
@app.route('/products-from-category/<products_category_id>', methods = ['GET'])
def get_products_by_category(products_category_id):
    check_category_id = db.session.query(Categories).get_or_404(products_category_id)
    if check_category_id is not None:
        show_products_by_category = db.session.query(Products).filter(Products.products_category_id == products_category_id)
        return jsonify([{'category id': spc.products_category_id,
                     'product id': spc.products_id,
                     'product name': spc.products_name,
                     'product price': spc.products_price} for spc in show_products_by_category])

## Seleciona um produto e traz todos os seu detalhes pelo seu ID
@app.route('/product-from-id/<products_id>/', methods = ['GET'])
def get_products_by_id(products_id):
    check_product_id = db.session.query(Products).get_or_404(products_id)
    print(check_product_id)
    print(products_id)
    if check_product_id is not None:
        show_product = db.session.query(Products).filter(Products.products_id == products_id)
        return jsonify([{'product id': sp.products_id,
                         'product category id': sp.products_category_id,
                         'product name': sp.products_name,
                         'product description': sp.products_description,
                         'product price': sp.products_price} for sp in show_product])
    else:
        return 'oops'

## Retorna a lista de produtos favoritos de um usuario
@app.route('/<user_id>/favorites', methods = ['GET'])
def get_favorites_by_user(user_id):
    check_user_id = db.session.query(Users).get(user_id)
    print(check_user_id)
    print(user_id)
    if check_user_id is not None:
        show_user_favorites = db.session.query(Favorites).filter(Favorites.user_id == user_id)
        return jsonify([{'favorite id': suf.favorites_id,
                         'user id': suf.user_id,
                         'product name': suf.products_id} for suf in show_user_favorites])
    else:
        return 'oops'

## Adiciona um produto na lista de favoritos de um usuário,verificando se o produto existe ou já está adicionado a lista de favoritos do usuario.
@app.route('/<user_id>/favorites/add/<products_id>', methods = ['POST'])
def add_favorite(user_id, products_id):
    check_user_id = db.session.query(Users).get_or_404(user_id)
    print(check_user_id)
    print(user_id)
    if check_user_id is not None:
        check_product_id = db.session.query(Products).get_or_404(products_id)
        print(check_product_id)
        print(products_id)
        if check_product_id is not None:
            add_favorite_product = Favorites(user_id = user_id, products_id = products_id)
            existing_favorite = db.session.query(Favorites.products_id).filter_by(products_id = products_id).first()
            print(products_id)
            print(add_favorite_product)
            print(existing_favorite)
            if existing_favorite is None:
                db.session.add(add_favorite_product)
                db.session.commit()
                return '<h1>Produto adicionado aos favoritos com sucesso</h1>'
            else:
                return 'Produto já existe nos favoritos'

## Remove um produto da lista de favoritos de um um usuario, verificando se o produto está realmente lá para ser deletado.
@app.route('/<user_id>/favorites/remove/<products_id>', methods = ['DELETE'])
def remove_favorite(user_id, products_id):
    check_user_id = db.session.query(Users).get_or_404(user_id)
    print(user_id)
    if check_user_id is not None:
        check_product_id = db.session.query(Products).get_or_404(products_id)
        print(check_product_id)
        print(products_id)
        if check_product_id is not None:
            remove_favorite_product = Favorites(user_id = user_id, products_id = products_id)
            print(remove_favorite_product)
            existing_favorite = db.session.query(Favorites.products_id).filter_by(user_id = user_id, products_id = products_id).first()
            print(existing_favorite)
            if existing_favorite is not None:
                db.session.execute(db.delete(Favorites).filter_by(user_id = user_id, products_id = products_id))
                db.session.commit()
                return 'Produto removido dos favoritos com sucesso>'
            else:
                return 'Produto não está em seus favoritos ou já foi removido'

## Exibe as imagens dos produtos junto com seu nome e preço
@app.route('/homepage', methods=['GET'])
def display_homepage():
    highlights = db.session.query(Products_Images.products_images).all()
    names = db.session.query(Products.products_name).all()

    return jsonify([[{h.products_images, '<br>', n.products_name, '<br>', n.products_price} for n in names]for h in highlights])





## Só algo para colocar no index, não é necessário.
@app.route('/')
def index():

    return '<h1>Bem Vindo ao Banco!</h1> <br> <img src = "https://media.istockphoto.com/id/513921039/photo/illustration-of-a-oool-yellow-smiley-with-sunglasses.jpg?s=612x612&w=0&k=20&c=hhVQxXTUhmcZLv2QrZ2WE2p7inzxQIA5H6XP8jPrQXw=" alt="Smile">'

##Roda o flask quando eu executo o código (da para colocar ele em debug)
if __name__ == '__main__':
    app.run()

## Enviroment = EnviromentTest













#@app.route('/')
#def index():

 #   results = db.session.query(Users).all()
 #   for r in results:
 #       print(r.user_id)
 #       print(r.username)
 #       print(r.password)
 #       print(r.name)
 #       print(r.lastname)
 #       print(r.email)

 #   return ''


## Adiciona uma categoria (debug)
#@app.route('/add/c')
#def add_category():
    #new_category = Categories(category_name = 'Categoria 2', category_description = 'Descrição da Categoria 2', categor y_image = 'imagem da categoria 2' )
    #db.session.add(new_category)
    #db.session.commit()

    #return '<h1>Categoria Inserida!</h1>'

## Adiciona um produto (debug)
#@app.route('/add/p', methods = ['POST'])
#def add_product():
    #new_product = Products(products_name = 'Produto 1', products_description = 'Descrição do Produto 1', products_price = 10.00, products_image = 'imagem do produto 1', products_category_id = 1)
    #db.session.add(new_product)
    #db.session.commit()

    #return '<h1>Produto adicionado</h1>'

##Roda o flask quando eu executo o código (da para colocar ele em debug)
if __name__ == '__main__':
    app.run()
