#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P1.41: RAG Evaluation Metrics

Provides comprehensive evaluation metrics for RAG systems:
- Retrieval metrics (MRR, MAP, NDCG, Recall@K)
- Generation metrics (BLEU, ROUGE, BERTScore)
- Faithfulness metrics
- Answer relevance metrics
"""

import math
import logging
from typing import List, Dict, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import Counter

logger = logging.getLogger(__name__)


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class EvaluationResult:
    """Result of RAG evaluation."""

    retrieval_metrics: Dict[str, float] = field(default_factory=dict)
    generation_metrics: Dict[str, float] = field(default_factory=dict)
    overall_score: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "retrieval_metrics": self.retrieval_metrics,
            "generation_metrics": self.generation_metrics,
            "overall_score": self.overall_score,
            "details": self.details,
        }


@dataclass
class RetrievalExample:
    """A single retrieval example for evaluation."""

    query: str
    retrieved_docs: List[str]
    relevant_docs: Set[str]
    doc_scores: Optional[List[float]] = None


# =============================================================================
# Retrieval Metrics
# =============================================================================


class RetrievalMetrics:
    """
    P1.41: Retrieval evaluation metrics.

    Implements standard IR metrics for evaluating retrieval quality.
    """

    @staticmethod
    def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
        """
        Calculate Precision@K.

        Args:
            retrieved: List of retrieved document IDs
            relevant: Set of relevant document IDs
            k: Number of top documents to consider

        Returns:
            Precision@K score
        """
        if k <= 0:
            return 0.0

        top_k = retrieved[:k]
        relevant_in_top_k = sum(1 for doc in top_k if doc in relevant)
        return relevant_in_top_k / k

    @staticmethod
    def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
        """
        Calculate Recall@K.

        Args:
            retrieved: List of retrieved document IDs
            relevant: Set of relevant document IDs
            k: Number of top documents to consider

        Returns:
            Recall@K score
        """
        if not relevant:
            return 0.0

        top_k = retrieved[:k]
        relevant_in_top_k = sum(1 for doc in top_k if doc in relevant)
        return relevant_in_top_k / len(relevant)

    @staticmethod
    def mrr(retrieved: List[str], relevant: Set[str]) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR).

        Returns the reciprocal of the rank of the first relevant document.

        Args:
            retrieved: List of retrieved document IDs
            relevant: Set of relevant document IDs

        Returns:
            MRR score
        """
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                return 1.0 / (i + 1)
        return 0.0

    @staticmethod
    def average_precision(retrieved: List[str], relevant: Set[str]) -> float:
        """
        Calculate Average Precision (AP).

        Args:
            retrieved: List of retrieved document IDs
            relevant: Set of relevant document IDs

        Returns:
            Average Precision score
        """
        if not relevant:
            return 0.0

        precisions = []
        relevant_count = 0

        for i, doc in enumerate(retrieved):
            if doc in relevant:
                relevant_count += 1
                precision = relevant_count / (i + 1)
                precisions.append(precision)

        if not precisions:
            return 0.0

        return sum(precisions) / len(relevant)

    @staticmethod
    def ndcg_at_k(
        retrieved: List[str],
        relevant: Set[str],
        k: int,
        relevance_scores: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain (NDCG@K).

        Args:
            retrieved: List of retrieved document IDs
            relevant: Set of relevant document IDs
            k: Number of top documents to consider
            relevance_scores: Optional dict of doc_id -> relevance score

        Returns:
            NDCG@K score
        """
        if k <= 0:
            return 0.0

        # Get relevance scores (binary if not provided)
        if relevance_scores is None:
            relevance_scores = {doc: 1.0 for doc in relevant}

        # Calculate DCG
        dcg = 0.0
        for i, doc in enumerate(retrieved[:k]):
            rel = relevance_scores.get(doc, 0.0)
            dcg += rel / math.log2(i + 2)  # i+2 because log2(1)=0

        # Calculate ideal DCG
        ideal_rels = sorted(
            [relevance_scores.get(doc, 0.0) for doc in relevant], reverse=True
        )[:k]

        idcg = 0.0
        for i, rel in enumerate(ideal_rels):
            idcg += rel / math.log2(i + 2)

        if idcg == 0:
            return 0.0

        return dcg / idcg

    @staticmethod
    def hit_rate(retrieved: List[str], relevant: Set[str], k: int) -> float:
        """
        Calculate Hit Rate (whether any relevant doc is in top-k).

        Args:
            retrieved: List of retrieved document IDs
            relevant: Set of relevant document IDs
            k: Number of top documents to consider

        Returns:
            1.0 if hit, 0.0 otherwise
        """
        top_k = set(retrieved[:k])
        return 1.0 if relevant & top_k else 0.0

    def evaluate(
        self, examples: List[RetrievalExample], k_values: List[int] = [1, 3, 5, 10]
    ) -> Dict[str, float]:
        """
        Evaluate retrieval on multiple examples.

        Args:
            examples: List of RetrievalExample
            k_values: K values for @K metrics

        Returns:
            Dictionary of metric scores
        """
        metrics = {}

        # Initialize accumulators
        mrr_scores = []
        ap_scores = []

        for k in k_values:
            metrics[f"precision@{k}"] = []
            metrics[f"recall@{k}"] = []
            metrics[f"ndcg@{k}"] = []
            metrics[f"hit_rate@{k}"] = []

        # Calculate metrics for each example
        for ex in examples:
            mrr_scores.append(self.mrr(ex.retrieved_docs, ex.relevant_docs))
            ap_scores.append(
                self.average_precision(ex.retrieved_docs, ex.relevant_docs)
            )

            for k in k_values:
                metrics[f"precision@{k}"].append(
                    self.precision_at_k(ex.retrieved_docs, ex.relevant_docs, k)
                )
                metrics[f"recall@{k}"].append(
                    self.recall_at_k(ex.retrieved_docs, ex.relevant_docs, k)
                )
                metrics[f"ndcg@{k}"].append(
                    self.ndcg_at_k(ex.retrieved_docs, ex.relevant_docs, k)
                )
                metrics[f"hit_rate@{k}"].append(
                    self.hit_rate(ex.retrieved_docs, ex.relevant_docs, k)
                )

        # Calculate averages
        result = {
            "mrr": sum(mrr_scores) / len(mrr_scores) if mrr_scores else 0,
            "map": sum(ap_scores) / len(ap_scores) if ap_scores else 0,
        }

        for key, values in metrics.items():
            result[key] = sum(values) / len(values) if values else 0

        return result


# =============================================================================
# Generation Metrics
# =============================================================================


class GenerationMetrics:
    """
    P1.41: Text generation evaluation metrics.

    Implements metrics for evaluating generated text quality.
    """

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple word tokenization."""
        return text.lower().split()

    @staticmethod
    def _ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
        """Generate n-grams from tokens."""
        return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]

    def bleu_score(
        self, candidate: str, references: List[str], max_n: int = 4
    ) -> float:
        """
        Calculate BLEU score (simplified version).

        Args:
            candidate: Generated text
            references: Reference texts
            max_n: Maximum n-gram order

        Returns:
            BLEU score
        """
        candidate_tokens = self._tokenize(candidate)

        if not candidate_tokens:
            return 0.0

        precisions = []

        for n in range(1, max_n + 1):
            candidate_ngrams = self._ngrams(candidate_tokens, n)

            if not candidate_ngrams:
                continue

            # Count reference n-grams
            max_ref_counts = Counter()
            for ref in references:
                ref_tokens = self._tokenize(ref)
                ref_ngrams = self._ngrams(ref_tokens, n)
                ref_counts = Counter(ref_ngrams)
                for ngram, count in ref_counts.items():
                    max_ref_counts[ngram] = max(max_ref_counts[ngram], count)

            # Count clipped matches
            candidate_counts = Counter(candidate_ngrams)
            clipped_count = 0
            for ngram, count in candidate_counts.items():
                clipped_count += min(count, max_ref_counts.get(ngram, 0))

            precision = clipped_count / len(candidate_ngrams)
            precisions.append(precision)

        if not precisions or 0 in precisions:
            return 0.0

        # Geometric mean of precisions
        log_precision_sum = sum(math.log(p) for p in precisions)
        bleu = math.exp(log_precision_sum / len(precisions))

        # Brevity penalty
        ref_lengths = [len(self._tokenize(ref)) for ref in references]
        closest_ref_len = min(ref_lengths, key=lambda x: abs(x - len(candidate_tokens)))

        if len(candidate_tokens) < closest_ref_len:
            brevity_penalty = math.exp(1 - closest_ref_len / len(candidate_tokens))
            bleu *= brevity_penalty

        return bleu

    def rouge_l_score(self, candidate: str, reference: str) -> Dict[str, float]:
        """
        Calculate ROUGE-L (Longest Common Subsequence) score.

        Args:
            candidate: Generated text
            reference: Reference text

        Returns:
            Dict with precision, recall, f1
        """
        candidate_tokens = self._tokenize(candidate)
        reference_tokens = self._tokenize(reference)

        if not candidate_tokens or not reference_tokens:
            return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

        # Find LCS length
        m, n = len(candidate_tokens), len(reference_tokens)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if candidate_tokens[i - 1] == reference_tokens[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        lcs_length = dp[m][n]

        precision = lcs_length / len(candidate_tokens)
        recall = lcs_length / len(reference_tokens)

        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * precision * recall / (precision + recall)

        return {"precision": precision, "recall": recall, "f1": f1}

    def exact_match(self, candidate: str, reference: str) -> float:
        """Check if candidate exactly matches reference."""
        return 1.0 if candidate.strip().lower() == reference.strip().lower() else 0.0

    def f1_token_score(self, candidate: str, reference: str) -> float:
        """
        Calculate token-level F1 score.

        Args:
            candidate: Generated text
            reference: Reference text

        Returns:
            F1 score
        """
        candidate_tokens = set(self._tokenize(candidate))
        reference_tokens = set(self._tokenize(reference))

        if not candidate_tokens or not reference_tokens:
            return 0.0

        common = candidate_tokens & reference_tokens

        precision = len(common) / len(candidate_tokens)
        recall = len(common) / len(reference_tokens)

        if precision + recall == 0:
            return 0.0

        return 2 * precision * recall / (precision + recall)


# =============================================================================
# RAG-Specific Metrics
# =============================================================================


class RAGMetrics:
    """
    P1.41: RAG-specific evaluation metrics.

    Metrics specific to RAG systems like faithfulness and context relevance.
    """

    def __init__(self):
        self.gen_metrics = GenerationMetrics()

    def context_relevance(self, query: str, contexts: List[str]) -> float:
        """
        Measure how relevant the retrieved contexts are to the query.

        Uses token overlap as a simple relevance proxy.

        Args:
            query: User query
            contexts: Retrieved context passages

        Returns:
            Average relevance score
        """
        if not contexts:
            return 0.0

        query_tokens = set(query.lower().split())

        relevance_scores = []
        for ctx in contexts:
            ctx_tokens = set(ctx.lower().split())
            if ctx_tokens:
                overlap = len(query_tokens & ctx_tokens)
                relevance = overlap / len(query_tokens) if query_tokens else 0
                relevance_scores.append(relevance)

        return sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0

    def answer_relevance(self, query: str, answer: str) -> float:
        """
        Measure how relevant the answer is to the query.

        Args:
            query: User query
            answer: Generated answer

        Returns:
            Relevance score
        """
        return self.gen_metrics.f1_token_score(answer, query)

    def faithfulness(self, answer: str, contexts: List[str]) -> float:
        """
        Measure how faithful the answer is to the source contexts.

        Checks if answer tokens appear in contexts.

        Args:
            answer: Generated answer
            contexts: Source context passages

        Returns:
            Faithfulness score (0-1)
        """
        if not answer or not contexts:
            return 0.0

        answer_tokens = set(answer.lower().split())

        # Combine all context tokens
        context_tokens = set()
        for ctx in contexts:
            context_tokens.update(ctx.lower().split())

        if not answer_tokens:
            return 0.0

        # What fraction of answer tokens appear in context
        supported = answer_tokens & context_tokens
        return len(supported) / len(answer_tokens)

    def context_utilization(self, answer: str, contexts: List[str]) -> float:
        """
        Measure how much of the context was used in the answer.

        Args:
            answer: Generated answer
            contexts: Source context passages

        Returns:
            Utilization score (0-1)
        """
        if not contexts:
            return 0.0

        answer_tokens = set(answer.lower().split())

        utilized_contexts = 0
        for ctx in contexts:
            ctx_tokens = set(ctx.lower().split())
            # Check if any context tokens appear in answer
            if answer_tokens & ctx_tokens:
                utilized_contexts += 1

        return utilized_contexts / len(contexts)


# =============================================================================
# Main Evaluator
# =============================================================================


class RAGEvaluator:
    """
    P1.41: Main RAG evaluation interface.

    Usage:
        evaluator = RAGEvaluator()
        result = evaluator.evaluate(
            query="What is X?",
            retrieved_docs=["doc1", "doc2"],
            generated_answer="X is...",
            reference_answer="X is...",
            relevant_doc_ids={"doc1"}
        )
    """

    def __init__(self):
        self.retrieval_metrics = RetrievalMetrics()
        self.generation_metrics = GenerationMetrics()
        self.rag_metrics = RAGMetrics()

    def evaluate(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        generated_answer: str,
        reference_answer: Optional[str] = None,
        relevant_doc_ids: Optional[Set[str]] = None,
        k_values: List[int] = [1, 3, 5],
    ) -> EvaluationResult:
        """
        Comprehensive RAG evaluation.

        Args:
            query: User query
            retrieved_docs: List of retrieved documents with 'id' and 'text'
            generated_answer: RAG-generated answer
            reference_answer: Ground truth answer (optional)
            relevant_doc_ids: Set of relevant document IDs (optional)
            k_values: K values for retrieval metrics

        Returns:
            EvaluationResult with all metrics
        """
        result = EvaluationResult()

        # Extract document texts and IDs
        doc_ids = [doc.get("id", str(i)) for i, doc in enumerate(retrieved_docs)]
        doc_texts = [doc.get("text", "") for doc in retrieved_docs]

        # Retrieval metrics (if relevant docs provided)
        if relevant_doc_ids:
            for k in k_values:
                result.retrieval_metrics[f"precision@{k}"] = (
                    self.retrieval_metrics.precision_at_k(doc_ids, relevant_doc_ids, k)
                )
                result.retrieval_metrics[f"recall@{k}"] = (
                    self.retrieval_metrics.recall_at_k(doc_ids, relevant_doc_ids, k)
                )
                result.retrieval_metrics[f"ndcg@{k}"] = (
                    self.retrieval_metrics.ndcg_at_k(doc_ids, relevant_doc_ids, k)
                )

            result.retrieval_metrics["mrr"] = self.retrieval_metrics.mrr(
                doc_ids, relevant_doc_ids
            )
            result.retrieval_metrics["map"] = self.retrieval_metrics.average_precision(
                doc_ids, relevant_doc_ids
            )

        # Generation metrics (if reference provided)
        if reference_answer:
            result.generation_metrics["bleu"] = self.generation_metrics.bleu_score(
                generated_answer, [reference_answer]
            )

            rouge_l = self.generation_metrics.rouge_l_score(
                generated_answer, reference_answer
            )
            result.generation_metrics["rouge_l_f1"] = rouge_l["f1"]

            result.generation_metrics["exact_match"] = (
                self.generation_metrics.exact_match(generated_answer, reference_answer)
            )

            result.generation_metrics["f1"] = self.generation_metrics.f1_token_score(
                generated_answer, reference_answer
            )

        # RAG-specific metrics
        result.generation_metrics["context_relevance"] = (
            self.rag_metrics.context_relevance(query, doc_texts)
        )
        result.generation_metrics["answer_relevance"] = (
            self.rag_metrics.answer_relevance(query, generated_answer)
        )
        result.generation_metrics["faithfulness"] = self.rag_metrics.faithfulness(
            generated_answer, doc_texts
        )
        result.generation_metrics["context_utilization"] = (
            self.rag_metrics.context_utilization(generated_answer, doc_texts)
        )

        # Calculate overall score
        all_scores = list(result.retrieval_metrics.values()) + list(
            result.generation_metrics.values()
        )
        result.overall_score = sum(all_scores) / len(all_scores) if all_scores else 0

        return result


__all__ = [
    "RetrievalMetrics",
    "GenerationMetrics",
    "RAGMetrics",
    "RAGEvaluator",
    "EvaluationResult",
    "RetrievalExample",
]
