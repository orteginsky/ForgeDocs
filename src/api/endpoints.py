from fastapi import APIRouter, HTTPException
from ..schemas.request_schemas import GenerateDocRequest, GenerateDocResponse
from ..services.google_docs_service import GoogleDocsService

router = APIRouter()

@router.post("/generate", response_model=GenerateDocResponse)
async def generate_document(request: GenerateDocRequest):
    """
    Endpoint to trigger Google Doc generation and permission assignment.
    """
    try:
        result = GoogleDocsService.process_generation(
            title=request.document_name,
            editor_emails=request.editor_emails,
            requesting_service=request.requesting_service,
            parent_folder_id=request.parent_folder_id,
            share_with_workspace=request.share_with_workspace
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
