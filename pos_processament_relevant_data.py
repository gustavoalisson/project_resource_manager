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






# import pandas as pd
# import sqlite3

# # Carregar o arquivo CSV
# df = pd.read_csv('relatorio_pedido_realizado.csv')

# # Filtrar as colunas relevantes
# df_filtrado = df[['Produto', 'Quantidade']]

# # Calcular a soma da coluna 'Quantidade' para cada produto
# df_produtos = df_filtrado.groupby('Produto')['Quantidade'].sum().reset_index()

# # Identificar o produto mais comprado
# produto_mais_comprado = df_produtos[df_produtos['Quantidade'] == df_produtos['Quantidade'].max()]

# # Conectar ao banco de dados SQLite
# con = sqlite3.connect('DB_MESHA_MANAGER.db')
# cursor = con.cursor()

# # Criar a tabela no banco de dados (caso ainda não exista)
# cursor.execute('''CREATE TABLE IF NOT EXISTS produto_mais_comprado (
#                     Produto TEXT,
#                     Quantidade INTEGER
#                     )''')

# # Inserir o produto mais comprado no banco de dados
# produto_mais_comprado.to_sql('produto_mais_comprado', con, if_exists='replace', index=False)

# # Fechar a conexão com o banco de dados
# con.close()











