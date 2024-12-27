from PyPDF2 import PdfReader
import os



def extrair_texto_pdf(caminho_pdf: str) -> list[str]:
    print(caminho_pdf)
    """
    Extrai o texto de um arquivo PDF.
    
    :param caminho_pdf: Caminho do arquivo PDF.
    :return: Texto extraído do PDF como uma string única.
    """
    linhas = []
    reader = PdfReader(caminho_pdf)
    for pagina in reader.pages:
        texto = pagina.extract_text()
        if texto:
            linhas.extend(texto.splitlines())
    return [linha.strip() for linha in linhas if linha.strip()]

if __name__  == '__main__':
    nome_arquivo = "curriculo_docs"
    caminho_arquivo_pdf = f"exemplos/{nome_arquivo}.pdf"
    caminho_arquivo_txt = f'saidas/{nome_arquivo}.txt'

    caminho_arquivo_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho_arquivo_pdf)
    caminho_arquivo_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), caminho_arquivo_txt)

    conteudo: list[str] = extrair_texto_pdf(caminho_arquivo_pdf)
    salvar_texto_curriculo_em_txt(caminho_arquivo_txt, conteudo)