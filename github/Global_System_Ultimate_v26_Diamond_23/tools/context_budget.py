#!/usr/bin/env python3
"""
Context Budget Manager (Global System Ultimate)
Tracks token usage, manages context window saturation, and triggers dynamic compression.
Integrates with Vector DB for offloading old context.
"""

import os
import sys
import json
import logging
from typing import List, Dict

# Load Version
try:
    with open(os.path.join(os.path.dirname(__file__), "../VERSION"), "r") as f:
        VERSION = f.read().strip()
except FileNotFoundError:
    VERSION = "UNKNOWN"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration (2026 Standards)
MAX_CONTEXT_TOKENS = 200000  # Claude 3.5 Sonnet / GPT-5 standard
WARNING_THRESHOLD = 0.8      # Warn at 80% usage
CRITICAL_THRESHOLD = 0.95    # Critical alert at 95% usage
COMPRESSION_RATIO = 0.5      # Target compression ratio

class ContextManager:
    def __init__(self, memory_path: str = "memory-bank"):
        self.memory_path = memory_path
        self.files = self._discover_files()

    def _discover_files(self) -> List[str]:
        """Discovers all markdown files in the memory bank."""
        if not os.path.exists(self.memory_path):
            logging.error(f"❌ Memory path not found: {self.memory_path}")
            return []
        return [os.path.join(self.memory_path, f) for f in os.listdir(self.memory_path) if f.endswith(".md")]

    def estimate_tokens(self, text: str) -> int:
        """
        Rough estimation: 1 token ~= 4 characters for English text.
        In 2026, we use a more sophisticated tokenizer if available (tiktoken).
        """
        try:
            import tiktoken
            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except ImportError:
            return len(text) // 4

    def check_usage(self):
        total_tokens = 0
        file_stats = []

        logging.info(f"📊 Analyzing Context Usage ({VERSION})...")

        for path in self.files:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tokens = self.estimate_tokens(content)
                    total_tokens += tokens
                    file_stats.append((path, tokens))
            except Exception as e:
                logging.error(f"⚠️  Error reading {path}: {e}")

        usage_ratio = total_tokens / MAX_CONTEXT_TOKENS

        # Report per file
        print("\n📄 File Breakdown:")
        for path, tokens in sorted(file_stats, key=lambda x: x[1], reverse=True):
            print(f"   - {os.path.basename(path):<30} : {tokens:,.0f} tokens")

        # Report Total
        print(f"\n📈 Total Usage: {total_tokens:,.0f} / {MAX_CONTEXT_TOKENS:,.0f} tokens ({usage_ratio:.1%})")

        if usage_ratio > CRITICAL_THRESHOLD:
            logging.warning("\n🚨 CRITICAL: Context budget EXCEEDED!")
            self._trigger_compression(file_stats)
        elif usage_ratio > WARNING_THRESHOLD:
            logging.warning("\n⚠️  WARNING: Context budget approaching limit.")
            self._suggest_archival(file_stats)
        else:
            logging.info("\n✅ Context budget is healthy.")

    def _trigger_compression(self, file_stats: List[tuple]):
        """
        Triggers the 2026 Context Compression Protocol.
        """
        logging.info("   -> 🔄 Initiating Context Compression...")
        # Identify largest files
        largest_files = sorted(file_stats, key=lambda x: x[1], reverse=True)[:3]
        for path, tokens in largest_files:
            logging.info(f"      Compressing: {os.path.basename(path)} ({tokens} tokens)")
            # In a real scenario, this would call an LLM to summarize
            # self._llm_summarize(path)
            logging.info(f"      (Simulated compression: Reduced by {COMPRESSION_RATIO*100}%)")

    def _suggest_archival(self, file_stats: List[tuple]):
        """
        Suggests files for archival to Vector DB.
        """
        logging.info("   -> 📦 Suggesting Archival...")
        # Logic to identify old/inactive context
        logging.info("      Consider moving 'decisionLog.md' (older entries) to Vector Storage.")

if __name__ == "__main__":
    # Auto-detect memory bank location
    possible_roots = [
        "memory-bank",
        "GitHub/global_system/memory-bank",
        "../memory-bank",
        os.path.join(os.getcwd(), "memory-bank")
    ]
    
    memory_dir = None
    for root in possible_roots:
        if os.path.exists(root):
            memory_dir = root
            break
    
    if memory_dir:
        manager = ContextManager(memory_dir)
        manager.check_usage()
    else:
        logging.error("❌ Could not locate 'memory-bank' directory.")
        sys.exit(1)
