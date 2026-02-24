#!/bin/bash

################################################################################
# Global Guidelines Setup Script
# Version: 8.0.0
# Description: Complete setup script for Global Guidelines in any project
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(pwd)"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_warning "$1 is not installed"
        return 1
    fi
}

################################################################################
# Main Setup Functions
################################################################################

check_prerequisites() {
    print_header "Checking Prerequisites"
    
    local all_ok=true
    
    # Check required commands
    check_command "git" || all_ok=false
    check_command "python3" || all_ok=false
    
    # Check optional commands
    check_command "node" || print_info "Node.js not found (optional)"
    check_command "psql" || print_info "PostgreSQL not found (optional)"
    check_command "redis-cli" || print_info "Redis not found (optional)"
    
    if [ "$all_ok" = false ]; then
        print_error "Some required tools are missing. Please install them first."
        exit 1
    fi
    
    print_success "All prerequisites satisfied"
    echo ""
}

check_existing_setup() {
    print_header "Checking Existing Setup"
    
    local has_existing=false
    
    # Check for existing directories
    if [ -d ".memory" ]; then
        print_warning ".memory/ directory already exists"
        has_existing=true
    fi
    
    if [ -d ".ai_maps" ]; then
        print_warning ".ai_maps/ directory already exists"
        has_existing=true
    fi
    
    if [ -d ".global" ]; then
        print_warning ".global/ directory already exists"
        has_existing=true
    fi
    
    if [ "$has_existing" = true ]; then
        echo ""
        read -p "Existing setup detected. Do you want to (s)kip, (o)verwrite, or (b)ackup? [s/o/b]: " choice
        case "$choice" in
            s|S)
                print_info "Skipping existing directories"
                return 1
                ;;
            o|O)
                print_warning "Will overwrite existing directories"
                return 0
                ;;
            b|B)
                print_info "Creating backup..."
                BACKUP_DIR="global_backup_$(date +%Y%m%d_%H%M%S)"
                mkdir -p "$BACKUP_DIR"
                [ -d ".memory" ] && cp -r .memory "$BACKUP_DIR/"
                [ -d ".ai_maps" ] && cp -r .ai_maps "$BACKUP_DIR/"
                [ -d ".global" ] && cp -r .global "$BACKUP_DIR/"
                print_success "Backup created: $BACKUP_DIR"
                return 0
                ;;
            *)
                print_error "Invalid choice. Exiting."
                exit 1
                ;;
        esac
    fi
    
    print_success "No existing setup found"
    echo ""
    return 0
}

create_memory_structure() {
    print_header "Creating Memory Structure"
    
    # Create memory directories
    mkdir -p .memory/{conversations,knowledge,preferences,state,checkpoints,vectors}
    
    # Create .gitkeep files
    for dir in conversations knowledge preferences state checkpoints vectors; do
        touch ".memory/$dir/.gitkeep"
    done
    
    print_success "Memory directories created"
    
    # Create memory README
    cat > .memory/README.md << 'EOF'
# AI Memory System

This directory contains the AI memory system for maintaining context and learning.

## Structure

- `conversations/` - Conversation history
- `knowledge/` - Knowledge base (facts, patterns, solutions)
- `preferences/` - User and project preferences
- `state/` - Current state and context
- `checkpoints/` - State checkpoints
- `vectors/` - Vector database for semantic search

## File Formats

### Conversation
```json
{
  "conversation_id": "conv_20231103_001",
  "user_id": "user123",
  "messages": [...],
  "timestamp": "2023-11-03T10:00:00Z"
}
```

### Knowledge
```json
{
  "id": "know_001",
  "type": "semantic|episodic|procedural",
  "content": "...",
  "importance": 8,
  "metadata": {...},
  "created_at": "2023-11-03T10:00:00Z"
}
```

### Preferences
```json
{
  "user_id": "user123",
  "project": "MyProject",
  "preferences": {...},
  "updated_at": "2023-11-03T10:00:00Z"
}
```

## Security

⚠️ **Important:** This directory contains local data only.
- Never commit data files to Git
- .gitignore is configured to exclude data files
- Only structure and documentation are tracked

## Maintenance

- Clean old conversations: `find conversations/ -mtime +30 -delete`
- Backup: `tar -czf memory_backup.tar.gz .memory/`
- Restore: `tar -xzf memory_backup.tar.gz`

## Database Setup (Optional)

For production use, consider:
- PostgreSQL for long-term memory
- Redis for short-term memory
- ChromaDB for vector storage
EOF
    
    print_success "Memory README created"
    
    # Create setup script
    cat > .memory/setup_example.py << 'EOF'
#!/usr/bin/env python3
"""
Memory System Setup Script
Creates initial memory structure and example files
"""

import json
import os
from datetime import datetime
from pathlib import Path

def setup_memory():
    """Setup memory system with example files."""
    
    print("🧠 Setting up AI Memory System...")
    print()
    
    # Get project info
    project_name = input("Project name: ").strip() or "MyProject"
    user_id = input("User ID (default: dev): ").strip() or "dev"
    
    # Create preferences
    preferences = {
        "user_id": user_id,
        "project": project_name,
        "preferences": {
            "language": "python",
            "framework": "flask",
            "database": "postgresql",
            "testing": "pytest"
        },
        "updated_at": datetime.now().isoformat()
    }
    
    prefs_file = Path(f"preferences/{user_id}.json")
    with open(prefs_file, 'w') as f:
        json.dump(preferences, f, indent=2)
    print(f"✅ Created: {prefs_file}")
    
    # Create initial state
    state = {
        "user_id": user_id,
        "current_project": project_name,
        "current_phase": "setup",
        "context": {
            "last_activity": datetime.now().isoformat(),
            "session_count": 1
        },
        "updated_at": datetime.now().isoformat()
    }
    
    state_file = Path("state/current_state.json")
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✅ Created: {state_file}")
    
    # Create example knowledge
    knowledge = {
        "id": "know_001",
        "type": "procedural",
        "content": f"Project {project_name} uses Global Guidelines v7.1.1",
        "importance": 9,
        "metadata": {
            "category": "setup",
            "project": project_name
        },
        "created_at": datetime.now().isoformat()
    }
    
    know_file = Path("knowledge/know_001.json")
    with open(know_file, 'w') as f:
        json.dump(knowledge, f, indent=2)
    print(f"✅ Created: {know_file}")
    
    print()
    print("✅ Memory system setup complete!")
    print()
    print("Next steps:")
    print("1. Review .memory/README.md")
    print("2. Configure database (optional)")
    print("3. Start using the system")

if __name__ == '__main__':
    setup_memory()
EOF
    
    chmod +x .memory/setup_example.py
    print_success "Setup script created and made executable"
    
    echo ""
}

create_ai_maps_structure() {
    print_header "Creating AI Maps Structure"
    
    # Create maps directory
    mkdir -p .ai_maps
    
    print_success "AI maps directory created"
    
    # Create maps README
    cat > .ai_maps/README.md << 'EOF'
# AI Project Maps

This directory contains the 7 mandatory project maps required by Global Guidelines Module 16.

## Required Maps

1. **01_project_structure.mmd** - Mermaid diagram of project structure
2. **02_imports_exports.json** - JSON mapping of imports/exports
3. **03_class_definitions.puml** - PlantUML class diagram
4. **04_libraries_dependencies.json** - JSON of all dependencies
5. **05_api_endpoints.yaml** - OpenAPI specification
6. **06_database_schema.sql** - SQL schema + ERD
7. **07_configuration.json** - Environment configuration

## Why These Maps?

These maps help AI to:
- ✅ Understand project structure instantly
- ✅ Navigate codebase efficiently
- ✅ Make informed architectural decisions
- ✅ Avoid breaking changes
- ✅ Suggest improvements accurately
- ✅ Generate documentation automatically

## Creating Maps

### Manual Creation
Follow the templates in Global Guidelines ACTIVATION_GUIDE_STORE.md

### Automated Creation
Use the project_config_manager.py tool:
```bash
python .global/project_config_manager.py generate-maps
```

## Updating Maps

Update maps when:
- ✅ Adding new features
- ✅ Changing architecture
- ✅ Adding dependencies
- ✅ Modifying API
- ✅ Changing database schema
- ✅ Updating configuration

## Tools

Generate diagrams:
```bash
# Mermaid
npx @mermaid-js/mermaid-cli -i 01_project_structure.mmd -o structure.png

# PlantUML
plantuml 03_class_definitions.puml
```

## Integration

These maps are automatically loaded by:
- Module 16: MCP Integration Layer
- Module 60: Memory Management
- All MCP servers that need project context
EOF
    
    print_success "AI maps README created"
    
    # Create template files
    cat > .ai_maps/01_project_structure.mmd << 'EOF'
graph TD
    Project[Project Name]
    
    Project --> Backend[Backend]
    Project --> Frontend[Frontend]
    Project --> Database[Database]
    
    Backend --> API[API Routes]
    Backend --> Models[Models]
    Backend --> Controllers[Controllers]
    
    Frontend --> Components[Components]
    Frontend --> Pages[Pages]
    Frontend --> Utils[Utils]
    
    Database --> Schema[Schema]
    Database --> Migrations[Migrations]
EOF
    
    print_success "Project structure template created"
    
    cat > .ai_maps/02_imports_exports.json << 'EOF'
{
  "backend": {
    "exports": [],
    "imports": {}
  },
  "frontend": {
    "exports": [],
    "imports": {}
  }
}
EOF
    
    print_success "Imports/exports template created"
    
    echo ""
}

create_global_config() {
    print_header "Creating Global Configuration"
    
    # Create .global directory
    mkdir -p .global
    
    print_success ".global directory created"
    
    # Create project config
    cat > .global/project_config.json << EOF
{
  "project": {
    "name": "$(basename "$PROJECT_DIR")",
    "version": "1.0.0",
    "created_at": "$(date -Iseconds)",
    "global_guidelines_version": "7.2.0"
  },
  "setup": {
    "memory_enabled": true,
    "ai_maps_enabled": true,
    "mcp_enabled": false
  },
  "paths": {
    "memory": ".memory",
    "ai_maps": ".ai_maps",
    "global": ".global"
  }
}
EOF
    
    print_success "Project config created"
    
    echo ""
}

update_gitignore() {
    print_header "Updating .gitignore"
    
    # Check if .gitignore exists
    if [ ! -f ".gitignore" ]; then
        touch .gitignore
        print_info "Created new .gitignore"
    fi
    
    # Check if already has our rules
    if grep -q "# Global Guidelines" .gitignore; then
        print_warning ".gitignore already contains Global Guidelines rules"
        return
    fi
    
    # Add our rules
    cat >> .gitignore << 'EOF'

# Global Guidelines - AI Memory System (local only)
.memory/conversations/*.json
.memory/knowledge/*.json
.memory/preferences/*.json
.memory/state/*.json
.memory/checkpoints/*.json
.memory/vectors/*
!.memory/vectors/.gitkeep
*.db
*.sqlite
*.sqlite3
redis-data/
chroma_data/
memory_backups/

# Global Guidelines - Project Config (local only)
.global/project_config.json

# Keep structure
!.memory/README.md
!.memory/setup_example.py
!.ai_maps/README.md
!.ai_maps/*.mmd
!.ai_maps/*.json
!.ai_maps/*.yaml
!.ai_maps/*.sql
!.ai_maps/*.puml
EOF
    
    print_success ".gitignore updated"
    
    echo ""
}

run_project_manager() {
    print_header "Running Project Config Manager"
    
    # Check if project_config_manager.py exists in global repo
    if [ -f "$SCRIPT_DIR/.global/tools/project_config_manager.py" ]; then
        print_info "Found project_config_manager.py in Global Guidelines repo"
        
        # Copy to .global
        cp "$SCRIPT_DIR/.global/tools/project_config_manager.py" .global/
        print_success "Copied project_config_manager.py to .global/"
        
        # Run setup
        print_info "Running interactive setup..."
        echo ""
        python3 .global/project_config_manager.py setup
        
    else
        print_warning "project_config_manager.py not found"
        print_info "You can run it manually later from Global Guidelines repo"
    fi
    
    echo ""
}

create_quick_start_guide() {
    print_header "Creating Quick Start Guide"
    
    cat > GLOBAL_GUIDELINES_QUICKSTART.md << 'EOF'
# Global Guidelines Quick Start

Welcome! Your project is now set up with Global Guidelines v7.1.1.

## 📁 What Was Created

### 1. Memory System (.memory/)
- `conversations/` - Conversation history
- `knowledge/` - Knowledge base
- `preferences/` - User preferences
- `state/` - Current state
- `checkpoints/` - State checkpoints
- `vectors/` - Vector database

### 2. AI Maps (.ai_maps/)
- Project structure map
- Imports/exports map
- Templates for other maps

### 3. Configuration (.global/)
- `project_config.json` - Project configuration
- `project_config_manager.py` - Management tool

## 🚀 Next Steps

### 1. Complete Memory Setup
```bash
cd .memory
python3 setup_example.py
```

### 2. Create Project Maps
Edit the templates in `.ai_maps/` or use the activation guide:
- See `ACTIVATION_GUIDE_STORE.md` in Global Guidelines repo
- Follow Section 2: Creating Mandatory Project Maps

### 3. Configure MCP Servers (Optional)
Create `.mcp_config.json` in project root:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

### 4. Use Global Guidelines

#### Option A: Modular (Recommended)
```bash
# Read MASTER prompt
cat ~/global/prompts/00_MASTER.txt

# Use specific modules
cat ~/global/prompts/10_backend.txt
cat ~/global/prompts/11_frontend.txt
cat ~/global/prompts/60_memory_management.txt
```

#### Option B: Unified
```bash
cat ~/global/GLOBAL_GUIDELINES_UNIFIED_v7.1.0.txt
```

## 📚 Documentation

- **Main README:** ~/global/README.md
- **Memory Guide:** .memory/README.md
- **AI Maps Guide:** .ai_maps/README.md
- **Activation Guide:** ~/global/ACTIVATION_GUIDE_STORE.md

## 🔧 Tools

### Project Config Manager
```bash
python3 .global/project_config_manager.py [command]

Commands:
  setup    - Interactive setup
  show     - Show current config
  env      - Generate .env file
  deploy   - Deploy configuration
```

### Memory Setup
```bash
cd .memory
python3 setup_example.py
```

## ✅ Checklist

- [ ] Run memory setup
- [ ] Create 7 mandatory maps
- [ ] Configure MCP servers (optional)
- [ ] Read relevant modules
- [ ] Create first checkpoint

## 📞 Support

- **Repository:** https://github.com/hamfarid/global
- **Issues:** https://github.com/hamfarid/global/issues
- **Docs:** ~/global/README.md

---

**Setup completed successfully! 🎉**

Start using Global Guidelines to build better software faster.
EOF
    
    print_success "Quick start guide created: GLOBAL_GUIDELINES_QUICKSTART.md"
    
    echo ""
}

create_admin_user() {
    print_header "Admin User Setup"
    
    # Check if admin already exists
    ADMIN_FILE=".memory/preferences/admin.json"
    
    if [ -f "$ADMIN_FILE" ]; then
        print_warning "Admin user already exists"
        echo ""
        read -p "Do you want to update admin user? [y/N]: " update_admin
        if [[ ! "$update_admin" =~ ^[Yy]$ ]]; then
            print_info "Keeping existing admin user"
            return 0
        fi
    fi
    
    echo ""
    print_info "Creating admin user..."
    echo ""
    
    # Get admin details
    read -p "Admin name (default: Admin User): " admin_name
    admin_name=${admin_name:-"Admin User"}
    
    read -p "Admin email (default: admin@example.com): " admin_email
    admin_email=${admin_email:-"admin@example.com"}
    
    read -p "Admin user ID (default: admin): " admin_id
    admin_id=${admin_id:-"admin"}
    
    # Generate admin file
    cat > "$ADMIN_FILE" << EOF
{
  "user_id": "$admin_id",
  "name": "$admin_name",
  "email": "$admin_email",
  "role": "admin",
  "permissions": [
    "read",
    "write",
    "delete",
    "manage_users",
    "manage_teams",
    "manage_settings"
  ],
  "created_at": "$(date -Iseconds)",
  "updated_at": "$(date -Iseconds)",
  "preferences": {
    "memory_retention_days": 90,
    "auto_cleanup": true,
    "sharing_default_level": "team",
    "analytics_enabled": true
  }
}
EOF
    
    print_success "Admin user created: $admin_name ($admin_email)"
    
    # Update project config with admin info
    if [ -f ".global/project_config.json" ]; then
        # Use Python to update JSON (more reliable than jq)
        python3 << PYTHON_EOF
import json
import sys

try:
    with open('.global/project_config.json', 'r') as f:
        config = json.load(f)
    
    config['admin'] = {
        'name': '$admin_name',
        'email': '$admin_email',
        'user_id': '$admin_id'
    }
    
    with open('.global/project_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print('✅ Updated project config with admin info')
except Exception as e:
    print(f'⚠️  Could not update project config: {e}', file=sys.stderr)
PYTHON_EOF
    fi
    
    echo ""
    print_info "Admin credentials saved to: $ADMIN_FILE"
    print_warning "Keep this file secure and do not commit to Git"
    echo ""
}

print_summary() {
    print_header "Setup Summary"
    
    echo "✅ Created directories:"
    echo "   - .memory/ (with 6 subdirectories)"
    echo "   - .ai_maps/"
    echo "   - .global/"
    echo ""
    
    echo "✅ Created files:"
    echo "   - .memory/README.md"
    echo "   - .memory/setup_example.py"
    if [ -f ".memory/preferences/admin.json" ]; then
        echo "   - .memory/preferences/admin.json (admin user)"
    fi
    echo "   - .ai_maps/README.md"
    echo "   - .ai_maps/01_project_structure.mmd"
    echo "   - .ai_maps/02_imports_exports.json"
    echo "   - .global/project_config.json"
    echo "   - GLOBAL_GUIDELINES_QUICKSTART.md"
    echo ""
    
    echo "✅ Updated:"
    echo "   - .gitignore"
    echo ""
    
    print_success "Setup completed successfully!"
    echo ""
    
    print_info "Next steps:"
    echo "1. Read GLOBAL_GUIDELINES_QUICKSTART.md"
    echo "2. Run: cd .memory && python3 setup_example.py"
    echo "3. Create the 7 mandatory project maps"
    echo "4. Start using Global Guidelines"
    echo ""
    
    print_info "For detailed instructions, see:"
    echo "   ~/global/ACTIVATION_GUIDE_STORE.md"
    echo ""
}

################################################################################
# Main Execution
################################################################################

main() {
    clear
    
    print_header "Global Guidelines Setup v8.0.0"
    echo ""
    echo "This script will set up Global Guidelines in your project."
    echo "Project directory: $PROJECT_DIR"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Check existing setup
    if ! check_existing_setup; then
        print_info "Skipping setup due to existing directories"
        exit 0
    fi
    
    # Create structures
    create_memory_structure
    create_ai_maps_structure
    create_global_config
    
    # Update gitignore
    update_gitignore
    
    # Create quick start guide
    create_quick_start_guide
    
    # Create admin user
    echo ""
    read -p "Do you want to create an admin user? [Y/n]: " create_admin
    if [[ ! "$create_admin" =~ ^[Nn]$ ]]; then
        create_admin_user
    else
        print_info "Skipping admin user creation"
    fi
    
    # Ask about project manager
    echo ""
    read -p "Do you want to run project_config_manager.py now? [y/N]: " run_pm
    if [[ "$run_pm" =~ ^[Yy]$ ]]; then
        run_project_manager
    else
        print_info "You can run it later: python3 .global/project_config_manager.py setup"
    fi
    
    # Print summary
    print_summary
    
    print_success "🎉 All done! Your project is ready for Global Guidelines."
}

# Run main function
main "$@"

