"""Testes do módulo de análise de lacunas e roadmap."""
import pytest

from consultor.conhecimento import TRILHAS
from consultor.roadmap import (
    CATALOGO_COMPETENCIAS,
    NIVEIS,
    competencias_da_trilha,
    gerar_roadmap,
)


def test_catalogo_cobre_as_dez_trilhas():
    assert set(CATALOGO_COMPETENCIAS) == set(TRILHAS)
    assert all(len(competencias_da_trilha(trilha)) >= 4 for trilha in TRILHAS)


@pytest.mark.parametrize("trilha", list(TRILHAS))
def test_roadmap_tem_campos_essenciais_para_todas_as_trilhas(trilha):
    resultado = gerar_roadmap(trilha, {})
    assert resultado["trilha"] == trilha
    assert resultado["nivel_alvo"] == "Júnior"
    assert resultado["competencias"]
    assert resultado["gaps"]
    assert resultado["tecnologias_prioritarias"]
    assert resultado["etapas"]
    assert resultado["certificacoes"]
    assert resultado["projeto_portfolio"]["titulo"]
    assert resultado["projeto_portfolio"]["entregaveis"]


def test_identifica_lacuna_quando_nivel_atual_esta_abaixo_do_alvo():
    primeira = CATALOGO_COMPETENCIAS["backend"][0]
    resultado = gerar_roadmap("backend", {primeira["id"]: 0})
    gap = next(item for item in resultado["gaps"] if item["id"] == primeira["id"])
    assert gap["nivel_atual"] == 0
    assert gap["nivel_alvo"] == primeira["nivel_alvo"]
    assert gap["status"] == "Lacuna"


def test_nao_retorna_lacunas_quando_todas_as_competencias_atingem_o_alvo():
    conhecimentos = {
        item["id"]: item["nivel_alvo"]
        for item in CATALOGO_COMPETENCIAS["backend"]
    }
    resultado = gerar_roadmap("backend", conhecimentos)
    assert resultado["gaps"] == []
    assert resultado["tecnologias_prioritarias"] == []


def test_competencia_omitida_e_tratada_como_nivel_zero():
    resultado = gerar_roadmap("qa", {})
    assert all(item["nivel_atual"] == 0 for item in resultado["competencias"])


def test_nivel_invalido_e_rejeitado():
    with pytest.raises(ValueError, match="Nível inválido"):
        gerar_roadmap("backend", {"linguagem": 4})


def test_nivel_booleano_e_rejeitado():
    with pytest.raises(ValueError, match="Nível inválido"):
        gerar_roadmap("backend", {"linguagem": True})


def test_competencia_desconhecida_e_rejeitada():
    with pytest.raises(ValueError, match="Competências desconhecidas"):
        gerar_roadmap("backend", {"magica": 2})


def test_trilha_desconhecida_e_rejeitada():
    with pytest.raises(ValueError, match="Trilha desconhecida"):
        gerar_roadmap("trilha_inexistente", {})


def test_niveis_de_autoavaliacao_sao_definidos_de_zero_a_tres():
    assert set(NIVEIS) == {0, 1, 2, 3}
