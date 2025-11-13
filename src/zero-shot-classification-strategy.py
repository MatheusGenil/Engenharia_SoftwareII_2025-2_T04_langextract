import os
import subprocess
from sympy.strategies.core import switch
from transformers import pipeline
import requests
import re

class HuggingFaceWrapper:
    def __init__(self, model_name: str):
        self.pipeline = pipeline("zero-shot-classification", model=model_name)

    def classify_text(self, text: str, candidate_labels: list[str]):
        return self.pipeline(text, candidate_labels=candidate_labels)

# 🔎 Termos de busca (equivalentes ao seu --grep)
termos_busca = [
    "architecture", "architectural", "pattern", "design",
    "provider", "plugin", "module", "interface", "layer", "service"
]

# 🧠 Candidatas de arquitetura
candidate_labels = [
    "Monolithic",
    "Microservices",
    "Serverless",
    "Event Driven",
    "Layered",
    "Hexagonal",
    "Clean Architecture",
    "Service Oriented Architecture",
    "Client Server",
    "MVC",
    "Singleton",
    "Factory Method",
    "Observer",
    "Strategy",
    "Adapter",
    "Facade",
    "Decorator",
    "Repository",
    "Command",
    "Dependency Injection",
    "Modular",
    "Pipe and Filter",
    "Provider-based Architecture",
    "Plugin-based Architecture"
]

model_name = ""
estrategia = 0
# discionário de estratégias de análise
estrategias = {
    1 : 'README.md',
    2 : 'Commits' 
}

# Gera automaticamente o menu de seleção
print("\nDIGITE A ESTRATÉGIA DE ANÁLISE:")
for chave, valor in estrategias.items():
    print(f"[{chave}] {valor}")

# Seleção do tipo de análise
while True:
    try:
        estrategia = int(input("\nSua opção: "))

        if estrategia == 1 or estrategia == 2 :
            print(f"\n✅ Estratégia selecionada: {estrategias[estrategia]}")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")
    except ValueError:
        print("❌ Entrada inválida. Digite apenas números.")

# Dicionário de modelos
modelos = {
    1: 'joeddav/xlm-roberta-large-xnli',
    2: 'facebook/bart-large-mnli',
    3: 'MoritzLaurer/mDeBERTa-v3-base-mnli-xnli'
}

# Gera automaticamente o menu de seleção
print("\nDIGITE O MODELO DESEJADO:")
for chave, valor in modelos.items():
    print(f"[{chave}] {valor}")

selecao = 0

# Recebe e valida a escolha do usuário
while True:
    try:
        selecao = int(input("\nSua opção: "))
        if selecao in modelos:
            model_name = modelos[selecao]
            print(f"\n✅ Modelo selecionado: {model_name}")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.")
    except ValueError:
        print("❌ Entrada inválida. Digite apenas números.")


hf = HuggingFaceWrapper(model_name)

# README
if estrategia == 1:
    # URL do README em formato raw
    url = "https://raw.githubusercontent.com/google/langextract/main/README.md"
    readme_text = requests.get(url).text

    # 🧹 Filtragem: seleciona linhas que contêm qualquer termo de busca
    padrao = re.compile("|".join(termos_busca), flags=re.IGNORECASE)
    linhas_relevantes = [linha for linha in readme_text.splitlines() if padrao.search(linha)]

    # 🔧 Concatena trechos relevantes para análise
    texto_filtrado = "\n".join(linhas_relevantes)

    if not texto_filtrado.strip():
        print("⚠ Nenhuma linha relevante encontrada no README.")
    else:
        print(f"✅ {len(linhas_relevantes)} linhas relevantes extraídas do README.\n")  

    # 🔎 Classificação baseada no texto filtrado
    result = hf.classify_text(texto_filtrado or readme_text, candidate_labels)

else:
    # Repositório alvo
    repo_url = "https://github.com/google/langextract.git"

    # Pasta temporária onde o repositório será clonado
    repo_dir = "repo_temp"

    # ======================================================
    # CLONAGEM DO REPOSITÓRIO
    # ======================================================
    if not os.path.exists(repo_dir):
        print(f"📥 Clonando repositório {repo_url} ...")
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
    else:
        print(f"✅ Repositório já clonado em {repo_dir}")

    # ======================================================
    # EXTRAÇÃO DOS COMMITS RELEVANTES
    # ======================================================

    padrao_grep = "|".join(termos_busca)

    # Executa comando git log e filtra mensagens de commit
    print("🔎 Coletando commits relevantes ...")

    result = subprocess.run(
        ["git", "-C", repo_dir, "log", "--all", "-i", "-E", f"--grep={padrao_grep}", "--pretty=format:%s"],
        capture_output=True,
        text=True
    )

    commits_filtrados = result.stdout.strip()

    if not commits_filtrados:
        print("⚠️ Nenhum commit relevante encontrado.")
    else:
        linhas_relevantes = commits_filtrados.splitlines()
        print(f"✅ {len(linhas_relevantes)} mensagens de commit relevantes extraídas.\n")

    # ======================================================
    # PREPARAÇÃO DO TEXTO PARA ANÁLISE
    # ======================================================
    texto_filtrado = "\n".join(linhas_relevantes) if commits_filtrados else ""

    if not texto_filtrado.strip():
        print("⚠️ Nenhum texto relevante encontrado nos commits.")
    else:
        print("🧠 Analisando mensagens de commit com modelo zero-shot ...")

    texto_para_analisar = texto_filtrado or "No commit data found."
    result = hf.classify_text(texto_para_analisar, candidate_labels)

# ======================================================
# RESULTADOS
# ======================================================
print("\n============== " + model_name + " ==============")
print("\n🏗️  Resultado da inferência de arquitetura:")
for label, score in zip(result["labels"], result["scores"]):
    print(f"{label}: {score:.2%}")

print(f"\n➡️  Arquitetura mais provável: {result['labels'][0]} (confiança: {result['scores'][0]:.2%})")