/**
 * Client-Side Authentication Manager
 */

function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function getStoredToken() {
    return localStorage.getItem('access_token');
}

function setStoredToken(token, refreshToken) {
    if (token) {
        localStorage.setItem('access_token', token);
    }
    if (refreshToken) {
        localStorage.setItem('refresh_token', refreshToken);
    }
}

function clearStoredToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const submitBtn = event.target.querySelector('button[type="submit"]');

    submitBtn.disabled = true;
    submitBtn.innerText = 'Authenticating...';

    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            setStoredToken(data.access_token, data.refresh_token);
            showToast('Authentication successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/dashboard';
            }, 800);
        } else {
            showToast(data.detail || 'Invalid email or password', 'error');
            submitBtn.disabled = false;
            submitBtn.innerText = 'Sign In';
        }
    } catch (err) {
        showToast('Network error during authentication.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerText = 'Sign In';
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const fullName = document.getElementById('full_name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const submitBtn = event.target.querySelector('button[type="submit"]');

    submitBtn.disabled = true;
    submitBtn.innerText = 'Creating Account...';

    try {
        const response = await fetch('/api/v1/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, full_name: fullName, password })
        });

        const data = await response.json();

        if (response.ok) {
            showToast('Account created successfully! Auto-logging in...', 'success');
            // Auto login after signup
            const loginResp = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (loginResp.ok) {
                const loginData = await loginResp.json();
                setStoredToken(loginData.access_token, loginData.refresh_token);
                setTimeout(() => { window.location.href = '/dashboard'; }, 800);
            } else {
                window.location.href = '/login';
            }
        } else {
            showToast(data.detail || 'Failed to create account', 'error');
            submitBtn.disabled = false;
            submitBtn.innerText = 'Register';
        }
    } catch (err) {
        showToast('Network error during registration.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerText = 'Register';
    }
}

async function handleLogout() {
    clearStoredToken();
    try {
        await fetch('/api/v1/auth/logout', { method: 'POST' });
    } catch (e) {
        console.error(e);
    }
    showToast('Logged out successfully', 'info');
    setTimeout(() => {
        window.location.href = '/';
    }, 500);
}
