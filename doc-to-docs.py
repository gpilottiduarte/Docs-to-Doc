import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import logging
import zipfile
import shutil

# Configuração do módulo de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

###############################
# GUI Principal
###############################
def run_gui():
    root = tk.Tk()
    root.title("Document360 para Docusaurus - Migração de Documentação")
    root.geometry("600x400")

    def select_zip():
        zip_path.set(filedialog.askopenfilename(title="Selecione o arquivo ZIP exportado pelo Document360", filetypes=[("Arquivos ZIP", "*.zip")]))
    
    def select_dest_dir():
        dest_dir.set(filedialog.askdirectory(title="Selecione o diretório onde gerar a nova estrutura de documentação"))
    
    def start_migration():
        if not zip_path.get():
            messagebox.showerror("Erro", "Nenhum arquivo ZIP selecionado.")
            return
        if not dest_dir.get():
            messagebox.showerror("Erro", "Nenhum diretório selecionado.")
            return

        threading.Thread(target=main, args=(zip_path.get(), dest_dir.get(), progress_bar)).start()

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
def create_directory_structure(base_path, categories, parent_path="", progress_callback=None, total_steps=1, current_step=[0]):
    try:
        for category in categories:
            current_step[0] += 1
            # Verifica se a chave 'Title' existe no dicionário da categoria
            if 'Title' not in category:
                logging.error(f"Categoria sem título encontrada. Categoria: {category}")
                continue

            # Define o caminho da categoria e cria o diretório se necessário
            category_name = sanitize_folder_name(category['Title'])
            category_path = os.path.join(base_path, parent_path, category_name)
            os.makedirs(category_path, exist_ok=True)
            logging.info(f"Diretório criado: {category_path}")

            # Atualizar barra de progresso
            if progress_callback:
                progress_callback(current_step[0], total_steps)

            # Cria recursivamente a estrutura para as subcategorias
            subcategories = category.get('SubCategories', [])
            create_directory_structure(base_path, subcategories, os.path.join(parent_path, category_name), progress_callback, total_steps, current_step)

    except Exception as error:
        logging.error(f"Erro ao criar estrutura de diretórios: {error}")

def move_articles(base_path, categories, parent_path="", articles_base_path="", progress_callback=None, total_steps=1, current_step=[0]):
    try:
        for category in categories:
            if 'Title' not in category:
                continue

            category_name = sanitize_folder_name(category['Title'])
            category_path = os.path.join(base_path, parent_path, category_name)

            # Move artigos nesta categoria
            articles = category.get('Articles', [])
            for article in articles:
                current_step[0] += 1
                move_article_to_category(articles_base_path, category_path, article)
                # Atualizar barra de progresso
                if progress_callback:
                    progress_callback(current_step[0], total_steps)

            # Recurse nas subcategorias
            subcategories = category.get('SubCategories', [])
            move_articles(base_path, subcategories, os.path.join(parent_path, category_name), articles_base_path, progress_callback, total_steps, current_step)

    except Exception as error:
        logging.error(f"Erro ao mover artigos: {error}")

def move_article_to_category(articles_base_path, category_path, article):
    if 'Path' not in article:
        logging.warning(f"Artigo sem 'Path': {article}")
        return

    source_article_path = os.path.join(articles_base_path, article['Path'])
    destination_article_path = os.path.join(category_path, os.path.basename(article['Path']))

    # Cria o diretório de destino, caso não exista
    os.makedirs(os.path.dirname(destination_article_path), exist_ok=True)

    # Verifica se o arquivo de origem existe antes de tentar movê-lo
    if os.path.exists(source_article_path):
        shutil.move(source_article_path, destination_article_path)
        logging.info(f"Artigo movido: {source_article_path} -> {destination_article_path}")
    else:
        logging.warning(f"Artigo não encontrado: {source_article_path}")

###############################
# Sanitizar Nomes de Pastas
###############################
def sanitize_folder_name(name):
    # Remove caracteres inválidos para nomes de pastas
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()

###############################
# Contar Total de Passos
###############################
def count_total_steps(categories):
    total = 0
    for category in categories:
        total += 1  # Para a categoria em si
        articles = category.get('Articles', [])
        total += len(articles)  # Cada artigo é um passo
        subcategories = category.get('SubCategories', [])
        total += count_total_steps(subcategories)  # Contar recursivamente
    return total

###############################
# Função Principal
###############################
def main(zip_file_path, dest_dir, progress_bar=None):
    def update_progress(current_step, total_steps):
        progress = (current_step / total_steps) * 100
        if progress_bar:
            progress_bar["value"] = progress
            progress_bar.update()

    # Extrair o arquivo ZIP
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
        logging.info(f"Arquivo ZIP extraído para {dest_dir}")
    except zipfile.BadZipFile:
        logging.error(f"O arquivo ZIP '{zip_file_path}' está corrompido.")
        messagebox.showerror("Erro", f"O arquivo ZIP '{zip_file_path}' está corrompido.")
        return
    except Exception as e:
        logging.error(f"Erro ao extrair o arquivo ZIP: {e}")
        messagebox.showerror("Erro", f"Erro ao extrair o arquivo ZIP: {e}")
        return

    # Localizar o arquivo JSON de categorias
    json_file_path = None
    for root, dirs, files in os.walk(dest_dir):
        for file in files:
            if file.endswith('_categories_articles.json'):
                json_file_path = os.path.join(root, file)
                break
        if json_file_path:
            break

    if not json_file_path:
        logging.error("Arquivo JSON de categorias não encontrado.")
        messagebox.showerror("Erro", "Arquivo JSON de categorias não encontrado.")
        return

    logging.info(f"Arquivo JSON encontrado: {json_file_path}")

    # Carrega o arquivo JSON contendo a estrutura da documentação
    data = load_json_file(json_file_path)
    if not data or 'Categories' not in data:
        logging.error("O arquivo JSON não contém a chave 'Categories'.")
        messagebox.showerror("Erro", "O arquivo JSON não contém a chave 'Categories'.")
        return

    # Contar total de passos para a barra de progresso
    total_steps = count_total_steps(data['Categories'])
    current_step = [0]

    # Criar estrutura de diretórios
    create_directory_structure(dest_dir, data['Categories'], progress_callback=update_progress, total_steps=total_steps, current_step=current_step)

    # Localizar a pasta 'articles'
    articles_folder = None
    for root, dirs, files in os.walk(dest_dir):
        for dir_name in dirs:
            if dir_name == "articles":
                articles_folder = os.path.join(root, dir_name)
                break
        if articles_folder:
            break

    if not articles_folder:
        logging.error("Pasta 'articles' não encontrada.")
        messagebox.showerror("Erro", "Pasta 'articles' não encontrada.")
        return

    logging.info(f"Pasta de artigos encontrada: {articles_folder}")

    # Mover os arquivos conforme a estrutura do JSON
    move_articles(dest_dir, data['Categories'], articles_base_path=articles_folder, progress_callback=update_progress, total_steps=total_steps, current_step=current_step)

    logging.info("Estrutura de diretórios criada e arquivos movidos com sucesso.")
    messagebox.showinfo("Concluído", "Estrutura de diretórios criada e arquivos movidos com sucesso.")

###############################
# Funções Utilitárias
###############################
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo JSON '{file_path}': {e}")
        messagebox.showerror("Erro", f"Erro ao carregar o arquivo JSON '{file_path}': {e}")
        return None

if __name__ == "__main__":
    run_gui()
