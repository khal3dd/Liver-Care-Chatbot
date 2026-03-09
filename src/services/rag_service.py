"""
RAG (Retrieval-Augmented Generation) Service

Handles:
- PDF text extraction
- Text chunking with overlap
- Embedding generation
- Vector database management with ChromaDB
- Semantic search and retrieval
"""

from typing import List, Tuple
from pathlib import Path

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

from src.config.settings import settings


class RecursiveCharacterTextSplitter:
    """
    Manual implementation of recursive character text splitter.
    Splits text by separators in order: ["\n\n", "\n", ".", " "]
    Respects chunk_size and chunk_overlap.
    """

    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ".", " "]

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks respecting size and overlap."""
        chunks = []
        separator = self.separators[-1]  # Default to space

        # Try each separator in order
        for _s in self.separators:
            if _s in text:
                separator = _s
                break

        # Split by the chosen separator
        if separator:
            splits = text.split(separator)
        else:
            splits = list(text)

        # Merge splits to respect chunk_size
        good_splits = []
        for s in splits:
            if len(s) < self.chunk_size:
                good_splits.append(s)
            else:
                # Recursively split if a split is too long
                if good_splits:
                    merged = self._merge_splits(good_splits, separator)
                    chunks.extend(merged)
                    good_splits = []

                other_info = self.split_text(s)
                chunks.extend(other_info)

        if good_splits:
            merged = self._merge_splits(good_splits, separator)
            chunks.extend(merged)

        return [chunk.strip() for chunk in chunks if chunk.strip()]

    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        """Merge splits into chunks respecting size and overlap."""
        separator_len = len(separator)
        chunks = []
        current_chunk = []
        current_len = 0

        for split in splits:
            split_len = len(split)
            if current_len + split_len + separator_len <= self.chunk_size:
                current_chunk.append(split)
                current_len += split_len + separator_len
            else:
                if current_chunk:
                    chunk_text = separator.join(current_chunk)
                    chunks.append(chunk_text)

                    # Start new chunk with overlap
                    overlap_chunk = []
                    overlap_len = 0
                    for i in range(len(current_chunk) - 1, -1, -1):
                        chunk_len = len(current_chunk[i])
                        if overlap_len + chunk_len <= self.chunk_overlap:
                            overlap_chunk.insert(0, current_chunk[i])
                            overlap_len += chunk_len + separator_len
                        else:
                            break

                    current_chunk = overlap_chunk + [split]
                    current_len = overlap_len + split_len + separator_len
                else:
                    current_chunk = [split]
                    current_len = split_len

        if current_chunk:
            chunk_text = separator.join(current_chunk)
            chunks.append(chunk_text)

        return chunks


class RAGService:
    """
    Manages the complete RAG pipeline:
    - PDF extraction
    - Text chunking
    - Embeddings
    - Vector storage
    - Semantic search
    """

    def __init__(self):
        """Initialize RAG service with lazy loading of expensive components."""
        self._embedding_model = None
        self._splitter = None
        self._chroma_client = None
        self._collection = None

    def _init_embeddings(self):
        """Lazy initialize embedding model."""
        if self._embedding_model is None:
            self._embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def _init_database(self):
        """Lazy initialize ChromaDB and collection."""
        if self._chroma_client is None:
            chroma_path = Path(settings.CHROMA_DB_PATH)
            chroma_path.mkdir(parents=True, exist_ok=True)
            self._chroma_client = chromadb.PersistentClient(path=str(chroma_path))
            self._collection = self._chroma_client.get_or_create_collection(
                name="liver_docs",
                metadata={"hnsw:space": "cosine"},
            )

    def _init_splitter(self):
        """Initialize text splitter."""
        if self._splitter is None:
            self._splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
            )

    @property
    def embedding_model(self):
        """Get embedding model, initialize if needed."""
        self._init_embeddings()
        return self._embedding_model

    @property
    def splitter(self):
        """Get text splitter, initialize if needed."""
        self._init_splitter()
        return self._splitter

    @property
    def collection(self):
        """Get ChromaDB collection, initialize if needed."""
        self._init_database()
        return self._collection


    # ──────────────────────────────────────────────
    # PDF Text Extraction
    # ──────────────────────────────────────────────

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text with cleaned whitespace
        """
        try:
            with open(pdf_path, "rb") as f:
                pdf_reader = PdfReader(f)
                text = ""

                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # Clean extra whitespace
            text = self._clean_text(text)
            return text

        except Exception as e:
            raise ValueError(f"Error extracting PDF text: {str(e)}")

    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove extra whitespace while preserving structure."""
        # Replace multiple newlines with double newline
        text = "\n\n".join(
            para.strip() for para in text.split("\n\n") if para.strip()
        )
        # Replace multiple spaces with single space
        text = " ".join(text.split())
        return text

    # ──────────────────────────────────────────────
    # Text Chunking
    # ──────────────────────────────────────────────

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks using recursive character splitter.

        Args:
            text: Raw text to chunk

        Returns:
            List of chunks respecting size and overlap
        """
        return self.splitter.split_text(text)

    # ──────────────────────────────────────────────
    # Embeddings
    # ──────────────────────────────────────────────

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        embeddings = self.embedding_model.encode(texts, convert_to_list=True)
        return embeddings

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string

        Returns:
            Embedding vector
        """
        return self.embedding_model.encode(text, convert_to_list=True)

    # ──────────────────────────────────────────────
    # Vector Database Management
    # ──────────────────────────────────────────────

    def add_documents(self, chunks: List[str], filename: str) -> None:
        """
        Add document chunks to the vector database.
        If document already exists, delete old chunks first.

        Args:
            chunks: List of text chunks
            filename: Source filename for reference
        """
        if not chunks:
            return

        # Delete existing chunks for this filename
        self.delete_document(filename)

        # Generate embeddings
        embeddings = self.get_embeddings(chunks)

        # Prepare metadata and IDs
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        metadatas = [{"filename": filename, "chunk_index": i} for i in range(len(chunks))]

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )

    def delete_document(self, filename: str) -> None:
        """
        Delete all chunks belonging to a document.

        Args:
            filename: Document filename to delete
        """
        # Get all documents with this filename
        results = self.collection.get(
            where={"filename": filename}
        )

        if results["ids"]:
            self.collection.delete(ids=results["ids"])

    # ──────────────────────────────────────────────
    # Search and Retrieval
    # ──────────────────────────────────────────────

    def search(self, query: str, top_k: int = None) -> List[Tuple[str, float]]:
        """
        Search for similar chunks in the vector database.

        Args:
            query: Search query
            top_k: Number of results to return (uses TOP_K_RESULTS if None)

        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        top_k = top_k or settings.TOP_K_RESULTS

        # Get collection count
        if self.collection.count() == 0:
            return []

        # Convert query to embedding
        query_embedding = self.get_embedding(query)

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        # Format results
        retrieved = []
        if results["documents"] and results["documents"][0]:
            for doc, distance in zip(results["documents"][0], results["distances"][0]):
                # Convert distance to similarity (cosine distance to similarity)
                similarity = 1 - distance
                retrieved.append((doc, similarity))

        return retrieved

    # ──────────────────────────────────────────────
    # Context Building
    # ──────────────────────────────────────────────

    def build_context(self, query: str, top_k: int = None) -> str:
        """
        Retrieve relevant chunks and format them as context.

        Args:
            query: User query
            top_k: Number of chunks to retrieve

        Returns:
            Formatted context string ready for LLM injection
        """
        results = self.search(query, top_k)

        if not results:
            return ""

        context = "## Retrieved Context\n\n"
        for i, (chunk, score) in enumerate(results, 1):
            context += f"### Reference {i} (Confidence: {score:.2%})\n"
            context += f"{chunk}\n\n"

        return context

    # ──────────────────────────────────────────────
    # Utilities
    # ──────────────────────────────────────────────

    def process_pdf(self, pdf_path: str) -> None:
        """
        Complete pipeline: extract → chunk → embed → store.

        Args:
            pdf_path: Path to PDF file
        """
        # Extract text
        text = self.extract_text_from_pdf(pdf_path)

        # Chunk text
        chunks = self.chunk_text(text)

        # Add to database
        filename = Path(pdf_path).name
        self.add_documents(chunks, filename)

    def get_collection_stats(self) -> dict:
        """Get statistics about the vector database."""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": "liver_docs",
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
            "top_k": settings.TOP_K_RESULTS,
        }


# Singleton instance
rag_service = RAGService()
