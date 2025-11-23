"""
Google Drive Integration for Louie Bernstein Content Agent

This module provides functionality to:
- Download files and folders from Google Drive
- Read files from Google Drive
- Organize content by type and category
"""

import os
import json
import io
from pathlib import Path
from typing import Optional, Dict, List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Scopes required for read access
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

class GoogleDriveIntegration:
    """Handle Google Drive operations for content ingestion."""
    
    def __init__(self, credentials_file: str = "credentials.json", token_file: str = "token.json"):
        """
        Initialize Google Drive integration.
        
        Args:
            credentials_file: Path to Google OAuth credentials JSON file
            token_file: Path to save/load authentication token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API."""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "Please download credentials.json from Google Cloud Console"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('drive', 'v3', credentials=creds)
        print("✅ Authenticated with Google Drive")
    
    def find_folder(self, folder_name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Find a folder by name.
        
        Args:
            folder_name: Name of the folder to find
            parent_id: Optional parent folder ID to search within
        
        Returns:
            Folder ID if found, None otherwise
        """
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        try:
            results = self.service.files().list(
                q=query,
                fields="files(id, name)"
            ).execute()
            
            items = results.get('files', [])
            if items:
                return items[0]['id']
            return None
        except HttpError as error:
            print(f"❌ Error finding folder: {error}")
            return None
    
    def list_files(self, folder_id: Optional[str] = None, query: Optional[str] = None, recursive: bool = True) -> List[Dict]:
        """
        List files in Google Drive folder recursively.
        
        Args:
            folder_id: Optional folder ID to list files from
            query: Optional custom query string
            recursive: Whether to recursively list subfolders
        
        Returns:
            List of file dictionaries with id, name, mimeType, parents
        """
        all_files = []
        
        if query is None:
            query = "trashed=false"
            if folder_id:
                query += f" and '{folder_id}' in parents"
        
        try:
            page_token = None
            while True:
                results = self.service.files().list(
                    q=query,
                    fields="nextPageToken, files(id, name, mimeType, parents, modifiedTime, size)",
                    pageToken=page_token,
                    pageSize=1000
                ).execute()
                
                items = results.get('files', [])
                all_files.extend(items)
                
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            
            # If recursive, also get subfolders
            if recursive and folder_id:
                # Get all folders
                folder_query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
                folders = []
                page_token = None
                while True:
                    folder_results = self.service.files().list(
                        q=folder_query,
                        fields="nextPageToken, files(id, name, parents)",
                        pageToken=page_token,
                        pageSize=1000
                    ).execute()
                    
                    folder_items = folder_results.get('files', [])
                    folders.extend(folder_items)
                    
                    page_token = folder_results.get('nextPageToken')
                    if not page_token:
                        break
                
                # Recursively get files from subfolders
                for folder in folders:
                    subfolder_files = self.list_files(folder_id=folder['id'], recursive=True)
                    all_files.extend(subfolder_files)
            
            return all_files
        except HttpError as error:
            print(f"❌ Error listing files: {error}")
            return []
    
    def read_file(self, file_id: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        Read a file from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            output_path: Optional local path to save the file
        
        Returns:
            File content as string (for text files) or path to saved file
        """
        try:
            # Get file metadata
            file_metadata = self.service.files().get(fileId=file_id).execute()
            file_name = file_metadata.get('name')
            mime_type = file_metadata.get('mimeType')
            
            # Handle Google Workspace files (Docs, Sheets, etc.)
            if 'google-apps' in mime_type:
                if mime_type == 'application/vnd.google-apps.document':
                    # Export as text
                    request = self.service.files().export_media(
                        fileId=file_id,
                        mimeType='text/plain'
                    )
                elif mime_type == 'application/vnd.google-apps.spreadsheet':
                    request = self.service.files().export_media(
                        fileId=file_id,
                        mimeType='text/csv'
                    )
                else:
                    # Try to export as PDF
                    request = self.service.files().export_media(
                        fileId=file_id,
                        mimeType='application/pdf'
                    )
            else:
                # Regular file download
                request = self.service.files().get_media(fileId=file_id)
            
            # Download file
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                fh = io.FileIO(output_path, 'wb')
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                print(f"✅ Downloaded: {file_name} -> {output_path}")
                return output_path
            else:
                # Return content as string
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                content = fh.getvalue().decode('utf-8', errors='ignore')
                return content
                
        except HttpError as error:
            print(f"❌ Error reading file: {error}")
            return None
    
    def download_folder(self, folder_id: str, local_path: str, file_filter: Optional[List[str]] = None) -> Dict[str, str]:
        """
        Download all files from a Google Drive folder.
        
        Args:
            folder_id: Google Drive folder ID
            local_path: Local directory to save files
            file_filter: Optional list of file extensions to include (e.g., ['.pdf', '.docx'])
        
        Returns:
            Dictionary mapping file IDs to local file paths
        """
        os.makedirs(local_path, exist_ok=True)
        files = self.list_files(folder_id=folder_id, recursive=True)
        
        downloaded = {}
        for file_info in files:
            file_id = file_info['id']
            file_name = file_info['name']
            mime_type = file_info.get('mimeType', '')
            
            # Apply file filter if provided
            if file_filter:
                file_ext = os.path.splitext(file_name)[1].lower()
                if file_ext not in file_filter and 'google-apps' not in mime_type:
                    continue
            
            # Create safe filename
            safe_name = "".join(c for c in file_name if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
            local_file_path = os.path.join(local_path, safe_name)
            
            # Handle duplicate names
            counter = 1
            original_path = local_file_path
            while os.path.exists(local_file_path):
                name, ext = os.path.splitext(original_path)
                local_file_path = f"{name}_{counter}{ext}"
                counter += 1
            
            content = self.read_file(file_id, local_file_path)
            if content:
                downloaded[file_id] = local_file_path
        
        print(f"✅ Downloaded {len(downloaded)} files to {local_path}")
        return downloaded

