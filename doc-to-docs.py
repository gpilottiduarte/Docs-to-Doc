import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
<<<<<<< HEAD
import markdownify as md
=======
import logging
import zipfile
import shutil
>>>>>>> 361e73057f22f1fbde4c7138d80b0aa96da801a9

# Configuração do módulo de logging
logging.basicConfig(filename='migration.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
<<<<<<< HEAD

    # Função que fecha a janela ao clicar no botão "Concluído"
    def concluido():
        root.quit()

=======
    
>>>>>>> 361e73057f22f1fbde4c7138d80b0aa96da801a9
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
<<<<<<< HEAD
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
    try:
        md_file_path = get_md_file_path(html_file_path)
        
        # Ler o conteúdo do arquivo HTML
        content = read_file(html_file_path)
        
        # Extrair o título e remover metadados
        title = extract_title(content)
        cleaned_content = remove_metadata(content)

        # Converter HTML para Markdown
        markdown_content = html_to_markdown(cleaned_content, title)

        # Escrever o conteúdo convertido no arquivo Markdown
        write_file(md_file_path, markdown_content)
        logging.info(f"Convertido: {html_file_path} -> {md_file_path}")

        # Remover o arquivo HTML original
        remove_file(html_file_path)
        logging.info(f"Removido arquivo HTML: {html_file_path}")
    
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo HTML '{html_file_path}': {e}")
=======
def sanitize_folder_name(name):
    # Remove caracteres inválidos para nomes de pastas
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    return name.strip()
>>>>>>> 361e73057f22f1fbde4c7138d80b0aa96da801a9

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

<<<<<<< HEAD

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
        # Converter HTML para Markdown usando markdownify
        markdown_content = md(content)
        # Escrever o conteúdo convertido no arquivo Markdown
        with open(md_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        logging.info(f"Processado: {md_file_path}")
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo Markdown '{md_file_path}': {e}")
=======
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
>>>>>>> 361e73057f22f1fbde4c7138d80b0aa96da801a9

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

<<<<<<< HEAD
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

=======
>>>>>>> 361e73057f22f1fbde4c7138d80b0aa96da801a9
if __name__ == "__main__":
    run_gui()
