# ⚙️ Filtro de Stopwords: C++ vs RISC-V Assembly

Este é um projeto prático de Arquitetura de Computadores que demonstra a filtragem de "stopwords" (palavras comuns irrelevantes para buscas, como artigos, conjunções, etc.) em um texto. 

O grande diferencial deste projeto é a comparação direta entre uma linguagem de alto nível (**C++**) e uma de baixo nível (**Assembly RISC-V**), com uma interface gráfica amigável desenvolvida em **Python (Tkinter)** para gerenciar todo o pipeline de dados.

---

## 🖥️ Como a Interface Funciona

A interface foi pensada para ser um painel de controle passo a passo do processamento do texto:

1. **Entrada de Dados:** Você pode digitar o texto bruto diretamente na interface ou importar um arquivo `.txt` pronto do seu computador.
2. **Pré-processamento:** Um script em Python varre o texto convertendo caracteres UTF-8 para ASCII puro (removendo acentuações e caracteres especiais), deixando o texto "limpo" e pronto para o processador.
3. **Filtros de Stopwords:** Botões para executar o programa em C++ e/ou o simulador do RISC-V (via RARS). Ambos processam o texto limpo e geram seus próprios arquivos de saída.
4. **Visualizador de Arquivos:** Uma seção dedicada para você abrir e acompanhar em tempo real as mudanças: o texto cru (*Raw*), o texto normalizado (*Clean*) e as saídas de ambas as linguagens.
5. **Comparação/Validação Final:** Um validador que checa os arquivos de saída gerados pelo C++ e pelo RISC-V. Se a lógica do Assembly estiver perfeita, os arquivos devem ser 100% idênticos!

---

## 📂 Organização do Código

O projeto está modularizado para separar a interface, os scripts auxiliares, o código fonte e os compilados:

* `/src/`: Contém os códigos fonte principais.
  * `high_level_filter.cpp`: A lógica de filtragem escrita em C++.
  * `low_level_filter.asm`: A mesma lógica escrita em Assembly RISC-V.
* `/scripts/`: Scripts auxiliares em Python e C++.
  * `text_normalizer.py`: Responsável por transformar UTF-8 em ASCII.
  * `output_comparator.cpp`: Lógica que compara as saídas finais.
* `/bin/`: Pasta que guarda os executáveis (binários) compilados do C++ para rodar na interface.
* `/data/`: Pasta de trabalho (ignorada no Git) onde os arquivos `.txt` (input e output) são temporariamente salvos e lidos pela interface.
* `main.py`: O código principal da Interface Gráfica em Tkinter.
* `rars.jar`: Simulador do processador RISC-V.

---

## 🚀 Como Rodar na Sua Máquina

### Pré-requisitos
Para rodar este projeto, você precisará ter instalado no seu sistema:
* **Python 3**
* **Tkinter** (Já vem por padrão no Windows. No Linux Ubuntu/Debian, instale com: `sudo apt-get install python3-tk`)
* **Java** (para rodar o simulador `rars.jar`)
* Um compilador **C++** (como `g++`) caso precise recompilar os binários para o seu sistema operacional.

### Execução
1. Faça o clone do repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/riscv-stopwords-filter.git](https://github.com/SEU_USUARIO/riscv-stopwords-filter.git)

2. Entre na pasta do projeto:
   ```bash
    cd riscv-stopwords-filter

3. (Opcional) Recompile os arquivos C++ se estiver fora de um ambiente Linux compatível:
   ```bash
    g++ src/high_level_filter.cpp -o bin/high_level_filter
    g++ scripts/output_comparator.cpp -o bin/output_comparator

4. Execute o painel gerenciador:
   ```bash
    python main.py

Projeto desenvolvido para a disciplina de Arquitetura de Computadores.
