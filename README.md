# ForgeDocs Microservice

Microservicio basado en FastAPI para la automatización de la creación de Google Docs y gestión de permisos en Google Workspace, optimizado para despliegue en Google Cloud Run.

## Características
- **FastAPI**: Arquitectura modular y validación estricta con Pydantic.
- **Google API Client**: Singleton pattern para conexiones eficientes a Docs y Drive.
- **Estructura Organizada**: Creación de documentos directamente en carpetas específicas.
- **Gestión de Permisos**: Permite otorgar acceso a correos específicos y a todo el dominio del Workspace de forma condicional.
- **Auth Cloud-Native**: Soporte para carga de credenciales vía archivos locales o variables de entorno (GCP Secret Manager).

## Estructura del Proyecto
```text
ForgeDocs/
├── scripts/
│   ├── generate_token.py   # Flujo OAuth2 interactivo para generar token.json
│   └── test_drive_access.py# Diagnóstico de permisos y usuario autenticado
├── src/
│   ├── api/                # Endpoints de la API
│   ├── core/               # Singleton de cliente y Configuración
│   ├── schemas/            # Definición de Requests/Responses
│   ├── services/           # Lógica de Google Docs/Drive
│   └── main.py             # App FastAPI
├── .gcloudignore           # Exclusión de archivos para despliegue rápido
├── cloudbuild.yaml         # Pipeline CI/CD para GCP
└── Dockerfile              # Imagen optimizada para Cloud Run
```

## Configuración y Ejecución Local

### 1. Preparación e Instalación
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generar Token de Acceso
Necesitas el archivo `credentials.json` (OAuth Client ID) en la raíz:
```bash
python scripts/generate_token.py
```
*Sigue el flujo en el navegador con tu cuenta de Workspace para generar el `token.json`.*

### 3. Iniciar el Servidor
```bash
uvicorn src.main:app --reload --port=8080
```

## Despliegue en Google Cloud (Producción)

Este proyecto está diseñado para ser **privado** dentro de tu organización de Google Cloud.

### 1. Preparar Secretos
Carga tu `token.json` en Secret Manager:
```bash
gcloud secrets create FORGE_DOCS_TOKEN --replication-policy="automatic"
gcloud secrets versions add FORGE_DOCS_TOKEN --data-file="token.json"
```

### 2. Desplegar
El despliegue usa Artifact Registry y Cloud Run. Asegúrate de tener el repositorio `forge-docs-repo` creado:
```bash
gcloud builds submit --config cloudbuild.yaml . --project=TU_PROJECT_ID
```

## Uso de la API (Endpoint Principal)

### `POST /generate`
Crea un documento, lo ubica en una carpeta y gestiona permisos.

**Ejemplo de Request:**
```json
{
  "document_name": "Reporte de Caso 001",
  "editor_emails": ["abogado@detrabajo.com"],
  "requesting_service": "Main-Orchestrator",
  "parent_folder_id": "ID_DE_LA_CARPETA_DRIVE",
  "share_with_workspace": false
}
```

**Ejemplo de llamada con CURL (Autenticada):**
```bash
curl -X 'POST' \
  'https://TU-URL-CLOUD-RUN/generate' \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H 'Content-Type: application/json' \
  -d '{...}'
```

## Seguridad e IAM
El servicio requiere que la cuenta de servicio de ejecución (o el usuario que lo llama) tenga los siguientes roles:
- `Cloud Run Invoker` (para llamar a la API).
- `Secret Manager Secret Accessor` (para leer el token).
- `Artifact Registry Writer` (para el proceso de build).
