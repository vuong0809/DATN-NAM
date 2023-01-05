
import os
import uuid
import aiofiles
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, UploadFile, File
from pydantic import BaseModel

# from fire_detect import run

router = APIRouter()