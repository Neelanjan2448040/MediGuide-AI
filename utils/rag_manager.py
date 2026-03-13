import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from config.config import DATA_DIR

class RAGManager:
    def __init__(self):
        self.retriever = None
        self.chunks = []
        self._initialize_from_folder()

    def _initialize_from_folder(self):
        """Load any existing documents on startup."""
        if os.path.exists(DATA_DIR):
            files = [f for f in os.listdir(DATA_DIR) if f.endswith(('.pdf', '.txt'))]
            for file in files:
                self.process_document(os.path.join(DATA_DIR, file))

    def process_document(self, file_path, llm=None):
        try:
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith('.txt'):
                loader = TextLoader(file_path)
            else:
                return 0, {}

            documents = loader.load()
            if not documents:
                return 0, {}

            full_text = " ".join([doc.page_content for doc in documents])
            
            # Smart Document Analyzer (Summary)
            metadata = {"summary": "Summary not available", "topics": []}
            if llm:
                try:
                    summary_prompt = f"Summarize this medical document in 3 sentences and list 5 key medical terms found: \n\n{full_text[:3000]}"
                    response = llm.invoke(summary_prompt).content
                    metadata["summary"] = response
                except: pass

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            new_chunks = text_splitter.split_documents(documents)
            
            self.chunks.extend(new_chunks)
            
            # Re-initialize the BM25 retriever with all chunks
            if self.chunks:
                self.retriever = BM25Retriever.from_documents(self.chunks)
                
            return len(new_chunks), metadata
        except Exception as e:
            print(f"Error processing document {file_path}: {e}")
            return 0, {"summary": f"Could not process file: {os.path.basename(file_path)}"}

    def retrieve_context(self, query, k=3):
        if not self.retriever:
            return []
        
        try:
            docs = self.retriever.get_relevant_documents(query)
            return [doc.page_content for doc in docs[:k]]
        except Exception as e:
            print(f"Error in BM25 retrieval: {e}")
            return []

    def get_stats(self):
        return {"total_chunks": len(self.chunks)}
