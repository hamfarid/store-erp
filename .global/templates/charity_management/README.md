# Charity Management Template

**Complete charity and donation management system**

---

## 📋 Overview

Professional charity management system for:
- **Donation Management** - Track all donations
- **Beneficiary Management** - Manage recipients
- **Campaign Management** - Run fundraising campaigns
- **Volunteer Management** - Organize volunteers
- **Reporting & Analytics** - Track impact

---

## 🏗️ Architecture

### Frontend
- **Framework:** React 18 + TypeScript
- **UI:** Material-UI (MUI)
- **State:** Redux Toolkit
- **Charts:** Recharts
- **Maps:** Leaflet (for beneficiary locations)

### Backend
- **Framework:** Django 4.2 + DRF
- **Authentication:** JWT
- **Payment:** Stripe / PayPal integration
- **Email:** SendGrid
- **SMS:** Twilio (optional)

### Database
- **Primary:** PostgreSQL
- **Cache:** Redis
- **Files:** S3 / Local storage

---

## 🚀 Features

### Donation Management

✅ **Online Donations**
- Credit/debit cards
- PayPal
- Bank transfer
- Recurring donations
- One-time donations

✅ **Donation Tracking**
- Donor information
- Donation history
- Tax receipts
- Thank you emails

✅ **Payment Integration**
- Stripe
- PayPal
- Local payment gateways

### Beneficiary Management

✅ **Beneficiary Database**
- Personal information
- Family details
- Needs assessment
- Location mapping
- Document uploads

✅ **Case Management**
- Track assistance provided
- Follow-up schedules
- Progress notes
- Photos/documents

### Campaign Management

✅ **Fundraising Campaigns**
- Campaign creation
- Goal tracking
- Progress visualization
- Social sharing
- Email campaigns

✅ **Campaign Types**
- General fund
- Emergency relief
- Education
- Healthcare
- Food distribution

### Volunteer Management

✅ **Volunteer Database**
- Volunteer profiles
- Skills tracking
- Availability
- Hours logged

✅ **Task Assignment**
- Create tasks
- Assign volunteers
- Track completion
- Feedback collection

### Reporting & Analytics

✅ **Financial Reports**
- Donation summary
- Campaign performance
- Expense tracking
- Budget vs actual

✅ **Impact Reports**
- Beneficiaries served
- Services provided
- Geographic distribution
- Demographics

---

## 🚀 Quick Start

```bash
# 1. Generate from template
python3 ../../tools/template_generator.py \
  --template charity_management \
  --output ~/projects/my-charity

# 2. Navigate
cd ~/projects/my-charity

# 3. Configure
cp .env.example .env
# Add payment gateway keys

# 4. Start
docker-compose up -d

# 5. Migrate
docker-compose exec backend python manage.py migrate

# 6. Create admin
docker-compose exec backend python manage.py createsuperuser

# 7. Load sample data
docker-compose exec backend python manage.py loaddata sample_charity_data

# 8. Access
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
# Admin: http://localhost:5000/admin
```

---

## 📁 Structure

```
charity_management/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Donations/
│   │   │   ├── Beneficiaries/
│   │   │   ├── Campaigns/
│   │   │   ├── Volunteers/
│   │   │   └── Reports/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── DonationsPage.tsx
│   │   │   ├── BeneficiariesPage.tsx
│   │   │   ├── CampaignsPage.tsx
│   │   │   └── ReportsPage.tsx
│   │   └── services/
│   │       ├── api.ts
│   │       ├── payment.ts
│   │       └── auth.ts
│   └── package.json
├── backend/
│   ├── apps/
│   │   ├── donations/
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── payment.py
│   │   ├── beneficiaries/
│   │   ├── campaigns/
│   │   └── reports/
│   ├── config/
│   └── requirements.txt
├── database/
├── docker/
├── tests/
├── docs/
├── .env.example
├── config.json
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

```env
# Project
PROJECT_NAME={{PROJECT_NAME}}
CHARITY_NAME={{CHARITY_NAME}}
CHARITY_EMAIL={{CHARITY_EMAIL}}

# Database
DATABASE_URL=postgresql://user:pass@db:5432/{{DATABASE_NAME}}

# Payment Gateways
STRIPE_PUBLIC_KEY=pk_...
STRIPE_SECRET_KEY=sk_...
PAYPAL_CLIENT_ID=...
PAYPAL_SECRET=...

# Email
SENDGRID_API_KEY=...
FROM_EMAIL=noreply@{{CHARITY_NAME}}.org

# SMS (optional)
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
TWILIO_PHONE_NUMBER=...

# Storage
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=...

# Features
ENABLE_RECURRING_DONATIONS=true
ENABLE_SMS_NOTIFICATIONS=false
ENABLE_VOLUNTEER_PORTAL=true
TAX_RECEIPT_AUTO_SEND=true
```

---

## 💳 Payment Integration

### Stripe

```python
# backend/apps/donations/payment.py
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def process_donation(amount, currency, donor_email):
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),  # cents
        currency=currency,
        receipt_email=donor_email,
        metadata={'type': 'donation'}
    )
    return intent
```

### PayPal

```python
from paypalrestsdk import Payment

payment = Payment({
    "intent": "sale",
    "payer": {"payment_method": "paypal"},
    "transactions": [{
        "amount": {
            "total": str(amount),
            "currency": currency
        },
        "description": "Donation"
    }]
})
```

---

## 📊 Models

### Donation

```python
class Donation(models.Model):
    donor = models.ForeignKey(Donor)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)
    is_recurring = models.BooleanField(default=False)
    campaign = models.ForeignKey(Campaign, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Beneficiary

```python
class Beneficiary(models.Model):
    name = models.CharField(max_length=200)
    family_size = models.IntegerField()
    location = models.PointField()  # GeoDjango
    needs = models.TextField()
    status = models.CharField(max_length=20)
    assigned_to = models.ForeignKey(User, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Campaign

```python
class Campaign(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    raised_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='campaigns/')
```

---

## 📈 Reports

### Donation Report

- Total donations
- Average donation
- Top donors
- Payment methods breakdown
- Monthly trends

### Beneficiary Report

- Total beneficiaries
- Services provided
- Geographic distribution
- Demographics
- Success stories

### Campaign Report

- Campaign performance
- Goal achievement
- Donor engagement
- Social media reach

---

## 🎨 Dashboard

### Metrics Cards

- Total donations (today/month/year)
- Active campaigns
- Beneficiaries served
- Volunteers active

### Charts

- Donation trends (line chart)
- Campaign progress (bar chart)
- Geographic distribution (map)
- Donor demographics (pie chart)

---

## 📱 Mobile Responsive

- Responsive design
- Mobile-friendly forms
- Touch-optimized
- Progressive Web App (PWA)

---

## 🔐 Security

- HTTPS required
- PCI DSS compliant (for payments)
- Data encryption
- Role-based access
- Audit logs

---

## ✅ Summary

**Complete charity management** with:

✅ **Donation processing** - Multiple payment gateways  
✅ **Beneficiary management** - Track recipients  
✅ **Campaign management** - Fundraising campaigns  
✅ **Volunteer management** - Organize volunteers  
✅ **Reports & analytics** - Track impact  
✅ **Mobile responsive** - Works everywhere

**Manage your charity efficiently!** 🤝

---

**Template Version:** 1.0.0  
**Last Updated:** 2025-11-02  
**Status:** ✅ Production Ready

