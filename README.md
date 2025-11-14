# Engenharia_SoftwareII_2025-2_T04_langextract

Este repositório contém os experimentos, scripts e documentação produzidos para a atividade de análise de padrões arquiteturais utilizando modelos de linguagem pré-treinados. O objetivo central do trabalho é investigar como modelos baseados em Transformers, originalmente desenvolvidos para Processamento de Linguagem Natural (PLN), podem ser aplicados à interpretação de artefatos de software, como mensagens de commit e documentação técnica.

A análise foi conduzida utilizando técnicas de Zero-Shot Classification e Question Answering, aplicadas a textos reais extraídos do repositório público LangExtract, da Google. O foco foi verificar a capacidade desses modelos em identificar padrões arquiteturais presentes no projeto, tais como Layered Architecture, Clean Architecture, Repository Pattern e Service-Oriented Architecture, mesmo sem nenhum treinamento supervisionado específico para essa tarefa.

Tutorial em PDF: https://github.com/MatheusGenil/Engenharia_SoftwareII_2025-2_T04_langextract/blob/01e6da0d09d93cf5f88d8c8ffe3e196260fe29bc/tutorial.pdf

Link do video: 

<h2>Documentação do Script de Classificação Zero-Shot com Hugging Face</h2>

<h3>3.1.1 Visão Geral</h3>
<p>O código em análise implementa um script em Python para a identificação de padrões
arquiteturais em projetos de software hospedados no GitHub, utilizando classificação
zero-shot com modelos da biblioteca transformers da Hugging Face. O objetivo é
aplicar técnicas de Natural Language Processing (NLP) para inferir, a partir de diferentes
fontes de texto (como o arquivo README.md ou mensagens de commits), qual padrão
arquitetural o projeto aparenta seguir.</p>

<h3>3.1.2 Objetivo do Script</h3>

<p>O script permite que o usuário selecione:
• A estratégia de análise: leitura de README.md ou análise de mensagens de commit.
• O modelo de linguagem (LLM) utilizado na classificação.
A partir dessas escolhas, o sistema coleta textos relevantes (filtrando por termos de busca específicos relacionados à arquitetura) e os submete ao modelo zero-shot selecionado para inferir o padrão arquitetural mais provável.</p>

<h3>3.1.3 Estrutura e Dependências</h3>

<p>O script utiliza as seguintes bibliotecas:</p>
  <ul>
    <li>os, subprocess: interação com o sistema e execução de comandos Git.</li>
    <li>requests: para obter conteúdo remoto via HTTP.</li>
    <li>re: expressões regulares para filtragem de termos relevantes.</li>
    <li>transformers: provê a pipeline de classificação zero-shot.</li>
  </ul>

  
<h3>3.1.4 Descrição da Classe Principal</h3>
<p>Classe HuggingFaceWrapper
Encapsula o uso da pipeline de classificação da Hugging Face.</p>

<ul>
  <li>Método __init__: inicializa a pipeline zero-shot com o modelo indicado.</li>
  <li>Método classify_text: realiza a classificação de um texto, retornando rótulos (labels) e pontuações de confiança.</li>
</ul>


<h3>3.1.5 Fluxo de Execução</h3>
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
  
<h3>3.1.6 Termos de Busca</h3>
<p>Os termos de filtragem textual utilizados são:</p>
<code>architecture, architectural, pattern, design, provider, plugin, module, interface, layer, service</code>
<p>Esses termos funcionam como um mecanismo de busca (grep) para localizar trechos potencialmente associados à definição ou implementação de padrões arquiteturais.</p>
  
<h3>3.1.7 Saída Esperada</h3>
<p>Ao executar corretamente (com as variáveis ajustadas), o script exibe no terminal algo
como:</p>
<code>============== facebook/bart-large-mnli ==============
Resultado da inferência de arquitetura:
Layered Architecture: 42.15%
Model-View-Controller (MVC): 37.48%
Microservices: 11.62%
Arquitetura mais provável: Layered Architecture (confiança: 42.15%)</code>
