=================================================================================
MEMORY MANAGEMENT & CONTEXT RETENTION
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



Version: Latest
Last Updated: 2025-11-03
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

1. CONTEXT COMPRESSION
   - Summarize old conversations
   - Extract key information
   - Remove redundant content
   - Keep only relevant context

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
            old_content = [item['content'] for item in self.contexts['archived']]
            summary = self._create_summary(old_content)
            
            # Replace archived with summary
            self.contexts['archived'] = [{
                'content': summary,
                'tokens': self.estimate_tokens(summary),
                'timestamp': datetime.now(),
                'metadata': {'type': 'summary', 'items': len(old_content)}
            }]
    
    def _create_summary(self, contents):
        """
        Create summary of multiple context items.
        """
        # This would use an AI model to summarize
        # For now, return a placeholder
        return f"Summary of {len(contents)} previous interactions"


# Usage Example
context_mgr = ContextManager(max_tokens=8000)

# Add essential context (always included)
context_mgr.add_context(
    "Project: E-commerce Platform\nStack: Python, React, PostgreSQL",
    priority='essential',
    metadata={'type': 'project_info'}
)

# Add important context
context_mgr.add_context(
    "User prefers functional programming style",
    priority='important',
    metadata={'type': 'preference'}
)

# Add conversation context
context_mgr.add_context(
    "User: How do I implement authentication?\nAI: Use JWT tokens...",
    priority='important',
    metadata={'type': 'conversation'}
)

# Get active context for AI
active_context = context_mgr.get_active_context()
```

=================================================================================
SECTION 3: MEMORY PERSISTENCE STRATEGIES
=================================================================================

PERSISTENT MEMORY STORAGE
--------------------------

1. FILE-BASED MEMORY
   ```bash
   # Create memory directory structure
   mkdir -p .memory/{conversations,knowledge,preferences,state}
   
   # Store conversation
   cat > .memory/conversations/$(date +%Y%m%d_%H%M%S).json << 'EOF'
   {
     "timestamp": "2025-11-03T10:30:00Z",
     "user_id": "user123",
     "conversation": [
       {"role": "user", "content": "..."},
       {"role": "assistant", "content": "..."}
     ],
     "context": {
       "project": "ecommerce",
       "task": "authentication"
     }
   }
   EOF
   ```

2. DATABASE-BASED MEMORY
   ```sql
   -- Memory schema
   CREATE TABLE ai_memory (
       id SERIAL PRIMARY KEY,
       user_id VARCHAR(255),
       memory_type VARCHAR(50), -- 'episodic', 'semantic', 'procedural'
       content TEXT,
       embedding VECTOR(1536), -- For semantic search
       metadata JSONB,
       importance INT DEFAULT 5, -- 1-10 scale
       created_at TIMESTAMP DEFAULT NOW(),
       accessed_at TIMESTAMP DEFAULT NOW(),
       access_count INT DEFAULT 0
   );
   
   CREATE INDEX idx_memory_user ON ai_memory(user_id);
   CREATE INDEX idx_memory_type ON ai_memory(memory_type);
   CREATE INDEX idx_memory_importance ON ai_memory(importance DESC);
   CREATE INDEX idx_memory_embedding ON ai_memory USING ivfflat (embedding vector_cosine_ops);
   
   -- Store memory
   INSERT INTO ai_memory (user_id, memory_type, content, metadata, importance)
   VALUES (
       'user123',
       'semantic',
       'User prefers PostgreSQL over MySQL for this project',
       '{"category": "preference", "project": "ecommerce"}',
       8
   );
   
   -- Retrieve relevant memories
   SELECT content, importance, metadata
   FROM ai_memory
   WHERE user_id = 'user123'
     AND memory_type = 'semantic'
   ORDER BY importance DESC, accessed_at DESC
   LIMIT 10;
   ```

3. VECTOR DATABASE MEMORY (Semantic Search)
   ```python
   from chromadb import Client
   from chromadb.config import Settings
   
   # Initialize vector database
   client = Client(Settings(
       chroma_db_impl="duckdb+parquet",
       persist_directory=".memory/vectors"
   ))
   
   # Create collection
   collection = client.create_collection(
       name="ai_memory",
       metadata={"description": "AI long-term memory"}
   )
   
   # Store memory with embedding
   collection.add(
       documents=["User prefers functional programming style"],
       metadatas=[{
           "type": "preference",
           "importance": 8,
           "timestamp": "2025-11-03T10:30:00Z"
       }],
       ids=["mem_001"]
   )
   
   # Semantic search for relevant memories
   results = collection.query(
       query_texts=["How should I write this function?"],
       n_results=5,
       where={"importance": {"$gte": 5}}
   )
   
   print("Relevant memories:", results['documents'])
   ```

4. REDIS-BASED SESSION MEMORY
   ```python
   import redis
   import json
   from datetime import timedelta
   
   # Connect to Redis
   r = redis.Redis(host='localhost', port=6379, db=0)
   
   # Store session memory (expires after 24 hours)
   session_data = {
       "user_id": "user123",
       "current_project": "ecommerce",
       "recent_context": "Working on authentication",
       "preferences": {
           "language": "python",
           "style": "functional"
       }
   }
   
   r.setex(
       "session:user123",
       timedelta(hours=24),
       json.dumps(session_data)
   )
   
   # Retrieve session memory
   session = json.loads(r.get("session:user123"))
   print("Current context:", session['recent_context'])
   ```

MEMORY RETRIEVAL STRATEGIES
----------------------------

1. RECENCY-BASED RETRIEVAL
   - Prioritize recent memories
   - Use time decay function
   - Balance with importance

2. RELEVANCE-BASED RETRIEVAL
   - Semantic similarity search
   - Keyword matching
   - Context-aware filtering

3. IMPORTANCE-BASED RETRIEVAL
   - User-defined importance
   - Access frequency
   - Impact on decisions

4. HYBRID RETRIEVAL
   ```python
   def retrieve_memories(query, user_id, top_k=10):
       """
       Hybrid memory retrieval combining multiple strategies.
       """
       # 1. Semantic search (relevance)
       semantic_results = vector_db.search(query, top_k=20)
       
       # 2. Recent memories (recency)
       recent_results = db.query(
           "SELECT * FROM ai_memory WHERE user_id = ? "
           "ORDER BY created_at DESC LIMIT 20",
           (user_id,)
       )
       
       # 3. Important memories (importance)
       important_results = db.query(
           "SELECT * FROM ai_memory WHERE user_id = ? "
           "ORDER BY importance DESC LIMIT 20",
           (user_id,)
       )
       
       # 4. Combine and rank
       all_results = {}
       
       for result in semantic_results:
           score = result['similarity'] * 0.4  # 40% weight
           all_results[result['id']] = {
               'memory': result,
               'score': score
           }
       
       for result in recent_results:
           memory_id = result['id']
           recency_score = calculate_recency_score(result['created_at']) * 0.3
           
           if memory_id in all_results:
               all_results[memory_id]['score'] += recency_score
           else:
               all_results[memory_id] = {
                   'memory': result,
                   'score': recency_score
               }
       
       for result in important_results:
           memory_id = result['id']
           importance_score = (result['importance'] / 10) * 0.3
           
           if memory_id in all_results:
               all_results[memory_id]['score'] += importance_score
           else:
               all_results[memory_id] = {
                   'memory': result,
                   'score': importance_score
               }
       
       # 5. Sort by combined score
       ranked_results = sorted(
           all_results.values(),
           key=lambda x: x['score'],
           reverse=True
       )
       
       return [r['memory'] for r in ranked_results[:top_k]]
   
   
   def calculate_recency_score(timestamp):
       """
       Calculate recency score with exponential decay.
       """
       age_hours = (datetime.now() - timestamp).total_seconds() / 3600
       return math.exp(-age_hours / 24)  # Half-life of 24 hours
   ```

=================================================================================
SECTION 4: CONTEXT RETENTION TECHNIQUES
=================================================================================

CONVERSATION SUMMARIZATION
---------------------------

```python
def summarize_conversation(messages, max_length=500):
    """
    Summarize long conversation to retain key information.
    """
    # Extract key information
    key_points = []
    decisions = []
    questions = []
    
    for msg in messages:
        # Identify important patterns
        if "decided" in msg['content'].lower() or "will" in msg['content'].lower():
            decisions.append(msg['content'])
        elif "?" in msg['content']:
            questions.append(msg['content'])
        elif any(keyword in msg['content'].lower() 
                for keyword in ['important', 'note', 'remember']):
            key_points.append(msg['content'])
    
    # Create structured summary
    summary = {
        'key_points': key_points[:5],
        'decisions': decisions[:5],
        'open_questions': questions[:3],
        'message_count': len(messages),
        'time_span': f"{messages[0]['timestamp']} to {messages[-1]['timestamp']}"
    }
    
    return summary


# Usage
old_messages = [...]  # Long conversation history
summary = summarize_conversation(old_messages)

# Store summary instead of full history
context_mgr.add_context(
    f"Previous conversation summary:\n"
    f"Key points: {', '.join(summary['key_points'])}\n"
    f"Decisions: {', '.join(summary['decisions'])}\n"
    f"Open questions: {', '.join(summary['open_questions'])}",
    priority='important',
    metadata={'type': 'summary', 'original_count': summary['message_count']}
)
```

INCREMENTAL CONTEXT UPDATES
----------------------------

```python
class IncrementalContextManager:
    """
    Manages context with incremental updates instead of full replacement.
    """
    
    def __init__(self):
        self.context_state = {
            'project': {},
            'user_preferences': {},
            'current_task': {},
            'decisions': [],
            'open_issues': []
        }
    
    def update_context(self, update_type, data):
        """
        Update specific part of context without replacing everything.
        """
        if update_type == 'project_info':
            self.context_state['project'].update(data)
        
        elif update_type == 'preference':
            self.context_state['user_preferences'].update(data)
        
        elif update_type == 'task':
            self.context_state['current_task'] = data
        
        elif update_type == 'decision':
            self.context_state['decisions'].append({
                'decision': data,
                'timestamp': datetime.now()
            })
            # Keep only recent decisions
            self.context_state['decisions'] = \
                self.context_state['decisions'][-10:]
        
        elif update_type == 'issue':
            self.context_state['open_issues'].append(data)
    
    def get_context_snapshot(self):
        """
        Get current context state as formatted string.
        """
        return f"""
PROJECT CONTEXT:
{json.dumps(self.context_state['project'], indent=2)}

USER PREFERENCES:
{json.dumps(self.context_state['user_preferences'], indent=2)}

CURRENT TASK:
{json.dumps(self.context_state['current_task'], indent=2)}

RECENT DECISIONS:
{chr(10).join(f"- {d['decision']}" for d in self.context_state['decisions'][-5:])}

OPEN ISSUES:
{chr(10).join(f"- {issue}" for issue in self.context_state['open_issues'])}
"""


# Usage
ctx = IncrementalContextManager()

# Initial setup
ctx.update_context('project_info', {
    'name': 'E-commerce Platform',
    'stack': ['Python', 'React', 'PostgreSQL']
})

# Add preference
ctx.update_context('preference', {
    'code_style': 'functional',
    'testing': 'pytest'
})

# Update task
ctx.update_context('task', {
    'current': 'Implementing authentication',
    'status': 'in_progress'
})

# Record decision
ctx.update_context('decision', 'Using JWT tokens for authentication')

# Get current context
print(ctx.get_context_snapshot())
```

CONTEXT CHECKPOINTING
----------------------

```python
class ContextCheckpoint:
    """
    Create checkpoints of context state for recovery.
    """
    
    def __init__(self, checkpoint_dir='.memory/checkpoints'):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(self, context_data, checkpoint_name=None):
        """
        Save current context state.
        """
        if checkpoint_name is None:
            checkpoint_name = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        checkpoint_file = self.checkpoint_dir / f"{checkpoint_name}.json"
        
        with open(checkpoint_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'context': context_data
            }, f, indent=2)
        
        print(f"✅ Checkpoint saved: {checkpoint_name}")
        return checkpoint_name
    
    def load_checkpoint(self, checkpoint_name):
        """
        Load context from checkpoint.
        """
        checkpoint_file = self.checkpoint_dir / f"{checkpoint_name}.json"
        
        if not checkpoint_file.exists():
            print(f"❌ Checkpoint not found: {checkpoint_name}")
            return None
        
        with open(checkpoint_file, 'r') as f:
            data = json.load(f)
        
        print(f"✅ Checkpoint loaded: {checkpoint_name}")
        return data['context']
    
    def list_checkpoints(self):
        """
        List all available checkpoints.
        """
        checkpoints = sorted(self.checkpoint_dir.glob('*.json'), reverse=True)
        return [cp.stem for cp in checkpoints]
    
    def auto_checkpoint(self, context_data, interval_minutes=30):
        """
        Automatically save checkpoint at intervals.
        """
        last_checkpoint = self.get_last_checkpoint_time()
        
        if last_checkpoint is None or \
           (datetime.now() - last_checkpoint).seconds >= interval_minutes * 60:
            return self.save_checkpoint(context_data)
        
        return None
    
    def get_last_checkpoint_time(self):
        """
        Get timestamp of last checkpoint.
        """
        checkpoints = list(self.checkpoint_dir.glob('*.json'))
        if not checkpoints:
            return None
        
        latest = max(checkpoints, key=lambda p: p.stat().st_mtime)
        return datetime.fromtimestamp(latest.stat().st_mtime)


# Usage
checkpoint_mgr = ContextCheckpoint()

# Save checkpoint
checkpoint_mgr.save_checkpoint({
    'project': 'ecommerce',
    'task': 'authentication',
    'progress': 0.75
}, checkpoint_name='auth_implementation')

# Auto-checkpoint every 30 minutes
checkpoint_mgr.auto_checkpoint(current_context, interval_minutes=30)

# List checkpoints
print("Available checkpoints:", checkpoint_mgr.list_checkpoints())

# Load checkpoint
restored_context = checkpoint_mgr.load_checkpoint('auth_implementation')
```

=================================================================================
SECTION 5: MEMORY CONSOLIDATION & LEARNING
=================================================================================

PATTERN DETECTION AND LEARNING
-------------------------------

```python
class MemoryConsolidation:
    """
    Consolidate memories and extract patterns for learning.
    """
    
    def __init__(self):
        self.patterns = {}
        self.lessons_learned = []
    
    def analyze_memories(self, memories):
        """
        Analyze memories to detect patterns.
        """
        # Group by type
        by_type = {}
        for memory in memories:
            mem_type = memory.get('metadata', {}).get('type', 'unknown')
            if mem_type not in by_type:
                by_type[mem_type] = []
            by_type[mem_type].append(memory)
        
        # Detect patterns
        for mem_type, mems in by_type.items():
            if len(mems) >= 3:  # Need at least 3 instances
                pattern = self._detect_pattern(mems)
                if pattern:
                    self.patterns[mem_type] = pattern
    
    def _detect_pattern(self, memories):
        """
        Detect common patterns in similar memories.
        """
        # Extract common elements
        common_keywords = self._find_common_keywords(
            [m['content'] for m in memories]
        )
        
        if len(common_keywords) >= 2:
            return {
                'keywords': common_keywords,
                'frequency': len(memories),
                'confidence': len(common_keywords) / 10
            }
        
        return None
    
    def _find_common_keywords(self, texts):
        """
        Find keywords that appear in multiple texts.
        """
        from collections import Counter
        
        all_words = []
        for text in texts:
            words = text.lower().split()
            all_words.extend([w for w in words if len(w) > 4])
        
        word_counts = Counter(all_words)
        common = [word for word, count in word_counts.items() 
                 if count >= len(texts) * 0.5]
        
        return common[:10]
    
    def extract_lessons(self, memories):
        """
        Extract lessons learned from past experiences.
        """
        # Find successful patterns
        successful = [m for m in memories 
                     if m.get('metadata', {}).get('outcome') == 'success']
        
        # Find failed patterns
        failed = [m for m in memories 
                 if m.get('metadata', {}).get('outcome') == 'failure']
        
        # Create lessons
        if successful:
            success_pattern = self._detect_pattern(successful)
            if success_pattern:
                self.lessons_learned.append({
                    'type': 'success',
                    'pattern': success_pattern,
                    'recommendation': 'Repeat this approach'
                })
        
        if failed:
            failure_pattern = self._detect_pattern(failed)
            if failure_pattern:
                self.lessons_learned.append({
                    'type': 'failure',
                    'pattern': failure_pattern,
                    'recommendation': 'Avoid this approach'
                })
    
    def get_recommendations(self, current_context):
        """
        Get recommendations based on learned patterns.
        """
        recommendations = []
        
        for lesson in self.lessons_learned:
            # Check if lesson is relevant to current context
            if any(keyword in current_context.lower() 
                  for keyword in lesson['pattern']['keywords']):
                recommendations.append(lesson['recommendation'])
        
        return recommendations


# Usage
consolidation = MemoryConsolidation()

# Analyze past memories
past_memories = [...]  # Load from database
consolidation.analyze_memories(past_memories)
consolidation.extract_lessons(past_memories)

# Get recommendations for current situation
current_context = "Implementing authentication for web application"
recommendations = consolidation.get_recommendations(current_context)
print("Based on past experience:", recommendations)
```

MEMORY IMPORTANCE SCORING
--------------------------

```python
def calculate_memory_importance(memory):
    """
    Calculate importance score for a memory (0-10).
    """
    score = 5.0  # Base score
    
    # Factor 1: Recency (0-2 points)
    age_hours = (datetime.now() - memory['timestamp']).total_seconds() / 3600
    recency_score = max(0, 2 - (age_hours / 24))
    score += recency_score
    
    # Factor 2: Access frequency (0-2 points)
    access_score = min(2, memory.get('access_count', 0) / 5)
    score += access_score
    
    # Factor 3: User-defined importance (0-2 points)
    user_importance = memory.get('metadata', {}).get('importance', 5)
    score += (user_importance / 5) * 2
    
    # Factor 4: Content type (0-2 points)
    content_type = memory.get('metadata', {}).get('type', '')
    type_scores = {
        'decision': 2.0,
        'preference': 1.5,
        'error': 1.5,
        'success': 1.0,
        'conversation': 0.5
    }
    score += type_scores.get(content_type, 0.5)
    
    # Factor 5: Outcome (0-2 points)
    outcome = memory.get('metadata', {}).get('outcome', '')
    if outcome == 'success':
        score += 1.5
    elif outcome == 'failure':
        score += 1.0  # Failures are also important to remember
    
    return min(10, score)


# Update memory importance periodically
def update_memory_importance(db):
    """
    Recalculate importance scores for all memories.
    """
    memories = db.query("SELECT * FROM ai_memory")
    
    for memory in memories:
        new_score = calculate_memory_importance(memory)
        db.execute(
            "UPDATE ai_memory SET importance = ? WHERE id = ?",
            (new_score, memory['id'])
        )
    
    print(f"✅ Updated importance scores for {len(memories)} memories")
```

=================================================================================
SECTION 6: PRACTICAL IMPLEMENTATION
=================================================================================

COMPLETE MEMORY SYSTEM
-----------------------

```python
class AIMemorySystem:
    """
    Complete AI memory management system.
    """
    
    def __init__(self, user_id, max_context_tokens=8000):
        self.user_id = user_id
        self.max_context_tokens = max_context_tokens
        
        # Components
        self.context_manager = ContextManager(max_context_tokens)
        self.checkpoint_manager = ContextCheckpoint()
        self.consolidation = MemoryConsolidation()
        
        # Storage
        self.db = self._init_database()
        self.vector_db = self._init_vector_db()
        self.cache = redis.Redis()
        
        # Load existing memories
        self._load_memories()
    
    def remember(self, content, memory_type='episodic', importance=5, metadata=None):
        """
        Store new memory.
        """
        # 1. Store in database
        memory_id = self.db.execute(
            "INSERT INTO ai_memory (user_id, memory_type, content, importance, metadata) "
            "VALUES (?, ?, ?, ?, ?) RETURNING id",
            (self.user_id, memory_type, content, importance, json.dumps(metadata or {}))
        )
        
        # 2. Store in vector database for semantic search
        self.vector_db.add(
            documents=[content],
            metadatas=[metadata or {}],
            ids=[f"mem_{memory_id}"]
        )
        
        # 3. Add to context manager
        priority = 'essential' if importance >= 8 else 'important' if importance >= 5 else 'optional'
        self.context_manager.add_context(content, priority, metadata)
        
        # 4. Cache in Redis for quick access
        self.cache.setex(
            f"memory:{self.user_id}:{memory_id}",
            timedelta(hours=24),
            json.dumps({'content': content, 'importance': importance})
        )
        
        print(f"✅ Memory stored: {memory_id}")
        return memory_id
    
    def recall(self, query, top_k=5):
        """
        Retrieve relevant memories.
        """
        # 1. Try cache first
        cached = self._check_cache(query)
        if cached:
            return cached
        
        # 2. Semantic search
        results = self.vector_db.query(
            query_texts=[query],
            n_results=top_k * 2
        )
        
        # 3. Get full memory details from database
        memory_ids = [r.replace('mem_', '') for r in results['ids'][0]]
        memories = self.db.query(
            f"SELECT * FROM ai_memory WHERE id IN ({','.join('?' * len(memory_ids))})",
            memory_ids
        )
        
        # 4. Rank by importance and recency
        ranked_memories = sorted(
            memories,
            key=lambda m: (m['importance'], m['created_at']),
            reverse=True
        )
        
        # 5. Update access count
        for memory in ranked_memories[:top_k]:
            self.db.execute(
                "UPDATE ai_memory SET access_count = access_count + 1, "
                "accessed_at = NOW() WHERE id = ?",
                (memory['id'],)
            )
        
        return ranked_memories[:top_k]
    
    def get_context(self):
        """
        Get current context for AI.
        """
        # 1. Get active context from context manager
        active_context = self.context_manager.get_active_context()
        
        # 2. Add user preferences
        preferences = self.db.query(
            "SELECT content FROM ai_memory WHERE user_id = ? AND memory_type = 'procedural' "
            "ORDER BY importance DESC LIMIT 5",
            (self.user_id,)
        )
        
        pref_text = "\n".join([p['content'] for p in preferences])
        
        # 3. Combine
        full_context = f"""
{active_context}

USER PREFERENCES:
{pref_text}
"""
        
        return full_context
    
    def consolidate(self):
        """
        Consolidate memories and learn patterns.
        """
        # 1. Get all memories
        memories = self.db.query(
            "SELECT * FROM ai_memory WHERE user_id = ?",
            (self.user_id,)
        )
        
        # 2. Analyze and extract patterns
        self.consolidation.analyze_memories(memories)
        self.consolidation.extract_lessons(memories)
        
        # 3. Update importance scores
        for memory in memories:
            new_importance = calculate_memory_importance(memory)
            self.db.execute(
                "UPDATE ai_memory SET importance = ? WHERE id = ?",
                (new_importance, memory['id'])
            )
        
        # 4. Archive very old, low-importance memories
        self.db.execute(
            "DELETE FROM ai_memory WHERE user_id = ? AND importance < 3 "
            "AND created_at < NOW() - INTERVAL '90 days'",
            (self.user_id,)
        )
        
        print("✅ Memory consolidation complete")
    
    def checkpoint(self, name=None):
        """
        Create checkpoint of current state.
        """
        context_data = {
            'user_id': self.user_id,
            'context': self.context_manager.contexts,
            'patterns': self.consolidation.patterns,
            'lessons': self.consolidation.lessons_learned
        }
        
        return self.checkpoint_manager.save_checkpoint(context_data, name)
    
    def restore(self, checkpoint_name):
        """
        Restore from checkpoint.
        """
        data = self.checkpoint_manager.load_checkpoint(checkpoint_name)
        if data:
            self.context_manager.contexts = data['context']
            self.consolidation.patterns = data['patterns']
            self.consolidation.lessons_learned = data['lessons']
            print("✅ Memory restored from checkpoint")
    
    def _init_database(self):
        # Initialize database connection
        pass
    
    def _init_vector_db(self):
        # Initialize vector database
        pass
    
    def _load_memories(self):
        # Load recent memories into context
        pass
    
    def _check_cache(self, query):
        # Check Redis cache
        pass


# Usage Example
memory_system = AIMemorySystem(user_id="user123", max_context_tokens=8000)

# Store memories
memory_system.remember(
    "User prefers PostgreSQL for this project",
    memory_type='procedural',
    importance=8,
    metadata={'category': 'preference', 'project': 'ecommerce'}
)

memory_system.remember(
    "Successfully implemented JWT authentication",
    memory_type='episodic',
    importance=7,
    metadata={'category': 'success', 'feature': 'authentication'}
)

# Recall relevant memories
relevant_memories = memory_system.recall("How to implement authentication?")
for memory in relevant_memories:
    print(f"- {memory['content']} (importance: {memory['importance']})")

# Get context for AI
context = memory_system.get_context()
print("Current context:", context)

# Consolidate memories periodically
memory_system.consolidate()

# Create checkpoint
memory_system.checkpoint(name='after_auth_implementation')
```

=================================================================================
SECTION 7: BEST PRACTICES
=================================================================================

MEMORY MANAGEMENT GUIDELINES
-----------------------------

1. PRIORITIZE RUTHLESSLY
   ✅ Keep only essential information in active context
   ✅ Archive or summarize old information
   ✅ Use importance scoring to decide what to keep
   ❌ Don't try to keep everything in context

2. STRUCTURE YOUR MEMORY
   ✅ Use clear categories (episodic, semantic, procedural)
   ✅ Add metadata for better retrieval
   ✅ Maintain consistent format
   ❌ Don't mix different types of information

3. UPDATE INCREMENTALLY
   ✅ Update specific parts of context
   ✅ Use state management patterns
   ✅ Track changes over time
   ❌ Don't replace entire context repeatedly

4. CONSOLIDATE REGULARLY
   ✅ Summarize old conversations
   ✅ Extract patterns and lessons
   ✅ Update importance scores
   ❌ Don't let memory grow unbounded

5. USE MULTIPLE STORAGE LAYERS
   ✅ Working memory: Current context
   ✅ Short-term: Session cache (Redis)
   ✅ Long-term: Database + Vector DB
   ✅ External: Files, GitHub, Notion
   ❌ Don't rely on single storage method

6. IMPLEMENT CHECKPOINTS
   ✅ Save state at key milestones
   ✅ Enable recovery from failures
   ✅ Track progress over time
   ❌ Don't lose work due to context loss

7. LEARN FROM EXPERIENCE
   ✅ Detect patterns in past interactions
   ✅ Extract lessons learned
   ✅ Apply knowledge to new situations
   ❌ Don't repeat past mistakes

CONTEXT RETENTION CHECKLIST
----------------------------

Before starting a task:
□ Load relevant long-term memories
□ Check for existing checkpoints
□ Review user preferences
□ Load project context

During the task:
□ Update context incrementally
□ Store important decisions
□ Create periodic checkpoints
□ Monitor context size

After the task:
□ Summarize the session
□ Store lessons learned
□ Update importance scores
□ Create final checkpoint

Maintenance:
□ Consolidate memories weekly
□ Archive old, low-importance memories
□ Update patterns and lessons
□ Optimize storage and retrieval

=================================================================================
SECTION 8: INTEGRATION WITH OTHER MODULES
=================================================================================

INTEGRATION POINTS
------------------

1. WITH MODULE 16 (MCP Integration)
   - Use Context7 for up-to-date documentation
   - Store project mappings in long-term memory
   - Remember tool preferences and workflows

2. WITH MODULE 17 (Thinking Framework)
   - Store problem-solving patterns
   - Remember successful approaches
   - Learn from past decisions

3. WITH MODULE 18 (Task AI)
   - Remember task preferences
   - Store workflow patterns
   - Track task history

4. WITH MODULE 19 (Context Engineering)
   - Share context state
   - Coordinate memory updates
   - Integrate learning systems

5. WITH MODULE 15 (MCP)
   - Use GitHub for code memory
   - Use Notion for documentation memory
   - Use Sentry for error memory

COMPLETE WORKFLOW EXAMPLE
--------------------------

```python
# Initialize all systems
memory_system = AIMemorySystem(user_id="user123")
context_engineer = ContextEngineer()  # From Module 19
task_ai = TaskAI()  # From Module 18

# 1. Start new task
task = "Implement user authentication"

# 2. Load relevant memories
memories = memory_system.recall(task)
context = memory_system.get_context()

# 3. Get recommendations from past experience
recommendations = memory_system.consolidation.get_recommendations(task)

# 4. Create tasks based on memory and context
tasks = task_ai.create_tasks(task, context, recommendations)

# 5. Execute tasks while updating memory
for subtask in tasks:
    result = execute_task(subtask)
    
    # Store result in memory
    memory_system.remember(
        f"Completed: {subtask.name}\nResult: {result}",
        memory_type='episodic',
        importance=7,
        metadata={'task': task, 'outcome': 'success' if result.success else 'failure'}
    )
    
    # Create checkpoint
    if subtask.is_milestone:
        memory_system.checkpoint(name=f"after_{subtask.name}")

# 6. Consolidate learnings
memory_system.consolidate()

# 7. Store final summary
summary = create_summary(tasks)
memory_system.remember(
    summary,
    memory_type='semantic',
    importance=9,
    metadata={'type': 'project_summary', 'project': task}
)
```

=================================================================================
END OF MEMORY MANAGEMENT MODULE
=================================================================================

For more information on related topics:
- Module 16: MCP Integration Layer
- Module 17: Thinking Framework
- Module 18: Task AI & Automation
- Module 19: Context Engineering & Learning System

Version: Latest
Last Updated: 2025-11-03

