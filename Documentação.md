Universidade Federal de Sergipe
Engenharia de Software II
Análise de Modelos de Linguagem na Interpretação de Código e Identificação de Padrões Arquiteturais de Software

Atividade 1

Membros:
Adriano Melo Santana Sobrinho – 201900050804
João Victor Oliveira Moura – 202200059830
José Domingos Valerio Serafim – 202100045733
José Fernando Bispo dos Santos – 202200014210
Matheus Nascimento dos Santos – 202100011708
Raphael Ferreira Portella Bacelar – 202100045822
Rivaldo José Nascimento dos Santos – 202200059974
Valter Fabricio dos Santos – 202000066991

Professor: Dr. Glauco de Figueiredo Carneiro
Novembro de 2025

Resumo
Este relatório apresenta a análise comparativa de diferentes modelos de linguagem pré-treinados aplicados à interpretação e compreensão de código-fonte. O estudo tem como objetivo investigar como modelos baseados em Transformers, originalmente desenvolvidos para Processamento de Linguagem Natural (PLN), podem ser utilizados para extrair informações semânticas de artefatos de software, como mensagens de commit, documentação e estrutura de projetos.
Foram avaliados três modelos distintos, cada um com características arquiteturais e propósitos específicos. O foco da análise foi verificar a capacidade desses modelos em identificar e inferir padrões arquiteturais e de design de software a partir de textos técnicos extraídos de repositórios reais.
Os experimentos foram conduzidos utilizando o repositório público LangExtract, da Google, que oferece um conjunto representativo de mensagens de commit e documentação técnica.
Os resultados obtidos demonstraram que modelos de linguagem são capazes de reconhecer indícios de padrões arquiteturais, como Layered, Clean Architecture, Repository e Service Oriented Architecture, mesmo sem treinamento supervisionado, evidenciando o potencial dessas abordagens para a engenharia de software assistida por aprendizado de máquina.
Palavras-chave: modelos de linguagem, text description, zero-shot classification, arquitetura de software, question-answering.

1. Introdução
Apresentar o contexto da análise de código com modelos de linguagem, explicando o objetivo geral do relatório e a motivação do estudo.

2. Fundamentação Teórica

3. Metodologia


4. Resultados e Discussão
### 4.1 Modelo: mDeBERTa-v3-base-xnli-multilingual
Descrição geral
O primeiro modelo utilizado neste estudo foi o mDeBERTa-v3-base-xnli-multilingual-nli-2mil7, disponibilizado pela plataforma Hugging Face. Trata-se de uma versão multilíngue da arquitetura DeBERTa v3 (Decoding-enhanced BERT with disentangled attention), treinada para tarefas de Natural Language Inference (NLI) e Zero-Shot Classification.

Ambiente e execução
O experimento foi executado no Google Colab, com Python 3.10 e GPU.
Principais comandos:
!pip install -U transformers
from transformers import pipeline

model_name = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
pipe = pipeline("zero-shot-classification", model=model_name)

Coleta e preparação dos dados
Foi utilizado o repositório LangExtract da Google.
Mensagens de commit relacionadas à arquitetura foram extraídas via git log, e o conteúdo do README.md também foi analisado para comparação.

Categorias utilizadas
O modelo foi configurado com 22 padrões arquiteturais e de design, como:
Monolithic, Microservices, Serverless, Event Driven, Layered, Hexagonal, Clean Architecture, Service Oriented Architecture, Client Server, MVC, Singleton, Factory Method, Observer, Strategy, Adapter, Facade, Decorator, Repository, Command, Dependency Injection, Modular, Pipe and Filter.

Resultados obtidos
Tabela 4.1 — Mensagens de Commit
Categoria	Score
Clean Architecture	0.8678
Modular	0.8616
Layered	0.8576
Service Oriented Architecture	0.8430
Repository	0.5965
Microservices	0.5076
...	...
Tabela 4.2 — README.md
Categoria	Score
Repository	0.9899
Service Oriented Architecture	0.9890
Microservices	0.9288
Modular	0.8627
Layered	0.8528
...	...
Análise

Os resultados mostram predominância dos padrões Clean Architecture, Layered e Modular nos commits.
Na documentação, prevalecem Repository, Service Oriented Architecture e Microservices, reforçando a coerência entre o código e a arquitetura declarada.

Conclusão parcial
O modelo mDeBERTa demonstrou boa capacidade de inferir padrões arquiteturais a partir de texto técnico, mostrando o potencial de modelos zero-shot multilíngues em engenharia de software.


## **4.2 Modelo: deepset/roberta-large-squad2**

### **Descrição geral do modelo**

O modelo utilizado neste experimento foi o **deepset/roberta-large-squad2**, baseado na arquitetura **RoBERTa** e ajustado para a tarefa de **Question Answering (QA)** com base no conjunto de dados **SQuAD2.0**.
Ele é capaz de identificar **trechos específicos do texto que respondem a uma pergunta em linguagem natural**, tornando-o adequado para **extrair informações sobre padrões de arquitetura de software a partir de commits**.

---

### **Ambiente de execução e dependências**

O experimento foi realizado no **Google Colab**

* Biblioteca principal: `transformers`

Comandos utilizados:

```python
!pip install -U transformers

from transformers import pipeline
pipe = pipeline("question-answering", model="deepset/roberta-large-squad2")
```

O repositório **LangExtract** foi clonado do GitHub:

```bash
!git clone https://github.com/google/langextract.git
```

Em seguida, os commits foram filtrados por termos relacionados à arquitetura:

```bash
git log --all -i -E --grep="architecture|pattern|registry|factory|refactor|design" --pretty=format:"%s" > commits_filtrados.txt
```

---

### **Coleta e preparação dos dados**

Foram utilizadas as **mensagens de commit** do repositório LangExtract, armazenadas no arquivo `commits_filtrados.txt`.
O conteúdo foi lido e servindo como **contexto textual** para o modelo.

Foram formuladas perguntas em inglês para identificar o padrão arquitetural adotado, como:

* “Which architectural pattern was implemented?”

---

### **Definição das categorias**

O modelo **QA** não utiliza categorias predefinidas, mas extrai diretamente do texto **o trecho que melhor responde à pergunta**.
Portanto, como já verificamos pelos commits qual arquitetura seria, formulamos a pergunta com base no que já tinhamos conhecimento.

---

### **Execução do modelo**

O pipeline de QA avaliou todas as perguntas sobre o conjunto de commits filtrados.
Para cada pergunta, o modelo retornou a **resposta mais provável** com seu respectivo **score de confiança**.

```python
questions = [
    "What architecture was the codebase refactored into?",
    "Into what architecture was the codebase refactored?",
    "What software architecture did the codebase adopt after refactoring?",
    "Which software architecture was applied during the refactor?",
    "What architecture style was implemented in the codebase?",
    "Which architectural pattern was implemented?",
    "What architecture pattern was introduced in the project?",
    "Which architecture pattern does the codebase follow after the refactor?",
    "What kind of software architecture does the codebase use?",
    "Which architecture framework or pattern was adopted?",
]

melhor = {"question": None, "answer": None, "score": 0}

for q in questions:
    result = pipe(question=q, context=context_filtrado)
    if result["score"] > melhor["score"]:
        melhor.update({"question": q, "answer": result["answer"], "score": result["score"]})
```

---

### **Resultados obtidos**

| Pergunta                                                                | Resposta                   | Score      |
| ----------------------------------------------------------------------- | -------------------------- | ---------- |
| What architecture was the codebase refactored into?                     | clean layered              | 0.9504     |
| Into what architecture was the codebase refactored?                     | clean layered              | **1.0264** |
| What software architecture did the codebase adopt after refactoring?    | clean layered architecture | 0.8975     |
| Which software architecture was applied during the refactor?            | clean layered architecture | 0.1456     |
| What architecture style was implemented in the codebase?                | clean layered architecture | 0.5889     |
| Which architectural pattern was implemented?                            | clean layered architecture | 0.0001     |
| What architecture pattern was introduced in the project?                | clean layered architecture | 0.0728     |
| Which architecture pattern does the codebase follow after the refactor? | clean layered              | 0.5556     |
| What kind of software architecture does the codebase use?               | clean layered architecture | 0.2713     |
| Which architecture framework or pattern was adopted?                    | clean layered architecture | 0.0000     |

**Observação:** Perguntas formuladas de forma próxima à redação dos commits produziram **scores mais altos**, indicando maior alinhamento semântico.

---

### **Conclusão parcial**
O modelo deepset/roberta-large-squad2 demonstrou alta precisão na identificação do padrão arquitetural adotado no projeto, extraindo consistentemente a arquitetura Clean Layered dos commits em inglês. Contudo, seu desempenho é fortemente influenciado pela formulação das perguntas, funcionando melhor quando elas estão semanticamente alinhadas ao texto dos commits.


### 4.3 Modelo 
Descrição geral do modelo
Ambiente de execução e dependências
Coleta e preparação dos dados
Definição das categorias
Execução do modelo
Resultados obtidos
Conclusão parcial


### 5. Distribuição de Atividades e Responsabilidades
Integrante	Atividades Realizadas
Adriano Melo Santana Sobrinho	xxx
João Victor Oliveira Moura	xxx
José Domingos Valerio Serafim	xxx
José Fernando Bispo dos Santos	xxx
Matheus Nascimento dos Santos	xxx
Raphael Ferreira Portella Bacelar	xxx
Rivaldo José Nascimento dos Santos	xxx
Valter Fabricio dos Santos	xxx
### 6. Conclusão

Resumo das descobertas, destacando o potencial dos modelos de linguagem para auxiliar na análise e detecção de padrões arquiteturais em software real.

### Referências
[Adicionar referências bibliográficas conforme normas da UFS]
