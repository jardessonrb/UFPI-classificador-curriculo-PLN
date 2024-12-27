import fitz  # PyMuPDF
import os
import sys
from collections import defaultdict
import re
from esteira_pre_processamento import EsteiraPreProcessamento
from filtros_processamento import limpar_linhas_em_branco
from classificador import ClassificadorTopico
import json

def salvar_texto_curriculo_em_txt(caminho: str, conteudo: list[str]) -> None:
    with open(caminho, 'w', encoding='utf-8') as arquivo:  
        for linha in conteudo: 
            arquivo.write(linha+'\n')

def limpar_texto(texto):
    # Remover caracteres indesejados
    caracteres_indesejados = ['❖', '●', '', '•']  # Adicione outros se necessário
    for char in caracteres_indesejados:
        texto = texto.replace(char, '')

    # Remover padrões que parecem hexadecimais (como 0x...)
    texto = re.sub(r'\b0x[0-9a-fA-F]+\b', '', texto)

    # Certificar-se de que o texto está em UTF-8
    texto = texto.encode('utf-8', errors='ignore').decode('utf-8')

    # Remover espaços extras
    return texto.strip()

def extrair_texto_por_formato(caminho_pdf: str):
    """
    Extrai texto do PDF organizado por formatação (tamanho da fonte, estilo, etc.).
    
    :param caminho_pdf: Caminho do arquivo PDF.
    :return: Dicionário onde as chaves são o estilo (fonte, tamanho) e os valores são listas de textos.
    """
    texto_por_formato = defaultdict(list)
    conteudo = []
    with fitz.open(caminho_pdf) as pdf:
        for pagina in pdf:
            for i_bloco, bloco in enumerate(pagina.get_text("dict")["blocks"]):
                if 'lines' in bloco:
                    for i_linha, linha in enumerate(bloco["lines"]):
                        for i_span, span in enumerate(linha["spans"]):
                            print(f'[{i_bloco}] - {span}')
                            conteudo.append(limpar_texto(span["text"].strip()))
                            texto_por_formato[i_bloco].append(limpar_texto(span["text"].strip()))
                            estilo = (span["font"], span["size"], span["color"])  # Identificador único de estilo
                            texto = span["text"].strip()
                            
                            if texto:  # Ignorar linhas vazias
                                if estilo not in texto_por_formato:
                                    texto_por_formato[estilo] = []
                                texto_por_formato[estilo].append(texto)
    # conteudo = []
    # for chave, valor in texto_por_formato.items():
        # print(f'[{chave}] - {valor}')
        # conteudo = conteudo + valor
    return conteudo

def organizar_topicos_por_formato(texto_por_formato):
    """
    Organiza o texto extraído em tópicos, assumindo que os títulos têm formatação distinta.

    :param texto_por_formato: Dicionário com textos organizados por formatação.
    :return: Dicionário de tópicos e seus conteúdos.
    """
    # Assumimos que fontes maiores e diferentes indicam tópicos
    estilos_ordenados = sorted(texto_por_formato.keys(), key=lambda x: -x[1])  # Ordena por tamanho de fonte (desc)
    topicos = {}
    topico_atual = None

    for estilo in estilos_ordenados:
        for linha in texto_por_formato[estilo]:
            if topico_atual is None or estilo != topico_atual:
                topico_atual = estilo
                topicos[linha] = []
            else:
                topicos[list(topicos.keys())[-1]].append(linha)
    
    return topicos

def preprocessar(conteudo: list[str]) -> list[str]:
    esteira = EsteiraPreProcessamento()
    esteira.add_filtro(limpar_linhas_em_branco)

    return esteira.run(conteudo)

def criar_topicos(conteudo: list[str]) -> None:
    classificador = ClassificadorTopico()
    for index, linha in enumerate(conteudo):
        classificador.classificar_linha(linha, index)

    topicos: dict = dict(sorted(classificador.get_dict_topicos().items(), key=lambda item: item[1]["n_linha"]))
    # print(topicos)
    return topicos

def ler_conteudo(caminho) -> list[str]:
    linhas = []
    with open(caminho, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
    return linhas

def salvar_dicionario_como_json(caminho, dicionario):
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        json.dump(dicionario, arquivo, ensure_ascii=False, indent=4)

def extruturar_json(arquivo: list[str] = None, topicos: dict = None) -> dict:
    vaga_json: dict = defaultdict(list[str])
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

if __name__  == '__main__':
    # nome_arquivo = "curriculo_docs"
    # nome_arquivo = "curriculo_linkedin"
    # nome_arquivo = "curriculo_jp"
    nome_arquivo = "curriculo_marcos"
    # nome_arquivo = "curriculo_kipper"
    caminho_arquivo_pdf = f"exemplos/{nome_arquivo}.pdf"
    caminho_arquivo_txt = f'saidas/teste_span_{nome_arquivo}.txt'
    caminho_arquivo_json = f'jsons/teste_span_{nome_arquivo}.json'

    caminho_arquivo_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho_arquivo_pdf)
    caminho_arquivo_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho_arquivo_txt)
    caminho_arquivo_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho_arquivo_json)

    # conteudo = extrair_texto_por_formato(caminho_arquivo_pdf)
    # salvar_texto_curriculo_em_txt(caminho_arquivo_txt, conteudo)

    conteudo = ler_conteudo(caminho_arquivo_txt)
    conteudo = preprocessar(conteudo)
    topicos  = criar_topicos(conteudo)
    json_curriculo = extruturar_json(conteudo, topicos)
    salvar_dicionario_como_json(caminho_arquivo_json, json_curriculo)

    
