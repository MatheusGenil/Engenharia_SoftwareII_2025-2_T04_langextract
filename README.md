# Engenharia_SoftwareII_2025-2_T04_langextract

Este repositório contém os experimentos, scripts e documentação produzidos para a atividade de análise de padrões arquiteturais utilizando modelos de linguagem pré-treinados. O objetivo central do trabalho é investigar como modelos baseados em Transformers, originalmente desenvolvidos para Processamento de Linguagem Natural (PLN), podem ser aplicados à interpretação de artefatos de software, como mensagens de commit e documentação técnica.

A análise foi conduzida utilizando técnicas de Zero-Shot Classification e Question Answering, aplicadas a textos reais extraídos do repositório público <a href="https://github.com/google/langextract" target="_blank">LangExtract</a>, da Google. O foco foi verificar a capacidade desses modelos em identificar padrões arquiteturais presentes no projeto, tais como Layered Architecture, Clean Architecture, Repository Pattern e Service-Oriented Architecture, mesmo sem nenhum treinamento supervisionado específico para essa tarefa.

Tutorial completo (PDF): https://github.com/MatheusGenil/Engenharia_SoftwareII_2025-2_T04_langextract/blob/01e6da0d09d93cf5f88d8c8ffe3e196260fe29bc/Tutorial.pdf

Link do video: https://drive.google.com/file/d/1UKRzWij-_ip2Oz2yoU1lPN26qh0kOO5a/view?usp=sharing

**Como executar as implementações:** https://colab.research.google.com/drive/16JMDe9skailRM10duQE4F_duC9Mkq1V_?usp=sharing

<section>
    <h1>Metodologia</h1>
    <p>
        Este capítulo descreve as etapas, ferramentas e procedimentos adotados na condução
        dos experimentos realizados para a análise de padrões arquiteturais em projetos de software,
        utilizando modelos de linguagem pré-treinados. O objetivo principal desta etapa é detalhar
        o processo que permitiu aplicar técnicas de <strong>Zero-Shot Classification</strong> e 
        <strong>Question Answering (QA)</strong> a artefatos textuais de repositórios reais,
        garantindo a reprodutibilidade dos resultados.
    </p>
    <h1>Motivo da escolha dos modelos</h1>
    <p>        
        
        
**joeddav/xlm-roberta-large-xnli:** Multilíngue forte e robusto, sendo melhor para Commits mistos e textos curtos e informais.

**facebook/bart-large-mnli:** Baseline clássico, ótimo com textos longos, sendo melhor para README, documentação e análises formais.

**mDeBERTa-v3-base-mnli-xnli:** Mais moderno e maior precisão, sendo melhor, no geral para Zero-Shot de arquitetura.

**deepset/roberta-large-squad2:** Modelo de Perguntas e Respostas capaz de identificar quando existe ou não resposta no texto, ótimo para validar conteúdo real dentro dos commits.

**google-bert/bert-large-cased-whole-word-masking-finetuned-squad:** É um modelo extremamente estável e previsível, diferente de modelos mais novos como RoBERTa ou DeBERTa. Trata-se de um modelo rápido, leve o suficiente para rodar em CPU, não introduz "alucinações", responde só baseado no contexto fornecido, excelente para análise técnica e documentação ou textos longos.
    </p>
    <h2>Infraestrutura para Execução dos Modelos</h2>
    <p>
        A execução dos modelos foi realizada em um ambiente na nuvem, utilizando o serviço Google Colab (Runtime Gratuito), que disponibiliza recursos computacionais suficientes para treinar e validar modelos de aprendizado de máquina.

**Especificação do Serviço:**
- Plataforma: Google Colab – Runtime Gratuito
- Tipo de ambiente: Google Compute Engine (instância temporária)
- Linguagem: Python 3
- Aceleração: GPU habilitada

**Recursos Computacionais Disponíveis:**
- GPU: NVIDIA Tesla T4
- VRAM: 15 GB
- Memória RAM do sistema: 12.7 GB
- Disco disponível: 112.6 GB
- Sistema Operacional: Linux (instância virtual do Google Cloud)
    </p>
    <h2>Ambiente de Experimentos</h2>
    <p>
        Todos os experimentos foram realizados no ambiente <strong>Google Colab</strong>, utilizando a
        biblioteca <strong>Transformers</strong> da Hugging Face, amplamente reconhecida por seu suporte
        a modelos baseados na arquitetura Transformer. Foram utilizados notebooks em <strong>Python 3</strong>,
        com versões atualizadas das bibliotecas <code>transformers</code>, <code>torch</code> e 
        <code>subprocess</code>.
    </p>
    <p>
        Os modelos foram carregados diretamente do repositório <strong>Hugging Face Hub</strong>, o que
        possibilitou o uso de diferentes arquiteturas de forma modular. O repositório público
        <code>google/langextract</code>, hospedado no GitHub, foi selecionado como base de análise
        por conter código-fonte e documentação textual representando um cenário real de engenharia
        de software.
    </p>
    <h2>Coleta de Dados</h2>
    <p>
        O primeiro passo consistiu em clonar o repositório <strong>LangExtract</strong> por meio de comandos
        Git executados dentro do notebook. A partir dele, foram extraídos dois tipos de artefatos textuais:
    </p>
    <ul>
        <li>
            <strong>Mensagens de commit</strong>: obtidas com o comando <code>git log</code>, filtrando mensagens
            que continham termos relacionados a padrões arquiteturais e de design, como
            <em>architecture</em>, <em>pattern</em>, <em>refactor</em>, entre outros.
        </li>
        <li>
            <strong>Documentação técnica</strong>: conteúdo do arquivo <code>README.md</code>, utilizado como
            base textual para a análise semântica.
        </li>
    </ul>
    <p>
        Esses textos foram utilizados como contexto para a execução dos modelos de linguagem,
        permitindo avaliar a capacidade de cada modelo em identificar referências explícitas
        ou implícitas a padrões de arquitetura.
    </p>
    <h2>Configuração dos Modelos</h2>
    <p>Foram utilizados dois tipos principais de abordagens baseadas em modelos pré-treinados:</p>
    <ol>
        <li>
            <strong>Zero-Shot Classification</strong>: nessa abordagem, o modelo recebe um texto e um
            conjunto de possíveis rótulos (<em>candidate labels</em>) correspondentes a padrões arquiteturais,
            como <em>Layered</em>, <em>Microservices</em>, <em>MVC</em>, <em>Factory Method</em>, entre outros.
            O modelo, sem treinamento supervisionado, calcula a probabilidade de cada rótulo estar
            relacionado ao conteúdo analisado.
        </li>
        <li>meto
            <strong>Question Answering (QA)</strong>: nesta etapa, foram aplicados modelos ajustados para
            responder perguntas baseadas em um contexto textual. O contexto fornecido foi o conteúdo
            do arquivo <code>README.md</code>, e as perguntas buscaram identificar qual padrão arquitetural
            o projeto segue, qual arquitetura foi adotada ou qual estilo de design está descrito
            na documentação.
        </li>
    </ol>
    <h2>Fluxo Experimental</h2>
    <p>A execução de cada experimento seguiu o seguinte fluxo:</p>
    <ol>
        <li>Instalação e importação das bibliotecas necessárias;</li>
        <li>Clonagem do repositório LangExtract;</li>
        <li>Extração e leitura dos artefatos textuais (commits e README);</li>
        <li>Processamento dos textos com os modelos de linguagem definidos;</li>
        <li>Registro dos resultados gerados (rótulos preditos ou respostas textuais);</li>
        <li>Análise comparativa entre os modelos.</li>
    </ol>
    <p>
        Cada modelo foi executado individualmente sobre os mesmos conjuntos de dados,
        garantindo a uniformidade da análise. As saídas foram registradas no console do notebook
        e posteriormente interpretadas para fins de discussão e comparação.
    </p>
    <h2>Critérios de Avaliação</h2>
    <p>A avaliação dos resultados baseou-se em dois aspectos principais:</p>
    <ul>
        <li>
            <strong>Relevância semântica</strong>: medida pela coerência entre a predição do modelo e o
            conteúdo real dos artefatos analisados.
        </li>
        <li>
            <strong>Confiança (score)</strong>: valor de probabilidade retornado por cada modelo,
            indicando a segurança da resposta ou classificação gerada.
        </li>
    </ul>
    <p>
        Esses critérios permitiram comparar o desempenho relativo das abordagens Zero-Shot
        e Question Answering, bem como discutir a adequação de cada modelo às tarefas
        de extração de informações arquiteturais em código e documentação.
    </p>
</section>


<h1>Documentação do Script de Classificação Zero-Shot com Hugging Face</h1>

<h3>Visão Geral</h3>
<p>O código em análise implementa um script em Python para a identificação de padrões
arquiteturais em projetos de software hospedados no GitHub, utilizando classificação
zero-shot com modelos da biblioteca transformers da Hugging Face. O objetivo é
aplicar técnicas de Natural Language Processing (NLP) para inferir, a partir de diferentes
fontes de texto (como o arquivo README.md ou mensagens de commits), qual padrão
arquitetural o projeto aparenta seguir.</p>

<h3>Objetivo do Script</h3>

<p>O script permite que o usuário selecione:
• A estratégia de análise: leitura de README.md ou análise de mensagens de commit.
• O modelo de linguagem (LLM) utilizado na classificação.
A partir dessas escolhas, o sistema coleta textos relevantes (filtrando por termos de busca específicos relacionados à arquitetura) e os submete ao modelo zero-shot selecionado para inferir o padrão arquitetural mais provável.</p>

<h3>Estrutura e Dependências</h3>

<p>O script utiliza as seguintes bibliotecas:</p>
  <ul>
    <li>os, subprocess: interação com o sistema e execução de comandos Git.</li>
    <li>requests: para obter conteúdo remoto via HTTP.</li>
    <li>re: expressões regulares para filtragem de termos relevantes.</li>
    <li>transformers: provê a pipeline de classificação zero-shot.</li>
  </ul>

  
<h3>Descrição da Classe Principal</h3>
<p>Classe HuggingFaceWrapper
Encapsula o uso da pipeline de classificação da Hugging Face.</p>

<ul>
  <li>Método __init__: inicializa a pipeline zero-shot com o modelo indicado.</li>
  <li>Método classify_text: realiza a classificação de um texto, retornando rótulos (labels) e pontuações de confiança.</li>
</ul>


<h3>Fluxo de Execução</h3>
<p>O fluxo principal do programa ocorre em etapas:</p>
<ol>
  <li>Exibição de um menu de estratégias disponíveis:
    <ol>
      <li>Análise via README.md</li>
      <li>Análise via Commits</li>
    </ol>
  </li>
  <li>Validação da entrada do usuário e confirmação da estratégia escolhida.</li>
  <li>Seleção do modelo de classificação entre as seguintes opções:
      <ul>
        <li>joeddav/xlm-roberta-large-xnli</li>
        <li>facebook/bart-large-mnli</li>
        <li>MoritzLaurer/mDeBERTa-v3-base-mnli-xnli</li>
      </ul>
  </li>
  <li>Instanciação da classe HuggingFaceWrapper com o modelo escolhido.</li>
  <li>Execução da análise, que varia conforme a estratégia:
    <ul>
      <li>Estratégia 1 – README.md: obtém o conteúdo do arquivo remoto via
HTTP e filtra linhas contendo termos relacionados à arquitetura.</li>
      <li>Estratégia 2 – Commits: clona o repositório e utiliza o comando git log
com filtros –grep para buscar mensagens relevantes.</li>
    </ul>
  </li>

  <li>Submissão do texto filtrado ao modelo zero-shot e exibição dos resultados, apresentando os rótulos mais prováveis e seus respectivos níveis de confiança.</li>
</ol>
  
<h3>Termos de Busca</h3>
<p>Os termos de filtragem textual utilizados são:</p>
<code>architecture, architectural, pattern, design, provider, plugin, module, interface, layer, service</code>
<p>Esses termos funcionam como um mecanismo de busca (grep) para localizar trechos potencialmente associados à definição ou implementação de padrões arquiteturais.</p>
  
<h3>Saída Esperada</h3>
<p>Ao executar corretamente (com as variáveis ajustadas), o script exibe no terminal algo
como:</p>
<code>============== facebook/bart-large-mnli ==============
Resultado da inferência de arquitetura:
Layered Architecture: 42.15%
Model-View-Controller (MVC): 37.48%
Microservices: 11.62%
Arquitetura mais provável: Layered Architecture (confiança: 42.15%)</code>

<h2>Resultados Consolidados</h2>

<p>Para consolidar a avaliação, foram analisadas duas fontes de evidência textual do
projeto:</p>

<ol>
  <li>O arquivo README.md, representando a documentação principal;</li>
  <li>As mensagens de commits, representando o histórico de desenvolvimento.</li>
<ol>

<p>As Tabelas 3.1 e 3.2 apresentam, respectivamente, as probabilidades associadas a cada
padrão arquitetural identificado pelos três modelos testados.</p>

<img width="612" height="515" alt="image" src="https://github.com/user-attachments/assets/6f653a08-e0b3-461e-bf02-76eb5b4e639a" />

<img width="617" height="521" alt="image" src="https://github.com/user-attachments/assets/20347adb-4ab8-4951-b1cd-31bb5a9899d7" />



<h1>Documentação do Script de Inferência QA sobre Commits</h1>

<h2>Visão Geral</h2>
<p>
    Este script utiliza modelos de Question Answering (QA) da biblioteca <strong>Transformers</strong>
    da Hugging Face para identificar, a partir do histórico de commits de um repositório,
    indícios de refatoração arquitetural. O método aplica perguntas predefinidas a mensagens
    de commits filtradas por termos relacionados a arquitetura e padrões de projeto, buscando
    inferir qual estilo arquitetural foi implementado.
</p>

<h2>Objetivo do Script</h2>
<p>
    O objetivo é determinar, com base no conteúdo textual dos commits, o tipo de arquitetura 
    ou padrão de projeto predominante após refatorações. Para isso, o código compara
    o desempenho de três modelos de QA distintos, avaliando suas respostas e níveis de confiança
    para selecionar a inferência mais coerente.
</p>

<h2>Estrutura e Dependências</h2>
<p>O script foi implementado em Python e depende das seguintes bibliotecas:</p>
<ul>
    <li><strong>transformers</strong>: para acesso ao pipeline de QA;</li>
    <li><strong>os</strong>: para manipulação de diretórios;</li>
    <li><strong>git</strong>: utilizado externamente para filtrar commits relevantes.</li>
</ul>

<p>Os modelos utilizados são:</p>
<ul>
    <li>google-bert/bert-large-cased-whole-word-masking-finetuned-squad</li>
    <li>deepset/roberta-large-squad2</li>
    <li>distilbert-base-cased-distilled-squad</li>
</ul>

<h2>Fluxo de Execução</h2>
<p>
    O script executa inicialmente um comando <code>git log</code> filtrando mensagens contendo termos:
</p>

<pre><code>architecture | pattern | registry | factory | refactor | design</code></pre>

<p>
    Os commits são armazenados em arquivo de texto. Em seguida, o pipeline de QA é aplicado
    ao contexto para responder perguntas otimizadas e extrair inferências sobre arquitetura.
    A resposta de maior confiança é selecionada para cada modelo.
</p>

<h2>Termos de Busca</h2>
<p>Utilizados para filtrar commits:</p>
<pre><code>architecture | pattern | registry | factory | refactor | design</code></pre>

<h2>Saída Esperada</h2>
<p>
    A saída consiste em múltiplas inferências (uma por pergunta) e, ao final,
    a resposta com maior confiança. Cada modelo gera seus próprios resultados.
</p>

<h2>Resultados Consolidados</h2>

<table border="1" cellpadding="6">
    <thead>
        <tr>
            <th>Modelo</th>
            <th>Pergunta com Maior Score</th>
            <th>Confiança</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>deepset/roberta-large-squad2</td>
            <td>Into what architecture was the codebase refactored?</td>
            <td>clean layered — 1.0264</td>
        </tr>
        <tr>
            <td>google-bert/bert-large-cased</td>
            <td>What software architecture did the codebase adopt after refactoring?</td>
            <td>clean layered architecture — 1.0435</td>
        </tr>
        <tr>
            <td>distilbert-base-cased-distilled-squad</td>
            <td>What software architecture did the codebase adopt after refactoring?</td>
            <td>clean layered architecture — 0.5736</td>
        </tr>
    </tbody>
</table>

<h2>Análise e Conclusão</h2>
<p>
    Os resultados indicam forte tendência de identificação da <strong>Clean Layered Architecture</strong>,
    especialmente nos modelos BERT e RoBERTa.  
    O modelo com melhor desempenho foi:
</p>
<p><strong>google-bert/bert-large-cased-whole-word-masking-finetuned-squad</strong>, com maior escore de confiança.</p>

<hr>


<h1>Documentação do Script de Inferência QA sobre README</h1>

<h2>Visão Geral</h2>
<p>
    Este script identifica padrões arquiteturais no arquivo <strong>README.md</strong> do repositório
    LangExtract utilizando modelos de Question Answering (QA). A estratégia consiste em aplicar
    perguntas semânticas sobre arquitetura ao conteúdo textual do README.
</p>

<h2>Objetivo do Script</h2>
<p>
    O objetivo é inferir automaticamente o estilo arquitetural descrito na documentação,
    como Layered, Plugin-based, Client-Server, Modular etc. O modelo gera respostas com escores de confiança.
</p>

<h2>Estrutura e Dependências</h2>
<ul>
    <li><strong>transformers</strong> — carregamento e inferência QA</li>
    <li><strong>os</strong> — manipulação de arquivos</li>
    <li><strong>git</strong> — para clonar o repositório, se necessário</li>
</ul>

<h2>Fluxo de Execução</h2>

<ol>
    <li>Modelos utilizados:
        <ul>
            <li>distilbert-base-cased-distilled-squad</li>
            <li>deepset/roberta-large-squad2</li>
            <li>google-bert/bert-large-cased-whole-word-masking-finetuned-squad</li>
        </ul>
    </li>
    <li>Carregamento do modelo com pipeline QA.
      <code>
        model_name = "distilbert-base-cased-distilled-squad"
        pipe = pipeline("question-answering", model=model_name)
      </code>
    </li>
    <li>Clonagem (ou verificação) do repositório LangExtract.
      <code>repo_url = "https://github.com/google/langextract.git"
        repo_dir = "langextract"</code>
    </li>
    <li>Leitura do arquivo README.md.
      <code>
        if not os.path.exists(repo_dir):
          print(" Clonando repositório LangExtract ...")
          Repo.clone_from(repo_url, repo_dir)
        else:
          print(" Repositório já disponível localmente.")
          readme_path = os.path.join(repo_dir, "README.md")
        if not os.path.exists(readme_path):
          raise FileNotFoundError(" README.md não encontrado.")
        with open(readme_path, "r", encoding="utf-8") as f:
          readme_text = f.read()
        print(f" README carregado ({len(readme_text)} caracteres)")
      </code>
    </li>
    <li>Definição de perguntas otimizadas sobre arquitetura.
      <code>
        questions = [
          "What software architecture does the project use?",
          "Which architectural pattern best describes the LangExtract system?",
          "Is this project modular, plugin-based, or monolithic?",
          "What architecture or design style does LangExtract follow?",
          "How is the system organized architecturally?",
          "What architectural approach or framework is implemented?",
          "What type of software architecture is described in the documentation?"
          ]
      </code>
    </li>
    <li>Execução da inferência para cada pergunta, armazenando respostas e escores.
      <code>melhor = {"question": None, "answer": None, "score": 0.0}
            contexto_total = contexto_extra + "\n" + contexto_relevante
            print(" Iniciando análise...")
            for q in questions:
              result = pipe(question=q, context=contexto_total)
              print(f"\n Pergunta: {q}")
              print(f"→ Resposta: {result[’answer’]}")
              print(f"→ Confiança: {result[’score’]:.4f}")
              if result["score"] > melhor["score"]:
                melhor = {"question": q, "answer": result["answer"], "score": result[’score’]} </code>
    </li>
    <li>Seleção automática da resposta com maior confiança.
      <code>
          print("\n === MELHOR RESULTADO ===")
          print(f"Pergunta: {melhor[’question’]}")
          print(f"Resposta: {melhor[’answer’]}")
          print(f"Confiança: {melhor[’score’]:.4f}")
      </code>
    </li>
</ol>

<h2>Termos de Busca</h2>
<p>
    O modelo analisa expressões como: architecture, modular, plugin, service, pattern, refactor.
</p>

<h2>Saída Esperada</h2>
<p>
    O script exibe todas as respostas e escores e, ao final, seleciona a arquitetura mais provável.
</p>

<h2>Resultados Consolidados</h2>

<table border="1" cellpadding="6">
    <thead>
        <tr>
            <th>Modelo</th>
            <th>Pergunta com Maior Score</th>
            <th>Confiança</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>deepset/roberta-large-squad2</td>
            <td>Into what architecture was the codebase refactored?</td>
            <td>Client-Server — 0.0654</td>
        </tr>
        <tr>
            <td>google-bert/bert-large-cased</td>
            <td>What architecture or design style does LangExtract follow?</td>
            <td>Software architecture — 0.6738</td>
        </tr>
        <tr>
            <td>distilbert-base-cased-distilled-squad</td>
            <td>What architecture or design style does LangExtract follow?</td>
            <td>custom model - 0.6982</td>
        </tr>
    </tbody>
</table>
