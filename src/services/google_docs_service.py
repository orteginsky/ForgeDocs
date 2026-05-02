import logging
from typing import List, Optional
from ..core.google_auth import google_client
from ..core.config import settings

logger = logging.getLogger(__name__)

class GoogleDocsService:
    @staticmethod
    def create_document(title: str, parent_folder_id: Optional[str] = None) -> str:
        """
        Creates a new Google Doc. 
        If parent_folder_id is provided, it's created inside that folder.
        """
        drive = google_client.drive
        
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        # Usar parent_folder_id provisto o el default de configuración
        pid = parent_folder_id or settings.DEFAULT_PARENT_FOLDER_ID
        
        if pid:
            file_metadata['parents'] = [pid]
            logger.info(f"Creating document in folder: {pid}")

        file = drive.files().create(
            body=file_metadata, 
            fields='id'
        ).execute()
        
        doc_id = file.get('id')
        logger.info(f"Created document: {title} with ID: {doc_id}")
        return doc_id

    @staticmethod
    def grant_permissions(file_id: str, emails: List[str], share_with_workspace: bool = False):
        """
        Grants 'writer' permissions to a list of emails and optionally to the workspace domain.
        Includes default service accounts from settings.
        """
        drive = google_client.drive

        # Combine provided emails with default service accounts
        all_emails = list(set(emails + settings.DEFAULT_SERVICE_ACCOUNTS))

        # 1. Grant domain-wide access if requested and domain is configured
        if share_with_workspace and settings.WORKSPACE_DOMAIN:
            domain_permission = {
                'type': 'domain',
                'role': 'writer',
                'domain': settings.WORKSPACE_DOMAIN
            }
            try:
                drive.permissions().create(
                    fileId=file_id,
                    body=domain_permission,
                    fields='id'
                ).execute()
                logger.info(f"Granted writer permission to domain: {settings.WORKSPACE_DOMAIN}")
            except Exception as e:
                logger.warning(f"Failed to grant domain permission: {str(e)}")

        # 2. Grant access to specific emails (explicit + defaults)
        for email in all_emails:
            user_permission = {
                'type': 'user',
                'role': 'writer',
                'emailAddress': email
            }
            try:
                drive.permissions().create(
                    fileId=file_id,
                    body=user_permission,
                    fields='id'
                ).execute()
                logger.info(f"Granted writer permission to: {email}")
            except Exception as e:
                logger.error(f"Failed to grant permission to {email}: {str(e)}")

    @classmethod
    def process_generation(cls, title: str, editor_emails: List[str], requesting_service: str, 
                           parent_folder_id: Optional[str] = None, share_with_workspace: bool = False) -> dict:
        """
        Orchestrates the creation and permission management.
        """
        logger.info(f"Processing request from {requesting_service} for doc: {title}")
        
        # Create the doc
        doc_id = cls.create_document(title, parent_folder_id)
        
        # Grant permissions
        cls.grant_permissions(
            file_id=doc_id, 
            emails=editor_emails, 
            share_with_workspace=share_with_workspace
        )
        
        return {
            "document_id": doc_id,
            "document_url": f"https://docs.google.com/document/d/{doc_id}/edit",
            "status": "success"
        }
