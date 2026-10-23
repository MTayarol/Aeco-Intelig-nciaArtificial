# Fase 1 – Engenharia de Conhecimento e Matriz de Decisão

## 1. Variáveis de entrada (entrevista)

| Chave | Pergunta | Valores possíveis |
|---|---|---|
| `matematica` | Afinidade com matemática/estatística | baixa, media, alta |
| `atuacao` | O que mais gostaria de fazer no dia a dia | algoritmos_logicos, layouts_visuais, apps_moveis, servidores_infra, automacao_deploy, dados_brutos, seguranca, testes, planejar_produto |
| `ferramenta` | Linguagem/ferramenta de maior afinidade | python, javascript, java_csharp_go, sql, linux_redes, mobile_lang, nenhuma |
| `entrega` | Tipo de entrega de valor preferida | produto_usuario, logica_negocio, infraestrutura, seguranca, insights, qualidade, estrategia |
| `dados_pref` | O que atrai em projetos com dados | modelar, pipelines, nenhum |
| `ambiente` | Onde o trabalho "vive" | navegador, celular, servidores_locais, nuvem, nao_importa |
| `criatividade_visual` | Gosto por design/criatividade visual | baixa, media, alta |
| `comunicacao` | Gosto por conversar e negociar prioridades | baixa, media, alta |
| `detalhismo` | Perfil detalhista (achar erros/brechas) | baixa, media, alta |
| `objetivo` | Objetivo profissional | especialista, arquitetura, lideranca, pesquisa_inovacao |
| `experiencia` | Nível de experiência em TI | iniciante, intermediario, avancado |

## 2. Modelo de raciocínio

Cada regra `SE <condições sobre as respostas> ENTÃO <±pontos> para <trilha>`.
Ao final, a trilha com maior pontuação é recomendada, e as regras que somaram
pontos para ela formam a justificativa. A **margem** para a 2ª colocada define a
confiança: ≥ 5 pontos = Alta, ≥ 2 = Média, abaixo disso = Baixa.

## 3. Tabela de decisão (regra → trilha)

### Back-end
| Regra | SE | Pontos |
|---|---|---|
| R01 | atuacao = algoritmos_logicos **E** ferramenta ∈ {python, java_csharp_go, sql} | +3 |
| R02 | ferramenta = java_csharp_go | +2 |
| R03 | entrega = logica_negocio | +4 |

### Front-end & UI/UX
| Regra | SE | Pontos |
|---|---|---|
| R04 | atuacao = layouts_visuais **E** criatividade_visual = alta | +5 |
| R05 | atuacao = layouts_visuais **E** criatividade_visual = media | +3 |
| R06 | ferramenta = javascript **E** ambiente = navegador | +3 |
| R07 | entrega = produto_usuario **E** ambiente = navegador | +2 |
| R08 | atuacao = layouts_visuais **E** criatividade_visual = baixa | −2 |

### Mobile
| Regra | SE | Pontos |
|---|---|---|
| R09 | atuacao = apps_moveis | +5 |
| R10 | ferramenta = mobile_lang | +4 |
| R11 | ambiente = celular | +3 |
| R12 | entrega = produto_usuario **E** ambiente = celular | +2 |

### Ciência de Dados e ML
| Regra | SE | Pontos |
|---|---|---|
| R13 | atuacao = dados_brutos **E** dados_pref = modelar **E** matematica = alta | +6 |
| R14 | ferramenta = python **E** matematica = alta **E** dados_pref = modelar | +3 |
| R15 | entrega = insights **E** dados_pref = modelar | +3 |
| R16 | objetivo = pesquisa_inovacao **E** matematica ∈ {alta, media} | +2 |
| R17 | dados_pref = modelar **E** matematica = baixa | −4 |
| R22 | dados_pref = pipelines | −2 |

### Engenharia de Dados
| Regra | SE | Pontos |
|---|---|---|
| R18 | atuacao = dados_brutos **E** dados_pref = pipelines | +6 |
| R19 | ferramenta = sql **E** dados_pref = pipelines | +3 |
| R20 | entrega = infraestrutura **E** dados_pref = pipelines | +3 |
| R21 | dados_pref = pipelines **E** matematica ∈ {baixa, media} | +2 |
| R23 | dados_pref = modelar | −2 |

> **Desambiguação DS × DE:** o fator decisivo é `dados_pref` (modelar × pipelines),
> reforçado por `matematica`. As regras R17, R21, R22 e R23 existem justamente para
> "separar" os dois perfis quando ambos escolhem `dados_brutos` e `python`/`sql`.

### Cibersegurança
| Regra | SE | Pontos |
|---|---|---|
| R24 | atuacao = seguranca | +5 |
| R25 | entrega = seguranca | +4 |
| R26 | ferramenta = linux_redes **E** atuacao = seguranca | +3 |
| R27 | detalhismo = alta **E** atuacao = seguranca | +2 |

### DevOps & SRE
| Regra | SE | Pontos |
|---|---|---|
| R28 | atuacao = automacao_deploy | +5 |
| R29 | ferramenta = linux_redes **E** atuacao = automacao_deploy | +3 |
| R30 | entrega = infraestrutura **E** atuacao = automacao_deploy | +2 |
| R31 | ambiente = servidores_locais **E** atuacao = servidores_infra | +3 |
| R32 | atuacao = servidores_infra **E** ferramenta = linux_redes | +2 |

### Computação em Nuvem
| Regra | SE | Pontos |
|---|---|---|
| R33 | ambiente = nuvem **E** atuacao = servidores_infra | +5 |
| R34 | objetivo = arquitetura **E** ambiente = nuvem | +4 |
| R35 | entrega = infraestrutura **E** ambiente = nuvem | +3 |
| R36 | atuacao = servidores_infra **E** objetivo = arquitetura | +2 |
| R37 | experiencia = iniciante **E** objetivo = arquitetura | −2 |

> **Desambiguação DevOps × Cloud:** infraestrutura em servidores próprios/automação
> pende para DevOps (R28–R32); infraestrutura na nuvem com viés de arquitetura pende
> para Cloud (R33–R37).

### QA
| Regra | SE | Pontos |
|---|---|---|
| R38 | atuacao = testes | +5 |
| R39 | entrega = qualidade | +4 |
| R40 | detalhismo = alta **E** atuacao = testes | +3 |

### Gestão de Produtos
| Regra | SE | Pontos |
|---|---|---|
| R41 | atuacao = planejar_produto | +5 |
| R42 | entrega = estrategia | +4 |
| R43 | comunicacao = alta **E** objetivo = lideranca | +3 |
| R44 | comunicacao = baixa **E** atuacao = planejar_produto | −3 |
| R45 | ferramenta = nenhuma **E** comunicacao = alta **E** atuacao = planejar_produto | +2 |

### Regra de decisão
| Regra | SE | ENTÃO |
|---|---|---|
| R46 | todas as regras de pontuação já dispararam (salience −100) | Escolher a trilha de maior pontuação, calcular margem/confiança e montar a justificativa |

## 4. Resumo

- **45 regras de inferência** + 1 regra de decisão = **46 regras** (requisito: 20–25+).
- Regras **cruzadas** (2 ou 3 condições): 31 das 45.
- Regras de **penalidade** (conflitos/pré-requisitos): R08, R17, R22, R23, R37, R44.
