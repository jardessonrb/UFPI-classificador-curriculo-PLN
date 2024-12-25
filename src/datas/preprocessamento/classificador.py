from sentence_transformers import SentenceTransformer, util
from typing import List, Dict

class ClassificadorTopico:
    GRUPO_TOPICOS: dict[int, str] = {
        1: "EXPERIENCIAS_PROFISSIONAIS",
        2: "REQUISITOS_QUALIFICACOES",
        3: "DESCRICAO_VAGA",
        4: "RESPONSABILIDADES_ATRIBUICOES",
        5: "DIFERENCIAIS",
        6: "INFORMACOES_ADICIONAIS",
        7: "ETAPAS_PROCESSO",
        8: "FORMACOES_DESEJADAS",
    }

    def __init__(self) -> None:
        self.similaridade_minima = 0.8
        self.modelo_escolhido = SentenceTransformer('all-mpnet-base-v2')
        self.topicos_encontrados: dict = {}
        self.topicos_buscados: List[Dict[str, str | int]] = [
            {"topico": "experiências profissionais", "grupo": 1},
            {"topico": "professional experience", "grupo": 1},
            {"topico": "requisitos e qualificações", "grupo": 2},
            {"topico": "requisitos mínimos", "grupo": 2},
            {"topico": "Requisitos", "grupo": 2},
            {"topico": "requirements and qualifications", "grupo": 2},
            {"topico": "descrição da vaga", "grupo": 3}, 
            {"topico": "job description", "grupo": 3},
            {"topico": "sobre a vaga", "grupo": 3},
            {"topico": "responsabilidades e atribuições", "grupo": 4},
            {"topico": "responsibilities and assignments", "grupo": 4},
            {"topico": "Atividades", "grupo": 4},
            {"topico": "diferencial", "grupo": 5},
            {"topico": "diferenciais", "grupo": 5},
            {"topico": "differential", "grupo": 5},
            {"topico": "differentials", "grupo": 5},
            {"topico": "um diferencial", "grupo": 5},
            {"topico": "será um diferencial", "grupo": 5},
            {"topico": "alguns diferenciais", "grupo": 5},
            {"topico": "você irá se destacar se tiver", "grupo": 5},
            {"topico": "seria legal ter", "grupo": 5},
            {"topico": "informações adicionais", "grupo": 6},
            {"topico": "additional information", "grupo": 6},
            {"topico": "etapas do processo", "grupo": 7},
            {"topico": "fases do processo", "grupo": 7},
            {"topico": "process stages", "grupo": 7},
            {"topico": "formação", "grupo": 8},
            {"topico": "formações desejadas", "grupo": 8}
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
