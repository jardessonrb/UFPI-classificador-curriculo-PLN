import re
import emoji

def limpar_linhas_em_branco(arquivo: list[str]) -> list[str]:
    return [linha.strip() for linha in arquivo if linha.strip() != "" and len(linha) > 1] 

def split_linha(linha: str, caracter: str) -> list[str]:
    return [linha for linha in linha.split(caracter)]

def remover_linhas_duplicadas(arquivo: list[str]) -> list[str]:
    linhas = []
    for l in arquivo:
        if l not in linhas:
            linhas.append(l)
    return linhas

def expandir_textos_separando_por_pontuacao(arquivo: list[str]) -> list[str]:
    separadores = [';', '.', ':', '!', '/']
    linhas = arquivo
    for caracter in separadores:
        linhas = expandir_texto(arquivo = linhas, caracter = caracter)
    return [linha for linha in linhas]

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

def remover_links(arquivo: list[str]) -> list[str]:
    link = "https://"
    linhas = []
    for linha in arquivo:
        if link in linha:
            partes = linha.split()
            linhas.append(" ".join([palavra for palavra in partes if link not in palavra]))
        else:
            linhas.append(linha)
    return linhas

def remover_palavras_com_hashtag(frase: str) -> str:
    palavras = [palavra for palavra in frase.split() if not palavra.startswith('#')]

    return ' '.join(palavras)

def contem_palavras_com_hashtag(frase: str) -> bool:
    # Verifica se existe alguma palavra que começa com '#'
    return bool(re.search(r'\B#\w+', frase))

def contem_camel_case(texto: str) -> bool:
    # Verifica se existe padrão camelCase na string, considerando caracteres Unicode
    return bool(re.search(r'[a-zá-úà-ùâ-ûã-õä-üç][A-ZÁ-ÚÀ-ÙÂ-ÛÃ-ÕÄ-ÜÇ]', texto, re.UNICODE))

def separar_camel_case(texto: str):
    # Expressão regular que captura a transição de camelCase, incluindo caracteres Unicode
    partes = re.split(r'(?<=[a-zá-úà-ùâ-ûã-õä-üç])(?=[A-ZÁ-ÚÀ-ÙÂ-ÛÃ-ÕÄ-ÜÇ])', texto)
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

def eliminar_palavras_com_hashtag(arquivo: list[str]) -> list[str] :
    linhas = []
    for linha in arquivo:
        if contem_palavras_com_hashtag(linha):
            linhas.append(remover_palavras_com_hashtag(linha))
        else:
            linhas.append(linha)
    return linhas

def capturar_link(texto: str) -> str:
    # Expressão regular para capturar o link que começa com 'https://'
    match = re.search(r'https://\S+', texto)
    return match.group(0) if match else None


def identificar_linha_substring(anterior: str, atual: str, index_anterior: int, index_atual: int):
    menor = (anterior, index_anterior) if len(anterior) < len(atual) else (atual, index_atual)
    maior = (anterior, index_anterior) if len(anterior) > len(atual) else (atual, index_atual)

    if menor[0] in maior[0]:
        if menor[1] > maior[1]: 
            return -1
        if menor[1] < maior[1]:
            return -2
    
    return index_atual

def eliminar_linhas_semelhantes(arquivo: list[str]) -> list[str]:
    linhas = []
    tamanho = len(arquivo)
    index = 1
    linhas.append(arquivo[0])
    while index < tamanho:
        index_add = identificar_linha_substring(arquivo[index - 1], arquivo[index], index - 1, index)

        if index_add >= 0:
            linhas.append(arquivo[index_add])
        if index_add == -1:
            linhas.pop()
            linhas.append(arquivo[index])
        index += 1
        
    return linhas

if __name__ == "__main__":
    linhas = [
        "Etapa 5:",
        "Etapa 5",
        "Análise do Processo5Análise do Processo:",
        "Análise do Processo:",
        "Análise do Processo"
    ]

    print(eliminar_linhas_semelhantes(linhas))
   

