import pandas as pd
import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()


def connection_database():
    try:        
        conn = sqlite3.connect(os.getenv('NAME_DB'))
        print('Conexão bem-sucedida!')
        return conn
    except Exception as e:
        print(f'Erro ao conectar com o banco de dados {e}')
        raise
    
def read_csv_orders():
    
    try:
        df = pd.read_csv(os.getenv('PATH_REPORT'))
        return df
    except FileNotFoundError:
        print('Arquivo CSV não foi encontrado')
        raise
    except pd.errors.EmptyDataError:
        print('O arquivo está vazio')
        raise

def filter_all_columns(df):
    df_filtered = df[['Cliente', 'Produto', 'Quantidade', 'Endereço', 'Data_do_Pedido', 'Tipo_Pagamento']]
    
    return df_filtered

# Insere todas as colunas gerada no arquivo CSV no database
def insert_all_orders_columns():
    df = read_csv_orders()
    
    df_filtered = filter_all_columns(df)
    
    conn = connection_database()

    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                        Cliente TEXT,
                        Produto TEXT,
                        Quantidade INTEGER,
                        Endereço TEXT,
                        Data_do_Pedido TEXT,
                        Tipo_Pagamento TEXT
                        )''')

    df_filtered.to_sql('pedidos', conn, if_exists='append', index=False)
    
    print('Dados inserido com sucesso!')
    
    conn.close()

def filter_column_quantity_and_product(df):
    df_filtered = df[['Produto', 'Quantidade']]
    
    return df_filtered

# Insere em uma tabela específica o produto mais comprado
def insert_most_purchased_product():
    df = read_csv_orders()
    df_filtered = filter_column_quantity_and_product(df)
    
    conn = connection_database()

    cursor = conn.cursor()
    
    df_products = df_filtered.groupby('Produto')['Quantidade'].sum().reset_index()
    
    product_most_bought = df_products[df_products['Quantidade'] == df_products['Quantidade'].max()]
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS produto_mais_comprado (
                        Produto TEXT,
                        Quantidade INTEGER
                        )''')

    product_most_bought.to_sql('produto_mais_comprado', conn, if_exists='replace', index=False)
    
    print('Dados de produto mais comprado inserido com sucesso!')

    conn.close()    
  
def filter_column_client_and_product(df):
    df_filtered = df[['Cliente', 'Produto']]
    
    return df_filtered
    
# Insere em uma tabela específica um produto mais popular para cada cliente
def product_most_popular_by_customer():
    df = read_csv_orders()
    df_filtered = filter_column_client_and_product(df)
    
    conn = connection_database()

    cursor = conn.cursor()
    
    count_products_per_customer = df_filtered.groupby(['Cliente', 'Produto']).size().reset_index(name='Contagem')
    
    popular_products_by_customer = count_products_per_customer.groupby('Cliente').apply(lambda x: x.nlargest(1, 'Contagem')).reset_index(drop=True)
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos_populares_por_cliente (
                        Cliente TEXT,
                        Produto TEXT,
                        Contagem INTEGER
                        )''')

    popular_products_by_customer.to_sql('produtos_populares_por_cliente', conn, if_exists='replace', index=False)
    
    print('Dados de produto mais popular por cliente, inserido com sucesso! ')
    
    conn.close()


def insert_relevant_information_into_database():

    insert_all_orders_columns() 
    insert_most_purchased_product()
    product_most_popular_by_customer()












