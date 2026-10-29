"""Testes adicionais de robustez para o motor de inferência.

Execute com: pytest -v
Complementa test_personas.py com contratos do resultado, determinismo e
comportamento diante de perfis válidos mas pouco informativos.
"""
import pytest

from consultor.conhecimento import CHAVES, TRILHAS
from consultor.motor import consultar
from consultor.personas import PERSONAS


def test_consulta_retorna_estrutura_completa():
    respostas = PERSONAS["ana_analitica"]["respostas"]
    resultado = consultar(respostas)

    campos_obrigatorios = {
        "trilha", "nome", "descricao", "pontos", "alternativa", "margem",
        "confianca", "inconclusivo", "motivos", "ressalvas", "ranking", "disparos",
    }
    assert campos_obrigatorios <= resultado.keys()
    assert resultado["trilha"] in TRILHAS
    assert resultado["confianca"] in {"Alta", "Média", "Baixa"}


def test_ranking_contem_todas_as_dez_trilhas():
    resultado = consultar(PERSONAS["ana_analitica"]["respostas"])
    trilhas_ranqueadas = [trilha for trilha, _ in resultado["ranking"]]

    assert len(trilhas_ranqueadas) == 10
    assert set(trilhas_ranqueadas) == set(TRILHAS)
    assert resultado["ranking"] == sorted(
        resultado["ranking"], key=lambda item: (-item[1], list(TRILHAS).index(item[0]))
    )


@pytest.mark.parametrize("chave", list(PERSONAS))
def test_consulta_e_deterministica(chave):
    respostas = PERSONAS[chave]["respostas"]

    primeira = consultar(respostas)
    segunda = consultar(respostas)

    assert primeira["trilha"] == segunda["trilha"]
    assert primeira["ranking"] == segunda["ranking"]
    assert primeira["disparos"] == segunda["disparos"]


def test_perfil_pouco_informativo_nao_interrompe_a_consulta():
    respostas = {
        "matematica": "media",
        "atuacao": "algoritmos_logicos",
        "ferramenta": "nenhuma",
        "entrega": "produto_usuario",
        "dados_pref": "nenhum",
        "ambiente": "nao_importa",
        "criatividade_visual": "media",
        "comunicacao": "media",
        "detalhismo": "media",
        "objetivo": "especialista",
        "experiencia": "intermediario",
    }

    resultado = consultar(respostas)

    assert resultado is not None
    assert resultado["trilha"] in TRILHAS
    assert len(resultado["ranking"]) == len(TRILHAS)
    assert isinstance(resultado["inconclusivo"], bool)


def test_chaves_da_entrevista_estao_presentes_em_todas_as_personas():
    esperadas = set(CHAVES)

    for persona in PERSONAS.values():
        assert set(persona["respostas"]) == esperadas, persona["nome"]


def test_respostas_incompletas_informam_erro():
    with pytest.raises(ValueError, match="Respostas faltando"):
        consultar({"matematica": "alta"})
