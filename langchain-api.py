import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import DeepLake
from langchain.document_loaders import GitLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": "*"}})



load_dotenv()

class RepoDatasetPreprocessor:
    def __init__(self, clone_url, repo_path, branch, username):
        self.clone_url = clone_url
        self.repo_path = repo_path
        self.branch = branch    
        self.username = username
        self.embeddings = OpenAIEmbeddings(disallowed_special=())
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

        self.dataset_name = self.generate_dataset_name()
        self.db = DeepLake(dataset_path=f"hub://{self.username}/{self.dataset_name}", embedding_function=self.embeddings)  # dataset would be publicly available

    def generate_dataset_name(self):
        parsed_url = urlparse(self.clone_url)
        repo_owner, repo_name = parsed_url.path.strip('/').split('/')
        dataset_name = f"{repo_owner}-{repo_name}"
        return dataset_name

    def load_documents(self):
        docs = []
        loader = GitLoader(clone_url=self.clone_url, repo_path=self.repo_path, branch=self.branch)
        repo_data = loader.load()
        for dirpath, dirnames, filenames in os.walk(self.repo_path):
            for file in filenames:
                try:
                    text_loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                    docs.extend(text_loader.load_and_split())
                except Exception as e:
                    pass
        return docs

    def split_documents(self, docs):
        return self.text_splitter.split_documents(docs)

    def add_documents(self, docs):
        self.db.add_documents(docs)

    def process_documents(self):
        docs = self.load_documents()
        texts = self.split_documents(docs)
        self.add_documents(texts)

class DeepLakeRetriever:
    def __init__(self, dataset_path, embedding_function):
        self.dataset_path = dataset_path
        self.embedding_function = embedding_function
        self.retriever = None

    def setup_retriever(self):
        db = DeepLake(dataset_path=self.dataset_path, read_only=True, embedding_function=self.embedding_function)
        self.retriever = db.as_retriever()
        self.retriever.search_kwargs['distance_metric'] = 'cos'
        self.retriever.search_kwargs['fetch_k'] = 100
        self.retriever.search_kwargs['maximal_marginal_relevance'] = True
        self.retriever.search_kwargs['k'] = 10

    def get_retriever(self):
        if not self.retriever:
            self.setup_retriever()
        return self.retriever
    
class ConversationalRetrievalChainManager:
    def __init__(self, retriever, model_name):
        self.retriever = retriever
        self.model_name = model_name
        self.chat_model = None
        self.conversational_chain = None
        self.chat_history = []

    def setup_chain(self):
        self.chat_model = ChatOpenAI(model_name=self.model_name)
        self.conversational_chain = ConversationalRetrievalChain.from_llm(self.chat_model, retriever=self.retriever)

    def ask_questions(self, questions):
        if not self.conversational_chain:
            self.setup_chain()
        for question in questions:  
            result = self.conversational_chain({"question": question, "chat_history": self.chat_history})
            self.chat_history.append((question, result['answer']))
            print(f"-> **Question**: {question} \n")
            print(f"**Answer**: {result['answer']} \n")



# Initialize the manager and retriever
preprocessor = RepoDatasetPreprocessor(
    clone_url="https://github.com/hwchase17/langchain",
    repo_path="./example_data/test_repo2/",
    branch="master",
    username='dirkjbreeuwer'
)
#preprocessor.process_documents()

embeddings = OpenAIEmbeddings(disallowed_special=())
dataset_path = f"hub://{preprocessor.username}/{preprocessor.dataset_name}"
retriever = DeepLakeRetriever(dataset_path=dataset_path, embedding_function=embeddings).get_retriever()
manager = ConversationalRetrievalChainManager(retriever, model_name='gpt-4')

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    if question:
        app.logger.info(f"Received question: {question}")
        if not manager.conversational_chain:
            manager.setup_chain()
        result = manager.conversational_chain({"question": question, "chat_history": manager.chat_history})
        manager.chat_history.append((question, result['answer']))
        return jsonify({"question": question, "answer": result['answer']})
    else:
        return jsonify({"error": "Please provide a question."})

if __name__ == "__main__":
    app.run()
