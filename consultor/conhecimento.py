"""Conhecimento estático do sistema: trilhas de carreira e perguntas da entrevista.

Os valores (primeiro item de cada opção) são as "chaves" usadas pelo motor de
inferência; os rótulos são apenas o texto exibido ao usuário na interface.
"""

TRILHAS = {
    "backend": {
        "nome": "Desenvolvimento Back-end",
        "descricao": "Lógica de servidores, construção de APIs, regras de negócio e bancos de dados.",
    },
    "frontend": {
        "nome": "Desenvolvimento Front-end & UI/UX",
        "descricao": "Interfaces web responsivas, experiência do usuário e frameworks reativos.",
    },
    "dados_ml": {
        "nome": "Ciência de Dados e Machine Learning",
        "descricao": "Estatística, modelagem preditiva, análise de grandes massas de dados e IA.",
    },
    "eng_dados": {
        "nome": "Engenharia de Dados",
        "descricao": "Arquitetura de dados, pipelines (ETL/ELT) e infraestrutura para Data Lakes.",
    },
    "ciberseguranca": {
        "nome": "Cibersegurança (Security / Pentesting)",
        "descricao": "Defesa cibernética, análise de vulnerabilidades, criptografia e redes seguras.",
    },
    "devops": {
        "nome": "DevOps & SRE",
        "descricao": "Automação de processos, integração e entrega contínua (CI/CD) e contêineres.",
    },
    "cloud": {
        "nome": "Computação em Nuvem (Cloud Architecture)",
        "descricao": "Planejamento, migração e gestão de infraestruturas escaláveis (AWS/Azure/GCP).",
    },
    "mobile": {
        "nome": "Desenvolvimento Mobile",
        "descricao": "Ecossistema de dispositivos móveis, nativo ou multiplataforma (Flutter/React Native).",
    },
    "qa": {
        "nome": "Engenharia de Qualidade e Testes (QA)",
        "descricao": "Testes automatizados, confiabilidade de software e processos de qualidade.",
    },
    "produto": {
        "nome": "Gestão de Produtos (Product Management)",
        "descricao": "Ponte entre negócio, design e desenvolvimento, metodologias ágeis e priorização.",
    },
}

NIVEIS = [("baixa", "Baixa"), ("media", "Média"), ("alta", "Alta")]

PERGUNTAS = [
    {
        "chave": "matematica",
        "titulo": "Qual é a sua afinidade com matemática e estatística?",
        "tipo": "nivel",
        "opcoes": NIVEIS,
        "padrao": "media",
    },
    {
        "chave": "atuacao",
        "titulo": "O que você mais gostaria de fazer no dia a dia de trabalho?",
        "tipo": "escolha",
        "opcoes": [
            ("algoritmos_logicos", "Escrever algoritmos e lógica de programação"),
            ("layouts_visuais", "Criar layouts e interfaces visuais"),
            ("apps_moveis", "Construir aplicativos para celular"),
            ("servidores_infra", "Lidar com servidores e infraestrutura"),
            ("automacao_deploy", "Automatizar processos, builds e deploys"),
            ("dados_brutos", "Analisar e trabalhar com dados brutos"),
            ("seguranca", "Garantir segurança e encontrar vulnerabilidades"),
            ("testes", "Testar sistemas e caçar falhas"),
            ("planejar_produto", "Planejar produtos, priorizar e conversar com várias áreas"),
        ],
        "padrao": "algoritmos_logicos",
    },
    {
        "chave": "ferramenta",
        "titulo": "Com qual linguagem/ferramenta você tem mais afinidade hoje?",
        "tipo": "escolha",
        "opcoes": [
            ("python", "Python"),
            ("javascript", "JavaScript / TypeScript"),
            ("java_csharp_go", "Java / C# / Go"),
            ("sql", "SQL / Bancos de dados"),
            ("linux_redes", "Linux / Redes"),
            ("mobile_lang", "Dart / Kotlin / Swift"),
            ("nenhuma", "Nenhuma / Iniciante"),
        ],
        "padrao": "python",
    },
    {
        "chave": "entrega",
        "titulo": "Que tipo de entrega de valor você prefere?",
        "tipo": "escolha",
        "opcoes": [
            ("produto_usuario", "O produto final que o usuário utiliza"),
            ("logica_negocio", "As regras de negócio e APIs que fazem o sistema funcionar"),
            ("infraestrutura", "A infraestrutura que sustenta o sistema"),
            ("seguranca", "A proteção do sistema contra invasões"),
            ("insights", "Insights e previsões extraídos de dados"),
            ("qualidade", "A confiabilidade e a qualidade do software"),
            ("estrategia", "A estratégia e a priorização do que será construído"),
        ],
        "padrao": "produto_usuario",
    },
    {
        "chave": "dados_pref",
        "titulo": "Em projetos com dados, o que mais te atrai?",
        "tipo": "escolha",
        "opcoes": [
            ("modelar", "Modelar, experimentar e prever (estatística / IA)"),
            ("pipelines", "Construir pipelines e armazenar dados em escala"),
            ("nenhum", "Não tenho interesse especial em dados"),
        ],
        "padrao": "nenhum",
    },
    {
        "chave": "ambiente",
        "titulo": "Em que ambiente você prefere que o seu trabalho 'viva'?",
        "tipo": "escolha",
        "opcoes": [
            ("navegador", "Navegador (web)"),
            ("celular", "Celular (apps)"),
            ("servidores_locais", "Servidores e contêineres próprios"),
            ("nuvem", "Nuvem (AWS / Azure / GCP)"),
            ("nao_importa", "Tanto faz"),
        ],
        "padrao": "nao_importa",
    },
    {
        "chave": "criatividade_visual",
        "titulo": "Quanto você gosta de design e criatividade visual?",
        "tipo": "nivel",
        "opcoes": NIVEIS,
        "padrao": "media",
    },
    {
        "chave": "comunicacao",
        "titulo": "Quanto você gosta de conversar com pessoas e negociar prioridades?",
        "tipo": "nivel",
        "opcoes": NIVEIS,
        "padrao": "media",
    },
    {
        "chave": "detalhismo",
        "titulo": "Quão detalhista você é para encontrar erros e brechas?",
        "tipo": "nivel",
        "opcoes": NIVEIS,
        "padrao": "media",
    },
    {
        "chave": "objetivo",
        "titulo": "Qual é o seu principal objetivo profissional?",
        "tipo": "escolha",
        "opcoes": [
            ("especialista", "Ser um especialista técnico mão na massa"),
            ("arquitetura", "Projetar a arquitetura de grandes soluções"),
            ("lideranca", "Liderar produtos e pessoas"),
            ("pesquisa_inovacao", "Pesquisar e inovar com novas tecnologias"),
        ],
        "padrao": "especialista",
    },
    {
        "chave": "experiencia",
        "titulo": "Qual é o seu nível de experiência em TI?",
        "tipo": "nivel_exp",
        "opcoes": [
            ("iniciante", "Iniciante"),
            ("intermediario", "Intermediário"),
            ("avancado", "Avançado"),
        ],
        "padrao": "iniciante",
    },
]

CHAVES = [p["chave"] for p in PERGUNTAS]


def rotulo(chave_pergunta: str, valor: str) -> str:
    """Devolve o texto amigável de uma opção a partir do seu valor interno."""
    for p in PERGUNTAS:
        if p["chave"] == chave_pergunta:
            return dict(p["opcoes"]).get(valor, valor)
    return valor
