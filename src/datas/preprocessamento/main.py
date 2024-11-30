import os
import re
import emoji
from classificador import ClassificadorTopico
import json

caminho_script = os.path.dirname(os.path.abspath(__file__))
def buscar_arquivo(pasta: str, nome_arquivo: str) -> list[str]:
    caminho = os.path.join(caminho_script, pasta)
    linhas = []
    with open(os.path.join(caminho, nome_arquivo), mode='r', encoding='utf-8') as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines()]
    return linhas

def escrever_texto(pasta: str, arquivo: list[str]) -> None:
    caminho_arquivo = os.path.join(f'{caminho_script}/{pasta}', "saida.txt")
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_saida:
        for linha in limpar_linhas_em_branco(arquivo):
            arquivo_saida.write(f'{linha}\n')

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

def extruturar_json(arquivo: list[str], topicos: dict) -> dict:
    vaga_json: dict = {}
    vaga_json['link']  = arquivo[0][5:]
    vaga_json['cargo'] = arquivo[1]
    linha_topico = [int(valor['n_linha']) for chave, valor in topicos.items()]
    for index, (chave, valor) in enumerate(topicos.items()):
        if index + 1 >= len(linha_topico):
            vaga_json[chave] = arquivo[linha_topico[index] + 1:]
            break
        proximo_topico = linha_topico[index + 1]
        sub_list = arquivo[linha_topico[index] + 1: proximo_topico]
        vaga_json[chave] = sub_list
    return vaga_json

def salvar_dicionario_como_json(pasta, origem, dicionario):
    caminho_arquivo = os.path.join(f'{caminho_script}/{pasta}', f"saida_{origem}.json")
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dicionario, arquivo, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    pasta = "teste"
    linhas = buscar_arquivo(pasta, nome_arquivo="exemplo_entrada.txt")
    linhas = expandir_textos_separando_por_pontuacao(linhas)
    linhas = separar_palavras_cases_diferentes(linhas)
    linhas = remover_linhas_duplicadas(linhas)
    linhas = remover_emojis(linhas)
    linhas = limpar_linhas_em_branco(linhas)
    linhas = eliminar_linhas_sem_palavras(linhas)
    escrever_texto(pasta, linhas)

    classificador = ClassificadorTopico()
    for index, linha in enumerate(linhas):
        classificador.classificar_linha(linha, index)

    topicos: dict = dict(sorted(classificador.get_dict_topicos().items(), key=lambda item: item[1]["n_linha"]))
    vaga_json = extruturar_json(linhas, topicos)
    salvar_dicionario_como_json("vaga_json", pasta, vaga_json)