# CryptoSolver

CryptoSolver es una aplicación web para resolver criptaritmos y descifrar mensajes codificados mediante un solver de backtracking. Combina un frontend en React con un backend en FastAPI que procesa la lógica de resolución y devuelve el mapeo de letras a dígitos.

## Qué hace

- Permite ingresar varias palabras que representan un cálculo criptográfico de suma.
- Recibe un mensaje codificado como una secuencia de dígitos separados por comas.
- Calcula una asignación letra → dígito que satisface la suma.
- Decodifica el mensaje con la solución encontrada.
- Presenta un historial de asignaciones para analizar el proceso de backtracking.

## Tecnologías

- Frontend: React 19, CSS, Create React App
- Backend: Python, FastAPI, Uvicorn
- Lógica: Solver de criptaritmos con backtracking, normalización de matriz y restricciones de dígitos no nulos

## Estructura del proyecto

```
backend/                # Backend Python con FastAPI y el solver
frontend/               # Frontend React para la interfaz web
frontend/.env           # Configuración del URL del API
frontend/package.json   # Dependencias y scripts del frontend
backend/api.py          # Endpoints del servidor
backend/CryptoSolver.py # Lógica de resolución criptográfica
``` 

## Desarrolladores

- Daniela Salazar
- Laura Indabur
- Andrés Mazo
- Santiago Ramírez

## Requisitos

- Node.js 14+ y npm
- Python 3.8+ (o compatible con FastAPI)
- Dependencias de Python: `fastapi`, `uvicorn`

## Instalación y ejecución

### 1. Iniciar el backend

Abre una terminal y ve a la carpeta del backend:

```powershell
cd C:\Users\15-cw1010la\Desktop\cryptoSolver\cryptoSolver
```

Instala FastAPI y Uvicorn si no están instalados:

```powershell
pip install fastapi uvicorn
```

Inicia el servidor:

```powershell
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

El backend quedará disponible en:

- `http://localhost:8000`

### 2. Iniciar el frontend

Abre otra terminal y ve a la carpeta del frontend:

```powershell
cd C:\Users\15-cw1010la\Desktop\cryptoSolver\cryptoSolver\frontend
```

Instala las dependencias de npm:

```powershell
npm install
```

Inicia la aplicación React:

```powershell
npm start
```

El frontend se abrirá en:

- `http://localhost:3000`

> Asegúrate de tener el backend corriendo antes de usar la aplicación para que el frontend pueda comunicarse con la API.

## Configuración del `.env`

En `frontend/.env` se define la URL del backend:

```env
REACT_APP_API_URL=http://localhost:8000
```

Si cambias el puerto o el host del backend, actualiza esta variable y reinicia `npm start`.

## API disponible

### POST /solve

Resuelve un criptograma.

**Request**:

```json
{
  "matrix": [["h","a","r","r","y"], ["p","o","t","t","e","r"], ["t","r","o","l","l","s"]],
  "encoded_message": [9,0,3,9,0,0,4,3,9,6,5,1,8,4,8]
}
```

**Response**:

```json
{
  "has_solution": true,
  "predictions": {"h": 9, "a": 0, "r": 3, "p": 4, ...},
  "history": [...],
  "decoded_message": ["m","a","g","i","c"]
}
```

### GET /health

Comprueba que el servidor está activo.

**Response**:

```json
{
  "status": "ok"
}
```

## Uso de la aplicación

1. Carga un ejemplo clásico o ingresa tus propias palabras.
2. Escribe el mensaje codificado como números separados por comas.
3. Haz clic en `Resolver`.
4. Revisa el mapeo letra → dígito, el estado de solución y el mensaje decodificado.
5. Observa el historial de asignaciones para ver cómo el solver construyó y descartó soluciones.

## Ejemplos incluidos

- `HARRY + POTTER = TROLLS`
- `SEND + MORE = MONEY`
- `TWO + TWO = FOUR`

## Problemas comunes

- Si el frontend muestra un error de conexión, valida que el backend esté corriendo en `http://localhost:8000`.
- Si el mensaje codificado no se parsea, usa números separados por comas sin texto adicional.
- Si el backend falla al iniciar, asegúrate de usar Python 3.8+ y tener instaladas las dependencias.

## Notas de desarrollo

- El solver construye una matriz de letras y aplica backtracking por columna.
- Las primeras letras de cada palabra no pueden recibir el dígito `0`.
- El historial de búsqueda refleja asignaciones tentativas y retrocesos.
