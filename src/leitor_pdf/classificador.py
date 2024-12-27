from sentence_transformers import SentenceTransformer, util
from typing import List, Dict

class ClassificadorTopico:
    GRUPO_TOPICOS: dict[int, str] = {
        1: "RESUMO_DESCRICAO",
        2: "COMPETENCIAS_HABILIDADES",
        3: "EXPERIENCIAS",
        4: "FORMACOES",
        5: "EXTRACURRICULARES",
        6: "CONQUISTAS_CERTIFICACOES",
        7: "CONTATO",
        8: "IDIOMAS",
    }

    def __init__(self) -> None:
        self.similaridade_minima = 0.8
        self.modelo_escolhido = SentenceTransformer('all-mpnet-base-v2')
        self.topicos_encontrados: dict = {}
        self.topicos_buscados: List[Dict[str, str | int]] = [
            {"topico": "Resumo", "grupo": 1},
            {"topico": "Resumo sobre mim", "grupo": 1},
            {"topico": "Sobre mim", "grupo": 1},
            {"topico": "Objetivo", "grupo": 1},
            {"topico": "Competências", "grupo": 2},
            {"topico": "Principais competências", "grupo": 2},
            {"topico": "Habilidades Técnicas", "grupo": 2},
            {"topico": "Habilidades", "grupo": 2},
            {"topico": "Experiências", "grupo": 3},
            {"topico": "Experiência", "grupo": 3},
            {"topico": "Experiências profissionais", "grupo": 3},
            {"topico": "Experiências de trabalho", "grupo": 3},
            {"topico": "Formações", "grupo": 4},
            {"topico": "Formações acadêmicas", "grupo": 4},
            {"topico": "Formação acadêmica", "grupo": 4},
            {"topico": "Escolaridade", "grupo": 4},
            {"topico": "Extracurricular", "grupo": 5},
            {"topico": "Extracurriculares", "grupo": 5},
            {"topico": "Conquistas", "grupo": 6},
            {"topico": "Conquistas e certificações", "grupo": 6},
            {"topico": "Conquistas e certificações", "grupo": 6},
            {"topico": "Cursos", "grupo": 6},
            {"topico": "Cursos e certificados", "grupo": 6},
            {"topico": "Certifications", "grupo": 6},
            {"topico": "Contato", "grupo": 7},
            {"topico": "Contatos", "grupo": 7},
            {"topico": "Idiomas", "grupo": 8},
            {"topico": "Languages", "grupo": 8}
        ]
        self.embeddings_topicos = self.modelo_escolhido.encode([item["topico"] for item in self.topicos_buscados], convert_to_tensor=True)

    def classificar_linha(self, linha: str, numero_linha: int) -> None:
        embedding_linha = self.modelo_escolhido.encode(linha.lower(), convert_to_tensor=True)
        similaridades = util.cos_sim(embedding_linha, self.embeddings_topicos)
        
        # Identificar o tópico mais semelhante
        indice_topico = similaridades.argmax().item()
        topico_mais_proximo = self.topicos_buscados[indice_topico]
        similaridade = similaridades[0][indice_topico].item()

        if similaridade > self.similaridade_minima:  # Limite ajustável
            self.topicos_encontrados[linha] = {'n_linha': numero_linha, 'topico_similar':  topico_mais_proximo}
            # print(topico_mais_proximo, linha, similaridade)

    def get_dict_topicos(self) -> dict:
        return dict(sorted(self.topicos_encontrados.items(), key=lambda item: item[1]["n_linha"]))
        
    
    def limpar_topicos_encontrados(self) -> None:
        self.topicos_encontrados.clear()
