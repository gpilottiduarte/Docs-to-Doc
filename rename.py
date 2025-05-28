import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import re

def get_title_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Procura pelo primeiro título H1 ou H2
                if line.startswith('# '):
                    return line[2:].strip()
                elif line.startswith('## '):
                    return line[3:].strip()
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
    return None

def sanitize_filename(filename):
    # Remove caracteres inválidos para nomes de arquivos
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Substitui espaços por sublinhados
    filename = filename.replace(' ', '_')
    filename = filename.strip()
    return filename

def rename_files_based_on_title(directory, progress_callback=None):
    total_files = 0
    file_paths = []

    # Coleta todos os arquivos primeiro
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.md'):
                total_files += 1
                file_paths.append(os.path.join(root, filename))

    processed_files = 0

    # Renomeia os arquivos
    for old_path in file_paths:
        if os.path.exists(old_path):
            title = get_title_from_file(old_path)
            if title:
                sanitized_title = sanitize_filename(title)
                if len(sanitized_title) > 50:
                    sanitized_title = sanitized_title[:50]
                new_filename = f"{sanitized_title}.md"
            else:
                new_filename = os.path.basename(old_path)  # Mantém o nome original se não encontrar título

            new_path = os.path.join(os.path.dirname(old_path), new_filename)

            if old_path != new_path:
                try:
                    # Verifica se o novo nome já existe
                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        print(f"Renomeado: {old_path} -> {new_path}")
                    else:
                        print(f"Aviso: O arquivo {new_path} já existe. Pulando renomeação.")
                except Exception as e:
                    print(f"Erro ao renomear {old_path}: {e}")
        else:
            print(f"Aviso: O arquivo {old_path} não existe mais.")
        processed_files += 1
        if progress_callback:
            progress_callback(processed_files, total_files)

    messagebox.showinfo("Concluído", "Renomeação concluída com sucesso.")

def run_gui():
    root = tk.Tk()
    root.title("Renomear Arquivos Markdown com Base no Título")
    root.geometry("600x200")

    def select_directory():
        directory.set(filedialog.askdirectory(title="Selecione a pasta com os arquivos Markdown"))

    def start_renaming():
        if not directory.get():
            messagebox.showerror("Erro", "Nenhuma pasta selecionada.")
            return

        progress_bar["value"] = 0
        threading.Thread(target=rename_thread, args=(directory.get(),)).start()

    def rename_thread(selected_directory):
        def update_progress(current, total):
            progress = (current / total) * 100
            progress_bar["value"] = progress
            progress_bar.update()

        rename_files_based_on_title(selected_directory, progress_callback=update_progress)

    directory = tk.StringVar()

    ttk.Label(root, text="Selecione a pasta com os arquivos Markdown:").pack(pady=10)
    ttk.Entry(root, textvariable=directory, width=50).pack()
    ttk.Button(root, text="Selecionar Pasta", command=select_directory).pack(pady=5)

    ttk.Button(root, text="Iniciar Renomeação", command=start_renaming).pack(pady=20)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
