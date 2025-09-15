from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vecteur import retriever

model = OllamaLLM(model="llama3.2:1b")

template = """
Tu es un guide touristique à Paris.

Utilise ces informations pour répondre à la question : {extraits}

Voici la question à laquelle répondre : {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True :
    question = input("Poser votre question (q pour quitter):")
    if question == "q" :
        break
    
    extraits = retriever.invoke(question)
    resultat = chain.invoke({"extraits":extraits,"question": question})
    print(resultat)