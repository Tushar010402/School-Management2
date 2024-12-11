"""
Storage module for handling file uploads to S3 or local filesystem.
"""
import os
import boto3
from typing import Optional
from fastapi import UploadFile
from app.core.config import get_settings

settings = get_settings()

def get_s3_client():
    """Get an S3 client."""
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

async def upload_file_to_s3(
    file: UploadFile,
    folder: str,
    filename: Optional[str] = None
) -> str:
    """
    Upload a file to S3 and return the URL.
    
    Args:
        file: The file to upload
        folder: The folder to upload to (e.g., "student-documents")
        filename: Optional filename to use instead of the original
    
    Returns:
        str: The URL of the uploaded file
    """
    if not settings.USE_S3:
        # Save locally
        local_path = os.path.join(settings.UPLOAD_DIR, folder)
        os.makedirs(local_path, exist_ok=True)
        
        if not filename:
            filename = file.filename
        
        file_path = os.path.join(local_path, filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return f"/uploads/{folder}/{filename}"
    
    # Upload to S3
    s3 = get_s3_client()
    
    if not filename:
        filename = file.filename
    
    key = f"{folder}/{filename}"
    content = await file.read()
    
    s3.put_object(
        Bucket=settings.AWS_BUCKET_NAME,
        Key=key,
        Body=content,
        ContentType=file.content_type
    )
    
    return f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/{key}"

async def delete_file_from_s3(file_url: str) -> bool:
    """
    Delete a file from S3.
    
    Args:
        file_url: The URL of the file to delete
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not settings.USE_S3:
        # Delete local file
        try:
            local_path = file_url.replace("/uploads/", settings.UPLOAD_DIR + "/")
            os.remove(local_path)
            return True
        except Exception:
            return False
    
    # Delete from S3
    try:
        s3 = get_s3_client()
        key = file_url.split(".com/")[-1]
        
        s3.delete_object(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=key
        )
        return True
    except Exception:
        return False