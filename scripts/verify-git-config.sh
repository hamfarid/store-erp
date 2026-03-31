#!/bin/bash

# ============================================================================
# Store ERP - Git Configuration Verification Script
# التحقق من إعدادات Git والفروع الصحيحة
# ============================================================================

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "🔍 Store ERP - Git Configuration Check"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# فحص 1: التحقق من تثبيت Git
# ============================================================================
echo "${BLUE}1️⃣  Checking Git installation...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "${GREEN}✅${NC} $GIT_VERSION"
else
    echo "${RED}❌ Git not installed${NC}"
    exit 1
fi
echo ""

# ============================================================================
# فحص 2: التحقق من معرّف المستخدم
# ============================================================================
echo "${BLUE}2️⃣  Checking Git user configuration...${NC}"
USER_NAME=$(git config --global user.name)
USER_EMAIL=$(git config --global user.email)

if [ -z "$USER_NAME" ] || [ -z "$USER_EMAIL" ]; then
    echo "${YELLOW}⚠️  Git user not configured globally${NC}"
    echo "   ${YELLOW}Run:${NC} git config --global user.name 'Your Name'"
    echo "   ${YELLOW}Run:${NC} git config --global user.email 'your@email.com'"
else
    echo "${GREEN}✅${NC} User: $USER_NAME <$USER_EMAIL>"
fi
echo ""

# ============================================================================
# فحص 3: التحقق من الفروع الموجودة
# ============================================================================
echo "${BLUE}3️⃣  Checking branches...${NC}"

# الفروع المطلوبة
REQUIRED_BRANCHES=("main" "develop")
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "   Current branch: ${GREEN}$CURRENT_BRANCH${NC}"
echo "   All branches:"
git branch -a | sed 's/^/   /'
echo ""

# ============================================================================
# فحص 4: التحقق من Remote URLs
# ============================================================================
echo "${BLUE}4️⃣  Checking remote URLs...${NC}"
git remote -v | sed 's/^/   /'
echo ""

# ============================================================================
# فحص 5: التحقق من الملفات الأساسية
# ============================================================================
echo "${BLUE}5️⃣  Checking required files...${NC}"

FILES_TO_CHECK=(
    ".github/CODEOWNERS"
    ".github/PULL_REQUEST_TEMPLATE.md"
    ".github/workflows/github-flow-ci.yml"
    ".github/workflows/hotfix.yml"
    ".github/workflows/release.yml"
    ".github/BRANCH_PROTECTION_RULES.md"
    "BRANCHING_STRATEGY.md"
    "QUICK_START_BRANCHING.md"
)

for file in "${FILES_TO_CHECK[@]}"; do
    if [ -f "$file" ]; then
        echo "${GREEN}✅${NC} $file"
    else
        echo "${RED}❌${NC} $file (missing)"
    fi
done
echo ""

# ============================================================================
# فحص 6: التحقق من الـ Commits الأخيرة
# ============================================================================
echo "${BLUE}6️⃣  Recent commits...${NC}"
git log --oneline -n 5 | sed 's/^/   /'
echo ""

# ============================================================================
# فحص 7: التحقق من الفروع غير المرغوبة
# ============================================================================
echo "${BLUE}7️⃣  Checking for old branches...${NC}"

# الفروع القديمة (أكثر من 30 يوم)
OLD_BRANCHES=$(git branch -a --merged | grep -v "^\*" | grep -v main | grep -v develop || true)

if [ -z "$OLD_BRANCHES" ]; then
    echo "${GREEN}✅${NC} No old branches found"
else
    echo "${YELLOW}⚠️  Found old merged branches:${NC}"
    echo "$OLD_BRANCHES" | sed 's/^/   /'
    echo "   ${YELLOW}Tip:${NC} Delete them with: git branch -d <branch-name>"
fi
echo ""

# ============================================================================
# فحص 8: التحقق من التغييرات غير المدمجة
# ============================================================================
echo "${BLUE}8️⃣  Checking uncommitted changes...${NC}"
STATUS=$(git status --porcelain)

if [ -z "$STATUS" ]; then
    echo "${GREEN}✅${NC} No uncommitted changes"
else
    echo "${YELLOW}⚠️  Uncommitted changes found:${NC}"
    echo "$STATUS" | sed 's/^/   /'
fi
echo ""

# ============================================================================
# فحص 9: التحقق من قواعس الأمان
# ============================================================================
echo "${BLUE}9️⃣  Security checks...${NC}"

# التحقق من وجود الملفات الحساسة
SENSITIVE_FILES=(".env" ".env.local" "*.pem" "*.key")

HAS_SENSITIVE=false
for pattern in "${SENSITIVE_FILES[@]}"; do
    if ls $pattern 2>/dev/null | grep -q .; then
        echo "${YELLOW}⚠️  Found potentially sensitive file: $pattern${NC}"
        HAS_SENSITIVE=true
    fi
done

if [ "$HAS_SENSITIVE" = false ]; then
    echo "${GREEN}✅${NC} No exposed sensitive files"
fi
echo ""

# ============================================================================
# النتيجة النهائية
# ============================================================================
echo "═══════════════════════════════════════════════════════════════"
echo "${GREEN}✅ Git configuration check completed!${NC}"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ============================================================================
# التوصيات
# ============================================================================
echo "${BLUE}📋 Next Steps:${NC}"
echo ""
echo "1. 📖 Read the documentation:"
echo "   - BRANCHING_STRATEGY.md (استراتيجية التفريع الكاملة)"
echo "   - QUICK_START_BRANCHING.md (دليل سريع)"
echo "   - .github/BRANCH_PROTECTION_RULES.md (قواعس الحماية)"
echo ""
echo "2. 🔐 Setup branch protection rules:"
echo "   - Go to GitHub Settings → Branches"
echo "   - Add rule for 'main' branch"
echo "   - Follow BRANCH_PROTECTION_RULES.md"
echo ""
echo "3. 🚀 Create your first feature branch:"
echo "   git checkout -b feature/your-feature-name"
echo ""
echo "4. 📝 Follow commit naming conventions:"
echo "   - feat: new feature"
echo "   - fix: bug fix"
echo "   - docs: documentation"
echo "   - refactor: code refactoring"
echo ""
echo "═══════════════════════════════════════════════════════════════"
