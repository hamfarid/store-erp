=================================================================================
MEMORY MANAGEMENT & CONTEXT RETENTION (Global System Ultimate)
=================================================================================

⚠️ NOTE: This module is part of Global Guidelines (instruction manual).
Apply this guidance to THE USER'S PROJECT, not to Global Guidelines itself.
Global Guidelines is in: ~/global/ or similar
User's project is in: A separate directory (ask user for project path)

⚡ MANDATORY USAGE:
================================================================================
AI MUST use memory management from the FIRST interaction!

When to activate:
-----------------
✅ At the start of any task
✅ When user provides important information
✅ When making project decisions
✅ When discovering requirements
✅ Throughout the entire task lifecycle

How to use:
-----------
1. Initialize memory at task start
2. Save context continuously
3. Retrieve context when needed
4. Update memory as project evolves

⚠️ CRITICAL: If you're NOT using memory management, you're NOT following
Global Guidelines properly! Memory is NOT optional - it's MANDATORY!

Example First Interaction:
--------------------------
User: "Help me build a web app"

AI MUST do:
✅ "I'll save this project context to memory..."
✅ Save: project_type=web_app, status=starting, user_goal=build_web_app

AI MUST NOT:
❌ Start without initializing memory
❌ Rely only on conversation context
❌ Forget to save important decisions

Version: Global System Ultimate
Last Updated: 2025-11-04
Type: Memory & Context Management
=================================================================================

OVERVIEW
=================================================================================

This module provides comprehensive strategies and techniques for managing AI
memory and maintaining context across long conversations, multiple sessions,
and complex projects. It addresses the fundamental challenge of AI systems:
limited context windows and stateless nature.

KEY CONCEPTS:
- Short-term Memory (STM): Current conversation context
- Long-term Memory (LTM): Persistent knowledge across sessions
- Working Memory: Active information being processed
- Episodic Memory: Specific events and interactions
- Semantic Memory: General knowledge and facts
- Procedural Memory: How-to knowledge and workflows

=================================================================================
SECTION 1: MEMORY ARCHITECTURE
=================================================================================

AI MEMORY HIERARCHY
-------------------

```
┌─────────────────────────────────────────────────────────────┐
│                    MEMORY HIERARCHY                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────────┐      │
│  │  WORKING MEMORY (Active Context)                  │      │
│  │  - Current conversation                            │      │
│  │  - Immediate task context                          │      │
│  │  - Active variables and state                      │      │
│  │  Size: Limited by context window                   │      │
│  └───────────────────────────────────────────────────┘      │
│                          ↕                                    │
│  ┌───────────────────────────────────────────────────┐      │
│  │  SHORT-TERM MEMORY (Session Memory)               │      │
│  │  - Recent interactions (last few hours)            │      │
│  │  - Session-specific context                        │      │
│  │  - Temporary decisions and preferences             │      │
│  │  Storage: In-memory cache, Redis                   │      │
│  └───────────────────────────────────────────────────┘      │
│                          ↕                                    │
│  ┌───────────────────────────────────────────────────┐      │
│  │  LONG-TERM MEMORY (Persistent Memory)             │      │
│  │  - User preferences and history                    │      │
│  │  - Project knowledge base                          │      │
│  │  - Learned patterns and lessons                    │      │
│  │  Storage: Database, Vector DB, Files               │      │
│  └───────────────────────────────────────────────────┘      │
│                          ↕                                    │
│  ┌───────────────────────────────────────────────────┐      │
│  │  EXTERNAL MEMORY (Knowledge Base)                 │      │
│  │  - Documentation and references                    │      │
│  │  - Code repositories                               │      │
│  │  - External APIs and services                      │      │
│  │  Storage: GitHub, Notion, Context7, etc.           │      │
│  └───────────────────────────────────────────────────┘      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

MEMORY TYPES
------------

1. EPISODIC MEMORY (What happened)
   - Conversation history
   - User interactions
   - Events and milestones
   - Decisions made

2. SEMANTIC MEMORY (What we know)
   - Facts and concepts
   - Project specifications
   - Technical knowledge
   - Best practices

3. PROCEDURAL MEMORY (How to do)
   - Workflows and processes
   - Code patterns
   - Problem-solving strategies
   - User preferences for tasks

4. PROSPECTIVE MEMORY (What to do)
   - Scheduled tasks
   - Reminders
   - Follow-ups
   - Future goals

=================================================================================
SECTION 2: CONTEXT WINDOW OPTIMIZATION
=================================================================================

STRATEGIES FOR MANAGING LIMITED CONTEXT
----------------------------------------

1. CONTEXT COMPRESSION (Advanced 2025 Techniques)
   - **Semantic Summarization:** Use LLMs to generate concise summaries of past interactions, preserving key decisions and facts while discarding conversational filler.
   - **Vector-Based Retrieval:** Store conversation chunks in a vector database (e.g., ChromaDB, Pinecone) and retrieve only the most relevant chunks based on the current query.
   - **Entity Extraction:** Automatically extract and store key entities (names, dates, technical terms) in a structured format (JSON/YAML) for instant retrieval.
   - **Recursive Summarization:** Periodically summarize the summaries to maintain a high-level overview of long-running projects without losing the "big picture."

2. HIERARCHICAL CONTEXT
   - Essential context (always included)
   - Important context (included when relevant)
   - Optional context (included if space allows)
   - Archived context (retrievable on demand)

3. DYNAMIC CONTEXT LOADING
   - Load context based on current task
   - Fetch relevant memories on demand
   - Unload irrelevant context
   - Prioritize recent and important information

4. CONTEXT CHUNKING
   - Break long context into chunks
   - Process chunks sequentially
   - Maintain summary of processed chunks
   - Merge results intelligently

IMPLEMENTATION: CONTEXT MANAGER
-------------------------------

```python
# Context Manager with Priority System
class ContextManager:
    """
    Manages AI context with priority-based retention.
    """
    
    def __init__(self, max_tokens=8000):
        self.max_tokens = max_tokens
        self.contexts = {
            'essential': [],      # Always included
            'important': [],      # Included when possible
            'optional': [],       # Included if space allows
            'archived': []        # Stored but not loaded
        }
        self.current_tokens = 0
    
    def add_context(self, content, priority='important', metadata=None):
        """
        Add context with priority level.
        
        Args:
            content: Context content
            priority: 'essential', 'important', 'optional', 'archived'
            metadata: Additional metadata (timestamp, tags, etc.)
        """
        context_item = {
            'content': content,
            'tokens': self.estimate_tokens(content),
            'timestamp': datetime.now(),
            'metadata': metadata or {}
        }
        
        self.contexts[priority].append(context_item)
        self._rebalance()
    
    def get_active_context(self):
        """
        Get context that fits within token limit.
        """
        active_context = []
        remaining_tokens = self.max_tokens
        
        # 1. Always include essential context
        for item in self.contexts['essential']:
            active_context.append(item['content'])
            remaining_tokens -= item['tokens']
        
        # 2. Include important context if space allows
        for item in sorted(self.contexts['important'], 
                          key=lambda x: x['timestamp'], 
                          reverse=True):
            if remaining_tokens >= item['tokens']:
                active_context.append(item['content'])
                remaining_tokens -= item['tokens']
        
        # 3. Include optional context if space allows
        for item in sorted(self.contexts['optional'], 
                          key=lambda x: x['timestamp'], 
                          reverse=True):
            if remaining_tokens >= item['tokens']:
                active_context.append(item['content'])
                remaining_tokens -= item['tokens']
        
        return '\n\n'.join(active_context)
    
    def _rebalance(self):
        """
        Move old important context to optional or archived.
        """
        threshold = datetime.now() - timedelta(hours=2)
        
        # Move old important to optional
        old_important = [
            item for item in self.contexts['important']
            if item['timestamp'] < threshold
        ]
        
        for item in old_important:
            self.contexts['important'].remove(item)
            self.contexts['optional'].append(item)
        
        # Archive very old optional context
        archive_threshold = datetime.now() - timedelta(hours=24)
        old_optional = [
            item for item in self.contexts['optional']
            if item['timestamp'] < archive_threshold
        ]
        
        for item in old_optional:
            self.contexts['optional'].remove(item)
            self.contexts['archived'].append(item)
    
    def estimate_tokens(self, text):
        """
        Estimate token count (rough approximation).
        """
        return len(text.split()) * 1.3  # ~1.3 tokens per word
    
    def summarize_old_context(self):
        """
        Summarize old context to save space.
        """
        # Summarize archived context
        if len(self.contexts['archived']) > 10:
            # Implementation of summarization logic
            pass
```
