import customtkinter
import pandas as pd
import os

from process_purchase import treat_client_request
from stock_storage import stock
from dotenv import load_dotenv
from tkinter import ttk

# Ler configuração que tem em .env
load_dotenv()

pedidos_realizado = []

def realizar_pedido(product_var, quantity_var, client_var, address_var, date_order, payment_method_var):
    produto = product_var.get()
    quantidade = quantity_var.get()
    cliente = client_var.get()
    address = address_var.get()
    date = date_order.get()
    payment = payment_method_var.get()
    
    # Condição que obriga o User passar todos os dados
    if produto and quantidade and cliente and address and date and payment:
  
        if quantidade.isdigit():
            
            quantidade = int(quantidade)
        
            treat_client_request(stock, produto, quantidade, cliente, address, date, payment, pedidos_realizado)
        else:
            print('Digite um valor válido em >>> quantidade <<< ')
        
    else:
        print('Dados incompletos. Preencha todos os campos.')

def finalizar_pedido():  
    
    print('Pedido finalizado com sucesso! ')
    
    # Gerando relatório em csv com os dados dos pedidos dos Clientes
    df_pedidos = pd.DataFrame(pedidos_realizado)
    df_pedidos.to_csv(os.getenv('PATH_REPORT'))
    
    return df_pedidos

# * Usando o customtkinter/tkinter  para gerar uma tela e simular o lado do Cliente / "Compra do Produto"
def generate_screen():

    
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")


    # Instancia para iniciar uma nova janela
    window = customtkinter.CTk()

    tree = ttk.Treeview(window, columns=list(stock.keys()), show='headings')

    tree.pack()

    # Definindo o cabeçalho
    for key in stock.keys():
        tree.heading(key, text=key)
        
    # Adicionando os dados
    for i in range(len(stock['Produto'])):
        tree.insert('', 'end',
                    values=(stock['Produto'][i], stock['Quantidade'][i], stock['Preço'][i]))    

    window.iconbitmap(os.getenv('ICON_MESHA_APP'))

    window.geometry("800x650")

    window.title('Registro de Pedido')

    client_var = customtkinter.StringVar()
    address_var = customtkinter.StringVar()
    date_order = customtkinter.StringVar()
    product_var = customtkinter.StringVar()
    quantity_var = customtkinter.StringVar()
    payment_method_var = customtkinter.StringVar()

    label_client = customtkinter.CTkLabel(window, text="Cliente:")
    entry_client = customtkinter.CTkEntry(window, textvariable=client_var, width=300, height=25)

    label_address = customtkinter.CTkLabel(window, text="Endereço de Entrega:")
    entry_address = customtkinter.CTkEntry(window, textvariable=address_var, width=300, height=25)

    label_date_order = customtkinter.CTkLabel(window, text="Data do Pedido:")
    entry_date = customtkinter.CTkEntry(window, textvariable=date_order, width=300, height=25)

    label_product = customtkinter.CTkLabel(window, text="Produto:")
    entry_product = customtkinter.CTkEntry(window, textvariable=product_var, width=300, height=25)

    label_quantity = customtkinter.CTkLabel(window, text="Quantidade:")
    entry_quantity = customtkinter.CTkEntry(window, textvariable=quantity_var, width=300, height=25)

    label_payment_method = customtkinter.CTkLabel(window, text="Método de Pagamento:")
    entry_payment_method = customtkinter.CTkEntry(window, textvariable=payment_method_var, width=300, height=25)


    # Botão de processar pedido
    button_process = customtkinter.CTkButton(window, text="Registrar Pedido",
                                        command=lambda: realizar_pedido(product_var, quantity_var, client_var, address_var, date_order, payment_method_var))


    # Botão para finalizar o pedido
    button_finalize = customtkinter.CTkButton(window, text="Finalizar Pedido",
                                          command=lambda: finalizar_pedido())

    # Posicionar os elementos na janela
    label_client.pack()
    entry_client.pack()

    label_address.pack()
    entry_address.pack()

    label_date_order.pack()
    entry_date.pack()

    label_product.pack()
    entry_product.pack()

    label_quantity.pack()
    entry_quantity .pack()

    label_payment_method.pack()
    entry_payment_method.pack()

    button_process.pack(pady=12,padx=10)

    button_finalize.pack(pady=12,padx=10)

    window.mainloop()


generate_screen()