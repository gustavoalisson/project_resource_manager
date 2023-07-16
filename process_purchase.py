def treat_client_request(stock: dict, product: str, amount: int, client: str, address: str, date_order: str, payment: str, completed_orders: list) -> None:
    """
    Função responsável por aplicar alguns tratamentos no processamento
    > Verificar se o produto solicitado existe em estoque
    > Verifica se a quantidae em estoque é suficiente 
    > Verificar se a quantidade está sendo passada como 0
    > Só adiciona o pedido realizado a lista pedidos_realizado se a quantidade for igual ou abaixo do que tem disponível em estoque
    

    Args:
        stock (dict): Dicionário contendo o estoque fictício da loja online
        product (str): Descrição do produto
        amount (int): Quantidade de produto em estoque
        client (str): Nome do cliente
        address (str): Nome do endereço
        date_order (str): Data do pedido
        payment (str): Método de pagamento
        completed_orders (list): Lista que será inserida, após o pedido ser finalizado
    """
    
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
    
    
    
