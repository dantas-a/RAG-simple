from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil

DATA_PATH = './data/'
DB_PATH = './chroma_db/'    

# Chargement des documents
def load_documents():
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

# Découpage des documents en morceaux
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

# Récupération de la fonction d'embedding qui va nous permettre d'encoder chaque morceau pour savoir de quoi le morceau "traite"
def get_embedding_function():
    return OllamaEmbeddings(model="bge-m3")

# Ajout de documents dans la base de données chroma (base de données vectorielle)
def add_to_chroma(chunks: list[Document]):
    # Récupère la base de données existante
    db = Chroma(
        persist_directory=DB_PATH, embedding_function=get_embedding_function()
    )

    # Calcule les id de chaque morceau
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Ajoute ou mets à jour les documents dans la base de données
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Nombre de documents existants dans la base de données: {len(existing_ids)}")

    # Identifie les nouveaux documents
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    # Ajoute les nouveaux documents
    if len(new_chunks):
        print(f"👉 Ajout de nouveaux documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ Pas de documents ajoutés")

def calculate_chunk_ids(chunks):

    # Création d'indice de la forme "répertoire/fichier:numero_page:numero_morceau"

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # Si on est toujours sur la même page alors +1
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Construction de l'id du morceau
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Ajout au méta-données
        chunk.metadata["id"] = chunk_id

    return chunks

# Nettoyer la base de données
def clear_database():
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

# Création de la base de données
def create_base(reset=False):
    if reset :
        print("✨ Nettoyage de la base de données")
        clear_database()

    # Création ou mise à jour des données
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)  
    
create_base(True)

# Permet de récupérer les documents les plus pertinents pour répondre aux questions
retriever = Chroma(persist_directory=DB_PATH,embedding_function = get_embedding_function()).as_retriever(search_kwargs={"k": 5})