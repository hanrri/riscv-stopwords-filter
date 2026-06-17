#include <bits/stdc++.h>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // Agora usa caminhos relativos à pasta raiz do projeto
    ifstream arq1("data/output_cpp.txt");
    ifstream arq2("data/output_riscv.txt");

    if (!arq1.is_open() || !arq2.is_open()) {
        cerr << "Erro ao abrir um dos arquivos de saída! Verifique se eles foram gerados na pasta /data." << endl;
        return 1;
    }

    string s1, s2;
    int pos = 1;
    bool diferente = false;

    while (arq1 >> s1 && arq2 >> s2) {
        if (s1 != s2) {
            cout << "Diferenca encontrada na posicao (token) " << pos << ":" << endl;
            cout << "Alto Nivel: " << s1 << endl;
            cout << "Baixo Nivel: " << s2 << endl;
            diferente = true;
            break;
        }
        pos++;
    }

    if (!diferente) {
        if (arq1 >> s1) {
            cout << "Arquivo AltoNivel possui mais tokens!" << endl;
            diferente = true;
        } else if (arq2 >> s2) {
            cout << "Arquivo BaixoNivel possui mais tokens!" << endl;
            diferente = true;
        }
    }

    if (!diferente) {
        cout << "Arquivos identicos! Sucesso." << endl;
        return 0;
    }

    return 1;
}