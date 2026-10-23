"""Interface web (Streamlit) do Consultor Inteligente de Carreiras em TI.

Execute com:  streamlit run app.py
"""
import pandas as pd
import streamlit as st

from consultor.conhecimento import CHAVES, PERGUNTAS, TRILHAS, rotulo
from consultor.motor import consultar
from consultor.personas import PERSONAS

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")

# Estado inicial dos widgets (valores padrão de cada pergunta)
for p in PERGUNTAS:
    st.session_state.setdefault(p["chave"], p["padrao"])
st.session_state.setdefault("persona_sel", "—")


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
if enviado:
    respostas = {c: st.session_state[c] for c in CHAVES}
    resultado = consultar(respostas)

    st.divider()
    if resultado["inconclusivo"]:
        st.warning(
            "Suas respostas não ativaram regras suficientes para uma recomendação clara. "
            "Tente detalhar mais o seu perfil."
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
            st.markdown(f"- **{d['id']}** → {TRILHAS[d['trilha']]['nome']} ({sinal}{d['pontos']}): {d['motivo']}")

    with st.expander("Ver as respostas informadas"):
        for p in PERGUNTAS:
            st.markdown(f"- {p['titulo']} **{rotulo(p['chave'], respostas[p['chave']])}**")
