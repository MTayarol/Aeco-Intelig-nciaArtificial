"""Testes da configuração do wizard Streamlit."""
import pytest
from consultor.conhecimento import CHAVES
from consultor.interface import ETAPAS_WIZARD, perguntas_da_etapa, validar_cobertura_etapas

def test_wizard_tem_tres_etapas():
    assert len(ETAPAS_WIZARD) == 3

def test_todas_as_perguntas_aparecem_exatamente_uma_vez():
    assert validar_cobertura_etapas()

@pytest.mark.parametrize("indice", range(3))
def test_cada_etapa_tem_perguntas(indice):
    assert perguntas_da_etapa(indice)

def test_primeira_etapa_coleta_experiencia():
    assert [p["chave"] for p in perguntas_da_etapa(0)] == ["experiencia"]

def test_ultima_etapa_coleta_objetivo():
    assert [p["chave"] for p in perguntas_da_etapa(2)] == ["objetivo"]

def test_cobertura_corresponde_as_chaves_da_entrevista():
    chaves = [c for etapa in ETAPAS_WIZARD for c in etapa["chaves"]]
    assert set(chaves) == set(CHAVES)
    assert len(chaves) == len(CHAVES)

@pytest.mark.parametrize("indice", [-1, 3, 100])
def test_indice_inexistente_gera_erro(indice):
    with pytest.raises(ValueError, match="Etapa inexistente"):
        perguntas_da_etapa(indice)

def test_indice_booleano_e_rejeitado():
    with pytest.raises(ValueError, match="inteiro"):
        perguntas_da_etapa(True)
