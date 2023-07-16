import pandas as pd
import sqlite3

def connection_database():
    conn = sqlite3.connect('DB_MESHA_MANAGER.db')
    
    return conn
    
def read_csv_orders():
    
    df = pd.read_csv('relatorio_pedido_realizado.csv')
    
    return df

def filter_all_columns(df):
    df_filtrado = df[['Cliente', 'Produto', 'Quantidade', 'Endereço', 'Data_do_Pedido', 'Tipo_Pagamento']]
    
    return df_filtrado

def insert_all_orders_columns():
    df = read_csv_orders()
    
    df_filtrado = filter_all_columns(df)
    
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

    df_filtrado.to_sql('pedidos', conn, if_exists='append', index=False)
    
    conn.close()


insert_all_orders_columns()











