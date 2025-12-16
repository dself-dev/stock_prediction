console.log("🔥 NEW INDEX.JS LOADED 🔥");


document.getElementById("stockForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const loader = document.getElementById("loader");
    const resultContainer = document.getElementById("resultContainer");

    // Clear previous results
    resultContainer.innerHTML = "";
    loader.style.display = "block";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            body: formData
        });

        loader.style.display = "none";

        if (!response.ok) {
            throw new Error("Prediction request failed");
        }

        const result = await response.json();

        const color = result.change_pct >= 0 ? "#28a745" : "#dc3545";

        const resultDiv = document.createElement("div");
        resultDiv.className = "prediction-result";
        resultDiv.style.border = `2px solid ${color}`;
        resultDiv.style.backgroundColor = "#f9f9f9";
        resultDiv.style.borderRadius = "8px";
        resultDiv.style.padding = "15px";
        resultDiv.style.marginTop = "20px";
        resultDiv.style.textAlign = "center";
        resultDiv.style.position = "relative";

        resultDiv.innerHTML = `
            <span class="close-btn"
                  style="position:absolute; top:10px; right:10px;
                         font-size:24px; font-weight:bold; cursor:pointer;
                         color:#6c757d;">&times;</span>

            <h2 style="color:${color};">${result.ticker} Prediction</h2>

            <h3>
                Tomorrow's Price:
                <span style="color:${color};">
                    $${result.predicted_close}
                </span>
            </h3>

            <p>Current Price: $${result.current_price}</p>
            <p>Expected Change: <strong>${result.change_pct}%</strong></p>
            <p>Direction: <strong>${result.direction}</strong></p>
        `;

        resultContainer.appendChild(resultDiv);

        // Fade-in effect
        setTimeout(() => resultDiv.classList.add("show"), 50);

        // Close button behavior
        const closeBtn = resultDiv.querySelector(".close-btn");

        closeBtn.addEventListener("click", () => {
            resultDiv.remove();
        });

        closeBtn.addEventListener("mouseover", () => {
            closeBtn.style.color = "#dc3545";
        });

        closeBtn.addEventListener("mouseout", () => {
            closeBtn.style.color = "#6c757d";
        });

    } catch (err) {
        loader.style.display = "none";
        alert("Error: " + err.message);
        console.error(err);
    }
});


