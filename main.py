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
INPUT_CLEAN = os.path.join(DATA_DIR, "input_clean.txt")
OUTPUT_CPP = os.path.join(DATA_DIR, "output_cpp.txt")
OUTPUT_RISCV = os.path.join(DATA_DIR, "output_riscv.txt")
RARS_PATH = os.path.join(BASE_DIR, "rars.jar") 

def escrever_texto():
    janela_texto = tk.Toplevel(root)
    janela_texto.title("Digitar Texto Bruto")
    janela_texto.geometry("500x400")

    def salvar_e_fechar():
        texto = caixa_texto.get("1.0", tk.END)
        with open(INPUT_RAW, 'w', encoding='utf-8') as f:
            f.write(texto.strip())
        janela_texto.destroy()

    btn_salvar = tk.Button(janela_texto, text="Salvar", command=salvar_e_fechar, bg="#4CAF50", fg="white")
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
            messagebox.showinfo("Sucesso", "Arquivo carregado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

def rodar_preprocessamento():
    script_path = os.path.join(SCRIPTS_DIR, "text_normalizer.py")
    try:
        subprocess.run(["python", script_path], cwd=BASE_DIR, check=True)
        messagebox.showinfo("Sucesso", "Pré-processamento concluído!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {e}")

def rodar_filtro_cpp():
    exe_path = os.path.join(BIN_DIR, "high_level_filter")
    try:
        subprocess.run([exe_path], cwd=BASE_DIR, check=True)
        messagebox.showinfo("Sucesso", "Filtro C++ executado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {e}")

def rodar_filtro_riscv():
    asm_path = os.path.join(SRC_DIR, "low_level_filter.asm")
    try:
        subprocess.run(["java", "-jar", RARS_PATH, "nc", asm_path], cwd=BASE_DIR, check=True)
        messagebox.showinfo("Sucesso", "Filtro RISC-V executado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {e}")

def abrir_txt(caminho):
    if not os.path.exists(caminho):
        messagebox.showwarning("Aviso", "Arquivo não encontrado!")
        return
    subprocess.run(["xdg-open", caminho], cwd=BASE_DIR)

def rodar_comparacao():
    exe_path = os.path.join(BIN_DIR, "output_comparator")
    try:
        resultado = subprocess.run([exe_path], cwd=BASE_DIR, capture_output=True, text=True, check=True)
        messagebox.showinfo("Resultado", resultado.stdout)
    except subprocess.CalledProcessError as e:
        messagebox.showwarning("Diferença Encontrada!", e.stdout)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro crítico: {e}")

root = tk.Tk()
root.title("RISC-V Filter Manager")
root.geometry("450x550")

fonte_titulo = ("Arial", 11, "bold")
fonte_btn = ("Arial", 9)

frame_entrada = tk.LabelFrame(root, text="1. Entrada", font=fonte_titulo, padx=10, pady=5)
frame_entrada.pack(fill="x", padx=10, pady=5)
tk.Button(frame_entrada, text="Digitar", font=fonte_btn, command=escrever_texto).pack(side="left", expand=True, fill="x", padx=2)
tk.Button(frame_entrada, text="Selecionar", font=fonte_btn, command=selecionar_arquivo).pack(side="right", expand=True, fill="x", padx=2)

frame_pre = tk.LabelFrame(root, text="2. Processamento", font=fonte_titulo, padx=10, pady=5)
frame_pre.pack(fill="x", padx=10, pady=5)
tk.Button(frame_pre, text="Rodar Normalizador (Python)", font=fonte_btn, command=rodar_preprocessamento).pack(fill="x")

frame_filtros = tk.LabelFrame(root, text="3. Filtros", font=fonte_titulo, padx=10, pady=5)
frame_filtros.pack(fill="x", padx=10, pady=5)
tk.Button(frame_filtros, text="Filtro C++", font=fonte_btn, command=rodar_filtro_cpp).pack(fill="x", pady=2)
tk.Button(frame_filtros, text="Filtro RISC-V", font=fonte_btn, command=rodar_filtro_riscv).pack(fill="x", pady=2)

frame_visualizar = tk.LabelFrame(root, text="4. Visualizar Arquivos", font=fonte_titulo, padx=10, pady=5)
frame_visualizar.pack(fill="x", padx=10, pady=5)
frame_visualizar.columnconfigure(0, weight=1)
frame_visualizar.columnconfigure(1, weight=1)

tk.Button(frame_visualizar, text="Ver Raw", command=lambda: abrir_txt(INPUT_RAW)).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
tk.Button(frame_visualizar, text="Ver Clean", command=lambda: abrir_txt(INPUT_CLEAN)).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
tk.Button(frame_visualizar, text="Ver Saída C++", command=lambda: abrir_txt(OUTPUT_CPP)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
tk.Button(frame_visualizar, text="Ver Saída RISC-V", command=lambda: abrir_txt(OUTPUT_RISCV)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)

frame_valida = tk.LabelFrame(root, text="5. Validação", font=fonte_titulo, padx=10, pady=5)
frame_valida.pack(fill="x", padx=10, pady=5)
tk.Button(frame_valida, text="COMPARAR SAÍDAS", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", command=rodar_comparacao).pack(fill="x", pady=5)

root.mainloop()