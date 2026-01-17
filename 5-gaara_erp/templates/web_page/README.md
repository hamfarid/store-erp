# Web Page Template

**Simple, responsive website template**

---

## 📋 Overview

Professional static/dynamic website template for:
- Landing pages
- Portfolios
- Company websites
- Product pages
- Marketing sites

---

## 🏗️ Features

✅ **Responsive Design** - Mobile-first approach  
✅ **SEO Optimized** - Meta tags, structured data  
✅ **Fast Loading** - Optimized assets  
✅ **Modern UI** - Clean and professional  
✅ **Contact Form** - With validation  
✅ **Cross-browser** - Works everywhere

---

## 🚀 Quick Start

```bash
# Generate from template
python3 ../../tools/template_generator.py \
  --template web_page \
  --output ~/projects/my-website

# Navigate
cd ~/projects/my-website

# Open in browser
open index.html

# Or use live server
python3 -m http.server 8000
# Visit: http://localhost:8000
```

---

## 📁 Structure

```
web_page/
├── src/
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── css/
│   │   ├── style.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── main.js
│   │   └── form.js
│   └── images/
│       ├── logo.png
│       └── hero.jpg
├── docs/
│   └── customization.md
├── config.json
└── README.md
```

---

## 🎨 Customization

### Colors

Edit `src/css/style.css`:

```css
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --text-color: #333;
  --bg-color: #fff;
}
```

### Content

Edit `src/index.html`:

```html
<h1>{{PROJECT_NAME}}</h1>
<p>Your content here</p>
```

### Images

Replace images in `src/images/`

---

## 📊 Sections

### Header
- Logo
- Navigation menu
- Mobile menu

### Hero
- Main headline
- Call-to-action
- Background image

### Features
- 3-column layout
- Icons
- Descriptions

### About
- Company info
- Team section
- Values

### Contact
- Contact form
- Address
- Social links

### Footer
- Copyright
- Links
- Social icons

---

## 🔧 Configuration

### config.json

```json
{
  "template_name": "web_page",
  "variables": {
    "PROJECT_NAME": "{{PROJECT_NAME}}",
    "COMPANY_NAME": "{{COMPANY_NAME}}",
    "CONTACT_EMAIL": "{{CONTACT_EMAIL}}",
    "PHONE": "{{PHONE}}",
    "ADDRESS": "{{ADDRESS}}"
  }
}
```

---

## 📱 Responsive

Breakpoints:

- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px

---

## ✅ Summary

**Simple website template** with:

✅ **Clean design**  
✅ **Responsive**  
✅ **SEO ready**  
✅ **Easy to customize**  
✅ **No build process**

**Perfect for simple websites!** 🚀

---

**Version:** 1.0.0  
**Status:** ✅ Ready

