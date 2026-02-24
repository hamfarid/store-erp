# 🔐 Container Signing Protocol (Cosign)

> **Standard**: Supply-chain Levels for Software Artifacts (SLSA) Level 3
> **Tool**: Cosign (Sigstore)

## 1. Policy
All container images deployed to production MUST be signed using Cosign.

## 2. Keyless Signing (OIDC)
We use Keyless Signing via GitHub Actions OIDC tokens.

### Workflow
1.  **Build**: Build the Docker image.
2.  **Push**: Push to registry (GHCR/ECR).
3.  **Sign**: Use `cosign sign` with OIDC identity.

```yaml
- name: Sign image with a key
  run: |
    cosign sign --yes --key env://COSIGN_PRIVATE_KEY "${TAGS}"
  env:
    TAGS: ${{ steps.meta.outputs.tags }}
    COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
    COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
```

## 3. Verification (Admission Controller)
The Kubernetes cluster MUST verify signatures before pulling images.

```yaml
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: verify-images
spec:
  images:
    - glob: "ghcr.io/my-org/*"
  authorities:
    - keyless:
        url: https://fulcio.sigstore.dev
        identities:
          - issuer: https://token.actions.githubusercontent.com
            subject: "https://github.com/my-org/my-repo/.github/workflows/build.yml@refs/heads/main"
```
