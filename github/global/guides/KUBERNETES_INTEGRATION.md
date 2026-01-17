# Kubernetes Integration Guide

دليل شامل لنشر التطبيقات على Kubernetes مع أفضل الممارسات.

---

## 📋 المحتويات

1. [المتطلبات الأساسية](#المتطلبات-الأساسية)
2. [Kubernetes Manifests](#kubernetes-manifests)
3. [Helm Charts](#helm-charts)
4. [ConfigMaps & Secrets](#configmaps--secrets)
5. [Ingress & Load Balancing](#ingress--load-balancing)
6. [Auto-Scaling](#auto-scaling)
7. [Monitoring & Logging](#monitoring--logging)
8. [CI/CD Integration](#cicd-integration)

---

## المتطلبات الأساسية

### التثبيت

#### kubectl
```bash
# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# macOS
brew install kubectl

# Windows
choco install kubernetes-cli
```

#### Helm
```bash
# Linux/macOS
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Windows
choco install kubernetes-helm
```

#### Minikube (للتطوير المحلي)
```bash
# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# macOS
brew install minikube

# Windows
choco install minikube
```

### التحقق
```bash
kubectl version --client
helm version
minikube version
```

---

## Kubernetes Manifests

### 1. Namespace

```yaml
# FILE: k8s/namespace.yaml | PURPOSE: Application namespace | OWNER: DevOps | LAST-AUDITED: 2025-10-28

apiVersion: v1
kind: Namespace
metadata:
  name: myapp
  labels:
    name: myapp
    environment: production
```

### 2. Deployment (Frontend)

```yaml
# FILE: k8s/frontend-deployment.yaml | PURPOSE: Frontend deployment | OWNER: DevOps | LAST-AUDITED: 2025-10-28

apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: myapp
  labels:
    app: frontend
    tier: presentation
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: presentation
    spec:
      containers:
      - name: frontend
        image: registry.example.com/myapp/frontend:v1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
          name: http
          protocol: TCP
        env:
        - name: NODE_ENV
          value: "production"
        - name: API_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: api_url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 3
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /api/ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
      imagePullSecrets:
      - name: registry-secret
```

### 3. Deployment (Backend)

```yaml
# FILE: k8s/backend-deployment.yaml | PURPOSE: Backend deployment | OWNER: DevOps | LAST-AUDITED: 2025-10-28

apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: myapp
  labels:
    app: backend
    tier: application
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
        tier: application
    spec:
      containers:
      - name: backend
        image: registry.example.com/myapp/backend:v1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database_url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: redis_url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
      imagePullSecrets:
      - name: registry-secret
```

### 4. Service

```yaml
# FILE: k8s/services.yaml | PURPOSE: Services configuration | OWNER: DevOps | LAST-AUDITED: 2025-10-28

---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: myapp
  labels:
    app: frontend
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
    name: http
  selector:
    app: frontend

---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: myapp
  labels:
    app: backend
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: backend
```

### 5. StatefulSet (PostgreSQL)

```yaml
# FILE: k8s/postgres-statefulset.yaml | PURPOSE: PostgreSQL stateful set | OWNER: DBA | LAST-AUDITED: 2025-10-28

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: myapp
spec:
  serviceName: postgres
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: POSTGRES_DB
          value: appdb
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - pg_isready
            - -U
            - postgres
          initialDelaySeconds: 10
          periodSeconds: 5
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

---

## ConfigMaps & Secrets

### ConfigMap

```yaml
# FILE: k8s/configmap.yaml | PURPOSE: Application configuration | OWNER: DevOps | LAST-AUDITED: 2025-10-28

apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp
data:
  api_url: "https://api.example.com"
  log_level: "info"
  max_connections: "100"
  nginx.conf: |
    server {
      listen 80;
      server_name _;
      
      location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
      }
      
      location /api {
        proxy_pass http://backend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
      }
    }
```

### Secret

```yaml
# FILE: k8s/secrets.yaml | PURPOSE: Sensitive data | OWNER: Security | LAST-AUDITED: 2025-10-28

apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: myapp
type: Opaque
stringData:
  database_url: "postgresql://user:password@postgres:5432/appdb"
  redis_url: "redis://:password@redis:6379/0"
  jwt_secret: "your-jwt-secret-here"
  api_key: "your-api-key-here"
```

### إنشاء Secret من سطر الأوامر

```bash
# من ملف
kubectl create secret generic app-secrets \
  --from-file=database_url=./secrets/db_url.txt \
  --from-file=redis_url=./secrets/redis_url.txt \
  -n myapp

# من literal
kubectl create secret generic app-secrets \
  --from-literal=database_url='postgresql://...' \
  --from-literal=redis_url='redis://...' \
  -n myapp

# من Docker registry
kubectl create secret docker-registry registry-secret \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=password \
  --docker-email=user@example.com \
  -n myapp
```

---

## Ingress & Load Balancing

### Ingress

```yaml
# FILE: k8s/ingress.yaml | PURPOSE: Ingress configuration | OWNER: DevOps | LAST-AUDITED: 2025-10-28

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: myapp
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - example.com
    - www.example.com
    secretName: app-tls-cert
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 80
```

---

## Auto-Scaling

### Horizontal Pod Autoscaler

```yaml
# FILE: k8s/hpa.yaml | PURPOSE: Horizontal pod autoscaling | OWNER: DevOps | LAST-AUDITED: 2025-10-28

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
  namespace: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## الأوامر الأساسية

### Deploy

```bash
# إنشاء namespace
kubectl apply -f k8s/namespace.yaml

# إنشاء secrets
kubectl apply -f k8s/secrets.yaml

# إنشاء configmaps
kubectl apply -f k8s/configmap.yaml

# Deploy services
kubectl apply -f k8s/

# التحقق
kubectl get all -n myapp
```

### Update

```bash
# تحديث image
kubectl set image deployment/frontend frontend=registry.example.com/myapp/frontend:v1.1.0 -n myapp

# Rollout status
kubectl rollout status deployment/frontend -n myapp

# Rollback
kubectl rollout undo deployment/frontend -n myapp
```

### Debugging

```bash
# Logs
kubectl logs -f deployment/frontend -n myapp

# Describe
kubectl describe pod <pod-name> -n myapp

# Exec
kubectl exec -it <pod-name> -n myapp -- /bin/sh

# Port forward
kubectl port-forward service/frontend 8080:80 -n myapp
```

---

## الخلاصة

### ✅ Best Practices

1. **Namespaces** - عزل الموارد
2. **Resource Limits** - تحديد الموارد
3. **Health Checks** - مراقبة الصحة
4. **Auto-Scaling** - توسع تلقائي
5. **Security Context** - أمان الحاويات
6. **Secrets Management** - إدارة الأسرار
7. **Ingress** - توجيه الطلبات
8. **Monitoring** - مراقبة شاملة

### 📝 Checklist

- [ ] Namespace مُعرّف
- [ ] Deployments مُحسّنة
- [ ] Services مُعدّة
- [ ] ConfigMaps & Secrets موجودة
- [ ] Ingress مُكوّن
- [ ] HPA مُفعّل
- [ ] Resource limits محددة
- [ ] Health checks مُعدّة
- [ ] Security context مُطبّق

---

**آخر تحديث:** 2025-10-28  
**الإصدار:** 1.0.0

