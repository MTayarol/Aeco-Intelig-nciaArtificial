"""Motor de inferência (Experta) do Consultor Inteligente de Carreiras em TI.

Este arquivo preserva as regras existentes e fortalece a validação de entrada:
chaves desconhecidas e respostas fora das opções da entrevista são rejeitadas.
"""

# --- Compatibilidade: Experta 1.9.x usa collections.Mapping, removido no Python 3.10+
import collections
import collections.abc

for _nome in ("Mapping", "MutableMapping", "Sequence", "Iterable", "Callable"):
    if not hasattr(collections, _nome):
        setattr(collections, _nome, getattr(collections.abc, _nome))
# ---------------------------------------------------------------------------------

from functools import reduce
from operator import or_

from experta import Fact, KnowledgeEngine, L, Rule

from .conhecimento import CHAVES, PERGUNTAS, TRILHAS


class Perfil(Fact):
    """Respostas do usuário na entrevista."""


class Decisao(Fact):
    """Sinaliza que a fase de pontuação terminou e a conclusão pode ser tirada."""


def em(*valores):
    """Condição 'o campo é um dos valores' (OU lógico)."""
    return reduce(or_, (L(v) for v in valores))


class ConsultorCarreiras(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.pontuacao = {trilha: 0 for trilha in TRILHAS}
        self.disparos = []
        self.resultado = None

    def _pontuar(self, regra_id, trilha, pontos, motivo):
        self.pontuacao[trilha] += pontos
        self.disparos.append({"id": regra_id, "trilha": trilha, "pontos": pontos, "motivo": motivo})

    # ======================= BACK-END =======================
    @Rule(Perfil(atuacao="algoritmos_logicos", ferramenta=em("python", "java_csharp_go", "sql")))
    def r01(self): self._pontuar("R01", "backend", 3, "Gosta de escrever lógica e domina uma linguagem típica de servidor.")
    @Rule(Perfil(ferramenta="java_csharp_go"))
    def r02(self): self._pontuar("R02", "backend", 2, "Java, C# e Go são linguagens muito usadas em sistemas de back-end.")
    @Rule(Perfil(entrega="logica_negocio"))
    def r03(self): self._pontuar("R03", "backend", 4, "Prefere entregar regras de negócio e APIs que sustentam o sistema.")

    # ======================= FRONT-END ======================
    @Rule(Perfil(atuacao="layouts_visuais", criatividade_visual="alta"))
    def r04(self): self._pontuar("R04", "frontend", 5, "Gosta de criar interfaces e tem alta criatividade visual.")
    @Rule(Perfil(atuacao="layouts_visuais", criatividade_visual="media"))
    def r05(self): self._pontuar("R05", "frontend", 3, "Gosta de criar interfaces e tem boa sensibilidade visual.")
    @Rule(Perfil(ferramenta="javascript", ambiente="navegador"))
    def r06(self): self._pontuar("R06", "frontend", 3, "Tem afinidade com JavaScript e quer trabalhar no navegador.")
    @Rule(Perfil(entrega="produto_usuario", ambiente="navegador"))
    def r07(self): self._pontuar("R07", "frontend", 2, "Quer entregar o produto final que o usuário vê na web.")
    @Rule(Perfil(atuacao="layouts_visuais", criatividade_visual="baixa"))
    def r08(self): self._pontuar("R08", "frontend", -2, "Prefere layouts, mas declara baixa criatividade visual (conflito).")

    # ================= MOBILE ===============================
    @Rule(Perfil(atuacao="apps_moveis"))
    def r09(self): self._pontuar("R09", "mobile", 5, "Quer construir aplicativos para celular no dia a dia.")
    @Rule(Perfil(ferramenta="mobile_lang"))
    def r10(self): self._pontuar("R10", "mobile", 4, "Tem afinidade com linguagens do ecossistema mobile (Dart/Kotlin/Swift).")
    @Rule(Perfil(ambiente="celular"))
    def r11(self): self._pontuar("R11", "mobile", 3, "Prefere que o seu trabalho rode em dispositivos móveis.")
    @Rule(Perfil(entrega="produto_usuario", ambiente="celular"))
    def r12(self): self._pontuar("R12", "mobile", 2, "Quer entregar o produto final ao usuário dentro de um app.")

    # ============== CIÊNCIA DE DADOS / ML ====================
    @Rule(Perfil(atuacao="dados_brutos", dados_pref="modelar", matematica="alta"))
    def r13(self): self._pontuar("R13", "dados_ml", 6, "Analisa dados brutos para modelar/prever e tem alta afinidade com estatística.")
    @Rule(Perfil(ferramenta="python", matematica="alta", dados_pref="modelar"))
    def r14(self): self._pontuar("R14", "dados_ml", 3, "Python + matemática forte + interesse em modelagem é o núcleo de ML.")
    @Rule(Perfil(entrega="insights", dados_pref="modelar"))
    def r15(self): self._pontuar("R15", "dados_ml", 3, "Quer entregar insights e previsões extraídos de dados.")
    @Rule(Perfil(objetivo="pesquisa_inovacao", matematica=em("alta", "media")))
    def r16(self): self._pontuar("R16", "dados_ml", 2, "Quer pesquisar e inovar e tem base matemática para isso.")
    @Rule(Perfil(dados_pref="modelar", matematica="baixa"))
    def r17(self): self._pontuar("R17", "dados_ml", -4, "Modelagem preditiva exige base estatística, que o perfil declara como baixa.")

    # ============== ENGENHARIA DE DADOS =====================
    @Rule(Perfil(atuacao="dados_brutos", dados_pref="pipelines"))
    def r18(self): self._pontuar("R18", "eng_dados", 6, "Trabalha com dados brutos e prefere construir pipelines a modelar.")
    @Rule(Perfil(ferramenta="sql", dados_pref="pipelines"))
    def r19(self): self._pontuar("R19", "eng_dados", 3, "SQL e pipelines de dados andam juntos (ETL/ELT).")
    @Rule(Perfil(entrega="infraestrutura", dados_pref="pipelines"))
    def r20(self): self._pontuar("R20", "eng_dados", 3, "Prefere entregar a infraestrutura que movimenta e armazena dados.")
    @Rule(Perfil(dados_pref="pipelines", matematica=em("baixa", "media")))
    def r21(self): self._pontuar("R21", "eng_dados", 2, "Engenharia de dados exige menos estatística que ciência de dados.")
    @Rule(Perfil(dados_pref="pipelines"))
    def r22(self): self._pontuar("R22", "dados_ml", -2, "Quem prefere construir pipelines em vez de modelar tende a Engenharia de Dados.")
    @Rule(Perfil(dados_pref="modelar"))
    def r23(self): self._pontuar("R23", "eng_dados", -2, "Quem prefere modelar e experimentar tende a Ciência de Dados.")

    # ================= CIBERSEGURANÇA =======================
    @Rule(Perfil(atuacao="seguranca"))
    def r24(self): self._pontuar("R24", "ciberseguranca", 5, "Quer trabalhar diariamente com segurança e vulnerabilidades.")
    @Rule(Perfil(entrega="seguranca"))
    def r25(self): self._pontuar("R25", "ciberseguranca", 4, "Valoriza proteger o sistema contra invasões como entrega de valor.")
    @Rule(Perfil(ferramenta="linux_redes", atuacao="seguranca"))
    def r26(self): self._pontuar("R26", "ciberseguranca", 3, "Linux e redes são a base prática de pentest e defesa.")
    @Rule(Perfil(detalhismo="alta", atuacao="seguranca"))
    def r27(self): self._pontuar("R27", "ciberseguranca", 2, "Perfil muito detalhista, ideal para achar brechas.")

    # ================= DEVOPS ===============================
    @Rule(Perfil(atuacao="automacao_deploy"))
    def r28(self): self._pontuar("R28", "devops", 5, "Gosta de automatizar processos, builds e deploys.")
    @Rule(Perfil(ferramenta="linux_redes", atuacao="automacao_deploy"))
    def r29(self): self._pontuar("R29", "devops", 3, "Automação sobre Linux/redes é o dia a dia de DevOps/SRE.")
    @Rule(Perfil(entrega="infraestrutura", atuacao="automacao_deploy"))
    def r30(self): self._pontuar("R30", "devops", 2, "Entrega valor automatizando a infraestrutura (CI/CD, contêineres).")
    @Rule(Perfil(ambiente="servidores_locais", atuacao="servidores_infra"))
    def r31(self): self._pontuar("R31", "devops", 3, "Cuida de servidores e contêineres próprios, típico de DevOps/SRE.")
    @Rule(Perfil(atuacao="servidores_infra", ferramenta="linux_redes"))
    def r32(self): self._pontuar("R32", "devops", 2, "Lida com servidores e domina Linux/redes.")

    # ================= CLOUD =================================
    @Rule(Perfil(ambiente="nuvem", atuacao="servidores_infra"))
    def r33(self): self._pontuar("R33", "cloud", 5, "Quer lidar com infraestrutura e prefere que ela viva na nuvem.")
    @Rule(Perfil(objetivo="arquitetura", ambiente="nuvem"))
    def r34(self): self._pontuar("R34", "cloud", 4, "Quer projetar arquiteturas de grande porte na nuvem.")
    @Rule(Perfil(entrega="infraestrutura", ambiente="nuvem"))
    def r35(self): self._pontuar("R35", "cloud", 3, "Entrega valor via infraestrutura escalável em provedores de nuvem.")
    @Rule(Perfil(atuacao="servidores_infra", objetivo="arquitetura"))
    def r36(self): self._pontuar("R36", "cloud", 2, "Combina infraestrutura com o desejo de arquitetar soluções.")
    @Rule(Perfil(experiencia="iniciante", objetivo="arquitetura"))
    def r37(self): self._pontuar("R37", "cloud", -2, "Arquitetura de nuvem costuma exigir experiência prévia (iniciante).")

    # ================= QA ====================================
    @Rule(Perfil(atuacao="testes"))
    def r38(self): self._pontuar("R38", "qa", 5, "Quer testar sistemas e caçar falhas no dia a dia.")
    @Rule(Perfil(entrega="qualidade"))
    def r39(self): self._pontuar("R39", "qa", 4, "Valoriza a confiabilidade e a qualidade do software.")
    @Rule(Perfil(detalhismo="alta", atuacao="testes"))
    def r40(self): self._pontuar("R40", "qa", 3, "Perfil muito detalhista, ideal para encontrar bugs.")

    # ================= PRODUTO ===============================
    @Rule(Perfil(atuacao="planejar_produto"))
    def r41(self): self._pontuar("R41", "produto", 5, "Gosta de planejar produtos, priorizar e dialogar com várias áreas.")
    @Rule(Perfil(entrega="estrategia"))
    def r42(self): self._pontuar("R42", "produto", 4, "Valoriza a estratégia e a priorização do que será construído.")
    @Rule(Perfil(comunicacao="alta", objetivo="lideranca"))
    def r43(self): self._pontuar("R43", "produto", 3, "Boa comunicação e objetivo de liderar produtos e pessoas.")
    @Rule(Perfil(comunicacao="baixa", atuacao="planejar_produto"))
    def r44(self): self._pontuar("R44", "produto", -3, "Planejar produtos exige muita interação, mas a comunicação é baixa (conflito).")
    @Rule(Perfil(ferramenta="nenhuma", comunicacao="alta", atuacao="planejar_produto"))
    def r45(self): self._pontuar("R45", "produto", 2, "Perfil de negócios com boa comunicação, sem depender de programação intensa.")

    # ================= DECISÃO ===============================
    @Rule(Decisao(pronto=True), salience=-100)
    def r46_decidir(self):
        ordem = list(TRILHAS)
        ranking = sorted(self.pontuacao.items(), key=lambda kv: (-kv[1], ordem.index(kv[0])))
        vencedora, pontos = ranking[0]
        segunda, pontos_segunda = ranking[1]
        margem = pontos - pontos_segunda
        confianca = "Alta" if margem >= 5 else "Média" if margem >= 2 else "Baixa"
        a_favor = sorted((d for d in self.disparos if d["trilha"] == vencedora and d["pontos"] > 0), key=lambda d: -d["pontos"])
        contra = [d for d in self.disparos if d["trilha"] == vencedora and d["pontos"] < 0]
        self.resultado = {
            "trilha": vencedora, "nome": TRILHAS[vencedora]["nome"],
            "descricao": TRILHAS[vencedora]["descricao"], "pontos": pontos,
            "alternativa": segunda, "margem": margem, "confianca": confianca,
            "inconclusivo": pontos <= 0, "motivos": a_favor, "ressalvas": contra,
            "ranking": ranking, "disparos": list(self.disparos),
        }


def validar_respostas(respostas: dict) -> None:
    """Valida a entrevista antes de inserir os valores no fato do Experta."""
    if not isinstance(respostas, dict):
        raise TypeError("Respostas devem ser fornecidas em um dicionário.")
    faltando = [chave for chave in CHAVES if chave not in respostas]
    if faltando:
        raise ValueError(f"Respostas faltando: {', '.join(faltando)}")
    extras = sorted(set(respostas) - set(CHAVES))
    if extras:
        raise ValueError(f"Respostas desconhecidas: {', '.join(extras)}")
    invalidas = []
    for pergunta in PERGUNTAS:
        chave = pergunta["chave"]
        valores_validos = {valor for valor, _rotulo in pergunta["opcoes"]}
        if respostas[chave] not in valores_validos:
            invalidas.append(f"{chave}={respostas[chave]!r}")
    if invalidas:
        raise ValueError("Respostas inválidas: " + ", ".join(invalidas))


def consultar(respostas: dict) -> dict:
    """Roda o motor para um dicionário de respostas e devolve o diagnóstico."""
    validar_respostas(respostas)
    motor = ConsultorCarreiras()
    motor.reset()
    motor.declare(Perfil(**{c: respostas[c] for c in CHAVES}))
    motor.declare(Decisao(pronto=True))
    motor.run()
    return motor.resultado
