<h1> Pycharm backend project </h1>

Comandos de Endpoint:

'(url)/categories' = Mostra as categorias.

'(url)/products-from-categories/<products_category_id>' = Mostra todos os produtos de uma categoria.

'(url)/products-from-id/<products_id>' = Mostra todas as informações de um produto pelo seu id.

'(url)/<user_id>/favorites' = Retorna a lista de produtos favoritos de um usuário.

'(url)/<user_id>/favorites/add/<products_id>' = Adiciona um produto na lista de favoritos de um usuário.

'(url)/<user_id>/favorites/remove/<products_id>' = Remove um produto da lista de favoritos de um usuário.

'(url)/homepage' = Exibe as imagens dos produtos junto com seu nome e preço

A database tem produtos e categorias agora, então da pra testar algumas das funções, especificamente as três primeiras e a última. Seria bom tomar cuidado com a favorites se quiserem testar sem me avisar, já que ela mexe diretamente com o banco, porém ela é a mais robusta pra qualquer tipo de erro(Ainda sim, seria bom me dar um toque antes).

Nota: O retorno que esses endpoints trazem podem ser customizados como html (como foi visto na página index), portanto se souberem/quiserem melhorar a aparência deles me avisem que eu não lembro bulhufas dessa linguagem.

<h4> URL do site = https://rendertccbackend.onrender.com/ </h4>
