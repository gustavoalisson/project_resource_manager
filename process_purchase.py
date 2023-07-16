def treat_client_request(stock, produto, quantidade, cliente, endereco, date_order, payment, pedidos_realizado):
    
    # Verificar se o produto solicitado existe em estoque
    
    if produto not in stock['Produto']:
        print(f"O produto >> {produto} << não existe em nosso estoque.")
        return
    
    # Verifica se a quantidade em estoque é suficiente
    
    index = stock['Produto'].index(produto)
    if quantidade > stock['Quantidade'][index]:
        print(f"A quantidade solicitada do produto {produto} excede a disponibilidade atual. Em estoque: {stock['Quantidade'][index]}")
        return
    
    # Verificar se a quantidade está sendo passada como 0
    if quantidade == 0:
        print('Não é possível passar o valor 0 para Realizar um pedido. ')
        return
    
    print(f"Pedido recebido: {produto}, Quantidade: {quantidade}, Cliente: {cliente}")
    
    
    pedido = {
    'Cliente': cliente,     
    'Produto': produto,
    'Quantidade': quantidade,
    'Endereço': endereco,
    'Data do Pedido': date_order,
    'Tipo_Pagamento': payment
        }

    # Só adiciona o pedido realizado a lista pedidos_realizado se a quantidade for igual ou abaixo do que tem disponível em estoque
    
    if quantidade <= stock['Quantidade'][index]:
        pedidos_realizado.append(pedido)     
        # Atualize o estoque
        stock['Quantidade'][index] -= quantidade
    
    
    
