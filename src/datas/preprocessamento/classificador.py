from sentence_transformers import SentenceTransformer, util

class ClassificadorTopico:

    def __init__(self) -> None:
        self.modelo_escolhido = SentenceTransformer('all-mpnet-base-v2')
        self.topicos_encontrados: dict = {}
        self.topicos_buscados: list[str] = [
            "experiências profissionais", "requisitos e qualificações",
            "descrição da vaga", "sobre a vaga", "responsabilidades e atribuições",
            "diferencial", "um diferencial", "seria legal", "informações adicionais",
            "etapas do processo", "process stages",
            "professional experience", "requirements and qualifications",
            "job description", "responsibilities and assignments",
            "differential", "additional information" 
        ]
        self.embeddings_topicos = self.modelo_escolhido.encode(self.topicos_buscados, convert_to_tensor=True)

    def classificar_linha(self, linha: str, numero_linha: int) -> bool :
        embedding_linha = self.modelo_escolhido.encode(linha.lower(), convert_to_tensor=True)
        similaridades = util.cos_sim(embedding_linha, self.embeddings_topicos)
        
        # Identificar o tópico mais semelhante
        indice_topico = similaridades.argmax().item()
        topico_mais_proximo = self.topicos_buscados[indice_topico]
        similaridade = similaridades[0][indice_topico].item()
        
        # Verificar se a similaridade é alta o suficiente
        resultado = {}
        if similaridade > 0.8:  # Limite ajustável
            self.topicos_encontrados[linha] = {'n_linha': numero_linha, 'topico_prox':  topico_mais_proximo}
            print(topico_mais_proximo, linha, similaridade)

        return False
    def get_dict_topicos(self) -> dict:
        return self.topicos_encontrados
