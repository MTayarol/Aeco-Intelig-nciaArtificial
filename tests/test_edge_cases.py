"""Fase 5 — testes de robustez e casos limite (edge cases)."""
import pytest

from consultor.conhecimento import CHAVES, TRILHAS
from consultor.motor import consultar
from consultor.personas import PERSONAS


def perfil_base(**alteracoes):
    respostas = dict(PERSONAS["ana_analitica"]["respostas"])
    respostas.update(alteracoes)
    return respostas


def test_perfil_hibrido_dados_e_web_preserva_as_duas_trilhas_no_top_3():
    resultado = consultar(perfil_base(
        matematica="alta", atuacao="dados_brutos", ferramenta="python",
        entrega="produto_usuario", dados_pref="modelar", ambiente="navegador",
        criatividade_visual="alta", objetivo="pesquisa_inovacao",
    ))
    top_3 = {trilha for trilha, _ in resultado["ranking"][:3]}
    assert "dados_ml" in top_3
    assert "frontend" in top_3


def test_conflito_de_preferencia_visual_dispara_regra_de_ressalva():
    resultado = consultar(perfil_base(
        atuacao="layouts_visuais", criatividade_visual="baixa",
        ferramenta="nenhuma", entrega="produto_usuario", ambiente="navegador",
    ))
    assert any(d["id"] == "R08" and d["pontos"] == -2 for d in resultado["disparos"])


def test_empate_ou_margem_zero_tem_confianca_baixa_e_alternativa_distinta():
    resultado = consultar(perfil_base(
        matematica="media", atuacao="algoritmos_logicos", ferramenta="nenhuma",
        entrega="produto_usuario", dados_pref="nenhum", ambiente="nao_importa",
        criatividade_visual="media", comunicacao="media", detalhismo="media",
        objetivo="especialista", experiencia="intermediario",
    ))
    assert resultado["margem"] >= 0
    if resultado["margem"] < 2:
        assert resultado["confianca"] == "Baixa"
    assert resultado["trilha"] != resultado["alternativa"]


def test_margem_e_confianca_sao_consistentes_com_o_ranking():
    resultado = consultar(PERSONAS["ana_analitica"]["respostas"])
    pontos_primeira = resultado["ranking"][0][1]
    pontos_segunda = resultado["ranking"][1][1]
    assert resultado["margem"] == pontos_primeira - pontos_segunda
    esperada = "Alta" if resultado["margem"] >= 5 else "Média" if resultado["margem"] >= 2 else "Baixa"
    assert resultado["confianca"] == esperada


def test_justificativas_sao_regras_positivas_da_trilha_vencedora():
    resultado = consultar(PERSONAS["ana_analitica"]["respostas"])
    ids_disparados = {d["id"] for d in resultado["disparos"]
                      if d["trilha"] == resultado["trilha"] and d["pontos"] > 0}
    assert resultado["motivos"]
    assert {m["id"] for m in resultado["motivos"]} <= ids_disparados
    assert all(m["trilha"] == resultado["trilha"] and m["pontos"] > 0 for m in resultado["motivos"])


def test_ranking_tem_todas_as_trilhas_sem_duplicatas_e_em_ordem():
    resultado = consultar(PERSONAS["ana_analitica"]["respostas"])
    ids = [trilha for trilha, _ in resultado["ranking"]]
    assert len(ids) == len(TRILHAS)
    assert set(ids) == set(TRILHAS)
    assert len(ids) == len(set(ids))
    assert resultado["ranking"] == sorted(resultado["ranking"], key=lambda item: (-item[1], list(TRILHAS).index(item[0])))


@pytest.mark.parametrize("persona", list(PERSONAS))
def test_todas_as_personas_tem_recomendacao_justificada(persona):
    resultado = consultar(PERSONAS[persona]["respostas"])
    assert resultado["trilha"] == PERSONAS[persona]["esperada"]
    assert resultado["motivos"]
    assert not resultado["inconclusivo"]


def test_resposta_incompleta_e_rejeitada():
    with pytest.raises(ValueError, match="Respostas faltando"):
        consultar({"matematica": "alta"})


@pytest.mark.parametrize("chave,valor", [
    ("matematica", "extrema"),
    ("atuacao", "programar_em_telepatia"),
    ("experiencia", 99),
    ("criatividade_visual", None),
])
def test_valores_fora_das_opcoes_sao_rejeitados(chave, valor):
    respostas = perfil_base()
    respostas[chave] = valor
    with pytest.raises(ValueError, match="Respostas inválidas"):
        consultar(respostas)


def test_chave_extra_e_rejeitada():
    respostas = perfil_base()
    respostas["campo_inexistente"] = "valor"
    with pytest.raises(ValueError, match="Respostas desconhecidas"):
        consultar(respostas)


def test_entrevista_tem_exatamente_as_chaves_esperadas():
    assert set(perfil_base()) == set(CHAVES)
