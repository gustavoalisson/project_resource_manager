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

def validate_zip(zip_var: str) -> bool:
    """
    A função valida se o CEP está no formato correto

    Args:
        zip_var (str): o código do CEP a ser validado

    Returns:
        bool: Retorna um valor booleano, se o CEP estiver em um formato correto.
    """
    
    zip_var = re.sub(r'\D', '', zip_var)

    if re.match(r'^\d{8}$', zip_var):
        return True
    else:
        return False

def apply_mask_zip(zip_var: str) -> str:
    """
    A função aplica uma máscara no CEP. 

    Args:
        zip_var (str): CEP a ser formatado

    Returns:
        str: O CEP formatado > 'XXXXX-XXX'
    """
    
    # Remove caracter que nao sao numéricos
    zip_var = re.sub(r'\D', '', zip_var)

    # Aplicar a máscara
    zip_formatted = re.sub(r'^(\d{5})(\d{3})$', r'\1-\2', zip_var)

    return zip_formatted

def get_address(zip_code_entry: str, label_address: str, uf_var: str, logger) -> None:
    """
    Função responsável por pegar o endereço e realizar uma requisição no VIA CEP.

    Args:
        zip_code_entry (str): Entrada do User
        label_address (str): Pega o logradouro que vem da api
    """
    zip_var = zip_code_entry.get()
         
    if validate_zip(zip_var):
        zip_formatted = apply_mask_zip(zip_var)
        url = f"{os.getenv('BASE_URL_VIACEP')}{zip_formatted}/json/"
        response = requests.get(url)
        data = response.json()
        if "erro" not in data:
            label_address.set(data["logradouro"])
            uf_var.set(data["uf"])
            
        logger.info('CEP válido')
    else:
        logger.warning('CEP inválido! ')
    
def execute_process(product_var: str, quantity_var: str, client_var: str, address_var: str, date_order: str, payment_method_var: str, logger) -> None:
    """_summary_

    Args:
        product_var (str): Descrição do produto
        quantity_var (str): Quantidade do produto - logo após essa var é convertida para inteiro
        client_var (str): Nome do cliente
        address_var (str): Endereço do cliente
        date_order (str): Data do Pedido
        payment_method_var (str): Método de pagamento
    """
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
        
            treat_client_request(stock, product, amount, client, address, date, payment, completed_orders, logger)
        else:
            logger.warning('Digite um valor válido em >>> quantidade <<< ')
        
    else:
        logger.warning('Dados incompletos. Preencha todos os campos.')

def finalize_order(logger, window) -> pd.DataFrame:
    """
    Função responsável por finalizar o pedido e gerar um relatório em CSV com os dados do pedido

    Returns:
        pd.Dataframe: Retorna um dataframe contendo os pedidos / caso não haja pedidos, retorna um df vazio
    """
      
    
    # Gerando relatório em csv com os dados dos pedidos dos Clientes
    df_orders = pd.DataFrame(completed_orders)
    if not df_orders.empty:
        
        df_orders.to_csv(os.getenv('PATH_REPORT'))
        logger.info('Pedido finalizado com sucesso! ')
        
    
    window.destroy()
        
    return df_orders

def configure_windows_screen_tkinter() -> customtkinter.CTk:
    """
    Função responsável por setar configurações da tela do tkinter

    Returns:
        customtkinter.CTk: retorna uma instancia da janela principal
    """
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    # Instancia para iniciar uma nova janela
    window = customtkinter.CTk()
    
    window.iconbitmap(os.getenv('ICON_MESHA_APP'))

    window.title('Registro de Pedido')
    
    return window

def generate_table_products(window: customtkinter.CTk) -> None:
    """
    Função responsável por gerar uma tabela de Produtos, com os valores.

    Args:
        window (customtkinter.CTk): Recebe como parâmetro uma janela 
    """
    tree = ttk.Treeview(window, columns=list(stock.keys()), show='headings')

    tree.pack()

    # Definindo o cabeçalho
    for key in stock.keys():
        tree.heading(key, text=key)
        
    # Adicionando os dados
    for i in range(len(stock['Produto'])):
        tree.insert('', 'end',
                    values=(stock['Produto'][i], stock['Quantidade'][i], stock['Preço'][i]))    
    
def declare_variables() -> str:
    """
    Função responsável por declarar as variáveis de entrada dos valores

    Returns:
        str: Cada valor retorna uma string
    """

    client_var = customtkinter.StringVar()
    address_var = customtkinter.StringVar()
    uf_var = customtkinter.StringVar()
    date_order = customtkinter.StringVar()
    product_var = customtkinter.StringVar()
    quantity_var = customtkinter.StringVar()
    payment_method_var = customtkinter.StringVar()
    zip_var = customtkinter.StringVar() 
    
    return client_var, address_var, uf_var, date_order, product_var, quantity_var, payment_method_var, zip_var


def btn_confirm_process(window: customtkinter.CTk, product_var: str, quantity_var: int, client_var: str, address_var: str, date_order: str, payment_method_var: str, logger) -> customtkinter.CTkButton:
    
    """
    Função responsável por gerar um botão para confirmar o processamento de pedido. 

    Returns:
        customtkinter.CTkButton: Retornar o botão para confirmar
    """
    
    button_process = customtkinter.CTkButton(window, text="Registrar Pedido",
                                        command=lambda: execute_process(product_var, quantity_var, client_var, address_var, date_order, payment_method_var, logger))
    
    return button_process


def btn_finalize_process(window: customtkinter.CTk, logger) -> customtkinter.CTkButton:
    """
    Função responsável por gerar um botão para finalziar o pedido.

    Args:
        window (customtkinter.CTk): Recebe como parametro a janela principal

    Returns:
        customtkinter.CTkButton: Retornar o botão para finalizar
    """
    button_finalize = customtkinter.CTkButton(window, text="Finalizar Pedido",
                                          command=lambda: finalize_order(logger, window), fg_color="red")
        
    return button_finalize
    

def generate_screen(logger) -> None:
    """
    Essa função é respponsável por gerar toda a tela da visão do cliente, com os label, e botões posicionados
    em seu devido lugar.
    """
 
    window = configure_windows_screen_tkinter()
    
    generate_table_products(window)
    
    client_var, address_var, uf_var, date_order, product_var, quantity_var, payment_method_var, zip_var = declare_variables()
    
    
    label_client = customtkinter.CTkLabel(window, text="Cliente:")
    entry_client = customtkinter.CTkEntry(window, textvariable=client_var, width=300, height=25)
     
    label_zip = customtkinter.CTkLabel(window, text="CEP: ") #novo
    entry_zip  = customtkinter.CTkEntry(window, textvariable=zip_var)
    btn_search = customtkinter.CTkButton(window, text='Buscar', command=lambda: get_address(zip_var, address_var, uf_var, logger))
        
    label_address = customtkinter.CTkLabel(window, text="Logradouro")
    entry_address = customtkinter.CTkEntry(window, textvariable=address_var, width=300, height=25)
    
    label_uf = customtkinter.CTkLabel(window, text="UF")
    entry_uf = customtkinter.CTkEntry(window, textvariable=uf_var, width=300, height=25)
    
    label_date_order = customtkinter.CTkLabel(window, text="Data do Pedido:")
    entry_date = customtkinter.CTkEntry(window, textvariable=date_order, width=300, height=25)

    label_product = customtkinter.CTkLabel(window, text="Produto:")
    entry_product = customtkinter.CTkEntry(window, textvariable=product_var, width=300, height=25)

    label_quantity = customtkinter.CTkLabel(window, text="Quantidade:")
    entry_quantity = customtkinter.CTkEntry(window, textvariable=quantity_var, width=300, height=25)

    label_payment_method = customtkinter.CTkLabel(window, text="Método de Pagamento:")
    entry_payment_method = customtkinter.CTkEntry(window, textvariable=payment_method_var, width=300, height=25)


    # # Botão de processar pedido
    button_process = btn_confirm_process(window,product_var, quantity_var, client_var, address_var, date_order, payment_method_var, logger)


    # Botão para finalizar o pedido
    button_finalize = btn_finalize_process(window, logger)

    # Posicionar os elementos na janela
    label_client.pack()
    entry_client.pack()

    label_zip.pack()
    entry_zip.pack()
    btn_search.pack()
    
    label_address.pack()
    entry_address.pack()
    
    label_uf.pack()
    entry_uf.pack()

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


