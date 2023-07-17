# Gerenciador de Recursos :gear::department_store:

# Objetivo
Automatizar um processo específico de negócio. O processo é capaz de automatizar algumas tarefas específicas de uma loja online. 

# CHANGELOG
2023-07-17 - Versão: 1.0.0 
* Nessa primeira versão do projeto, o sistema é capaz de realizar a adição de pedidos via interface, bem como a automação de alguns processos na área de processar o pedido. Além disso, o sitema é capaz de gerar um relatório em extensão CSV, detalhando os pedidos realizados. Todas as informações do pedido e também algumas informações relevantes (produto mais comprado, produtos populares)  são inseridas em um banco de dados. Nessa versão também foi implementado geração de logs em arquivo TXT.

# CONFIGURAÇÃO 
As configs estão em um arquivo .env de exemplo (sample.env), para o projeto rodar é necessário criar um arquivo .env de exemplo no raiz do projeto, conforme estabelecido no arquivo de exemplo. 

# EXECUTANDO LOCALMENTE
Para executar o projeto localmente em sua máquina é necessário seguir os seguintes passos:
* Clonar o projeto
* Criar uma virtualenv dentro do projeto
* Instalar as dependências necessárias que estão todas contidas em um arquivo (requirements.txt)
* Verificar se o arquivo .env está configurado (Informações de como configurar no tópico de CONFIGURAÇÃO)

Após as etapas acima serem concluídas, para rodar o projeto é muito simples, basta chamar um python main.py

# DEMONSTRAÇÃO DO PROJETO RODANDO 
* Para melhor simulação do negócio, foi criado uma interface grática, na qual é possível registrar informações/ dados de pedido.
  
![2023-07-16 14_40_11-Window](https://github.com/gustavoalisson/project_resource_manager/assets/52181576/3aec7985-5588-43cd-86fd-edc809982169)
* Após ser finalizado os pedidos, irá ser gerado um relatório em .CSV no raiz do projeto
  
![2023-07-16 14_48_02-Window](https://github.com/gustavoalisson/project_resource_manager/assets/52181576/e820c90b-a095-4a70-bcd3-dd89b019e9aa)

* Em uma base de dados SQLite é inserido informações do pedido, entre outros tipos de dados relevantes que não mostro em uma repesentação, mas segue um exemplo:

![2023-07-16 15_04_57-Window](https://github.com/gustavoalisson/project_resource_manager/assets/52181576/43199876-34f5-465e-b47b-50e4f08ab5de)

# PRINCIPAIS TECNOLOGIAS USADAS
* customtkinter / tkinter - Construção de Interface gráfica
* Pandas - Manipulação de dados
* Requests - Para lhe da com API de serviços VIA CEP
  





