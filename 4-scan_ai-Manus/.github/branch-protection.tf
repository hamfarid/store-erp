# =============================================================================
# Branch Protection Rules - Terraform Configuration
# =============================================================================
# 
# هذا الملف يوثق قواعد حماية الفروع الموصى بها لمشروع Gaara Scan AI
# يمكن تطبيقها يدوياً من GitHub Settings أو باستخدام Terraform
#
# =============================================================================

# -----------------------------------------------------------------------------
# Main Branch Protection (الإنتاج)
# -----------------------------------------------------------------------------
resource "github_branch_protection" "main" {
  repository_id = github_repository.gaara_scan_ai.node_id
  pattern       = "main"

  # إعدادات أساسية
  enforce_admins                  = true
  allows_deletions                = false
  allows_force_pushes             = false
  require_conversation_resolution = true
  required_linear_history         = false
  require_signed_commits          = false

  # فحوصات الحالة المطلوبة
  required_status_checks {
    strict   = true
    contexts = [
      "🔍 Lint Code",
      "🐍 Test Backend",
      "⚛️ Test Frontend",
      "🔒 Security Scan"
    ]
  }

  # مراجعات طلب السحب
  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = true
    required_approving_review_count = 2
    require_last_push_approval      = true
    
    # فرق يمكنها تجاوز المراجعة (للطوارئ)
    # bypass_pull_request_allowances {
    #   users = ["emergency-admin"]
    #   teams = ["site-reliability"]
    # }
  }

  # تقييد من يمكنه الدفع
  restrict_pushes {
    push_allowances = []  # لا أحد يمكنه الدفع مباشرة
  }
}

# -----------------------------------------------------------------------------
# Develop Branch Protection (التطوير)
# -----------------------------------------------------------------------------
resource "github_branch_protection" "develop" {
  repository_id = github_repository.gaara_scan_ai.node_id
  pattern       = "develop"

  enforce_admins                  = false
  allows_deletions                = false
  allows_force_pushes             = false
  require_conversation_resolution = true

  required_status_checks {
    strict   = true
    contexts = [
      "🔍 Lint Code",
      "🐍 Test Backend",
      "⚛️ Test Frontend"
    ]
  }

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = false
    required_approving_review_count = 1
    require_last_push_approval      = false
  }
}

# -----------------------------------------------------------------------------
# Release Branches Protection
# -----------------------------------------------------------------------------
resource "github_branch_protection" "release" {
  repository_id = github_repository.gaara_scan_ai.node_id
  pattern       = "release/**"

  enforce_admins                  = false
  allows_deletions                = true  # يمكن حذفها بعد الدمج
  allows_force_pushes             = false
  require_conversation_resolution = true

  required_status_checks {
    strict   = true
    contexts = [
      "🔍 Lint Code",
      "🐍 Test Backend",
      "⚛️ Test Frontend",
      "🔒 Security Scan"
    ]
  }

  required_pull_request_reviews {
    dismiss_stale_reviews           = true
    require_code_owner_reviews      = true
    required_approving_review_count = 1
  }
}

# -----------------------------------------------------------------------------
# Hotfix Branches Protection
# -----------------------------------------------------------------------------
resource "github_branch_protection" "hotfix" {
  repository_id = github_repository.gaara_scan_ai.node_id
  pattern       = "hotfix/**"

  enforce_admins                  = false
  allows_deletions                = true
  allows_force_pushes             = false

  # فحوصات مخففة للإصلاحات الطارئة
  required_status_checks {
    strict   = false  # لا يتطلب تحديث الفرع
    contexts = [
      "🔍 Lint Code",
      "🐍 Test Backend"
    ]
  }

  required_pull_request_reviews {
    dismiss_stale_reviews           = false
    require_code_owner_reviews      = false
    required_approving_review_count = 1
  }
}

# =============================================================================
# إعدادات الفرع يدوياً في GitHub
# =============================================================================
# 
# للتطبيق اليدوي، اذهب إلى:
# Settings → Branches → Add rule
#
# main:
# ✅ Require a pull request before merging
#    - Required approving reviews: 2
#    - Dismiss stale pull request approvals
#    - Require review from Code Owners
#    - Require approval of the most recent push
# ✅ Require status checks to pass before merging
#    - Require branches to be up to date
#    - Status checks: Lint Code, Test Backend, Test Frontend, Security Scan
# ✅ Require conversation resolution before merging
# ✅ Do not allow bypassing the above settings
# ✅ Restrict who can push: No direct pushes
# ❌ Allow force pushes
# ❌ Allow deletions
#
# develop:
# ✅ Require a pull request before merging
#    - Required approving reviews: 1
# ✅ Require status checks to pass
# ❌ Require Code Owner review
#
# release/**:
# ✅ Require a pull request before merging
# ✅ Require status checks (all)
# ✅ Require Code Owner review
# ✅ Allow deletions (after merge)
#
# hotfix/**:
# ✅ Require a pull request (1 review)
# ✅ Basic status checks only
# ✅ Allow deletions
# =============================================================================

# =============================================================================
# GitHub CLI Commands for Branch Protection
# =============================================================================
# 
# يمكنك أيضاً استخدام GitHub CLI لإعداد الحماية:
#
# # تثبيت GitHub CLI
# winget install --id GitHub.cli
#
# # تسجيل الدخول
# gh auth login
#
# # عرض قواعد الحماية الحالية
# gh api repos/{owner}/{repo}/branches/main/protection
#
# # تحديث قواعد الحماية
# gh api repos/{owner}/{repo}/branches/main/protection \
#   -X PUT \
#   -H "Accept: application/vnd.github+json" \
#   -f required_status_checks='{"strict":true,"contexts":["ci/build","ci/test"]}' \
#   -f enforce_admins=true \
#   -f required_pull_request_reviews='{"required_approving_review_count":2}'
#
# =============================================================================
