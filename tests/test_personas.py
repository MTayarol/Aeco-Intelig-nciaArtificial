"""Fase 4 – Validação com personas de teste.

Execute com:  pytest -v
"""
import pytest

from consultor.conhecimento import TRILHAS
from consultor.motor import ConsultorCarreiras, consultar
from consultor.personas import PERSONAS


def test_quantidade_minima_de_regras():
    # Requisito do trabalho: pelo menos 20 a 25 regras lógicas cruzadas
    assert len(ConsultorCarreiras().get_rules()) >= 25


def test_ha_pelo_menos_4_personas():
    assert len(PERSONAS) >= 4


def test_toda_trilha_e_coberta_por_alguma_persona():
    cobertas = {p["esperada"] for p in PERSONAS.values()}
    assert cobertas == set(TRILHAS)


@pytest.mark.parametrize("chave", list(PERSONAS))
def test_persona_recebe_a_trilha_esperada(chave):
    persona = PERSONAS[chave]
    resultado = consultar(persona["respostas"])
    assert resultado["trilha"] == persona["esperada"], (
        f"{persona['nome']}: esperado {persona['esperada']}, "
        f"obtido {resultado['trilha']} | ranking: {resultado['ranking'][:3]}"
    )


@pytest.mark.parametrize("chave", list(PERSONAS))
def test_recomendacao_sempre_tem_justificativa(chave):
    resultado = consultar(PERSONAS[chave]["respostas"])
    assert resultado["motivos"], "A recomendação deve ter ao menos uma regra que a justifique"
    assert not resultado["inconclusivo"]


def test_respostas_incompletas_geram_erro():
    with pytest.raises(ValueError):
        consultar({"matematica": "alta"})
