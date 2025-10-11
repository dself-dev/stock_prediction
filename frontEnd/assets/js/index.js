document.getElementById("stockForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const loader = document.getElementById("loader");
        const resultContainer = document.getElementById("resultContainer");

        // Remove any previous results
        resultContainer.innerHTML = "";
        loader.style.display = "block";

        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                body: formData
            });

            loader.style.display = "none"; // Hide spinner

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

            resultDiv.innerHTML = `
                <h2 style="color:${color};">${result.ticker} Prediction</h2>
                <h3>Tomorrow's Price: <span style="color:${color};">$${result.predicted_close}</span></h3>
                <p>Current Price: $${result.current_price}</p>
                <p>Expected Change: <strong>${result.change_pct}%</strong></p>
                <p>Sentiment: ${result.sentiment.label.toUpperCase()} (avg: ${result.sentiment.avg_sentiment.toFixed(3)})</p>
            `;

            resultContainer.appendChild(resultDiv);
            // Fade in
            setTimeout(() => resultDiv.classList.add("show"), 50);

        } catch (err) {
            loader.style.display = "none";
            alert("Error: " + err.message);
            console.error(err);
        }
    });