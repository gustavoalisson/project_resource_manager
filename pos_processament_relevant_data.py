import pandas as pd
import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()


def connection_database(logger):
    try:        
        conn = sqlite3.connect(os.getenv('NAME_DB'))
        logger.info('Conexão bem-sucedida!')
        return conn
    except Exception as e:
        logger.error(f'Erro ao conectar com o banco de dados {e}')
        raise
    
def read_csv_orders():
    
    try:
        df = pd.read_csv(os.getenv('PATH_REPORT'))
        return df
    except FileNotFoundError:
        return None


def filter_all_columns(df):
    df_filtered = df[['Cliente', 'Produto', 'Quantidade', 'Endereço', 'Data_do_Pedido', 'Tipo_Pagamento']]
    
    return df_filtered

# Insere todas as colunas gerada no arquivo CSV no database
def insert_all_orders_columns(df, conn, logger):
    
    df_filtered = filter_all_columns(df)
    
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
    
    logger.info('Dados do relatório inserido na base de dados com sucesso!!!')
    

def filter_column_quantity_and_product(df):
    df_filtered = df[['Produto', 'Quantidade']]
    
    return df_filtered

# Insere em uma tabela específica o produto mais comprado
def insert_most_purchased_product(df, conn, logger):
    df_filtered = filter_column_quantity_and_product(df)
    
    cursor = conn.cursor()
    
    df_products = df_filtered.groupby('Produto')['Quantidade'].sum().reset_index()
    
    product_most_bought = df_products[df_products['Quantidade'] == df_products['Quantidade'].max()]
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS produto_mais_comprado (
                        Produto TEXT,
                        Quantidade INTEGER
                        )''')

    product_most_bought.to_sql('produto_mais_comprado', conn, if_exists='replace', index=False)
    
    logger.info('Dados de produto mais comprado inserido com sucesso!')

  
def filter_column_client_and_product(df):
    df_filtered = df[['Cliente', 'Produto']]
    
    return df_filtered
    
# Insere em uma tabela específica um produto mais popular para cada cliente
def product_most_popular_by_customer(df, conn, logger):
    df_filtered = filter_column_client_and_product(df)
    
    cursor = conn.cursor()
    
    count_products_per_customer = df_filtered.groupby(['Cliente', 'Produto']).size().reset_index(name='Contagem')
    
    popular_products_by_customer = count_products_per_customer.groupby('Cliente').apply(lambda x: x.nlargest(1, 'Contagem')).reset_index(drop=True)
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos_populares_por_cliente (
                        Cliente TEXT,
                        Produto TEXT,
                        Contagem INTEGER
                        )''')

    popular_products_by_customer.to_sql('produtos_populares_por_cliente', conn, if_exists='replace', index=False)
    
    logger.info('Dados de produto mais popular por cliente, inserido com sucesso! ')
    
# Identifica padrão de vende = Quais dias tem mais compras
def orders_by_day_of_week(df, conn, logger):
    df['Data_do_Pedido'] = pd.to_datetime(df['Data_do_Pedido'])
    df['Dia_da_Semana'] = df['Data_do_Pedido'].dt.day_name()
    
    orders_by_day_week = df['Dia_da_Semana'].value_counts().reset_index()
    orders_by_day_week.columns = ['Dia_da_Semana', 'Total_Pedidos']
    
    orders_by_day_week.to_sql('pedidos_por_dia_semana', conn, if_exists='replace', index=False)
    
    logger.info('Dados de pedidos por dia da semana inserido com sucesso!')
    
# Identifica padrão de vende = Quais meses tem mais compra    
def orders_by_month(df, conn, logger):
    df['Data_do_Pedido'] = pd.to_datetime(df['Data_do_Pedido'])
    df['Mes'] = df['Data_do_Pedido'].dt.month_name()
    
    orders_per_month = df['Mes'].value_counts().reset_index()
    orders_per_month.columns = ['Mês', 'Total_Pedidos']
    
    orders_per_month.to_sql('pedidos_por_mes', conn, if_exists='replace', index=False)
    
    logger.info('Dados de pedidos por mês inserido com sucesso!')
        

def insert_relevant_information_into_database(logger):
     
    df = read_csv_orders()
    
    if df is None:
        logger.warning('Arquivo CSV não foi encontrado. Não é possível inserir os dados relevantes ao banco de dados.')
    else:
        conn = connection_database(logger)
        
        insert_all_orders_columns(df, conn, logger) 
        insert_most_purchased_product(df, conn, logger)
        product_most_popular_by_customer(df, conn, logger)
        orders_by_day_of_week(df, conn, logger)
        orders_by_month(df, conn, logger)
        
        conn.close()
    


