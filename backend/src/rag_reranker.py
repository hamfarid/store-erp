#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.40: RAG Reranker Optimization

Provides reranking capabilities for RAG search results to improve relevance.
Implements multiple reranking strategies:
- Cross-encoder reranking
- BM25 scoring
- Hybrid scoring (semantic + keyword)
- Diversity-aware reranking
"""

import os
import re
import math
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import Counter

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

RERANKER_MODEL = os.environ.get(
    "RAG_RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2"
)
RERANKER_TOP_K = int(os.environ.get("RAG_RERANKER_TOP_K", 10))
BM25_K1 = float(os.environ.get("BM25_K1", 1.5))
BM25_B = float(os.environ.get("BM25_B", 0.75))
DIVERSITY_LAMBDA = float(os.environ.get("DIVERSITY_LAMBDA", 0.5))


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class RankedDocument:
    """A document with ranking scores."""

    id: str
    text: str
    metadata: Dict[str, Any]
    original_score: float
    reranked_score: float
    final_score: float
    rank: int


# =============================================================================
# BM25 Scorer
# =============================================================================


class BM25Scorer:
    """
    P1.40: BM25 scoring for keyword-based relevance.

    BM25 (Best Matching 25) is a ranking function used by search engines
    to estimate the relevance of documents to a given search query.
    """

    def __init__(self, k1: float = BM25_K1, b: float = BM25_B):
        self.k1 = k1
        self.b = b
        self.avgdl = 0
        self.doc_freqs: Dict[str, int] = {}
        self.doc_lengths: List[int] = []
        self.corpus_size = 0

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        text = text.lower()
        # Remove punctuation and split
        tokens = re.findall(r"\b\w+\b", text)
        return tokens

    def fit(self, documents: List[str]) -> "BM25Scorer":
        """
        Fit BM25 scorer on a corpus of documents.

        Args:
            documents: List of document texts
        """
        self.corpus_size = len(documents)
        self.doc_lengths = []
        self.doc_freqs = Counter()

        total_length = 0
        for doc in documents:
            tokens = self._tokenize(doc)
            self.doc_lengths.append(len(tokens))
            total_length += len(tokens)

            # Count document frequencies (unique terms per doc)
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] += 1

        self.avgdl = total_length / self.corpus_size if self.corpus_size > 0 else 0
        return self

    def score(self, query: str, doc_text: str, doc_idx: int = 0) -> float:
        """
        Calculate BM25 score for a query-document pair.

        Args:
            query: Search query
            doc_text: Document text
            doc_idx: Document index for length lookup
        """
        query_tokens = self._tokenize(query)
        doc_tokens = self._tokenize(doc_text)
        doc_len = len(doc_tokens)

        if doc_idx < len(self.doc_lengths):
            doc_len = self.doc_lengths[doc_idx]

        score = 0.0
        doc_term_freqs = Counter(doc_tokens)

        for term in query_tokens:
            if term not in doc_term_freqs:
                continue

            # Term frequency in document
            tf = doc_term_freqs[term]

            # Document frequency
            df = self.doc_freqs.get(term, 0)

            # IDF calculation
            idf = math.log((self.corpus_size - df + 0.5) / (df + 0.5) + 1)

            # BM25 score component
            tf_component = (tf * (self.k1 + 1)) / (
                tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
            )

            score += idf * tf_component

        return score


# =============================================================================
# Cross-Encoder Reranker
# =============================================================================


class CrossEncoderReranker:
    """
    P1.40: Cross-encoder based reranking using transformer models.

    Cross-encoders process query and document together for more accurate
    relevance scoring than bi-encoders.
    """

    def __init__(self, model_name: str = RERANKER_MODEL):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        """Lazy load the cross-encoder model."""
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder

                self._model = CrossEncoder(self.model_name)
                logger.info(f"P1.40: Loaded cross-encoder model: {self.model_name}")
            except ImportError:
                logger.warning(
                    "P1.40: sentence-transformers not available, using fallback"
                )
                self._model = None
            except Exception as e:
                logger.error(f"P1.40: Failed to load cross-encoder: {e}")
                self._model = None
        return self._model

    def rerank(
        self, query: str, documents: List[Dict[str, Any]], top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using cross-encoder.

        Args:
            query: Search query
            documents: List of documents with 'text' field
            top_k: Number of top documents to return

        Returns:
            Reranked documents with scores
        """
        if not documents:
            return []

        top_k = top_k or RERANKER_TOP_K

        if self.model is None:
            # Fallback: return documents with original scores
            return documents[:top_k]

        # Prepare pairs for cross-encoder
        pairs = [(query, doc.get("text", "")) for doc in documents]

        try:
            # Get cross-encoder scores
            scores = self.model.predict(pairs)

            # Combine with original documents
            for i, doc in enumerate(documents):
                doc["rerank_score"] = float(scores[i])

            # Sort by rerank score
            reranked = sorted(
                documents, key=lambda x: x.get("rerank_score", 0), reverse=True
            )

            return reranked[:top_k]

        except Exception as e:
            logger.error(f"P1.40: Cross-encoder reranking failed: {e}")
            return documents[:top_k]


# =============================================================================
# Hybrid Reranker
# =============================================================================


class HybridReranker:
    """
    P1.40: Hybrid reranker combining semantic and keyword scores.

    Combines:
    - Semantic similarity (from initial retrieval)
    - BM25 keyword matching
    - Optional cross-encoder scores
    """

    def __init__(
        self,
        semantic_weight: float = 0.5,
        bm25_weight: float = 0.3,
        cross_encoder_weight: float = 0.2,
        use_cross_encoder: bool = True,
    ):
        self.semantic_weight = semantic_weight
        self.bm25_weight = bm25_weight
        self.cross_encoder_weight = cross_encoder_weight
        self.use_cross_encoder = use_cross_encoder

        self.bm25 = BM25Scorer()
        self.cross_encoder = CrossEncoderReranker() if use_cross_encoder else None

    def rerank(
        self, query: str, documents: List[Dict[str, Any]], top_k: Optional[int] = None
    ) -> List[RankedDocument]:
        """
        Rerank documents using hybrid scoring.

        Args:
            query: Search query
            documents: List of documents with 'text' and 'distance' fields
            top_k: Number of top documents to return

        Returns:
            List of RankedDocument objects
        """
        if not documents:
            return []

        top_k = top_k or RERANKER_TOP_K

        # Extract texts for BM25
        texts = [doc.get("text", "") for doc in documents]
        self.bm25.fit(texts)

        # Calculate BM25 scores
        bm25_scores = []
        for i, doc in enumerate(documents):
            score = self.bm25.score(query, doc.get("text", ""), i)
            bm25_scores.append(score)

        # Normalize BM25 scores
        max_bm25 = max(bm25_scores) if bm25_scores else 1
        bm25_scores = [s / max_bm25 if max_bm25 > 0 else 0 for s in bm25_scores]

        # Get cross-encoder scores if available
        ce_scores = [0.0] * len(documents)
        if self.use_cross_encoder and self.cross_encoder and self.cross_encoder.model:
            reranked = self.cross_encoder.rerank(
                query, documents.copy(), len(documents)
            )
            for i, doc in enumerate(documents):
                for j, reranked_doc in enumerate(reranked):
                    if doc.get("id") == reranked_doc.get("id"):
                        ce_scores[i] = reranked_doc.get("rerank_score", 0)
                        break

            # Normalize cross-encoder scores
            max_ce = max(ce_scores) if ce_scores else 1
            min_ce = min(ce_scores) if ce_scores else 0
            if max_ce > min_ce:
                ce_scores = [(s - min_ce) / (max_ce - min_ce) for s in ce_scores]

        # Calculate final hybrid scores
        results = []
        for i, doc in enumerate(documents):
            # Convert distance to similarity (1 - distance for cosine)
            semantic_score = 1 - doc.get("distance", 0)

            # Weighted combination
            final_score = (
                self.semantic_weight * semantic_score
                + self.bm25_weight * bm25_scores[i]
                + self.cross_encoder_weight * ce_scores[i]
            )

            results.append(
                RankedDocument(
                    id=doc.get("id", ""),
                    text=doc.get("text", ""),
                    metadata=doc.get("meta", {}),
                    original_score=semantic_score,
                    reranked_score=(
                        ce_scores[i] if self.use_cross_encoder else bm25_scores[i]
                    ),
                    final_score=final_score,
                    rank=0,  # Will be set after sorting
                )
            )

        # Sort by final score
        results.sort(key=lambda x: x.final_score, reverse=True)

        # Set ranks
        for i, doc in enumerate(results):
            doc.rank = i + 1

        return results[:top_k]


# =============================================================================
# MMR Diversifier
# =============================================================================


class MMRDiversifier:
    """
    P1.40: Maximal Marginal Relevance for diversity-aware reranking.

    MMR balances relevance and diversity to reduce redundancy in results.
    """

    def __init__(self, lambda_param: float = DIVERSITY_LAMBDA):
        self.lambda_param = lambda_param

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def diversify(
        self,
        query_embedding: List[float],
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]],
        top_k: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Apply MMR diversification to documents.

        Args:
            query_embedding: Query vector
            documents: List of documents
            embeddings: Document embeddings
            top_k: Number of documents to return

        Returns:
            Diversified document list
        """
        if not documents or not embeddings:
            return documents

        top_k = top_k or min(RERANKER_TOP_K, len(documents))

        # Calculate relevance scores (similarity to query)
        relevance_scores = [
            self._cosine_similarity(query_embedding, emb) for emb in embeddings
        ]

        selected_indices = []
        remaining_indices = list(range(len(documents)))

        while len(selected_indices) < top_k and remaining_indices:
            best_idx = None
            best_mmr = float("-inf")

            for idx in remaining_indices:
                # Relevance to query
                relevance = relevance_scores[idx]

                # Maximum similarity to already selected documents
                max_sim = 0.0
                if selected_indices:
                    for sel_idx in selected_indices:
                        sim = self._cosine_similarity(
                            embeddings[idx], embeddings[sel_idx]
                        )
                        max_sim = max(max_sim, sim)

                # MMR score
                mmr = self.lambda_param * relevance - (1 - self.lambda_param) * max_sim

                if mmr > best_mmr:
                    best_mmr = mmr
                    best_idx = idx

            if best_idx is not None:
                selected_indices.append(best_idx)
                remaining_indices.remove(best_idx)

        # Return diversified documents
        return [documents[i] for i in selected_indices]


# =============================================================================
# Main Reranker Interface
# =============================================================================


class RAGReranker:
    """
    P1.40: Main reranker interface combining all strategies.

    Usage:
        reranker = RAGReranker(strategy='hybrid')
        results = reranker.rerank(query, documents)
    """

    def __init__(
        self,
        strategy: str = "hybrid",
        top_k: int = RERANKER_TOP_K,
        use_diversity: bool = False,
    ):
        self.strategy = strategy
        self.top_k = top_k
        self.use_diversity = use_diversity

        # Initialize rerankers based on strategy
        if strategy == "cross_encoder":
            self.reranker = CrossEncoderReranker()
        elif strategy == "bm25":
            self.reranker = BM25Scorer()
        else:  # hybrid
            self.reranker = HybridReranker()

        self.diversifier = MMRDiversifier() if use_diversity else None

    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        query_embedding: Optional[List[float]] = None,
        doc_embeddings: Optional[List[List[float]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents using configured strategy.

        Args:
            query: Search query
            documents: List of documents
            query_embedding: Optional query vector for diversity
            doc_embeddings: Optional document vectors for diversity

        Returns:
            Reranked documents
        """
        if not documents:
            return []

        # Apply main reranking strategy
        if self.strategy == "hybrid":
            results = self.reranker.rerank(query, documents, self.top_k)
            # Convert RankedDocument back to dict
            reranked = [
                {
                    "id": r.id,
                    "text": r.text,
                    "meta": r.metadata,
                    "distance": 1 - r.original_score,
                    "final_score": r.final_score,
                    "rank": r.rank,
                }
                for r in results
            ]
        elif self.strategy == "cross_encoder":
            reranked = self.reranker.rerank(query, documents, self.top_k)
        else:  # bm25
            # Simple BM25 scoring
            texts = [doc.get("text", "") for doc in documents]
            self.reranker.fit(texts)
            scores = [
                self.reranker.score(query, doc.get("text", ""), i)
                for i, doc in enumerate(documents)
            ]
            # Sort by score
            doc_scores = list(zip(documents, scores))
            doc_scores.sort(key=lambda x: x[1], reverse=True)
            reranked = [d for d, s in doc_scores[: self.top_k]]

        # Apply diversity if enabled
        if self.use_diversity and query_embedding and doc_embeddings:
            reranked = self.diversifier.diversify(
                query_embedding, reranked, doc_embeddings, self.top_k
            )

        return reranked


__all__ = [
    "BM25Scorer",
    "CrossEncoderReranker",
    "HybridReranker",
    "MMRDiversifier",
    "RAGReranker",
    "RankedDocument",
]
