# Global Guidelines - Modular Prompts System

Version: 5.0.0

## Overview

The Global Guidelines project has been split into modular, specialized prompts for better organization, performance, and maintainability.

## Structure

```
prompts/
├── 00_MASTER.txt                 # Main orchestrator prompt
├── core/
│   ├── 01_requirements.txt       # Project requirements gathering
│   ├── 02_analysis.txt           # Project analysis
│   └── 03_planning.txt           # Project planning
├── architecture/
│   ├── 10_backend.txt            # Backend development
│   ├── 11_frontend.txt           # Frontend development
│   ├── 12_database.txt           # Database design
│   └── 13_api.txt                # API design
├── security/
│   ├── 20_security.txt           # Security best practices
│   └── 21_authentication.txt     # Authentication systems
├── quality/
│   ├── 30_quality.txt            # Code quality
│   └── 31_testing.txt            # Testing strategies
├── deployment/
│   └── 40_deployment.txt         # Deployment & DevOps
└── templates/
    └── 50_templates.txt          # Project templates
```

## Usage

### For Augment

1. **Load MASTER prompt:**
   ```
   Load: prompts/00_MASTER.txt
   ```

2. **The MASTER will automatically load relevant sub-prompts based on context**

### For Manual Use

Load specific prompts as needed:

```
# For backend development
Load: prompts/10_backend.txt

# For security
Load: prompts/20_security.txt

# For deployment
Load: prompts/40_deployment.txt
```

## Benefits

✅ **Faster Loading** - Load only what you need  
✅ **Better Organization** - Clear separation of concerns  
✅ **Easier Maintenance** - Update individual modules  
✅ **Flexible Usage** - Mix and match as needed  
✅ **Scalable** - Easy to add new modules

## Prompt Sizes

| Prompt | Lines | Size | Purpose |
|--------|-------|------|---------|
| 00_MASTER.txt | ~500 | 12KB | Orchestration |
| 01_requirements.txt | ~90 | 2KB | Requirements |
| 02_analysis.txt | ~580 | 14KB | Analysis |
| 03_planning.txt | ~600 | 15KB | Planning |
| 10_backend.txt | ~900 | 22KB | Backend |
| 11_frontend.txt | ~700 | 17KB | Frontend |
| 12_database.txt | ~600 | 15KB | Database |
| 13_api.txt | ~800 | 20KB | APIs |
| 20_security.txt | ~600 | 15KB | Security |
| 21_authentication.txt | ~500 | 12KB | Auth |
| 30_quality.txt | ~600 | 15KB | Quality |
| 31_testing.txt | ~500 | 12KB | Testing |
| 40_deployment.txt | ~600 | 15KB | Deployment |
| 50_templates.txt | ~400 | 10KB | Templates |

**Total:** ~7,970 lines, ~196KB

## Migration from v4.x

The monolithic `GLOBAL_GUIDELINES_v4.x.txt` has been split into these modules.

**Old way:**
```
Load entire 10,700-line prompt
```

**New way:**
```
Load 00_MASTER.txt (500 lines)
+ Load relevant modules as needed
```

## Contributing

When adding new content:

1. Identify the appropriate module
2. Update the specific prompt file
3. Update this README if adding new modules
4. Test with MASTER prompt

## Version History

- **v5.0.0** - Modular prompts system
- **v4.2.0** - Added project templates
- **v4.1.0** - Added project analyzer
- **v4.0.0** - Interactive setup system
- **v3.9.0** - Added `__init__.py` best practices
- **v3.6.0** - Quality audit and fixes

## License

MIT License - See LICENSE file

## Support

- GitHub: https://github.com/hamfarid/global
- Issues: https://github.com/hamfarid/global/issues
