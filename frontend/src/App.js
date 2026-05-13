import React, { useMemo, useState } from "react";
import "./App.css";
import { solveAPI } from "./services/api";

const EXAMPLES = [
  {
    id: "harry_potter_trolls",
    name: "Harry + Potter = Trolls",
    description: "Caso del proyecto para probar el solver con tres palabras.",
    words: ["harry", "potter", "trolls"],
    encodedMessage: "9,0,3,9,0,0,4,3,9,6,5,1,8,4,8",
  },
  {
    id: "send_more_money",
    name: "SEND + MORE = MONEY",
    description: "El criptaritmético clásico para observar carry y poda.",
    words: ["send", "more", "money"],
    encodedMessage: "9,5,6,7,1,0,8,5,1,0,6,5,2",
  },
  {
    id: "two_two_four",
    name: "TWO + TWO = FOUR",
    description: "Ejemplo corto para ver el árbol de búsqueda rápidamente.",
    words: ["two", "two", "four"],
    encodedMessage: "7,3,4,1,4,6,8",
  },
];

function App() {
  const [words, setWords] = useState(["harry", "potter", "trolls"]);
  const [encodedMessage, setEncodedMessage] = useState("9,0,3,9,0,0,4,3,9,6,5,1,8,4,8");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedExample, setSelectedExample] = useState(EXAMPLES[0].id);

  const handleWordChange = (index, value) => {
    const newWords = [...words];
    newWords[index] = value;
    setWords(newWords);
  };

  const addWord = () => {
    setWords([...words, ""]);
  };

  const removeWord = (index) => {
    setWords(words.filter((_, i) => i !== index));
  };

  const loadExample = (exampleId) => {
    const example = EXAMPLES.find((item) => item.id === exampleId);
    if (!example) {
      return;
    }

    setSelectedExample(exampleId);
    setWords(example.words);
    setEncodedMessage(example.encodedMessage);
    setResult(null);
    setError("");
  };

  const statistics = useMemo(() => {
    const historyCount = result?.history?.length || 0;
    const distinctAssignments = result?.predictions ? Object.keys(result.predictions).length : 0;
    return {
      historyCount,
      distinctAssignments,
      decodedMessage: result?.decoded_message?.join("") || "",
    };
  }, [result]);

  const historyPreview = useMemo(() => {
    if (!result?.history?.length) {
      return [];
    }

    return result.history.slice(-8).map((snapshot, index) => {
      const entries = Object.entries(snapshot);
      return {
        id: `${index}-${entries.length}`,
        title: `Paso ${index + 1}`,
        detail: entries.length
          ? entries.map(([letter, digit]) => `${letter}=${digit}`).join(", ")
          : "Sin asignaciones en este paso",
      };
    });
  }, [result]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      // Validar que las palabras no estén vacías
      if (words.some(w => w.trim() === "")) {
        throw new Error("Por favor completa todas las palabras");
      }

      const data = await solveAPI(words, encodedMessage);
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div className="app-container">
      <div className="header">
        <div className="hero-badge">Data Structures Practice</div>
        <h1>CryptoSolver</h1>
        <p>Resolución de criptaritméticos con backtracking y análisis paso a paso</p>
      </div>

      <section className="examples-panel">
        <div className="section-title">
          <h2>Ejemplos clásicos</h2>
          <p>Carga un caso listo para explorar el comportamiento del solver.</p>
        </div>
        <div className="examples-grid">
          {EXAMPLES.map((example) => (
            <button
              key={example.id}
              type="button"
              className={`example-card ${selectedExample === example.id ? "active" : ""}`}
              onClick={() => loadExample(example.id)}
            >
              <span className="example-name">{example.name}</span>
              <span className="example-description">{example.description}</span>
            </button>
          ))}
        </div>
      </section>

      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-section">
          <h2>Palabras a sumar</h2>
          <p className="hint">Puedes editar las palabras o cargar un ejemplo clásico desde arriba.</p>
          <div className="words-list">
            {words.map((word, index) => (
              <div key={index} className="word-input-group">
                <input
                  type="text"
                  value={word}
                  onChange={(e) => handleWordChange(index, e.target.value)}
                  placeholder={`Palabra ${index + 1}`}
                  className="word-input"
                />
                {words.length > 2 && (
                  <button
                    type="button"
                    onClick={() => removeWord(index)}
                    className="btn-remove"
                  >
                    ✕
                  </button>
                )}
              </div>
            ))}
          </div>
          <button
            type="button"
            onClick={addWord}
            className="btn-secondary"
          >
            + Agregar palabra
          </button>
        </div>

        <div className="form-section">
          <h2>Mensaje codificado</h2>
          <p className="hint">Ingresa los números separados por comas (ej: 9,0,3,9,0,...)</p>
          <textarea
            rows={3}
            value={encodedMessage}
            onChange={(e) => setEncodedMessage(e.target.value)}
            placeholder="9,0,3,9,0,0,4,3,9,6,5,1,8,4,8"
            className="textarea-input"
          />
        </div>

        {error && <div className="error-message">{error}</div>}

        <button
          type="submit"
          disabled={loading}
          className="btn-primary"
        >
          {loading ? "Resolviendo..." : "Resolver"}
        </button>
      </form>

      {result && (
        <div className="results-container">
          <h2>Resultados</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Nodos explorados</span>
              <strong>{statistics.historyCount}</strong>
            </div>
            <div className="stat-card">
              <span className="stat-label">Asignaciones</span>
              <strong>{statistics.distinctAssignments}</strong>
            </div>
            <div className="stat-card">
              <span className="stat-label">Estado</span>
              <strong>{result.has_solution ? "Solución" : "Sin solución"}</strong>
            </div>
          </div>
          
          {result.has_solution ? (
            <>
              <div className="result-section">
                <h3>Solución encontrada</h3>
                
                <div className="predictions">
                  <h4>Mapeo letra a dígito</h4>
                  <div className="predictions-grid">
                    {Object.entries(result.predictions).map(([letter, digit]) => (
                      <div key={letter} className="prediction-item">
                        <span className="letter">{letter}</span>
                        <span className="equals">=</span>
                        <span className="digit">{digit}</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="decoded-message">
                  <h4>Mensaje Decodificado</h4>
                  <div className="message-box">
                    {statistics.decodedMessage || "Sin mensaje decodificado"}
                  </div>
                </div>
              </div>

              <div className="result-section educational-section">
                <h3>Modo educativo</h3>
                <p className="hint">El historial muestra cómo el solver fue construyendo y descartando asignaciones.</p>
                <div className="history-list">
                  {historyPreview.length > 0 ? historyPreview.map((item) => (
                    <div key={item.id} className="history-item">
                      <div className="history-title">{item.title}</div>
                      <div className="history-detail">{item.detail}</div>
                    </div>
                  )) : (
                    <div className="history-empty">El historial no contiene pasos intermedios.</div>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="no-solution">No se encontró solución para este criptograma</div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;