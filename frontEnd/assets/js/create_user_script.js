document.getElementById('createUserForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const country = document.getElementById('country').value;
    const state = document.getElementById('state').value;
    const password = document.getElementById('password').value;
    const reenterPassword = document.getElementById('reenter_password').value;
    const messageDiv = document.getElementById('message');

    if (password !== reenterPassword) {
        messageDiv.textContent = 'Passwords do not match!';
        messageDiv.style.color = '#d9534f';
        return;
    }

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, country, state, password })
        });
        const data = await response.json();
        if (response.ok) {
            messageDiv.textContent = data.message;
            messageDiv.style.color = '#5cb85c';
            setTimeout(() => window.location.href = 'login.html', 2000);
        } else {
            messageDiv.textContent = data.detail;
            messageDiv.style.color = '#d9534f';
        }
    } catch (error) {
        messageDiv.textContent = 'Error creating account. Try again.';
        console.error(error);
    }
});