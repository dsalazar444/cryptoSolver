// API configuration and helper functions

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const fetchExamples = async () => {
  const response = await fetch(`${API_BASE_URL}/examples`);

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return await response.json();
};

export const solveAPI = async (words, encodedMessage) => {
  // Convert words to matrix
  const matrix = words.map(word => word.toLowerCase().split(""));
  
  // Parse encoded message
  const encoded = encodedMessage
    .split(",")
    .map(n => parseInt(n.trim()))
    .filter(n => !isNaN(n));

  if (!matrix.length || !encoded.length) {
    throw new Error("Please provide valid input");
  }

  const response = await fetch(`${API_BASE_URL}/solve`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json" 
    },
    body: JSON.stringify({
      matrix: matrix,
      encoded_message: encoded,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || `API Error: ${response.statusText}`
    );
  }

  return await response.json();
};

export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
};
