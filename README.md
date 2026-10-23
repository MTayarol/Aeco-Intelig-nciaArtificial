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

- **Entrevista:** 11 perguntas objetivas (afinidade matemática, preferência de atuação, linguagem/ferramenta,
  tipo de entrega, interesse em dados, ambiente, criatividade visual, comunicação, detalhismo, objetivo e experiência).
- **Motor de inferência (Experta):** as respostas viram um fato `Perfil`. **45 regras** SE-ENTÃO
  (31 delas cruzando 2 ou 3 respostas) somam ou subtraem pontos para cada trilha, usando
  encadeamento para frente. Uma regra final de menor prioridade (`salience=-100`) escolhe a vencedora.
- **Desambiguação:** regras cruzadas e de penalidade separam perfis parecidos, como
  Cientista de Dados × Engenheiro de Dados e DevOps × Cloud.
- **Justificativa transparente:** a interface mostra a trilha, a confiança (pela margem para a 2ª colocada),
  as regras que sustentam a decisão, os pontos de atenção e o rastro completo de regras disparadas.

A tabela de decisão completa está em [`docs/matriz_decisao.md`](docs/matriz_decisao.md).

## Estrutura do projeto

```
Aeco-Intelig-nciaArtificial/
├── app.py                    # Interface web (Streamlit)
├── consultor/
│   ├── conhecimento.py       # Trilhas e perguntas da entrevista
│   ├── motor.py              # Base de conhecimento: fatos e regras (Experta)
│   └── personas.py           # Personas de teste
├── tests/
│   └── test_personas.py      # Validação automatizada (pytest)
├── docs/
│   └── matriz_decisao.md     # Fase 1: matriz de decisão
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
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
streamlit run app.py
```

O navegador abrirá em `http://localhost:8501`.

> **Nota sobre o Experta no Python 3.10+:** a versão 1.9.4 do Experta usa `collections.Mapping`,
> removido no Python 3.10. O arquivo `consultor/motor.py` já aplica uma pequena correção de
> compatibilidade antes de importar a biblioteca, então nada precisa ser feito manualmente.

## Validação com personas (Fase 4)

```bash
pytest -v
```

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
| 2 casos limite | Dados com Python: prever × pipelines | DS × DE |

As personas também podem ser carregadas na barra lateral da aplicação para demonstração.

## Tecnologias

Python 3.10+ · [Experta](https://github.com/nilp0inter/experta) · [Streamlit](https://streamlit.io) · pytest
