import customtkinter
import pandas as pd
import requests
import os
import re

from process_purchase import treat_client_request
from stock_storage import stock
from dotenv import load_dotenv
from tkinter import ttk

# Ler configuração que tem em .env
load_dotenv()

completed_orders = []

def validate_zip(zip_var):
    # Remove caracter que nao sao numéricos
    zip_var = re.sub(r'\D', '', zip_var)

    # Verificar se o CEP possui o formato correto
    if re.match(r'^\d{8}$', zip_var):
        return True
    else:
        return False

def apply_mask_zip(zip_var):
    # Remove caracter que nao sao numéricos
    zip_var = re.sub(r'\D', '', zip_var)

    # Aplicar a máscara
    zip_formatted = re.sub(r'^(\d{5})(\d{3})$', r'\1-\2', zip_var)

    return zip_formatted

def get_address(zip_code_entry, label_address):
    zip_var = zip_code_entry.get()
         
    if validate_zip(zip_var):
        zip_formatted = apply_mask_zip(zip_var)
        url = f"{os.getenv('BASE_URL_VIACEP')}{zip_formatted}/json/"
        response = requests.get(url)
        data = response.json()
        if "erro" not in data:
            label_address.set(data["logradouro"])
        print('CEP válido')
    else:
        print('CEP inválido! ')
    
def execute_request(product_var, quantity_var, client_var, address_var, date_order, payment_method_var):
    product = product_var.get()
    amount = quantity_var.get()
    client = client_var.get()
    address = address_var.get()
    date = date_order.get()
    payment = payment_method_var.get()
    
    # Condição que obriga o User passar todos os dados
    if product and amount and client and address and date and payment:
  
        if amount.isdigit():
            
            amount = int(amount)
        
            treat_client_request(stock, product, amount, client, address, date, payment, completed_orders)
        else:
            print('Digite um valor válido em >>> quantidade <<< ')
        
    else:
        print('Dados incompletos. Preencha todos os campos.')

def finalize_order():  
    
    print('Pedido finalizado com sucesso! ')
    
    # Gerando relatório em csv com os dados dos pedidos dos Clientes
    df_pedidos = pd.DataFrame(completed_orders)
    df_pedidos.to_csv(os.getenv('PATH_REPORT'))
    
    return df_pedidos

def configure_windows_screen_tkinter():
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    # Instancia para iniciar uma nova janela
    window = customtkinter.CTk()
    
    window.iconbitmap(os.getenv('ICON_MESHA_APP'))

    window.title('Registro de Pedido')
    
    return window

def generate_table_products(window):
    tree = ttk.Treeview(window, columns=list(stock.keys()), show='headings')

    tree.pack()

    # Definindo o cabeçalho
    for key in stock.keys():
        tree.heading(key, text=key)
        
    # Adicionando os dados
    for i in range(len(stock['Produto'])):
        tree.insert('', 'end',
                    values=(stock['Produto'][i], stock['Quantidade'][i], stock['Preço'][i]))    
    
def declare_variables():
    
    #declaracao de variaveis 

    client_var = customtkinter.StringVar()
    address_var = customtkinter.StringVar()
    date_order = customtkinter.StringVar()
    product_var = customtkinter.StringVar()
    quantity_var = customtkinter.StringVar()
    payment_method_var = customtkinter.StringVar()
    zip_var = customtkinter.StringVar() 
    
    return client_var, address_var, date_order, product_var, quantity_var, payment_method_var, zip_var


def btn_confirm_process(window,product_var, quantity_var, client_var, address_var, date_order, payment_method_var):
    # Botão de processar pedido
    button_process = customtkinter.CTkButton(window, text="Registrar Pedido",
                                        command=lambda: execute_request(product_var, quantity_var, client_var, address_var, date_order, payment_method_var))
    
    return button_process


def btn_finalize_process(window):
    # Botão para finalizar o pedido
    button_finalize = customtkinter.CTkButton(window, text="Finalizar Pedido",
                                          command=lambda: finalize_order(), fg_color="red")
    
    return button_finalize
    

# * Usando o customtkinter/tkinter  para gerar uma tela e simular o lado do Cliente / "Compra do Produto"
def generate_screen():
 
    window = configure_windows_screen_tkinter()
    
    generate_table_products(window)
    
    client_var, address_var, date_order, product_var, quantity_var, payment_method_var, zip_var = declare_variables()
    
    
    label_client = customtkinter.CTkLabel(window, text="Cliente:")
    entry_client = customtkinter.CTkEntry(window, textvariable=client_var, width=300, height=25)
     
    label_zip = customtkinter.CTkLabel(window, text="CEP: ") #novo
    entry_zip  = customtkinter.CTkEntry(window, textvariable=zip_var)
    btn_search = customtkinter.CTkButton(window, text='Buscar', command=lambda: get_address(zip_var, address_var))
        
    label_address = customtkinter.CTkLabel(window, text="Logradouro")
    entry_address = customtkinter.CTkEntry(window, textvariable=address_var, width=300, height=25)
    
    label_date_order = customtkinter.CTkLabel(window, text="Data do Pedido:")
    entry_date = customtkinter.CTkEntry(window, textvariable=date_order, width=300, height=25)

    label_product = customtkinter.CTkLabel(window, text="Produto:")
    entry_product = customtkinter.CTkEntry(window, textvariable=product_var, width=300, height=25)

    label_quantity = customtkinter.CTkLabel(window, text="Quantidade:")
    entry_quantity = customtkinter.CTkEntry(window, textvariable=quantity_var, width=300, height=25)

    label_payment_method = customtkinter.CTkLabel(window, text="Método de Pagamento:")
    entry_payment_method = customtkinter.CTkEntry(window, textvariable=payment_method_var, width=300, height=25)


    # # Botão de processar pedido
    button_process = btn_confirm_process(window,product_var, quantity_var, client_var, address_var, date_order, payment_method_var)


    # Botão para finalizar o pedido
    button_finalize = btn_finalize_process(window)

    # Posicionar os elementos na janela
    label_client.pack()
    entry_client.pack()

    label_zip.pack()
    entry_zip.pack()
    btn_search.pack()
    
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

    button_process.pack(pady=3,padx=5)

    button_finalize.pack()

    # mantem a tela aberta
    window.mainloop()


generate_screen()