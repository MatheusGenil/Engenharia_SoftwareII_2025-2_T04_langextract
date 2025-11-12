from transformers import pipeline
import requests
import re

class HuggingFaceWrapper:
    def __init__(self, model_name: str):
        self.pipeline = pipeline("zero-shot-classification", model=model_name)
    
    def classify_text(self, text: str, candidate_labels: list[str]):
        return self.pipeline(text, candidate_labels=candidate_labels)

# ✅ URL do README em formato raw
url = "https://raw.githubusercontent.com/google/langextract/main/README.md"
readme_text = requests.get(url).text

# 🔎 Termos de busca (equivalentes ao seu --grep)
termos_busca = [
    "architecture", "architectural", "pattern", "design",
    "provider", "plugin", "module", "interface", "layer", "service"
]

# 🧹 Filtragem: seleciona linhas que contêm qualquer termo de busca
padrao = re.compile("|".join(termos_busca), flags=re.IGNORECASE)
linhas_relevantes = [linha for linha in readme_text.splitlines() if padrao.search(linha)]

# 🔧 Concatena trechos relevantes para análise
texto_filtrado = "\n".join(linhas_relevantes)

if not texto_filtrado.strip():
    print("⚠️ Nenhuma linha relevante encontrada no README.")
else:
    print(f"✅ {len(linhas_relevantes)} linhas relevantes extraídas do README.\n")

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

# ✅ Modelo compatível
model_name = "facebook/bart-large-mnli"
hf = HuggingFaceWrapper(model_name)

# 🔎 Classificação baseada no texto filtrado
result = hf.classify_text(texto_filtrado or readme_text, candidate_labels)

print("\n============== " + model_name + " ==============")
print("\n🏗️  Resultado da inferência de arquitetura:")
for label, score in zip(result["labels"], result["scores"]):
    print(f"{label}: {score:.2%}")

print(f"\n➡️  Arquitetura mais provável: {result['labels'][0]} (confiança: {result['scores'][0]:.2%})")
