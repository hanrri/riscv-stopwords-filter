import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
BIN_DIR = os.path.join(BASE_DIR, "bin")
SRC_DIR = os.path.join(BASE_DIR, "src")

INPUT_RAW = os.path.join(DATA_DIR, "input_raw.txt")
OUTPUT_CPP = os.path.join(DATA_DIR, "output_cpp.txt")
OUTPUT_RISCV = os.path.join(DATA_DIR, "output_riscv.txt")

RARS_PATH = os.path.join(BASE_DIR, "rars.jar") 

def escrever_texto():
    janela_texto = tk.Toplevel(root)
    janela_texto.title("Digitar Texto Bruto")
    janela_texto.geometry("500x400")

    def salvar_texto():
        texto = caixa_texto.get("1.0", tk.END)
        with open(INPUT_RAW, 'w', encoding='utf-8') as f:
            f.write(texto.strip())
        messagebox.showinfo("Sucesso", "Texto salvo em input_raw.txt!")
        janela_texto.destroy()

    btn_salvar = tk.Button(janela_texto, text="Salvar Texto", command=salvar_texto, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    btn_salvar.pack(side="top", fill="x", padx=10, pady=10)

    caixa_texto = scrolledtext.ScrolledText(janela_texto, wrap=tk.WORD, font=("Arial", 11))
    caixa_texto.pack(side="bottom", expand=True, fill='both', padx=10, pady=(0, 10))

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo de texto",
        filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*"))
    )
    if caminho_arquivo:
        try:
            shutil.copy(caminho_arquivo, INPUT_RAW)
            messagebox.showinfo("Sucesso", "Arquivo carregado para input_raw.txt com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar arquivo:\n{e}")

def rodar_preprocessamento():
    script_path = os.path.join(SCRIPTS_DIR, "text_normalizer.py")
    try:
        subprocess.run(["python", script_path], cwd=BASE_DIR, check=True)
        messagebox.showinfo("Sucesso", "Pré-processamento concluído! (input_clean.txt gerado)")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao rodar pré-processamento:\n{e}")

def rodar_filtro_cpp():
    exe_path = os.path.join(BIN_DIR, "high_level_filter")
    try:
        subprocess.run([exe_path], cwd=BASE_DIR, check=True)
        messagebox.showinfo("Sucesso", "Filtro C++ executado! (output_cpp.txt gerado)")
    except FileNotFoundError:
        messagebox.showerror("Erro", "Executável do C++ não encontrado. Compile-o e coloque na pasta /bin.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao executar o código C++:\n{e}")

def rodar_filtro_riscv():
    asm_path = os.path.join(SRC_DIR, "low_level_filter.asm")
    if not os.path.exists(RARS_PATH):
        messagebox.showwarning("Aviso", "Arquivo rars.jar não encontrado na raiz do projeto.")
        return
    try:
        subprocess.run(["java", "-jar", RARS_PATH, "nc", asm_path], cwd=BASE_DIR, check=True)
        messagebox.showinfo("Sucesso", "Filtro RISC-V executado! (output_riscv.txt gerado)")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao executar o Assembly:\n{e}")

def abrir_txt(caminho):
    if not os.path.exists(caminho):
        messagebox.showwarning("Aviso", f"O arquivo não existe ainda:\n{caminho}")
        return
    try:
        subprocess.run(["xdg-open", caminho], cwd=BASE_DIR)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível abrir o arquivo:\n{e}")

def rodar_comparacao():
    exe_path = os.path.join(BIN_DIR, "output_comparator")
    try:
        resultado = subprocess.run([exe_path], cwd=BASE_DIR, capture_output=True, text=True, check=True)
        messagebox.showinfo("Resultado da Comparação", resultado.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showwarning("Diferença Encontrada!", e.stdout)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Executável do comparador não encontrado. Compile-o e coloque na pasta /bin.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro crítico ao comparar:\n{e}")

root = tk.Tk()
root.title("RISC-V Stopwords Filter - Manager")
root.geometry("450x500")
root.resizable(False, False)

fonte_titulo = ("Arial", 12, "bold")
fonte_btn = ("Arial", 10)

frame_entrada = tk.LabelFrame(root, text="1. Entrada de Dados", font=fonte_titulo, padx=10, pady=10)
frame_entrada.pack(fill="x", padx=15, pady=5)

tk.Button(frame_entrada, text="Digitar Texto Bruto", font=fonte_btn, command=escrever_texto).pack(side="left", expand=True, fill="x", padx=5)
tk.Button(frame_entrada, text="Selecionar Arquivo .txt", font=fonte_btn, command=selecionar_arquivo).pack(side="right", expand=True, fill="x", padx=5)

frame_pre = tk.LabelFrame(root, text="2. Pré-processamento", font=fonte_titulo, padx=10, pady=10)
frame_pre.pack(fill="x", padx=15, pady=5)

tk.Button(frame_pre, text="Rodar Normalizador (Python)", font=fonte_btn, command=rodar_preprocessamento).pack(fill="x", padx=5)

frame_filtros = tk.LabelFrame(root, text="3. Execução dos Filtros", font=fonte_titulo, padx=10, pady=10)
frame_filtros.pack(fill="x", padx=15, pady=5)

tk.Button(frame_filtros, text="Rodar Filtro em C++", font=fonte_btn, command=rodar_filtro_cpp, bg="#e0e0e0").pack(fill="x", padx=5, pady=2)
tk.Button(frame_filtros, text="Rodar Filtro RISC-V (Assembly)", font=fonte_btn, command=rodar_filtro_riscv, bg="#e0e0e0").pack(fill="x", padx=5, pady=2)

frame_visualizar = tk.LabelFrame(root, text="4. Visualização", font=fonte_titulo, padx=10, pady=10)
frame_visualizar.pack(fill="x", padx=15, pady=5)

tk.Button(frame_visualizar, text="Ver Saída C++", font=fonte_btn, command=lambda: abrir_txt(OUTPUT_CPP)).pack(side="left", expand=True, fill="x", padx=5)
tk.Button(frame_visualizar, text="Ver Saída RISC-V", font=fonte_btn, command=lambda: abrir_txt(OUTPUT_RISCV)).pack(side="right", expand=True, fill="x", padx=5)

frame_valida = tk.LabelFrame(root, text="5. Validação Final", font=fonte_titulo, padx=10, pady=10)
frame_valida.pack(fill="x", padx=15, pady=5)

tk.Button(frame_valida, text="COMPARAR SAÍDAS", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", command=rodar_comparacao).pack(fill="x", padx=5, pady=5)

root.mainloop()