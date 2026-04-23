from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>DevSecOps Dashboard</title>
    <style>
        body {
            background-color: #1e1e2f;
            color: white;
            font-family: Arial;
            text-align: center;
            padding-top: 80px;
        }
        .card {
            background: #2d2d44;
            padding: 30px;
            margin: auto;
            width: 50%;
            border-radius: 10px;
            box-shadow: 0px 0px 10px #000;
        }
        button {
            padding: 10px 20px;
            background: #28a745;
            border: none;
            color: white;
            cursor: pointer;
            margin-top: 20px;
            border-radius: 5px;
        }
    </style>
</head>

<body>

<div class="card">
    <h1>🚀 FastAPI CI/CD Dashboard</h1>
    <p>Deployed via Jenkins on EC2</p>

    <button onclick="fetchMsg()">Check API</button>

    <h3 id="result"></h3>
</div>

<script>
function fetchMsg() {
    fetch('/api')
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = data.message;
    });
}
</script>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return html_content

@app.get("/api")
def api():
    return {"message": "Backend is working perfectly 🚀"}
