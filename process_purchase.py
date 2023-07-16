def treat_client_request(stock, product, amount, client, address, date_order, payment, completed_orders):
    
    # Verificar se o produto solicitado existe em estoque
    
    if product not in stock['Produto']:
        print(f"O produto >> {product} << não existe em nosso estoque.")
        return
    
    # Verifica se a quantidade em estoque é suficiente
    
    index = stock['Produto'].index(product)
    if amount > stock['Quantidade'][index]:
        print(f"A quantidade solicitada do produto {product} excede a disponibilidade atual. Em estoque: {stock['Quantidade'][index]}")
        return
    
    # Verificar se a quantidade está sendo passada como 0
    if amount == 0:
        print('Não é possível passar o valor 0 para Realizar um pedido. ')
        return
    
    print(f"Pedido recebido: {product}, Quantidade: {amount}, Cliente: {client}")
    
    
    pedido = {
    'Cliente': client,     
    'Produto': product,
    'Quantidade': amount,
    'Endereço': address,
    'Data do Pedido': date_order,
    'Tipo_Pagamento': payment
        }

    # Só adiciona o pedido realizado a lista pedidos_realizado se a quantidade for igual ou abaixo do que tem disponível em estoque
    
    if amount <= stock['Quantidade'][index]:
        completed_orders.append(pedido)     
        # Atualize o estoque
        stock['Quantidade'][index] -= amount
    
    
    
