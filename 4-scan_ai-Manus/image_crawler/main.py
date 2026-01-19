"""
Image Crawler Service - Gaara Scan AI v4.3.1
Intelligent crawler for searching, downloading, and analyzing plant disease images
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
from datetime import datetime, timezone
import asyncio

from crawler import ImageCrawler
from analyzer import ImageAnalyzer
from knowledge_base import KnowledgeBase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Gaara Scan AI - Image Crawler Service",
    description="Intelligent crawler for plant disease images",
    version="4.3.1"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
crawler = ImageCrawler()
analyzer = ImageAnalyzer()
knowledge_base = KnowledgeBase()

# Models
class CrawlRequest(BaseModel):
    """Image crawl request"""
    query: str
    max_images: int = 50
    languages: List[str] = ["en", "ar"]
    sources: List[str] = ["google", "bing", "unsplash"]

class CrawlResponse(BaseModel):
    """Image crawl response"""
    success: bool
    task_id: str
    message: str

class CrawlStatus(BaseModel):
    """Crawl task status"""
    task_id: str
    status: str
    progress: int
    total_images: int
    analyzed_images: int
    message: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
    stats: Dict

# In-memory task storage (use Redis in production)
tasks = {}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    stats = {
        "total_tasks": len(tasks),
        "active_tasks": len([t for t in tasks.values() if t["status"] == "running"]),
        "completed_tasks": len([t for t in tasks.values() if t["status"] == "completed"]),
        "total_images": knowledge_base.get_total_images()
    }
    
    return HealthResponse(
        status="healthy",
        version="4.3.1",
        timestamp=datetime.now(timezone.utc).isoformat(),
        stats=stats
    )

@app.post("/api/v1/crawl", response_model=CrawlResponse)
async def start_crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    """
    Start intelligent image crawling

    - **query**: Search query (e.g., "tomato leaf disease")
    - **max_images**: Maximum number of images to download
    - **languages**: Languages for search
    - **sources**: Image sources to use
    """
    try:
        # Generate task ID
        task_id = f"crawl_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

        # Initialize task
        tasks[task_id] = {
            "status": "running",
            "progress": 0,
            "total_images": 0,
            "analyzed_images": 0,
            "message": "Starting crawl...",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Start background task
        background_tasks.add_task(
            run_crawl_task,
            task_id,
            request.query,
            request.max_images,
            request.languages,
            request.sources
        )
        
        logger.info(f"Started crawl task {task_id} for query: {request.query}")
        
        return CrawlResponse(
            success=True,
            task_id=task_id,
            message="Crawl task started successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to start crawl: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/crawl/{task_id}", response_model=CrawlStatus)
async def get_crawl_status(task_id: str):
    """
    Get crawl task status
    
    - **task_id**: Task ID from crawl request
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    return CrawlStatus(
        task_id=task_id,
        status=task["status"],
        progress=task["progress"],
        total_images=task["total_images"],
        analyzed_images=task["analyzed_images"],
        message=task["message"]
    )

@app.get("/api/v1/knowledge")
async def get_knowledge_stats():
    """Get knowledge base statistics"""
    try:
        stats = knowledge_base.get_stats()
        return {
            "success": True,
            "data": stats,
            "message": "Knowledge base statistics retrieved"
        }
    except Exception as e:
        logger.error(f"Failed to get knowledge stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/diseases")
async def list_diseases():
    """List all known diseases in knowledge base"""
    try:
        diseases = knowledge_base.list_diseases()
        return {
            "success": True,
            "data": diseases,
            "message": "Diseases list retrieved"
        }
    except Exception as e:
        logger.error(f"Failed to list diseases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/diseases/{disease_name}")
async def get_disease_info(disease_name: str):
    """Get detailed information about a specific disease"""
    try:
        info = knowledge_base.get_disease_info(disease_name)
        if not info:
            raise HTTPException(status_code=404, detail="Disease not found")
        
        return {
            "success": True,
            "data": info,
            "message": "Disease information retrieved"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get disease info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_crawl_task(
    task_id: str,
    query: str,
    max_images: int,
    languages: List[str],
    sources: List[str]
):
    """Background task for crawling and analyzing images"""
    try:
        # Update task status
        tasks[task_id]["message"] = "Searching for images..."
        
        # Search and download images
        images = await crawler.search_and_download(
            query=query,
            max_images=max_images,
            languages=languages,
            sources=sources
        )
        
        tasks[task_id]["total_images"] = len(images)
        tasks[task_id]["progress"] = 50
        tasks[task_id]["message"] = f"Downloaded {len(images)} images, analyzing..."
        
        # Analyze each image
        for i, image_path in enumerate(images):
            try:
                # Analyze image
                analysis = await analyzer.analyze_image(image_path)
                
                # Add to knowledge base
                knowledge_base.add_image(
                    image_path=image_path,
                    disease_name=analysis.get("disease_name"),
                    confidence=analysis.get("confidence"),
                    metadata=analysis
                )
                
                tasks[task_id]["analyzed_images"] = i + 1
                tasks[task_id]["progress"] = 50 + int((i + 1) / len(images) * 50)
                
            except Exception as e:
                logger.error(f"Failed to analyze image {image_path}: {str(e)}")
                continue
        
        # Update task status
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["progress"] = 100
        tasks[task_id]["message"] = f"Completed! Analyzed {tasks[task_id]['analyzed_images']} images"
        
        logger.info(f"Crawl task {task_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Crawl task {task_id} failed: {str(e)}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["message"] = f"Failed: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 4601))
    uvicorn.run(app, host="0.0.0.0", port=port)
