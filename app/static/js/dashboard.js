/**
 * Interactive Dashboard & Live JWT Inspector Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    initDashboard();
});

async function initDashboard() {
    const token = getStoredToken();
    if (token) {
        renderTokenInfo(token);
    } else {
        // Try fetching user from cookie session
        tryFetchProfile();
    }
}

async function tryFetchProfile() {
    const token = getStoredToken();
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch('/api/v1/auth/me', { headers });
        if (!response.ok) {
            // Not authenticated, redirect to login
            window.location.href = '/login';
            return;
        }

        const user = await response.json();
        updateUIUser(user);
        fetchStats(headers);
    } catch (err) {
        showToast('Error connecting to backend server', 'error');
    }
}

function updateUIUser(user) {
    const emailElem = document.getElementById('user-email');
    const nameElem = document.getElementById('user-name');
    const avatarElem = document.getElementById('user-avatar');

    if (emailElem) emailElem.innerText = user.email;
    if (nameElem) nameElem.innerText = user.full_name || 'Anonymous User';
    if (avatarElem) {
        const initial = (user.full_name || user.email)[0].toUpperCase();
        avatarElem.innerText = initial;
    }
}

async function fetchStats(headers) {
    try {
        const res = await fetch('/api/v1/dashboard/stats', { headers });
        if (res.ok) {
            const data = await res.json();
            const statsElem = document.getElementById('sys-stats-json');
            if (statsElem) {
                statsElem.innerText = JSON.stringify(data, null, 2);
            }
        }
    } catch (e) {
        console.error(e);
    }
}

function renderTokenInfo(token) {
    const tokenDisplay = document.getElementById('raw-jwt-display');
    if (tokenDisplay) tokenDisplay.innerText = token;

    try {
        const parts = token.split('.');
        if (parts.length === 3) {
            const header = JSON.parse(atob(parts[0]));
            const payload = JSON.parse(atob(parts[1]));

            const headerElem = document.getElementById('jwt-header-json');
            const payloadElem = document.getElementById('jwt-payload-json');

            if (headerElem) headerElem.innerText = JSON.stringify(header, null, 2);
            if (payloadElem) payloadElem.innerText = JSON.stringify(payload, null, 2);

            if (payload.exp) {
                const expDate = new Date(payload.exp * 1000);
                const expElem = document.getElementById('jwt-exp-countdown');
                if (expElem) expElem.innerText = `Expires: ${expDate.toLocaleString()}`;
            }
        }
    } catch (e) {
        console.error('Failed to parse JWT token parts', e);
    }
}

async function testProtectedEndpoint(endpoint) {
    const token = getStoredToken();
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const outputElem = document.getElementById('api-tester-output');
    outputElem.innerText = 'Sending Request...';

    try {
        const res = await fetch(endpoint, { headers });
        const statusText = `HTTP ${res.status} ${res.statusText}\n`;
        const data = await res.json();
        outputElem.innerText = statusText + JSON.stringify(data, null, 2);
    } catch (err) {
        outputElem.innerText = 'Request Failed: ' + err.message;
    }
}
