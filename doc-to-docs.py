# Document360 para Docusaurus - Migração de Documentação

# Este script realiza a migração de documentação do Document360 para Docusaurus.
# Inclui etapas de extração, estruturação, conversão de HTML para Markdown e sanitização do conteúdo.

import os
import json
import shutil
import re
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from bs4 import BeautifulSoup, Comment
from concurrent.futures import ThreadPoolExecutor
import logging
import threading

# Configuração do módulo de logging
logging.basicConfig(filename='migration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminhos base para a estrutura de documentos do Docusaurus e os arquivos a serem migrados
BASE_DOCS_PATH = ""
SOURCE_FILES_PATH = ""
CATEGORIES_JSON_PATH = ""
MEDIA_PATH = ""

###############################
# GUI Principal
###############################
# Esta função cria a interface gráfica do usuário (GUI) que permite selecionar o arquivo ZIP exportado pelo Document360
# e o diretório onde os arquivos serão extraídos e migrados.

def run_gui():
    root = tk.Tk()
    root.title("Document360 para Docusaurus - Migração de Documentação")
    root.geometry("600x400")

    def select_zip():
        zip_path.set(filedialog.askopenfilename(title="Selecione o arquivo ZIP exportado pelo Document360", filetypes=[("Arquivos ZIP", "*.zip")]))

    def select_dest_dir():
        dest_dir.set(filedialog.askdirectory(title="Selecione o diretório onde gerar a nova estrutura de documentação"))

    # Função que mostra o botão "Concluído"
    def mostrar_botao_concluido():
        botao_concluido.pack(pady=20) # type: ignore

    # Função que fecha a janela ao clicar no botão "Concluído"
    def concluido():
        root.quit()

    def start_migration():
        if not zip_path.get():
            messagebox.showerror("Erro", "Nenhum arquivo ZIP selecionado.")
            return
        if not dest_dir.get():
            messagebox.showerror("Erro", "Nenhum diretório selecionado.")
            return

        threading.Thread(target=lambda: main(zip_path.get(), dest_dir.get(), progress_bar)).start()
        mostrar_botao_concluido()

    zip_path = tk.StringVar()
    dest_dir = tk.StringVar()

    ttk.Label(root, text="Arquivo ZIP do Document360:").pack(pady=10)
    ttk.Entry(root, textvariable=zip_path, width=50).pack()
    ttk.Button(root, text="Selecionar ZIP", command=select_zip).pack(pady=5)

    ttk.Label(root, text="Diretório de Destino:").pack(pady=10)
    ttk.Entry(root, textvariable=dest_dir, width=50).pack()
    ttk.Button(root, text="Selecionar Diretório", command=select_dest_dir).pack(pady=5)

    ttk.Button(root, text="Iniciar Migração", command=start_migration).pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(pady=20)

    root.mainloop()


###############################
# Cria Estrutura de Diretórios
###############################
# Esta função cria a estrutura de diretórios para armazenar os arquivos do Docusaurus de acordo com as categorias definidas no JSON.

def create_directory_structure(base_path, categories, parent_path="", progress_callback=None, total_steps=1, current_step=0):
    try:
        for category in categories:
            current_step += 1
            # Verifica se a chave 'Title' existe no dicionário da categoria
            if 'Title' not in category:
                logging.error(f"Categoria sem título encontrada. Categoria: {category}")
                continue
            
            # Define o caminho da categoria e cria o diretório se necessário
            category_path = os.path.join(base_path, parent_path, category['Title'])
            os.makedirs(category_path, exist_ok=True)
            
            # Atualizar barra de progresso
            if progress_callback:
                progress_callback(current_step, total_steps)
            
            # Move os artigos correspondentes para o diretório da categoria
            move_articles_to_category(category_path, category.get('Articles', []))
            
            # Cria recursivamente a estrutura para as subcategorias
            subcategories = category.get('SubCategories', [])
            total_steps += len(subcategories)
            create_directory_structure(base_path, subcategories, os.path.join(parent_path, category['Title']), progress_callback, total_steps, current_step)
    except Exception as error:
        logging.error(f"Erro ao criar estrutura de diretórios: {error}")

###############################
# Movimentar Artigos com Tratamento de Erros Centralizado
###############################
# Esta função move os artigos para as pastas correspondentes de acordo com a categoria especificada no JSON.

def move_articles_to_category(category_path, articles):
    try:
        for article in articles:
            move_article_to_category(category_path, article)
    except Exception as error:
        logging.error(f"Erro ao mover artigos para a categoria '{category_path}': {error}")


def move_article_to_category(category_path, article):
    article_path = os.path.join(category_path, article['Path'])
    source_article_path = os.path.join(SOURCE_FILES_PATH, article['Path'])
    
    # Cria o diretório de destino, caso não exista
    os.makedirs(os.path.dirname(article_path), exist_ok=True)
    
    # Verifica se o arquivo de origem existe antes de tentar movê-lo
    if os.path.exists(source_article_path):
        shutil.move(source_article_path, article_path)
        logging.info(f"Arquivo movido: {source_article_path} -> {article_path}")
    else:
        logging.warning(f"Arquivo não encontrado: {source_article_path}")

###############################
# Converter HTML para Markdown com Threads
###############################
# Esta função converte arquivos HTML em arquivos Markdown utilizando múltiplas threads para melhorar a performance.

def convert_html_to_markdown(base_docs_path, progress_callback=None, total_steps=1, current_step=0):
    html_files = list(get_files_by_extension(base_docs_path, ".html"))
    total_steps = len(html_files)
    with ThreadPoolExecutor() as executor:
        for _ in executor.map(process_html_file, html_files):
            current_step += 1
            if progress_callback:
                progress_callback(current_step, total_steps)

def process_html_file(html_file_path):
    md_file_path = get_md_file_path(html_file_path)
    content = read_file(html_file_path)
    
    title = extract_title(content)
    content = remove_metadata(content)
    markdown_content = html_to_markdown(content, title)
    
    write_file(md_file_path, markdown_content)
    logging.info(f"Convertido: {html_file_path} -> {md_file_path}")
    
    remove_file(html_file_path)
    logging.info(f"Removido arquivo HTML: {html_file_path}")

###############################
# Sanitizar Markdown com Threads
###############################
# Esta função sanitiza arquivos Markdown removendo conteúdos indesejados ou problemáticos.

def sanitize_markdown_files(base_docs_path, progress_callback=None, total_steps=1, current_step=0):
    md_files = list(get_files_by_extension(base_docs_path, ".md"))
    total_steps = len(md_files)
    with ThreadPoolExecutor() as executor:
        for _ in executor.map(process_md_file, md_files):
            current_step += 1
            if progress_callback:
                progress_callback(current_step, total_steps)

def process_md_file(md_file_path):
    try:
        with open(md_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remover cabeçalho de metadados e extrair o título
        title_match = re.search(r"## Metadata_Start.*?## title: (.*?)\n.*?## Metadata_End", content, re.DOTALL)
        if title_match:
            title = title_match.group(1)
            content = re.sub(r"## Metadata_Start.*?## Metadata_End", "", content, flags=re.DOTALL).strip()
            content = f"# {title}\n\n" + content

        with open(md_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        logging.info(f"Processado: {md_file_path}")
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo Markdown '{md_file_path}': {e}")


###############################
# Funções Utilitárias
###############################
# Funções auxiliares para lidar com arquivos, como leitura, escrita e remoção.

def get_files_by_extension(base_path, extension):
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)

def get_md_file_path(html_file_path):
    return os.path.splitext(html_file_path)[0] + ".md"

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def remove_file(file_path):
    os.remove(file_path)

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo JSON '{file_path}': {e}")
        return None

###############################
# Extração e Limpeza de Conteúdo
###############################
# Estas funções lidam com a extração do título do HTML, a limpeza de metadados e a conversão do HTML para Markdown.

def extract_title(content):
    match = re.search(r"## title: (.*?)\n", content)
    return f"# {match.group(1)}\n\n" if match else ""

def remove_metadata(content):
    return re.sub(r"## Metadata_Start.*?## Metadata_End", "", content, flags=re.DOTALL)

def html_to_markdown(content, title):
    soup = BeautifulSoup(content, 'html.parser')
    remove_unwanted_tags(soup)
    markdown_content = soup.get_text(separator="\n")
    sanitized_content = sanitize_content(markdown_content)
    return title + sanitized_content.strip()

def remove_unwanted_tags(soup):
    for tag in soup(['script', 'style']):
        tag.decompose()
    for comment in soup.findAll(string=lambda text: isinstance(text, Comment)):
        comment.extract()

# Compilação de padrões regex para melhor performance
TAG_PATTERN = re.compile(r"[{<].*?[}>]")
LINK_PATTERN = re.compile(r"\[.*?\]\(.*?\)")
INLINE_CODE_PATTERN = re.compile(r"`.*?`")
BOLD_PATTERN = re.compile(r"\*\*.*?\*\*")
UNDERLINE_PATTERN = re.compile(r"__.*?__")

def sanitize_content(content):
    content = TAG_PATTERN.sub("", content)  # Remove expressões e tags problemáticas
    content = LINK_PATTERN.sub("", content)  # Remove links malformados
    content = INLINE_CODE_PATTERN.sub("", content)  # Remove expressões em inline code malformadas
    content = BOLD_PATTERN.sub("", content)  # Remove negrito problemático
    content = UNDERLINE_PATTERN.sub("", content)  # Remove sublinhados malformados
    return content

###############################
# Função Principal
###############################
# Esta é a função principal que gerencia o fluxo de migração.

def main(zip_path, dest_dir, progress_bar=None):
    def update_progress(current_step, total_steps):
        progress = (current_step / total_steps) * 100
        if progress_bar:
            progress_bar["value"] = progress
            progress_bar.update()
    
    # Remover verificação da estrutura do ZIP
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
    except zipfile.BadZipFile:
        logging.error(f"O arquivo ZIP '{zip_path}' está corrompido e não pôde ser extraído.")
        messagebox.showerror("Erro", f"O arquivo ZIP '{zip_path}' está corrompido e não pôde ser extraído.")
        return
    except Exception as error:
        logging.error(f"Erro ao extrair o arquivo ZIP: {error}")
        messagebox.showerror("Erro", f"Erro ao extrair o arquivo ZIP: {error}")
        return
    
    # Determinar o nome da pasta de versão automaticamente
    version_folder = None
    for item in os.listdir(dest_dir):
        if os.path.isdir(os.path.join(dest_dir, item)) and item.startswith("v"):
            version_folder = item
            break

    if not version_folder:
        logging.error("Não foi possível determinar a pasta da versão automaticamente.")
        messagebox.showerror("Erro", "Não foi possível determinar a pasta da versão automaticamente.")
        return
        
    # Definir caminhos após extração
    global BASE_DOCS_PATH, SOURCE_FILES_PATH, CATEGORIES_JSON_PATH, MEDIA_PATH
    BASE_DOCS_PATH = os.path.join(dest_dir, "docusaurus", "docs")
    SOURCE_FILES_PATH = os.path.join(dest_dir, version_folder, "articles")
    CATEGORIES_JSON_PATH = os.path.join(dest_dir, version_folder, f"{version_folder}_categories_articles.json")
    MEDIA_PATH = os.path.join(dest_dir, "Media")

    # Carrega o arquivo JSON contendo a estrutura da documentação
    data = load_json_file(CATEGORIES_JSON_PATH)
    if data and 'Categories' in data:
        total_steps = len(data['Categories'])
        create_directory_structure(BASE_DOCS_PATH, data['Categories'], progress_callback=update_progress, total_steps=total_steps)
    
    # Converte arquivos HTML para Markdown
    logging.info("Iniciando a conversão de HTML para Markdown...")
    convert_html_to_markdown(BASE_DOCS_PATH, progress_callback=update_progress)
    logging.info("Processo de conversão concluído.")
    
    # Sanitiza arquivos Markdown
    logging.info("Iniciando a sanitização dos arquivos Markdown...")
    sanitize_markdown_files(BASE_DOCS_PATH, progress_callback=update_progress)
    logging.info("Sanitização dos arquivos Markdown concluída.")

if __name__ == "__main__":
    run_gui()
