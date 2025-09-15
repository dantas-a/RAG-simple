# RAG-simple

RAG-simple est un projet de démonstration d'un système de Retrieval-Augmented Generation (RAG) en Python. Il permet d'interroger des documents PDF locaux à l'aide d'une base de vecteurs (ChromaDB) et d'un LLM (Ollama). Les documents indexés sont en français et concernent Paris (guides touristiques, présentations, etc.). Les questions posées doivent également être en français et porter sur Paris.

## Fonctionnalités
- Indexation de documents PDF (guides, présentations, etc.)
- Recherche sémantique via ChromaDB
- Génération de réponses augmentées par récupération de contexte
- Facile à configurer et à utiliser

## Structure du projet
```
main.py                # Script principal pour lancer le RAG
vecteur.py             # Gestion des vecteurs et de la base ChromaDB
requirements.txt       # Dépendances Python
chroma_db/             # Dossier de la base de données ChromaDB
RAG_env/               # Environnement virtuel Python (recommandé)
data/                  # Dossier contenant les fichiers PDF à indexer
```

## Installation
1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/dantas-a/RAG-simple.git
   cd RAG-simple
   ```
2. **Créer un environnement virtuel**
   ```bash
   python3 -m venv RAG_env
   source RAG_env/bin/activate
   ```
3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation
1. Placez vos fichiers PDF (en français, traitant de Paris) dans le dossier `data/` (par exemple : guides touristiques parisiens, présentations sur Paris, etc.).
2. Assurez-vous qu'Ollama est lancé sur votre machine.
3. Lancez le script principal :
   ```bash
   python main.py
   ```
4. Suivez les instructions pour interroger vos documents en français, en posant des questions sur Paris ou son guide touristique.

## Dépendances principales
- Python 3.12+
- ChromaDB
- langchain
- langchain-chroma
- langchain-ollama

Toutes les dépendances sont listées dans `requirements.txt`.

Le projet utilise [Ollama](https://ollama.com/) pour l'inférence locale de modèles de langage. Assurez-vous qu'Ollama est installé et configuré sur votre machine.

## Auteurs
- Alexandre Dantas
