from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2:3b")

template = """
Tu es un expert qui sait répondre à des questions à propos de la Normandie

Voici quelques éléments importants : {extraits}

Voici la question à laquelle répondre : {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True :
    question = input("Poser votre question (q pour quitter):")
    if question == "q" :
        break
    
    resultat = chain.invoke({"extraits":[],"question":"Quel est le plus grand monument de Rouen?"})
    print(resultat)