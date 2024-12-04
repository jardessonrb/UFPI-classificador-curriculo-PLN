import os
from classificador import ClassificadorTopico
from esteira_pre_processamento import EsteiraPreProcessamento
import json
from collections import defaultdict
from filtros_processamento import *

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

def extruturar_json(arquivo: list[str], topicos: dict) -> dict:
    vaga_json: dict = defaultdict(list[str])
    vaga_json['link']  = capturar_link(arquivo[0])
    vaga_json['cargo'] = arquivo[1]
    linha_topico = [int(valor['n_linha']) for chave, valor in topicos.items()]
    for index, (chave, valor) in enumerate(topicos.items()):
        grupo_topico: int = int(valor["topico_similar"]["grupo"])
        if index + 1 >= len(linha_topico):

            if ClassificadorTopico.GRUPO_TOPICOS[grupo_topico] in vaga_json:
                vaga_json[ClassificadorTopico.GRUPO_TOPICOS[grupo_topico]].extend(arquivo[linha_topico[index] + 1:])
            else:
                vaga_json[ClassificadorTopico.GRUPO_TOPICOS[grupo_topico]] = arquivo[linha_topico[index] + 1:]
            break
        
        proximo_topico = linha_topico[index + 1]
        sub_list = arquivo[linha_topico[index] + 1: proximo_topico]
        if ClassificadorTopico.GRUPO_TOPICOS[grupo_topico] in vaga_json:
            vaga_json[ClassificadorTopico.GRUPO_TOPICOS[grupo_topico]].extend(sub_list)
        else:
            vaga_json[ClassificadorTopico.GRUPO_TOPICOS[grupo_topico]] = sub_list

    return vaga_json

def salvar_dicionario_como_json(pasta, origem, dicionario):
    caminho_arquivo = os.path.join(f'{caminho_script}/{pasta}', f"saida_{origem}.json")
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dicionario, arquivo, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    pasta = "teste"
    linhas = buscar_arquivo(pasta, nome_arquivo="exemplo_entrada.txt")

    esteira = EsteiraPreProcessamento()
    esteira.add_filtro(expandir_textos_separando_por_pontuacao)
    esteira.add_filtro(separar_palavras_cases_diferentes)
    esteira.add_filtro(remover_emojis)
    esteira.add_filtro(limpar_linhas_em_branco)
    esteira.add_filtro(eliminar_linhas_sem_palavras)
    esteira.add_filtro(eliminar_palavras_com_hashtag)
    esteira.add_filtro(remover_linhas_duplicadas)
    esteira.add_filtro(eliminar_linhas_semelhantes)

    linhas = esteira.run(linhas)
    escrever_texto(pasta, linhas)

    classificador = ClassificadorTopico()
    for index, linha in enumerate(linhas):
        classificador.classificar_linha(linha, index)

    topicos: dict = dict(sorted(classificador.get_dict_topicos().items(), key=lambda item: item[1]["n_linha"]))
    # print(topicos)
    vaga_json = extruturar_json(linhas, topicos)
    salvar_dicionario_como_json("vaga_json", "vaga_ux_ui_39_gupy_rm_semelhantes", vaga_json)