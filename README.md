# Consultor Inteligente de Carreiras em TI

Sistema Especialista baseado em regras que entrevista o usuário e recomenda a trilha de
carreira em TI mais adequada entre **10 opções**, justificando a decisão com as regras que
foram disparadas.

Trabalho desenvolvido para o **Centro Universitário Presidente Antônio Carlos – UNIPAC Barbacena**.

## Trilhas de carreira

1. Desenvolvimento Back-end
2. Desenvolvimento Front-end & UI/UX
3. Ciência de Dados e Machine Learning
4. Engenharia de Dados
5. Cibersegurança (Security / Pentesting)
6. DevOps & SRE
7. Computação em Nuvem (Cloud Architecture)
8. Desenvolvimento Mobile
9. Engenharia de Qualidade e Testes (QA)
10. Gestão de Produtos (Product Management)

## Como funciona

- **Entrevista:** 11 perguntas objetivas sobre afinidade matemática, preferência de atuação,
  linguagem/ferramenta, tipo de entrega, interesse em dados, ambiente, criatividade visual,
  comunicação, detalhismo, objetivo e experiência.
- **Motor de inferência (Experta):** as respostas válidas são convertidas em um fato `Perfil`.
  **45 regras** SE-ENTÃO de pontuação (incluindo regras que cruzam 2 ou 3 respostas) somam ou
  subtraem pontos para cada trilha, usando encadeamento para frente. Uma regra final, de menor
  prioridade (`salience=-100`), seleciona a trilha vencedora.
- **Desambiguação:** regras cruzadas e de penalidade ajudam a diferenciar perfis parecidos,
  como Cientista de Dados × Engenheiro de Dados e DevOps × Cloud.
- **Validação das respostas:** o motor verifica se todas as perguntas foram respondidas e se
  as chaves e os valores informados pertencem às opções previstas na entrevista.
- **Justificativa transparente:** o resultado apresenta a trilha recomendada, a confiança
  (calculada pela margem em relação à segunda colocada), as regras favoráveis, as ressalvas,
  a pontuação e o ranking completo.
- **Roadmap de aprendizagem:** a partir da trilha recomendada, o sistema compara a
  autoavaliação do usuário com níveis-alvo de competências e apresenta lacunas, etapas de
  estudo, recursos e uma proposta de projeto para portfólio.

A tabela de decisão completa está em [`docs/matriz_decisao.md`](docs/matriz_decisao.md).

## Estrutura do projeto

```text
Aeco-Intelig-nciaArtificial/
├── app.py                       # Interface web (Streamlit)
├── consultor/
│   ├── __init__.py
│   ├── conhecimento.py          # Trilhas, perguntas e opções da entrevista
│   ├── motor.py                 # Fatos, regras e motor de inferência (Experta)
│   ├── personas.py              # Personas e perfis de demonstração/teste
│   ├── roadmap.py               # Análise de lacunas e geração do roadmap
│   └── dados/
│       └── roadmaps.json        # Competências, recursos e projetos por trilha
├── tests/
│   ├── test_personas.py         # Validação das personas e recomendações
│   ├── test_robustez.py         # Contratos, determinismo e ranking
│   ├── test_roadmap.py          # Testes do gerador de roadmap
│   └── test_edge_cases.py       # Casos limite e validação de entradas
├── docs/
│   └── matriz_decisao.md        # Matriz de decisão do sistema
├── conftest.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalação e execução

Requer **Python 3.10 ou superior**.

```bash
# 1. Clone o repositório
git clone https://github.com/MTayarol/Aeco-Intelig-nciaArtificial.git
cd Aeco-Intelig-nciaArtificial

# 2. (Recomendado) crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1

# 3. Instale as dependências
python -m pip install -r requirements.txt

# 4. Execute a aplicação
python -m streamlit run app.py
```

O navegador abrirá em `http://localhost:8501`.

> **Nota sobre o Experta no Python 3.10+:** a versão 1.9.4 do Experta usa `collections.Mapping`,
> removido no Python 3.10. O arquivo `consultor/motor.py` aplica uma correção de compatibilidade
> antes de importar a biblioteca, então não é necessário fazer esse ajuste manualmente.

## Testes e validação

Para executar toda a suíte automatizada, incluindo personas, robustez, roadmap e casos limite:

```bash
python -m pytest -v
```

A suíte verifica, entre outros pontos:

- se todas as trilhas são contempladas pelas personas e recebem recomendações justificadas;
- se o resultado contém os campos esperados, um ranking completo e comportamento determinístico;
- se perfis pouco informativos ou ambíguos não interrompem a consulta;
- se conflitos entre respostas são tratados pelas regras correspondentes;
- se respostas ausentes, chaves desconhecidas ou valores fora das opções válidas são rejeitados;
- se o roadmap valida competências e níveis e identifica corretamente as lacunas de aprendizagem.

### Personas utilizadas na validação

| Persona | Perfil | Trilha esperada |
|---|---|---|
| Ana | Analítica: estatística, Python, previsões | Ciência de Dados e ML |
| Bruno | Dados com foco em SQL e pipelines | Engenharia de Dados |
| Carla | Infra/segurança: Linux, redes, vulnerabilidades | Cibersegurança |
| Diego | Visual: layouts, JavaScript, navegador | Front-end & UI/UX |
| Elisa | Negócios/produto: estratégia e comunicação | Gestão de Produtos |
| Felipe | Automação, CI/CD, Linux | DevOps & SRE |
| Gabi | Infraestrutura escalável na nuvem | Computação em Nuvem |
| Hugo | Apps para celular (Dart/Kotlin) | Mobile |
| Iara | Detalhista, caça bugs | QA |
| João | Java, regras de negócio, APIs | Back-end |
| Casos ambíguos | Dados com Python: modelagem × pipelines | Ciência de Dados × Engenharia de Dados |

As personas também podem ser utilizadas como exemplos de perfis para demonstração da aplicação.

## Tecnologias

Python 3.10+ · [Experta](https://github.com/nilp0inter/experta) · [Streamlit](https://streamlit.io) · pytest
