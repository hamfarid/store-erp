#!/bin/bash
# 📥 Global System Ultimate - Project Scaffolding Script
# Usage: ./download_from_github.sh <new_project_name>

PROJECT_NAME=${1:-"my-new-project"}
REPO_URL="https://github.com/$(gh api user -q .login)/global-system-ultimate.git"

echo "🚀 Scaffolding New Project: '$PROJECT_NAME'..."

# 1. Clone the Global System
git clone "$REPO_URL" "$PROJECT_NAME"

if [ $? -ne 0 ]; then
    echo "❌ Error cloning repository. Please check your GitHub CLI login ('gh auth login')."
    exit 1
fi

cd "$PROJECT_NAME" || exit

# 2. Remove .git history (Start fresh)
rm -rf .git
git init
echo "✅ Git history reset."

# 3. Run Genesis Setup
echo "🛠️ Running Genesis Setup (v15.0)..."
python3 tools/genesis.py

# 4. Final Instructions
echo "✅ Project '$PROJECT_NAME' is ready!"
echo "📋 Next Steps:"
echo "  1. cd $PROJECT_NAME"
echo "  2. Review .env file"
echo "  3. Run 'python3 tools/speckit.py plan' to start coding."
