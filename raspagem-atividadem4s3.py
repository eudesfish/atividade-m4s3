import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3

# Configuração do WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')  # Executar em modo headless (sem interface gráfica)
chrome_service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# URL do site alvo
url = "https://criancaenatureza.org.br/pt/noticias/"
driver.get(url)

# Aguarde até que a página seja carregada completamente (ajuste conforme necessário)
time.sleep(5)

# Função para obter os dados do site
def obter_dados_do_site():
    try:
        # Ajuste do seletor para obter o título
        titulo = driver.find_element(By.CSS_SELECTOR, 'h1.entry-title').text
        # Ajuste do seletor para obter a data
        data = driver.find_element(By.CSS_SELECTOR, 'span.entry-meta-date').text
        # Ajuste do seletor e adição do .text para obter o texto do elemento <p>
        descricao = driver.find_element(By.CSS_SELECTOR, 'div.entry-content p').text

        # Criar uma lista de dicionários com os dados
        dados = [{'titulo': titulo, 'data': data, 'descricao': descricao}]
        return dados

    except Exception as e:
        print(f"Erro ao obter dados: {str(e)}")
        return None

# Função para salvar os dados no banco de dados SQLite
def salvar_no_sqlite(dados):
    if dados:
        try:
            conn = sqlite3.connect('banco.sqlite3')
            cursor = conn.cursor()

            # Criar a tabela se não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS noticias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT,
                    data TEXT,
                    descricao TEXT
                )
            ''')
            conn.commit()

            # Inserir os dados na tabela
            for dado in dados:
                cursor.execute('''
                    INSERT INTO noticias (titulo, data, descricao) VALUES (?, ?, ?)
                ''', (dado['titulo'], dado['data'], dado['descricao']))
                conn.commit()

            print("Dados salvos com sucesso!")

        except Exception as e:
            print(f"Erro ao salvar no banco de dados: {str(e)}")

        finally:
            conn.close()

# Executar as funções
dados_do_site = obter_dados_do_site()
salvar_no_sqlite(dados_do_site)

# Fechar o navegador
driver.quit()
