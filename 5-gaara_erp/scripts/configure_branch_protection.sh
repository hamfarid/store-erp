#!/bin/bash

# Configure Branch Protection for Store ERP Repository
# Based on docs/github/BRANCH_PROTECTION.md

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_OWNER="hamfarid"
REPO_NAME="Store"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# Check if GitHub token is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN environment variable is not set${NC}"
    echo "Please set it with: export GITHUB_TOKEN=your_token_here"
    exit 1
fi

echo -e "${GREEN}Configuring branch protection for ${REPO_OWNER}/${REPO_NAME}${NC}"
echo ""

# Function to configure branch protection
configure_branch_protection() {
    local branch=$1
    local config_file=$2
    
    echo -e "${YELLOW}Configuring protection for branch: ${branch}${NC}"
    
    curl -X PUT \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer ${GITHUB_TOKEN}" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/branches/${branch}/protection" \
        -d @"${config_file}" \
        -s -o /dev/null -w "HTTP Status: %{http_code}\n"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Branch protection configured for ${branch}${NC}"
    else
        echo -e "${RED}❌ Failed to configure branch protection for ${branch}${NC}"
    fi
    echo ""
}

# Main branch protection configuration
cat > /tmp/main_branch_protection.json <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "backend-tests / test",
      "pr-quality-gate / pr-quality-gate"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1,
    "require_last_push_approval": false
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": true,
  "lock_branch": false,
  "allow_fork_syncing": false
}
EOF

# Development branch protection configuration
cat > /tmp/development_branch_protection.json <<'EOF'
{
  "required_status_checks": {
    "strict": false,
    "contexts": [
      "backend-tests / test"
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": false,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 1,
    "require_last_push_approval": false
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "lock_branch": false,
  "allow_fork_syncing": false
}
EOF

# Configure main branch
echo -e "${GREEN}=== Configuring Main Branch ===${NC}"
configure_branch_protection "main" "/tmp/main_branch_protection.json"

# Configure development branch (if exists)
echo -e "${GREEN}=== Configuring Development Branch ===${NC}"
if git ls-remote --heads origin development > /dev/null 2>&1; then
    configure_branch_protection "development" "/tmp/development_branch_protection.json"
else
    echo -e "${YELLOW}⚠️  Development branch does not exist, skipping${NC}"
    echo ""
fi

# Cleanup
rm -f /tmp/main_branch_protection.json
rm -f /tmp/development_branch_protection.json

echo -e "${GREEN}=== Branch Protection Configuration Complete ===${NC}"
echo ""
echo "To verify the configuration:"
echo "  1. Go to: https://github.com/${REPO_OWNER}/${REPO_NAME}/settings/branches"
echo "  2. Check the protection rules for each branch"
echo ""
echo "Or use GitHub CLI:"
echo "  gh api repos/${REPO_OWNER}/${REPO_NAME}/branches/main/protection"

