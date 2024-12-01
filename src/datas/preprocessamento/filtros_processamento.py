import re
import emoji

def limpar_linhas_em_branco(arquivo: list[str]) -> list[str]:
    return [linha.strip() for linha in arquivo if linha.strip() != ""] 

def split_linha(linha: str, caracter: str) -> list[str]:
    return [f'{linha}{caracter}' for linha in linha.split(caracter)]

def remover_linhas_duplicadas(arquivo: list[str]) -> list[str]:
    linhas = []
    for l in arquivo:
        if l not in linhas:
            linhas.append(l)
    return linhas

def expandir_textos_separando_por_pontuacao(arquivo: list[str]) -> list[str]:
    separadores = [';', '.', ':', '!']
    linhas = arquivo
    for caracter in separadores:
        linhas = expandir_texto(arquivo = linhas, caracter = caracter)
    return linhas

def expandir_texto(arquivo: list[str], caracter: str) -> list[str]:
    linhas_expandidas = []
    linhas_expandidas.extend(arquivo[0:3]) #Pega as 3 primeiras linhas do arquivo com link, nome, linha em branco
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

def remover_emojis(arquivo: list[str]):
   linhas = []
   for linha in arquivo:
       linhas.append(emoji.replace_emoji(linha, replace=''))
   return linhas

def eliminar_linhas_sem_palavras(arquivo: list[str]) -> list[str] :
    return [linha for linha in arquivo if re.search(r'[a-zA-Z]', linha)]

def capturar_link(texto: str) -> str:
    # Expressão regular para capturar o link que começa com 'https://'
    match = re.search(r'https://\S+', texto)
    return match.group(0) if match else None