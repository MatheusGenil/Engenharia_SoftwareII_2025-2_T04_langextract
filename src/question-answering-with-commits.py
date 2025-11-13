!pip install -U Transformers
from transformers import pipeline
import os

pipe = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

!rm -rf langextract
!git clone https://github.com/google/langextract.git
#Entrando na pasta
os.chdir('langextract')
termos_busca = "architecture|pattern|registry|factory|refactor|design"
!git log --all -i -E --grep="{termos_busca}" --pretty=format:"%s" > ../commits_filtrados.txt
os.chdir('..')

with open("commits_filtrados.txt", "r", encoding="utf-8") as f:
        context_filtrado = f.read()


# 🔹 Perguntas otimizadas
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

# 🔹 Avalia todas e seleciona a mais confiável
melhor = {"question": None, "answer": None, "score": 0}

for q in questions:
    result = pipe(question=q, context=context_filtrado)
    print(f"\nPergunta: {q}")
    print(f"→ Resposta: {result['answer']}")
    print(f"→ Confiança: {result['score']:.4f}")

    if result["score"] > melhor["score"]:
        melhor = {"question": q, "answer": result["answer"], "score": result["score"]}

# 🔹 Resultado final
print("\n=== MELHOR RESULTADO ===")
print(f"Pergunta: {melhor['question']}")
print(f"Resposta: {melhor['answer']}")
print(f"Confiança: {melhor['score']:.4f}")

