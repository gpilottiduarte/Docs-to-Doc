import os
import re

def process_markdown_file(file_path):
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

        # Remove o bloco de metadados do conteúdo
        content = content[:metadata_match.start()] + content[metadata_match.end():]

        # Remove espaços em branco iniciais
        content = content.lstrip()

        # Adiciona o título H1 no início do conteúdo
        content = h1_title + content

        # Escreve o conteúdo atualizado de volta no arquivo
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Arquivo processado: {file_path}")
    else:
        print(f"Nenhum metadado encontrado em: {file_path}")

def process_markdown_files_in_directory(directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                process_markdown_file(file_path)

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    folder_selected = filedialog.askdirectory(title="Selecione a pasta com os arquivos Markdown")
    if folder_selected:
        process_markdown_files_in_directory(folder_selected)
        messagebox.showinfo("Concluído", "Processamento concluído com sucesso.")
    else:
        messagebox.showwarning("Aviso", "Nenhuma pasta selecionada.")
