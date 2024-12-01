from typing import Callable, List

class EsteiraPreProcessamento:
    def __init__(self):
        self._filtros: List[Callable[[List[str]], List[str]]] = []

    def add_filtro(self, filtro: Callable[[List[str]], List[str]]) -> None:
        self._filtros.append(filtro)

    def run(self, arquivo: list[str]) -> list[str]:
        for filtro in self._filtros:
            arquivo = filtro(arquivo)
        return arquivo