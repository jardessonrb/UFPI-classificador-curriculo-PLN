import os
import re

caminho_script = os.path.dirname(os.path.abspath(__file__))

def buscar_arquivo(nome_arquivo: str) -> list[str]:
    linhas = []
    with open(os.path.join(caminho_script, nome_arquivo), mode='r', encoding='utf-8') as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines()]
    return linhas

def escrever_texto(arquivo: list[str]) -> None:
    caminho_arquivo = os.path.join(caminho_script, "saida.txt")
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_saida:
        for linha in limpar_linhas_em_branco(arquivo):
            arquivo_saida.write(f'{linha}\n')

def limpar_linhas_em_branco(arquivo: list[str]) -> list[str]:
    return [linha for linha in arquivo if linha.strip()] 

def split_linha(linha: str, caracter: str) -> list[str]:
    return linha.split(caracter)

def remover_linhas_duplicadas(arquivo: list[str]) -> list[str]:
    linhas = []
    for l in arquivo:
        if l not in linhas:
            linhas.append(l)
    return linhas

def expandir_textos_separando_por_pontuacao(arquivo: list[str]) -> list[str]:
    separadores = [';', '.', ':']
    linhas = arquivo
    for caracter in separadores:
        linhas = expandir_texto(arquivo = linhas, caracter = caracter)
    return linhas

def expandir_texto(arquivo: list[str], caracter: str) -> list[str]:
    linhas_expandidas = []
    linhas_expandidas.extend(arquivo[0:3])
    for i, linha in enumerate(arquivo):
        if i > 1:
            if caracter in linha:
                linhas_expandidas.extend(split_linha(linha, caracter))
            else:
                linhas_expandidas.append(linha)
    return linhas_expandidas

def separar_palavras_cases_diferentes(arquivo: list[str]) -> list[str]:
    cont = 1
    tamanho_list = len(arquivo)
    linhas = arquivo[:1]
    while cont < tamanho_list:
        if contem_camel_case(arquivo[cont]):
            linhas.extend(separar_camel_case(arquivo[cont]))
        else:
            linhas.append(arquivo[cont])
        cont += 1
    return linhas

def contem_camel_case(texto) -> bool:
    # Verifica se existe padrão camelCase na string
    return bool(re.search(r'[a-z][A-Z]', texto))

def separar_camel_case(texto):
    # Expressão regular que captura a transição de camelCase
    partes = re.split(r'(?<=[a-z])(?=[A-Z])', texto)
    return partes


def print_l(arquivo: list[str]) -> None:
    for l in arquivo:
        print(l)

if __name__ == "__main__":
    linhas = buscar_arquivo(nome_arquivo="exemplo_entrada.txt")
    sem_linhas_vazias = limpar_linhas_em_branco(linhas)
    linhas_expandidas = expandir_textos_separando_por_pontuacao(sem_linhas_vazias)
    sem_linhas_duplicadas = remover_linhas_duplicadas(linhas_expandidas)
    separar_palavras_case_dif = separar_palavras_cases_diferentes(sem_linhas_duplicadas)
    escrever_texto(separar_palavras_case_dif)