#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

int main() {
    ifstream arquivo_entrada("data/input_clean.txt");
    ofstream arquivo_saida("data/output_cpp.txt");

    if (!arquivo_entrada.is_open() || !arquivo_saida.is_open()) {
        cerr << "Erro ao abrir os arquivos!" << endl;
        return 1;
    }

    vector<string> stopwords = {"o", "a", "os", "as", "um", "uma", "de", "do", "da", "em", "para", "com", "por", "e", "ou", "mas", "que", "se"};

    string palavra_atual = "";
    char c;

    while (arquivo_entrada.get(c)) {
        if (isalnum(c)) {
            palavra_atual += tolower(c);
        } else {
            if (!palavra_atual.empty()) {
                bool is_stopword = false;
                for (const string& sw : stopwords) {
                    if (palavra_atual == sw) {
                        is_stopword = true;
                        break;
                    }
                }
                if (!is_stopword) {
                    arquivo_saida << palavra_atual << " ";
                }
                palavra_atual = "";
            }
        }
    }

    if (!palavra_atual.empty()) {
        bool is_stopword = false;
        for (const string& sw : stopwords) {
            if (palavra_atual == sw) {
                is_stopword = true;
                break;
            }
        }
        if (!is_stopword) {
            arquivo_saida << palavra_atual << " ";
        }
    }

    return 0;
}