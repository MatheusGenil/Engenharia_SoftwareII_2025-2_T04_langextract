from transformers import pipeline
import requests

class HuggingFaceWrapper:
    def __init__(self, model_name: str):
        self.pipeline = pipeline("zero-shot-classification", model=model_name)
    
    def classify_text(self, text: str, candidate_labels: list[str]):
        return self.pipeline(text, candidate_labels=candidate_labels)

# URL do README do projeto langextract
url = "https://github.com/google/langextract/blob/main/README.md"
readme_text = requests.get(url).text

# Candidatas de arquitetura
candidate_labels = ["MVC", "Layered", "Microservices", "Event Driven", "Pipe and Filter", "Factory", "Provider"]

# Modelo compatível com o pipeline zero-shot-classification
model_name = "MoritzLaurer/deberta-v3-large-zeroshot-v1"
hf = HuggingFaceWrapper(model_name)

result = hf.classify_text(readme_text, candidate_labels)

print("\n============== " + model_name + " ==============")
print("\n🏗️  Resultado da inferência de arquitetura:")
for label, score in zip(result["labels"], result["scores"]):
    print(f"{label}: {score:.2%}")

print(f"\n➡️  Arquitetura mais provável: {result['labels'][0]} (confiança: {result['scores'][0]:.2%})")
