import React, { useState } from "react";

function App() {
  const [matrix, setMatrix] = useState('[["h","a","r","r","y"],["p","o","t","t","e","r"],["t","r","o","l","l","s"]]');
  const [encodedMessage, setEncodedMessage] = useState('[9,0,3,9,0,0,4,3,9,6,5,1,8,4,8]');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          matrix: JSON.parse(matrix),
          encoded_message: JSON.parse(encodedMessage),
        }),
      });
      if (!response.ok) throw new Error("Error en la API");
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Error: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h2>CryptoSolver Frontend Test</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Matriz (JSON):</label>
          <textarea
            rows={4}
            style={{ width: "100%" }}
            value={matrix}
            onChange={(e) => setMatrix(e.target.value)}
          />
        </div>
        <div>
          <label>Mensaje codificado (JSON):</label>
          <input
            style={{ width: "100%" }}
            value={encodedMessage}
            onChange={(e) => setEncodedMessage(e.target.value)}
          />
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: 10 }}>
          {loading ? "Procesando..." : "Resolver"}
        </button>
      </form>
      {error && <div style={{ color: "red", marginTop: 10 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Resultado</h3>
          <div><b>¿Tiene solución?</b> {result.has_solution ? "Sí" : "No"}</div>
          <div><b>Predicciones:</b> <pre>{JSON.stringify(result.predictions, null, 2)}</pre></div>
          <div><b>Mensaje decodificado:</b> {result.decoded_message && result.decoded_message.join("")}</div>
          <details>
            <summary>Ver historial de pasos</summary>
            <pre style={{ maxHeight: 200, overflow: "auto" }}>
              {JSON.stringify(result.history, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

export default App;