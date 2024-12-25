import os
from classificador import ClassificadorTopico
from esteira_pre_processamento import EsteiraPreProcessamento
import json
from collections import defaultdict
from filtros_processamento import *
from typing import Dict, List

caminho_script = os.path.dirname(os.path.abspath(__file__))
descricoes_com_falha = []

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

def extruturar_json(arquivo: list[str] = None, topicos: dict = None, origem: str = "sem_origem", area: str = "sem_area") -> dict:
    vaga_json: dict = defaultdict(list[str])
    vaga_json['link']  = capturar_link(arquivo[0])
    vaga_json['cargo'] = arquivo[1]
    vaga_json['origem'] = origem
    vaga_json['area'] = area
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
    caminho_arquivo = os.path.join(caminho_script, "..", pasta, f"corpus_{origem}.json")
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dicionario, arquivo, ensure_ascii=False, indent=4)

def salvar_dicionario_como_json_teste(pasta, origem, dicionario):
    caminho_arquivo = os.path.join(caminho_script, pasta, f"{origem}.json")
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dicionario, arquivo, ensure_ascii=False, indent=4)


def agrupar_vagas_em_json() -> None:
    caminhos_descricoes_vagas = os.path.join(caminho_script, "..", "vagas")
    caminhos_arquivos: list[tuple] = []

    classificador = ClassificadorTopico()
    esteira = EsteiraPreProcessamento()

    esteira.add_filtro(expandir_textos_separando_por_pontuacao)
    esteira.add_filtro(separar_palavras_cases_diferentes)
    esteira.add_filtro(remover_emojis)
    esteira.add_filtro(limpar_linhas_em_branco)
    esteira.add_filtro(eliminar_linhas_sem_palavras)
    esteira.add_filtro(eliminar_palavras_com_hashtag)
    esteira.add_filtro(remover_linhas_duplicadas)
    esteira.add_filtro(eliminar_linhas_semelhantes)

    for pasta in os.listdir(caminhos_descricoes_vagas):
        caminho_descricoes = os.path.join(caminhos_descricoes_vagas, pasta, "descricoes_vagas")
        for area in os.listdir(caminho_descricoes):
            caminho_arquivo_descricao_vagas = os.path.join(caminho_descricoes, area)
            for nome_arquivo in os.listdir(caminho_arquivo_descricao_vagas):
                caminhos_arquivos.append((pasta, area, os.path.join(caminho_arquivo_descricao_vagas, nome_arquivo)))
    
    dicionario_vagas_json: Dict[str, List] = defaultdict(list)
    pas = ""
    ar = ""
    for pasta, area, caminho in caminhos_arquivos:
        if pas != pasta or ar != area:
            pas = pasta
            ar = area
            print(f"Iniciando {pasta} na área {ar}")
    
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                # linhas = arquivo.readlines()
                linhas = buscar_arquivo("teste", nome_arquivo="exemplo_entrada.txt")
                print("linhas - ", len(linhas))
                if len(linhas) < 3:
                    continue

                linhas = esteira.run(linhas)

                for index, linha in enumerate(linhas):
                    classificador.classificar_linha(linha, index)
                
                topicos = classificador.get_dict_topicos()
                classificador.limpar_topicos_encontrados()
                vaga_json = extruturar_json(arquivo = linhas, topicos = topicos, origem = pasta, area = area)
                dicionario_vagas_json[pasta].append(vaga_json)

        except Exception as e :
            print(pasta, area, caminho)
        
        break

    salvar_dicionario_como_json("corpus", "v3", dicionario_vagas_json)
    print("Arquivo final salvo")


if __name__ == "__main__":
    agrupar_vagas_em_json()

    # pasta = "teste"
    # linhas = buscar_arquivo(pasta, nome_arquivo="exemplo_entrada.txt")

    # esteira = EsteiraPreProcessamento()
    # esteira.add_filtro(expandir_textos_separando_por_pontuacao)
    # esteira.add_filtro(separar_palavras_cases_diferentes)
    # esteira.add_filtro(remover_emojis)
    # esteira.add_filtro(limpar_linhas_em_branco)
    # esteira.add_filtro(eliminar_linhas_sem_palavras)
    # esteira.add_filtro(eliminar_palavras_com_hashtag)
    # esteira.add_filtro(remover_linhas_duplicadas)
    # esteira.add_filtro(eliminar_linhas_semelhantes)

    # linhas = esteira.run(linhas)
    # escrever_texto(pasta, linhas)

    # classificador = ClassificadorTopico()
    # for index, linha in enumerate(linhas):
    #     classificador.classificar_linha(linha, index)

    # topicos: dict = dict(sorted(classificador.get_dict_topicos().items(), key=lambda item: item[1]["n_linha"]))
    # print(topicos)
    # vaga_json = extruturar_json(linhas, topicos)
    # salvar_dicionario_como_json_teste("vaga_json", "gupy_analista_133", vaga_json)