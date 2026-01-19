// Common functionality for the admin panel

// Flash message handling
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 3000);
    });
});

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
}

// Toggle password visibility
function togglePasswordVisibility(inputId, toggleId) {
    const passwordInput = document.getElementById(inputId);
    const toggleButton = document.getElementById(toggleId);

    if (passwordInput && toggleButton) {
        toggleButton.addEventListener('click', () => {
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;
            toggleButton.querySelector('i').textContent = type === 'password' ? 'visibility' : 'visibility_off';
        });
    }
}

// Confirm action
function confirmAction(message) {
    return confirm(message || 'هل أنت متأكد من تنفيذ هذا الإجراء؟');
}

// Format date
function formatDate(date) {
    return new Date(date).toLocaleDateString('ar-SA', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format number
function formatNumber(number) {
    return new Intl.NumberFormat('ar-SA').format(number);
}

// Handle AJAX requests
async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

// Handle form submission
async function handleFormSubmit(form, url, method = 'POST') {
    if (!validateForm(form)) {
        return false;
    }

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetchData(url, {
            method,
            body: JSON.stringify(data)
        });

        if (response.success) {
            window.location.href = response.redirect || window.location.href;
        } else {
            alert(response.message || 'حدث خطأ أثناء معالجة الطلب');
        }
    } catch (error) {
        alert('حدث خطأ أثناء معالجة الطلب');
    }

    return false;
}

// Initialize tooltips
function initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.title = element.dataset.tooltip;
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();

    // Initialize password toggles
    const passwordToggles = document.querySelectorAll('[data-password-toggle]');
    passwordToggles.forEach(toggle => {
        const inputId = toggle.dataset.passwordToggle;
        togglePasswordVisibility(inputId, toggle.id);
    });

    // Initialize form validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}); 