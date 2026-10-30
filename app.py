"""Interface em etapas do Consultor Inteligente de Carreiras em TI.
Execute com: streamlit run app.py
"""
import pandas as pd
import streamlit as st
from consultor.conhecimento import CHAVES, PERGUNTAS, TRILHAS, rotulo
from consultor.motor import consultar
from consultor.personas import PERSONAS
from consultor.roadmap import NIVEIS, competencias_da_trilha, gerar_roadmap

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")
for p in PERGUNTAS:
    st.session_state.setdefault(p["chave"], p["padrao"])
for k, v in {"persona_sel":"—", "etapa_wizard":1, "resultado_consulta":None,
             "respostas_consulta":None, "roadmap_resultado":None, "roadmap_trilha":None}.items():
    st.session_state.setdefault(k, v)

def limpar_resultado():
    st.session_state["resultado_consulta"] = None
    st.session_state["respostas_consulta"] = None
    st.session_state["roadmap_resultado"] = None
    st.session_state["roadmap_trilha"] = None

def carregar_persona():
    escolhida = st.session_state["persona_sel"]
    if escolhida in PERSONAS:
        for chave, valor in PERSONAS[escolhida]["respostas"].items():
            st.session_state[chave] = valor
    limpar_resultado()
    st.session_state["etapa_wizard"] = 1

def mostrar_pergunta(p):
    valores = [v for v, _ in p["opcoes"]]
    labels = dict(p["opcoes"])
    if p["tipo"] in ("nivel", "nivel_exp"):
        st.radio(p["titulo"], valores, format_func=labels.get, key=p["chave"], horizontal=True)
    else:
        st.selectbox(p["titulo"], valores, format_func=labels.get, key=p["chave"])

def executar_consulta():
    respostas = {chave: st.session_state[chave] for chave in CHAVES}
    st.session_state["resultado_consulta"] = consultar(respostas)
    st.session_state["respostas_consulta"] = respostas
    st.session_state["roadmap_resultado"] = None
    st.session_state["roadmap_trilha"] = None

with st.sidebar:
    st.header("Sobre o sistema")
    st.write("Sistema especialista baseado em regras (Python + **Experta**). As respostas ativam regras SE-ENTÃO que pontuam trilhas de carreira.")
    st.divider()
    st.subheader("Testar com uma persona")
    st.selectbox("Preencher com um perfil de exemplo:", ["—"] + list(PERSONAS),
                 format_func=lambda k: "—" if k == "—" else PERSONAS[k]["nome"],
                 key="persona_sel", on_change=carregar_persona)
    st.caption("A seleção preenche as respostas e reinicia a análise.")

st.title("Consultor Inteligente de Carreiras em TI")
st.write("Descubra sua trilha e monte um plano de desenvolvimento em três etapas.")
etapa = st.session_state["etapa_wizard"]
st.progress(etapa / 3, text=f"Etapa {etapa} de 3")

if etapa == 1:
    st.header("Passo 1 — Perfil pessoal")
    st.write("Informe seu nível atual de experiência em tecnologia.")
    with st.form("wizard_perfil"):
        for p in PERGUNTAS:
            if p["chave"] == "experiencia": mostrar_pergunta(p)
        avancar = st.form_submit_button("Continuar para afinidades técnicas →", type="primary", use_container_width=True)
    if avancar:
        st.session_state["etapa_wizard"] = 2
        st.rerun()
elif etapa == 2:
    st.header("Passo 2 — Afinidades técnicas")
    st.write("Selecione as atividades, ferramentas e ambientes com que você mais se identifica.")
    chaves = {"matematica", "atuacao", "ferramenta", "dados_pref", "ambiente", "criatividade_visual", "comunicacao", "detalhismo"}
    with st.form("wizard_afinidades"):
        for p in PERGUNTAS:
            if p["chave"] in chaves: mostrar_pergunta(p)
        a, b = st.columns(2)
        voltar = a.form_submit_button("← Voltar")
        avancar = b.form_submit_button("Continuar para objetivos →", type="primary", use_container_width=True)
    if voltar:
        st.session_state["etapa_wizard"] = 1
        st.rerun()
    if avancar:
        st.session_state["etapa_wizard"] = 3
        st.rerun()
else:
    st.header("Passo 3 — Objetivos de carreira")
    st.write("Defina a entrega de valor que prefere e seu principal objetivo profissional.")
    with st.form("wizard_objetivos"):
        for p in PERGUNTAS:
            if p["chave"] in {"entrega", "objetivo"}: mostrar_pergunta(p)
        a, b = st.columns(2)
        voltar = a.form_submit_button("← Voltar")
        concluir = b.form_submit_button("Descobrir minha trilha", type="primary", use_container_width=True)
    if voltar:
        st.session_state["etapa_wizard"] = 2
        st.rerun()
    if concluir:
        executar_consulta()
        st.rerun()

resultado = st.session_state["resultado_consulta"]
respostas = st.session_state["respostas_consulta"]
if resultado is not None and respostas is not None:
    st.divider()
    st.header("Resultado da análise")
    if resultado["inconclusivo"]:
        st.warning("As respostas não ativaram evidências suficientes para uma recomendação clara. Considere o resultado exploratório.")
    else:
        st.success(f"### Trilha recomendada: {resultado['nome']}")
        st.write(resultado["descricao"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Pontuação", resultado["pontos"])
    c2.metric("Confiança", resultado["confianca"])
    if dict(resultado["ranking"]).get(resultado["alternativa"], 0) > 0:
        c3.metric("Segunda opção", TRILHAS[resultado["alternativa"]]["nome"].split(" (")[0])
    st.subheader("Ranking das trilhas")
    df = pd.DataFrame([{"Trilha": TRILHAS[t]["nome"], "Pontuação": pontos} for t, pontos in resultado["ranking"]])
    st.bar_chart(df.set_index("Trilha"))
    st.caption("As barras representam pontuações das regras, não probabilidades absolutas de sucesso profissional.")
    st.subheader("Por que essa recomendação?")
    for m in resultado["motivos"]:
        st.markdown(f"- **{m['id']}** ({m['pontos']:+}): {m['motivo']}")
    if resultado["ressalvas"]:
        with st.expander("Pontos de atenção"):
            for m in resultado["ressalvas"]: st.markdown(f"- **{m['id']}** ({m['pontos']}): {m['motivo']}")
    with st.expander("Ver regras disparadas (rastro de inferência)"):
        for d in resultado["disparos"]:
            sinal = "+" if d["pontos"] > 0 else ""
            st.markdown(f"- **{d['id']}** → {TRILHAS[d['trilha']]['nome']} ({sinal}{d['pontos']}): {d['motivo']}")
    with st.expander("Ver respostas informadas"):
        for p in PERGUNTAS: st.markdown(f"- {p['titulo']} **{rotulo(p['chave'], respostas[p['chave']])}**")

    st.divider()
    st.header("Plano de desenvolvimento individual")
    st.write("Avalie suas competências para identificar lacunas em relação ao nível de preparação júnior.")
    st.caption("Escala: 0 = ainda não conheço; 1 = básico; 2 = intermediário; 3 = avançado. Autoavaliação orientativa, não prova técnica.")
    trilha = resultado["trilha"]
    with st.form("autoavaliacao_competencias"):
        conhecimentos = {}
        for comp in competencias_da_trilha(trilha):
            conhecimentos[comp["id"]] = st.select_slider(f"{comp['nome']} — {comp['descricao']}", options=[0,1,2,3], value=0, format_func=lambda n: NIVEIS[n], key=f"roadmap_{trilha}_{comp['id']}")
        gerar = st.form_submit_button("Analisar lacunas e gerar roadmap", type="primary", use_container_width=True)
    if gerar:
        st.session_state["roadmap_resultado"] = gerar_roadmap(trilha, conhecimentos)
        st.session_state["roadmap_trilha"] = trilha
    plano = st.session_state["roadmap_resultado"]
    if plano is not None and st.session_state["roadmap_trilha"] == trilha:
        st.subheader("Lacunas de competências")
        if plano["gaps"]:
            tabela = pd.DataFrame([{"Competência": x["nome"], "Nível atual": x["nivel_atual_rotulo"], "Nível-alvo": x["nivel_alvo_rotulo"], "Tecnologia / prática": x["tecnologia"]} for x in plano["gaps"]])
            st.dataframe(tabela, use_container_width=True, hide_index=True)
            st.write("**Prioridades de estudo:** " + "; ".join(plano["tecnologias_prioritarias"]))
        else: st.success("Todas as competências avaliadas atingiram o nível-alvo definido.")
        st.subheader("Sequência sugerida")
        for e in plano["etapas"]:
            st.markdown(f"**{e['titulo']}**")
            st.write(e["descricao"])
        st.subheader("Certificações e formações para pesquisar")
        for c in plano["certificacoes"]: st.markdown(f"- {c}")
        projeto = plano["projeto_portfolio"]
        st.subheader(f"Projeto para o portfólio: {projeto['titulo']}")
        st.write(projeto["descricao"])
        st.write("**Entregáveis sugeridos:**")
        for e in projeto["entregaveis"]: st.markdown(f"- {e}")
        st.caption(plano["observacao"])
    st.divider()
    if st.button("Começar uma nova avaliação", use_container_width=True):
        limpar_resultado()
        st.session_state["etapa_wizard"] = 1
        st.rerun()
