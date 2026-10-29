"""Análise de lacunas e geração de roadmap para as trilhas de carreira.

A autoavaliação usa níveis de 0 a 3:
0 = ainda não conheço; 1 = básico; 2 = intermediário; 3 = avançado.
O nível-alvo representa uma referência de preparação inicial para uma vaga júnior,
não uma garantia de contratação.
"""
from __future__ import annotations

import json
from pathlib import Path

from .conhecimento import TRILHAS

NIVEIS = {
    0: "Ainda não conheço",
    1: "Básico",
    2: "Intermediário",
    3: "Avançado",
}

# O catálogo de competências e os recursos ficam fora do código para facilitar
# manutenção da base de conhecimento sem alterar o motor.
_ARQUIVO_DADOS = Path(__file__).resolve().parent / "dados" / "roadmaps.json"
with _ARQUIVO_DADOS.open("r", encoding="utf-8") as _arquivo:
    _DADOS_ROADMAP = json.load(_arquivo)

CATALOGO_COMPETENCIAS = _DADOS_ROADMAP["competencias"]
RECURSOS_POR_TRILHA = _DADOS_ROADMAP["recursos"]

def competencias_da_trilha(trilha: str) -> list[dict]:
    """Retorna uma cópia do catálogo de competências da trilha."""
    if trilha not in CATALOGO_COMPETENCIAS:
        raise ValueError(f"Trilha desconhecida: {trilha}")
    return [item.copy() for item in CATALOGO_COMPETENCIAS[trilha]]


def gerar_roadmap(trilha: str, conhecimentos: dict[str, int]) -> dict:
    """Compara a autoavaliação com o alvo júnior e gera um plano de ação.

    Competências omitidas são consideradas nível 0 para não ocultar lacunas.
    Chaves desconhecidas e níveis fora de 0..3 são rejeitados para detectar erros.
    """
    if trilha not in CATALOGO_COMPETENCIAS or trilha not in TRILHAS:
        raise ValueError(f"Trilha desconhecida: {trilha}")
    if not isinstance(conhecimentos, dict):
        raise TypeError("Conhecimentos deve ser um dicionário de competência para nível.")

    catalogo = CATALOGO_COMPETENCIAS[trilha]
    ids_validos = {item["id"] for item in catalogo}
    desconhecidos = set(conhecimentos) - ids_validos
    if desconhecidos:
        raise ValueError(f"Competências desconhecidas para {trilha}: {', '.join(sorted(desconhecidos))}")

    avaliacao = []
    for ordem, item in enumerate(catalogo, start=1):
        nivel = conhecimentos.get(item["id"], 0)
        if isinstance(nivel, bool) or not isinstance(nivel, int) or nivel not in NIVEIS:
            raise ValueError(f"Nível inválido para '{item['id']}': use um inteiro de 0 a 3.")
        registro = {
            **item,
            "nivel_atual": nivel,
            "nivel_atual_rotulo": NIVEIS[nivel],
            "nivel_alvo_rotulo": NIVEIS[item["nivel_alvo"]],
            "ordem": ordem,
            "status": "Atendido" if nivel >= item["nivel_alvo"] else "Lacuna",
        }
        avaliacao.append(registro)

    gaps = [item.copy() for item in avaliacao if item["status"] == "Lacuna"]
    recursos = RECURSOS_POR_TRILHA[trilha]
    tecnologias = []
    for item in gaps:
        if item["tecnologia"] not in tecnologias:
            tecnologias.append(item["tecnologia"])

    etapas = []
    if gaps:
        etapas.append({
            "titulo": "1. Construir a base",
            "descricao": "Comece pelas competências fundamentais ainda abaixo do nível-alvo: " +
                         ", ".join(item["nome"] for item in gaps if item["nivel_alvo"] == 1) +
                         ("." if any(item["nivel_alvo"] == 1 for item in gaps) else "Nenhuma lacuna básica identificada."),
        })
        intermediarias = [item["nome"] for item in gaps if item["nivel_alvo"] >= 2]
        if intermediarias:
            etapas.append({
                "titulo": "2. Praticar competências centrais",
                "descricao": "Faça exercícios e pequenas entregas nas competências: " + ", ".join(intermediarias) + ".",
            })
    else:
        etapas.append({
            "titulo": "1. Consolidar e demonstrar",
            "descricao": "As competências avaliadas atingiram o nível-alvo. Pratique-as em conjunto no projeto de portfólio.",
        })
    etapas.append({
        "titulo": f"{len(etapas) + 1}. Publicar o projeto de portfólio",
        "descricao": "Implemente o projeto proposto, documente decisões e resultados e publique o repositório no GitHub.",
    })

    return {
        "trilha": trilha,
        "nome_trilha": TRILHAS[trilha]["nome"],
        "nivel_alvo": "Júnior",
        "competencias": avaliacao,
        "gaps": gaps,
        "tecnologias_prioritarias": tecnologias,
        "etapas": etapas,
        "certificacoes": list(recursos["certificacoes"]),
        "projeto_portfolio": {
            "titulo": recursos["projeto"][0],
            "descricao": recursos["projeto"][1],
            "entregaveis": list(recursos["projeto"][2]),
        },
        "observacao": (
            "O resultado é uma orientação baseada em autoavaliação, não uma certificação "
            "formal de competência. Confirme os pré-requisitos, custos e disponibilidade "
            "das certificações antes de se inscrever."
        ),
    }
