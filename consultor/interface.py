"""Configuração e validação das etapas do wizard Streamlit."""
from .conhecimento import PERGUNTAS

ETAPAS_WIZARD = [
    {"titulo": "Etapa 1 de 3 — Perfil profissional",
     "descricao": "Informe seu nível atual de experiência em tecnologia.",
     "chaves": ["experiencia"]},
    {"titulo": "Etapa 2 de 3 — Afinidades técnicas",
     "descricao": "Conte quais atividades, ferramentas e ambientes combinam com você.",
     "chaves": ["matematica", "atuacao", "ferramenta", "entrega", "dados_pref",
                "ambiente", "criatividade_visual", "comunicacao", "detalhismo"]},
    {"titulo": "Etapa 3 de 3 — Objetivos de carreira",
     "descricao": "Defina seu objetivo profissional para concluir a entrevista.",
     "chaves": ["objetivo"]},
]

def perguntas_da_etapa(indice: int) -> list[dict]:
    if isinstance(indice, bool) or not isinstance(indice, int):
        raise ValueError("O índice da etapa deve ser um inteiro.")
    if indice < 0 or indice >= len(ETAPAS_WIZARD):
        raise ValueError(f"Etapa inexistente: {indice}")
    chaves = set(ETAPAS_WIZARD[indice]["chaves"])
    return [p for p in PERGUNTAS if p["chave"] in chaves]

def validar_cobertura_etapas() -> bool:
    chaves = [chave for etapa in ETAPAS_WIZARD for chave in etapa["chaves"]]
    esperadas = [p["chave"] for p in PERGUNTAS]
    return len(chaves) == len(set(chaves)) and set(chaves) == set(esperadas)
