Pycharm backend project

Comandos de Endpoint:

'(url)/categories' = Mostra as categorias.

'(url)/products_from_categories/<products_category_id>' = Mostra todos os produtos de uma categoria.

'(url)/products_from_id/<products_id>' = Mostra todas as informações de um produto pelo seu id.

'(url)/<user_id>/favorites' = Retorna a lista de produtos favoritos de um usuário.

'(url)/<user_id>/favorites/add/<products_id>' = Adiciona um produto na lista de favoritos de um usuário.

'(url)/<user_id>/favorites/remove/<products_id>' = Remove um produto da lista de favoritos de um usuário.

'(url)/homepage' = Exibe as imagens dos produtos junto com seu nome e preço

Lembrando que a database está vazia, então quase nenhum desses endpoints funciona por enquanto. Porém, eu criei alguns produtos e categorias pra testar a versão localhost e eles funcionaram quase certo (não entendi que tipo de dado é pra ser inserido nas imagens). Pra adicionar ou mudar alguma coisa desse código é de boa também, então qualquer alteração necessária é só falar.

URL do site = https://rendertccbackend.onrender.com/
