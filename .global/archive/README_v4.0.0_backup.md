# Global Guidelines v4.0.0

**Professional AI-Assisted Development Framework**

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/hamfarid/global/releases/tag/v4.0.0)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production-brightgreen.svg)](https://github.com/hamfarid/global)

---

## 🎉 What's New in v4.0.0

**Interactive System Edition** - The biggest update yet!

✨ **Interactive Project Setup** - Augment asks 7 questions and configures everything  
🔧 **Configuration Management** - Project-specific settings in `.global/project_config.json`  
🚀 **Automated Deployment** - `start deploy` command for full automation  
📊 **State Management** - Development/Production phases with intelligent behavior  
🎯 **Admin Panel Auto-Open** - Professional deployment experience  
📚 **727 new lines** of comprehensive documentation (Section 64)

[Read the full changelog →](CHANGELOG_v4.0.0.md)

---

## 📖 Overview

**Global Guidelines** is a comprehensive framework that transforms how AI assistants (like Augment) work with your projects. It provides:

- **64 sections** of best practices and patterns
- **5 automated tools** for code analysis and management
- **6 integration scripts** for seamless setup
- **Interactive configuration** system
- **Automated deployment** workflow
- **13 practical examples**

**Result:** Professional, intelligent, context-aware AI assistance from development to production.

---

## 🚀 Quick Start

### 1. Install

```bash
# Clone the repository
git clone https://github.com/hamfarid/global.git
cd global

# Or download the latest release
wget https://github.com/hamfarid/global/releases/download/v4.0.0/global_v4.0.0_complete.tar.gz
tar -xzf global_v4.0.0_complete.tar.gz
```

### 2. Use with Augment

```bash
# Copy the prompt to Augment
cp GLOBAL_GUIDELINES_FINAL.txt ~/augment/prompts/global_guidelines.txt

# Or use the versioned file
cp GLOBAL_GUIDELINES_v4.0.0.txt ~/augment/prompts/
```

### 3. Start a Project

```
User: "I want to create a new e-commerce platform"

Augment: "Great! Let me collect some information first..."

[Interactive questionnaire - 7 questions]

Augment: "✓ Configuration saved!

Your e-commerce platform is set up:
- Development mode
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Database: ecommerce_db
- Sample data will be added

Ready to start building!"
```

### 4. Deploy When Ready

```
User: "start deploy"

[Automated deployment - 7 steps]

🎉 Deployment successful!
Admin panel and setup wizard are now open.
```

---

## 💡 Key Features

### 1. Interactive Setup

**No more hardcoded values!**

Augment asks you about:
- Project phase (Development/Production)
- Project name
- Port configuration
- Database settings
- Environment (Local/External)
- Admin credentials (Production)

**Everything is saved and used throughout the project.**

### 2. Configuration Management

**File:** `.global/project_config.json`

```json
{
  "project": {
    "name": "E-Commerce Platform",
    "phase": "development",
    "deployed": false
  },
  "ports": {
    "frontend": 3000,
    "backend": 5000,
    "database": 5432
  },
  "database": {
    "name": "ecommerce_db",
    "preserve_data": false,
    "add_sample_data": true
  }
}
```

### 3. State Management

**Development Phase:**
- Debug mode enabled
- Sample data available
- Destructive operations allowed
- Detailed logging

**Production Phase:**
- Debug mode disabled
- Data preservation mandatory
- Security hardened
- Automatic backups

### 4. Automated Deployment

**One command:**
```bash
./scripts/start_deploy.sh
```

**7 automated steps:**
1. Pre-deployment checks
2. Backup current state
3. Build production assets
4. Database setup
5. Security hardening
6. Launch application
7. Post-deployment tasks

**Result:**
- Admin panel opens automatically
- Setup wizard opens automatically
- Credentials displayed
- Production ready

---

## 📦 What's Included

### The Prompt (9,508 lines)

- **64 sections** of comprehensive guidelines
- **Section 64** - Interactive Project Setup (727 lines)
- **All best practices** and patterns
- **Complete documentation**

**Files:**
- `GLOBAL_GUIDELINES_v4.0.0.txt` - Versioned prompt
- `GLOBAL_GUIDELINES_FINAL.txt` - Latest version

### Tools (5)

1. **analyze_dependencies.py** - Dependency analysis
2. **detect_code_duplication.py** - Code duplication detection
3. **smart_merge.py** - Intelligent file merging
4. **validate_structure.py** - Project structure validation
5. **project_config_manager.py** ⭐ - Configuration management

### Scripts (6)

1. **integrate.sh** - Install Global Guidelines in existing project
2. **configure.sh** - Configure components
3. **apply.sh** - Apply components
4. **update.sh** - Update Global Guidelines
5. **uninstall.sh** - Uninstall Global Guidelines
6. **start_deploy.sh** ⭐ - Automated deployment

### Examples (13 files)

- **Central Registry** pattern (4 files)
- **Lazy Loading** pattern (6 files)
- **Plugin System** pattern (3 files)

### Documentation

- **INTERACTIVE_SYSTEM_GUIDE.md** ⭐ - Complete user guide
- **AUGMENT_INTEGRATION_GUIDE.md** - Integration guide
- **INIT_PY_BEST_PRACTICES.md** - __init__.py patterns
- **CHANGELOG_v4.0.0.md** - Release notes
- **FINAL_DELIVERY_v4.0.0.md** - Delivery summary

---

## 🎯 Use Cases

### Use Case 1: New Development Project

```
User: "Create a task management app"

Augment: [Interactive setup]

✓ Configuration saved!
✓ Development environment ready
✓ Sample data will be added
✓ Ready to start building
```

### Use Case 2: Existing Production App

```
User: "Work on my production e-commerce site"

Augment: [Load configuration]

✓ Production mode enabled
✓ Data preservation ON
✓ Destructive operations require confirmation
✓ Ready to work safely
```

### Use Case 3: Deployment

```
User: "start deploy"

Augment: [7-step automated deployment]

✓ Checks passed
✓ Backup created
✓ Production build ready
✓ Database migrated
✓ Security hardened
✓ Application launched
🎉 Deployment successful!
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **Lines** | 9,508 |
| **Size** | 236K |
| **Sections** | 64 |
| **Tools** | 5 |
| **Scripts** | 6 |
| **Examples** | 13 files |
| **Documentation** | 10+ guides |

---

## 🛠️ Installation

### Option 1: Use with Augment (Recommended)

```bash
# Copy the prompt
cp GLOBAL_GUIDELINES_FINAL.txt ~/augment/prompts/

# Start using with Augment
# Augment will automatically run interactive setup on first use
```

### Option 2: Integrate into Existing Project

```bash
# Run the integration script
cd /path/to/your/project
/path/to/global/scripts/integrate.sh

# This will:
# - Create .global/ directory
# - Copy tools and scripts
# - Set up configuration
```

### Option 3: Manual Setup

```bash
# Copy files manually
cp -r tools/ /path/to/your/project/.global/tools/
cp -r scripts/ /path/to/your/project/.global/scripts/
cp -r examples/ /path/to/your/project/.global/examples/

# Run configuration setup
python3 .global/tools/project_config_manager.py setup
```

---

## 📚 Documentation

### Getting Started

1. **[Interactive System Guide](INTERACTIVE_SYSTEM_GUIDE.md)** - Complete user guide
2. **[Augment Integration Guide](AUGMENT_INTEGRATION_GUIDE.md)** - How to use with Augment
3. **[Changelog v4.0.0](CHANGELOG_v4.0.0.md)** - What's new

### Technical Documentation

- **[Section 64](SECTION_64_INTERACTIVE_PROJECT_SETUP.md)** - Interactive setup system
- **[__init__.py Best Practices](INIT_PY_BEST_PRACTICES.md)** - Python package patterns
- **[Flows](flows/README.md)** - Development workflows

### Examples

- **[init_py_patterns](examples/init_py_patterns/README.md)** - __init__.py patterns

---

## 🎓 Learning Path

### For New Users (30 minutes)

1. **Read:** [Interactive System Guide](INTERACTIVE_SYSTEM_GUIDE.md) (15 min)
2. **Read:** [Augment Integration Guide](AUGMENT_INTEGRATION_GUIDE.md) (10 min)
3. **Try:** Interactive setup (5 min)

### For Advanced Users (1 hour)

1. **Review:** [Section 64](SECTION_64_INTERACTIVE_PROJECT_SETUP.md) (30 min)
2. **Explore:** Tools and scripts (20 min)
3. **Customize:** Configuration and workflows (10 min)

---

## 💻 Commands Reference

### Configuration

```bash
# Interactive setup
python3 tools/project_config_manager.py setup

# Show current configuration
python3 tools/project_config_manager.py show

# Generate .env file
python3 tools/project_config_manager.py env

# Deploy to production
python3 tools/project_config_manager.py deploy
```

### Deployment

```bash
# Start deployment process
./scripts/start_deploy.sh

# Or in Augment
User: "start deploy"
```

### Integration

```bash
# Install in existing project
./scripts/integrate.sh

# Update to latest version
./scripts/update.sh

# Uninstall
./scripts/uninstall.sh
```

---

## 🔄 Version History

| Version | Date | Highlights |
|---------|------|------------|
| **v4.0.0** | 2025-11-02 | Interactive system, automated deployment |
| v3.9.2 | 2025-11-02 | Generic variables, no hardcoded values |
| v3.9.1 | 2025-11-02 | Optimization, code cleanup |
| v3.9.0 | 2025-11-02 | Repository documentation (Section 63) |
| v3.8.0 | 2025-11-01 | Flows and integration scripts |
| v3.7.0 | 2025-11-01 | __init__.py patterns (Section 62) |
| v3.6.0 | 2025-11-01 | Quality audit and improvements |
| v3.5.0 | 2025-01-15 | Advanced tooling |
| v3.4.0 | 2024-12-15 | Quality & verification |
| v3.3.0 | 2024-11-15 | Problem solver edition |
| v3.2.0 | 2024-10-28 | Production-ready edition |

[View all releases →](https://github.com/hamfarid/global/releases)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

**Areas for contribution:**
- New tools
- New patterns
- Documentation improvements
- Bug fixes
- Examples

---

## 📞 Support

### Documentation

- **[Interactive System Guide](INTERACTIVE_SYSTEM_GUIDE.md)** - Complete guide
- **[Section 64](SECTION_64_INTERACTIVE_PROJECT_SETUP.md)** - Technical details
- **[Changelog](CHANGELOG_v4.0.0.md)** - Release notes

### Community

- **GitHub Issues:** [Report bugs or request features](https://github.com/hamfarid/global/issues)
- **Discussions:** [Ask questions or share ideas](https://github.com/hamfarid/global/discussions)

### Quick Help

```bash
# Show configuration
python3 tools/project_config_manager.py show

# Read guide
cat INTERACTIVE_SYSTEM_GUIDE.md | less

# Check version
cat VERSION
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Augment** - For inspiring this framework
- **Community** - For feedback and contributions
- **Contributors** - For improvements and bug fixes

---

## 🎯 Roadmap

### v4.1.0 (Planned)

- [ ] Multi-project support
- [ ] Project templates
- [ ] Automated testing integration
- [ ] CI/CD pipeline generation
- [ ] Cloud deployment support
- [ ] **Auto-read existing projects** ⭐
- [ ] **Generate project-specific prompts** ⭐

### v5.0.0 (Future)

- [ ] AI-powered configuration suggestions
- [ ] Auto-detection of project type
- [ ] Smart dependency management
- [ ] Performance optimization recommendations
- [ ] Security vulnerability scanning

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=hamfarid/global&type=Date)](https://star-history.com/#hamfarid/global&Date)

---

## 📈 Project Stats

![GitHub stars](https://img.shields.io/github/stars/hamfarid/global?style=social)
![GitHub forks](https://img.shields.io/github/forks/hamfarid/global?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/hamfarid/global?style=social)

---

## 🚀 Get Started Now!

```bash
# Clone the repository
git clone https://github.com/hamfarid/global.git

# Copy the prompt to Augment
cp global/GLOBAL_GUIDELINES_FINAL.txt ~/augment/prompts/

# Start building with intelligent AI assistance!
```

**Welcome to the future of AI-assisted development!** 🎉

---

**Version:** 4.0.0  
**Release Date:** 2025-11-02  
**Status:** ✅ Production Ready  
**Recommended:** Yes ⭐⭐⭐

**Happy Coding!** 🚀

