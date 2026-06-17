#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef vector<int> vi;
typedef pair<int, int> pii;

const int INF = 0x3f3f3f3f;
const int MOD = 1e9 + 7;

#define endl '\n'

bool eh_alfanumerico(char c) {
    return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9');
}

char para_minusculo(char c) {
    if (c >= 'A' && c <= 'Z') return c + 32;
    return c;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    set<string> stop_words = {
        "o", "a", "os", "as", "um", "uma", "de", "do", "da", "em", "para", "com", "por", 
        "e", "ou", "mas", "que", "se", "eu", "ele", "ela", 
        ".", ",", "!", "?", ";", ":", "-", "(", ")"
    };
    
    ifstream arquivo_entrada("data/input_clean.txt");
    ofstream arquivo_saida("data/output_cpp.txt");

    string linha, palavra_atual;
    
    if (arquivo_entrada.is_open() && arquivo_saida.is_open()) {
        while (getline(arquivo_entrada, linha)) {
            palavra_atual = "";
            
            for (char c : linha) {
                if (eh_alfanumerico(c)) {
                    palavra_atual += para_minusculo(c);
                } else {
                    if (!palavra_atual.empty()) {
                        if (stop_words.find(palavra_atual) == stop_words.end()) {
                            arquivo_saida << palavra_atual << " ";
                        }
                        palavra_atual = "";
                    }
                }
            }
            if (!palavra_atual.empty()) {
                if (stop_words.find(palavra_atual) == stop_words.end()) {
                    arquivo_saida << palavra_atual << " ";
                }
            }
        }
        arquivo_entrada.close();
        arquivo_saida.close();
    } else {
        cerr << "Erro ao abrir arquivos." << endl;
        return 1;
    }
    
    return 0;
}