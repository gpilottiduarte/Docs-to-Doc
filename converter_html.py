import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import logging
import markdownify  # Você precisa instalar este pacote: pip install markdownify
import re

# Configuração do módulo de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

###############################
# Função para Converter HTML para Markdown
###############################
def convert_html_to_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Remover o bloco de metadados comentado, se existir
        html_content = remove_commented_metadata(html_content)

        # Usar markdownify para converter HTML para Markdown mantendo a formatação
        markdown_content = markdownify.markdownify(html_content, heading_style="ATX")

        # Salvar o conteúdo Markdown no mesmo local, mas com extensão .md
        md_file_path = os.path.splitext(file_path)[0] + '.md'
        with open(md_file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)

        logging.info(f"Arquivo convertido: {file_path} -> {md_file_path}")
    except Exception as e:
        logging.error(f"Erro ao converter o arquivo {file_path}: {e}")

def remove_commented_metadata(html_content):
    # Remover o bloco de metadados comentado, se existir
    pattern = r'<!--\s*## Metadata_Start(.*?)## Metadata_End\s*-->'
    html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)

    # Remover quaisquer linhas restantes que começam com '##' e não fazem parte de comentários HTML
    pattern_uncommented = r'^##.*(?:\n|$)'
    html_content = re.sub(pattern_uncommented, '', html_content, flags=re.MULTILINE)

    # Remover quaisquer comentários HTML que possam ter permanecido
    pattern_html_comments = r'<!--.*?-->'
    html_content = re.sub(pattern_html_comments, '', html_content, flags=re.DOTALL)

    # Remover quaisquer espaços em branco extras
    html_content = html_content.strip()

    return html_content

###############################
# Função para Processar Arquivos em um Diretório
###############################
def process_html_files_in_directory(directory, progress_callback=None, total_files=1, current_file=[0]):
    html_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html') or filename.endswith('.htm'):
                file_path = os.path.join(root, filename)
                html_files.append(file_path)

    total_files = len(html_files)
    current_file[0] = 0

    for file_path in html_files:
        convert_html_to_markdown(file_path)
        current_file[0] += 1
        if progress_callback:
            progress_callback(current_file[0], total_files)

    messagebox.showinfo("Concluído", "Conversão concluída com sucesso.")

###############################
# GUI Principal
###############################
def run_gui():
    root = tk.Tk()
    root.title("Conversão de HTML para Markdown")
    root.geometry("600x200")

    def select_directory():
        directory.set(filedialog.askdirectory(title="Selecione a pasta com os arquivos HTML"))

    def start_conversion():
        if not directory.get():
            messagebox.showerror("Erro", "Nenhuma pasta selecionada.")
            return

        progress_bar["value"] = 0
        threading.Thread(target=process_files_thread, args=(directory.get(),)).start()

    def process_files_thread(selected_directory):
        def update_progress(current, total):
            progress = (current / total) * 100
            progress_bar["value"] = progress
            progress_bar.update()

        process_html_files_in_directory(selected_directory, progress_callback=update_progress)

    directory = tk.StringVar()

    ttk.Label(root, text="Selecione a pasta com os arquivos HTML:").pack(pady=10)
    ttk.Entry(root, textvariable=directory, width=50).pack()
    ttk.Button(root, text="Selecionar Pasta", command=select_directory).pack(pady=5)

    ttk.Button(root, text="Iniciar Conversão", command=start_conversion).pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
