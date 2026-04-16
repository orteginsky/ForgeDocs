from pydantic import BaseModel, EmailStr
from typing import List, Optional

class GenerateDocRequest(BaseModel):
    document_name: str
    editor_emails: List[EmailStr]
    requesting_service: str
    parent_folder_id: Optional[str] = None
    share_with_workspace: bool = False

class GenerateDocResponse(BaseModel):
    document_id: str
    document_url: str
    status: str
