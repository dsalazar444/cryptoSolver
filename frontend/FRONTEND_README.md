# CryptoSolver Frontend

Una interfaz web moderna y responsiva para resolver criptogramas de suma (cryptarithmetic puzzles).

## Características

✨ **Interfaz intuitiva**: Formularios amigables para ingresar datos
🎨 **Diseño profesional**: UI moderna con gradientes y animaciones suaves
📊 **Visualización clara**: Resultados presentados de forma visual y fácil de entender
🔗 **Integración con API**: Conecta con el backend de Python mediante FastAPI
📱 **Responsivo**: Funciona perfectamente en desktop, tablet y móvil

## Requisitos

- Node.js 14+ 
- npm o yarn
- Backend corriendo en `http://localhost:8000`

## Instalación

1. **Instalar dependencias**:
```bash
npm install
```

2. **Configurar la URL del API** (opcional):
Crear un archivo `.env` en la raíz del proyecto:
```
REACT_APP_API_URL=http://localhost:8000
```

## Uso

### Modo desarrollo
```bash
npm start
```
La aplicación se abrirá en `http://localhost:3000`

### Build para producción
```bash
npm run build
```

### Ejecutar tests
```bash
npm test
```

## Cómo usar la aplicación

1. **Ingresa las palabras**: Escribe las palabras que forman parte del criptograma
   - Usa el botón "+ Agregar palabra" para añadir más palabras
   - Usa la "✕" para eliminar palabras

2. **Ingresa el mensaje codificado**: Los números separados por comas representan el mensaje
   - Ejemplo: `9,0,3,9,0,0,4,3,9,6,5,1,8,4,8`

3. **Resuelve**: Haz clic en "Resolver"

4. **Ver resultados**:
   - Mapeo de letras a dígitos
   - Mensaje decodificado
   - Indicador de si se encontró solución

## Estructura del proyecto

```
frontend/
├── public/              # Archivos estáticos
├── src/
│   ├── components/      # Componentes React
│   ├── services/
│   │   └── api.js       # Funciones de API
│   ├── App.js           # Componente principal
│   ├── App.css          # Estilos principales
│   ├── index.css        # Estilos globales
│   └── index.js         # Punto de entrada
└── package.json         # Dependencias
```

## API disponible

### POST /solve
Resuelve un criptograma

**Request:**
```json
{
  "matrix": [["h","a","r","r","y"],["p","o","t","t","e","r"],["t","r","o","l","l","s"]],
  "encoded_message": [9,0,3,9,0,0,4,3,9,6,5,1,8,4,8]
}
```

**Response:**
```json
{
  "has_solution": true,
  "predictions": {"h": 9, "a": 0, "r": 3, "p": 4, ...},
  "history": [...],
  "decoded_message": ["m", "a", "g", "i", "c"]
}
```

### GET /health
Verifica que el servidor está activo

## Tecnologías

- **React 19**: Interfaz de usuario
- **CSS3**: Estilos y animaciones
- **Fetch API**: Comunicación con el backend

## Troubleshooting

### "Error: The API server is not responding"
- Verifica que el backend esté corriendo en `http://localhost:8000`
- Comprueba la URL configurada en `.env`

### "Error: Por favor completa todas las palabras"
- Asegúrate de completar todos los campos de palabras sin dejar ninguno vacío

### "Error: Por favor ingresa números válidos"
- Verifica que los números estén separados por comas
- Los números deben ser enteros válidos

## Desarrollo

### Agregar una nueva característica

1. Crea un nuevo componente en `src/components/`
2. Importa el componente en `App.js`
3. Añade los estilos correspondientes en el CSS
4. Prueba con `npm test`

### Mejorar los estilos

Modifica `src/App.css` y `src/index.css` según necesites. Los estilos están organizados por secciones para facilitar el mantenimiento.

## Licencia

Este proyecto es parte de un proyecto académico.

## Contribuciones

Para reportar bugs o sugerir mejoras, por favor abre un issue en el repositorio.
