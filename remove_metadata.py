import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import logging

# Configuração do módulo de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

###############################
# Função para Processar Arquivo Markdown
###############################
def process_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Expressão regular para encontrar o bloco de metadados
        metadata_pattern = re.compile(r"## Metadata_Start(.*?)## Metadata_End", re.DOTALL)
        metadata_match = metadata_pattern.search(content)

        if metadata_match:
            metadata_block = metadata_match.group(1)

            # Expressão regular para extrair o valor do título
            title_pattern = re.compile(r"## title: (.*)")
            title_match = title_pattern.search(metadata_block)

            if title_match:
                title = title_match.group(1).strip()
                h1_title = f"# {title}\n\n"
            else:
                h1_title = ""
                logging.warning(f"Título não encontrado em {file_path}")

            # Remove o bloco de metadados do conteúdo
            content = content[:metadata_match.start()] + content[metadata_match.end():]

            # Remove espaços em branco iniciais
            content = content.lstrip()

            # Adiciona o título H1 no início do conteúdo
            content = h1_title + content

            # Escreve o conteúdo atualizado de volta no arquivo
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logging.info(f"Arquivo processado: {file_path}")
        else:
            logging.info(f"Nenhum metadado encontrado em: {file_path}")
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo {file_path}: {e}")

###############################
# Função para Processar Arquivos em um Diretório
###############################
def process_markdown_files_in_directory(directory, progress_callback=None, total_files=1, current_file=[0]):
    markdown_files = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                markdown_files.append(file_path)

    total_files = len(markdown_files)
    current_file[0] = 0

    for file_path in markdown_files:
        process_markdown_file(file_path)
        current_file[0] += 1
        if progress_callback:
            progress_callback(current_file[0], total_files)

###############################
# GUI Principal
###############################
def run_gui():
    root = tk.Tk()
    root.title("Limpeza de Arquivos Markdown")
    root.geometry("600x200")

    def select_directory():
        directory.set(filedialog.askdirectory(title="Selecione a pasta com os arquivos Markdown"))

    def start_processing():
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

        process_markdown_files_in_directory(selected_directory, progress_callback=update_progress)
        messagebox.showinfo("Concluído", "Processamento concluído com sucesso.")

    directory = tk.StringVar()

    ttk.Label(root, text="Selecione a pasta com os arquivos Markdown:").pack(pady=10)
    ttk.Entry(root, textvariable=directory, width=50).pack()
    ttk.Button(root, text="Selecionar Pasta", command=select_directory).pack(pady=5)

    ttk.Button(root, text="Iniciar Limpeza", command=start_processing).pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
