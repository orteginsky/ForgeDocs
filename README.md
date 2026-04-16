# ForgeDocs Microservice

Microservicio basado en FastAPI para la automatización de la creación de Google Docs y gestión de permisos en Google Workspace.

## Características
- **FastAPI**: Arquitectura modular y limpia.
- **Google API Client**: Singleton pattern para conexiones eficientes.
- **Autenticación**: OAuth2 de Usuario con manejo de tokens persistentes.
- **Permisos**: Gestión automática de permisos para dominios y correos específicos.

## Estructura del Proyecto
```text
ForgeDocs/
├── scripts/
│   └── generate_token.py  # Script para generar token.json (browser flow)
├── src/
│   ├── api/               # Endpoints de la API
│   ├── core/              # Configuración y Auth
│   ├── schemas/           # Modelos Pydantic (Validación)
│   ├── services/          # Lógica de negocio
│   └── main.py            # Punto de entrada
├── Dockerfile             # Optimizado para Cloud Run
├── requirements.txt       # Dependencias
├── credentials.json       # Tu Client ID de Google (OAuth)
└── token.json             # Generado por el script (No subir a Git)
```

## Configuración y Ejecución Local

### 1. Preparación
Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### 2. Autenticación (Solo la primera vez)
Como este servicio usa OAuth2 de Usuario, necesitas generar un token inicial mediante el navegador:
```bash
python scripts/generate_token.py
```
*Esto abrirá una ventana en tu navegador. Autoriza la aplicación y se creará el archivo `token.json` automáticamente.*

### 3. Iniciar el Servidor
Una vez generado el token, arranca el microservicio:
```bash
uvicorn src.main:app --reload --port=8080
```
*El servidor refrescará el token automáticamente si expira.*

## Despliegue con Google Cloud Build

Para despliegue en producción (Cloud Run):
1. Asegúrate de incluir el `token.json` en un lugar seguro (Secret Manager es lo ideal).
2. Ejecuta:
```bash
gcloud builds submit --config cloudbuild.yaml .
```

## Endpoints Principales

### `POST /generate`
Genera un documento y otorga permisos.

**Request Body:**
```json
{
  "document_name": "Reporte Mensual Abril",
  "editor_emails": ["usuario@ejemplo.com"],
  "requesting_service": "Servicio_Ventas"
}
```
