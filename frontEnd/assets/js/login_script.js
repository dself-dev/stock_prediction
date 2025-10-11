// frontEnd/assets/js/login_script.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const message = document.getElementById("message");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
      });

      if (res.ok) {
        message.textContent = "Login successful!";
        message.style.color = "green";
      } else {
        const data = await res.json();
        message.textContent = data.detail || "Login failed";
        message.style.color = "red";
      }
    } catch (err) {
      message.textContent = "Server error";
      message.style.color = "red";
      console.error(err);
    }
  });
});
