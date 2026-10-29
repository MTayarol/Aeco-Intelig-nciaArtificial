"""Interface web (Streamlit) do Consultor Inteligente de Carreiras em TI.

Execute com:  streamlit run app.py
"""
import pandas as pd
import streamlit as st

from consultor.conhecimento import CHAVES, PERGUNTAS, TRILHAS, rotulo
from consultor.motor import consultar
from consultor.personas import PERSONAS
from consultor.roadmap import NIVEIS, competencias_da_trilha, gerar_roadmap

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")

# Estado inicial dos widgets (valores padrão de cada pergunta)
for p in PERGUNTAS:
    st.session_state.setdefault(p["chave"], p["padrao"])
st.session_state.setdefault("persona_sel", "—")
st.session_state.setdefault("resultado_consulta", None)
st.session_state.setdefault("respostas_consulta", None)
st.session_state.setdefault("roadmap_resultado", None)
st.session_state.setdefault("roadmap_trilha", None)


def carregar_persona():
    """Preenche o formulário com as respostas de uma persona de exemplo."""
    escolhida = st.session_state["persona_sel"]
    if escolhida in PERSONAS:
        for chave, valor in PERSONAS[escolhida]["respostas"].items():
            st.session_state[chave] = valor


# ------------------------------- Barra lateral -------------------------------
with st.sidebar:
    st.header("Sobre o sistema")
    st.write(
        "Sistema especialista baseado em regras (Python + **Experta**, "
        "encadeamento para frente). Suas respostas viram fatos e as regras "
        "SE-ENTÃO pontuam cada trilha de carreira."
    )
    st.divider()
    st.subheader("Testar com uma persona")
    st.selectbox(
        "Preencher o formulário com um exemplo:",
        ["—"] + list(PERSONAS),
        format_func=lambda k: "—" if k == "—" else PERSONAS[k]["nome"],
        key="persona_sel",
        on_change=carregar_persona,
    )
    st.caption("Depois é só clicar em *Descobrir minha trilha*.")

# ------------------------------- Cabeçalho -----------------------------------
st.title("Consultor Inteligente de Carreiras em TI")
st.write("Responda às perguntas abaixo e descubra qual das **10 trilhas** combina mais com o seu perfil.")

# ------------------------------- Formulário ----------------------------------
with st.form("entrevista"):
    for i, p in enumerate(PERGUNTAS, start=1):
        valores = [v for v, _ in p["opcoes"]]
        rotulos = dict(p["opcoes"])
        titulo = f"{i}. {p['titulo']}"
        if p["tipo"] in ("nivel", "nivel_exp"):
            st.radio(titulo, valores, format_func=rotulos.get, key=p["chave"], horizontal=True)
        else:
            st.selectbox(titulo, valores, format_func=rotulos.get, key=p["chave"])
    enviado = st.form_submit_button("Descobrir minha trilha", type="primary", use_container_width=True)

# ------------------------------- Resultado -----------------------------------
# Guardar o resultado permite preencher a autoavaliação sem perder a recomendação
# quando o Streamlit executar novamente o script após o segundo formulário.
if enviado:
    respostas = {c: st.session_state[c] for c in CHAVES}
    st.session_state["resultado_consulta"] = consultar(respostas)
    st.session_state["respostas_consulta"] = respostas
    st.session_state["roadmap_resultado"] = None
    st.session_state["roadmap_trilha"] = None

resultado = st.session_state["resultado_consulta"]
respostas = st.session_state["respostas_consulta"]

if resultado is not None and respostas is not None:
    st.divider()
    if resultado["inconclusivo"]:
        st.warning(
            "Suas respostas não ativaram regras suficientes para uma recomendação clara. "
            "Tente detalhar mais o seu perfil. O roadmap deve ser considerado exploratório."
        )
    else:
        st.success(f"### Trilha recomendada: {resultado['nome']}")
        st.write(resultado["descricao"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Pontuação", resultado["pontos"])
    c2.metric("Confiança", resultado["confianca"])
    pts_segunda = dict(resultado["ranking"])[resultado["alternativa"]]
    if pts_segunda > 0:
        c3.metric("Segunda opção", TRILHAS[resultado["alternativa"]]["nome"].split(" (")[0])

    if resultado["confianca"] == "Baixa" and pts_segunda > 0:
        st.info(
            "A diferença para a segunda colocada é pequena. "
            f"Vale pesquisar também **{TRILHAS[resultado['alternativa']]['nome']}**."
        )

    st.subheader("Por que essa recomendação?")
    for m in resultado["motivos"]:
        st.markdown(f"- **{m['id']}** (+{m['pontos']}): {m['motivo']}")

    if resultado["ressalvas"]:
        st.subheader("Pontos de atenção")
        for m in resultado["ressalvas"]:
            st.markdown(f"- **{m['id']}** ({m['pontos']}): {m['motivo']}")

    st.subheader("Pontuação de todas as trilhas")
    df = pd.DataFrame(
        {"Pontuação": [pts for _, pts in resultado["ranking"]]},
        index=[TRILHAS[t]["nome"] for t, _ in resultado["ranking"]],
    )
    st.bar_chart(df)

    with st.expander("Ver todas as regras disparadas (rastro de inferência)"):
        for d in resultado["disparos"]:
            sinal = "+" if d["pontos"] > 0 else ""
            st.markdown(
                f"- **{d['id']}** → {TRILHAS[d['trilha']]['nome']} "
                f"({sinal}{d['pontos']}): {d['motivo']}"
            )

    with st.expander("Ver as respostas informadas"):
        for p in PERGUNTAS:
            st.markdown(
                f"- {p['titulo']} **{rotulo(p['chave'], respostas[p['chave']])}**"
            )

    # ---------------- Fase 3: análise de lacunas e roadmap ----------------
    st.divider()
    st.header("Plano de desenvolvimento individual")
    st.write(
        "Avalie seu conhecimento atual nas competências da trilha recomendada. "
        "O sistema compara sua autoavaliação com um nível-alvo de preparação júnior."
    )
    st.caption(
        "Escala: 0 = ainda não conheço; 1 = básico; 2 = intermediário; "
        "3 = avançado. Trata-se de uma autoavaliação orientativa, não de uma prova técnica."
    )

    trilha = resultado["trilha"]
    competencias = competencias_da_trilha(trilha)
    with st.form("autoavaliacao_competencias"):
        conhecimentos = {}
        for competencia in competencias:
            chave_widget = f"roadmap_{trilha}_{competencia['id']}"
            conhecimentos[competencia["id"]] = st.select_slider(
                f"{competencia['nome']} — {competencia['descricao']}",
                options=[0, 1, 2, 3],
                value=0,
                format_func=lambda nivel: NIVEIS[nivel],
                key=chave_widget,
            )
        gerar = st.form_submit_button(
            "Analisar lacunas e gerar roadmap",
            type="primary",
            use_container_width=True,
        )

    if gerar:
        st.session_state["roadmap_resultado"] = gerar_roadmap(trilha, conhecimentos)
        st.session_state["roadmap_trilha"] = trilha

    plano = st.session_state["roadmap_resultado"]
    if plano is not None and st.session_state["roadmap_trilha"] == trilha:
        st.subheader("Lacunas de competências")
        if plano["gaps"]:
            tabela = pd.DataFrame(
                [
                    {
                        "Competência": item["nome"],
                        "Nível atual": item["nivel_atual_rotulo"],
                        "Nível-alvo": item["nivel_alvo_rotulo"],
                        "Tecnologia / prática": item["tecnologia"],
                    }
                    for item in plano["gaps"]
                ]
            )
            st.dataframe(tabela, use_container_width=True, hide_index=True)
            st.write(
                "**Prioridades de estudo:** "
                + "; ".join(plano["tecnologias_prioritarias"])
            )
        else:
            st.success(
                "Todas as competências avaliadas atingiram o nível-alvo definido "
                "para este roadmap."
            )

        st.subheader("Sequência sugerida")
        for etapa in plano["etapas"]:
            st.markdown(f"**{etapa['titulo']}**")
            st.write(etapa["descricao"])

        st.subheader("Certificações e formações para pesquisar")
        for certificacao in plano["certificacoes"]:
            st.markdown(f"- {certificacao}")

        projeto = plano["projeto_portfolio"]
        st.subheader(f"Projeto para o portfólio: {projeto['titulo']}")
        st.write(projeto["descricao"])
        st.write("**Entregáveis sugeridos:**")
        for entregavel in projeto["entregaveis"]:
            st.markdown(f"- {entregavel}")
        st.caption(plano["observacao"])
