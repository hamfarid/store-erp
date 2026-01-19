"""
Knowledge Base - Gaara Scan AI v4.3.1
Store and manage disease knowledge from analyzed images using PostgreSQL
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Disease knowledge base using PostgreSQL"""
    
    def __init__(self):
        """Initialize knowledge base with PostgreSQL connection"""
        self.database_url = os.getenv("DATABASE_URL", "postgresql://gaara_user:gaara_secure_2024@database:5432/gaara_scan_ai")
        self.pool = None
        self._init_connection_pool()
        self._init_database()
    
    def _init_connection_pool(self):
        """Initialize PostgreSQL connection pool"""
        try:
            self.pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dsn=self.database_url
            )
            logger.info("PostgreSQL connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize connection pool: {str(e)}")
            raise
    
    def _get_connection(self):
        """Get connection from pool"""
        return self.pool.getconn()
    
    def _return_connection(self, conn):
        """Return connection to pool"""
        self.pool.putconn(conn)
    
    def _init_database(self):
        """Initialize database schema"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Create images table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crawler_images (
                    id SERIAL PRIMARY KEY,
                    image_path TEXT NOT NULL,
                    disease_name TEXT,
                    plant_type TEXT,
                    confidence REAL,
                    symptoms JSONB,
                    severity TEXT,
                    affected_area INTEGER,
                    description_en TEXT,
                    description_ar TEXT,
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create diseases table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crawler_diseases (
                    id SERIAL PRIMARY KEY,
                    name TEXT UNIQUE NOT NULL,
                    plant_types JSONB,
                    common_symptoms JSONB,
                    treatments JSONB,
                    image_count INTEGER DEFAULT 0,
                    avg_confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_crawler_disease_name ON crawler_images(disease_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_crawler_plant_type ON crawler_images(plant_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_crawler_created_at ON crawler_images(created_at DESC)")
            
            conn.commit()
            logger.info("Knowledge base schema initialized")
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Failed to initialize database: {str(e)}")
            raise
        finally:
            if conn:
                self._return_connection(conn)
    
    def add_image(
        self,
        image_path: str,
        disease_name: Optional[str],
        confidence: float,
        metadata: Dict
    ):
        """
        Add analyzed image to knowledge base
        
        Args:
            image_path: Path to image file
            disease_name: Detected disease name
            confidence: Detection confidence
            metadata: Additional metadata
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Insert image
            cursor.execute("""
                INSERT INTO crawler_images (
                    image_path, disease_name, plant_type, confidence,
                    symptoms, severity, affected_area,
                    description_en, description_ar, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                image_path,
                disease_name,
                metadata.get("plant_type"),
                confidence,
                json.dumps(metadata.get("symptoms", [])),
                metadata.get("severity"),
                metadata.get("affected_area", 0),
                metadata.get("description_en"),
                metadata.get("description_ar"),
                json.dumps(metadata)
            ))
            
            # Update disease statistics
            if disease_name:
                self._update_disease_stats(cursor, disease_name, metadata)
            
            conn.commit()
            logger.info(f"Added image to knowledge base: {image_path}")
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Failed to add image: {str(e)}")
            raise
        finally:
            if conn:
                self._return_connection(conn)
    
    def _update_disease_stats(self, cursor, disease_name: str, metadata: Dict):
        """Update disease statistics"""
        try:
            # Check if disease exists
            cursor.execute(
                "SELECT id, image_count FROM crawler_diseases WHERE name = %s",
                (disease_name,)
            )
            result = cursor.fetchone()
            
            if result:
                # Update existing disease
                disease_id, image_count = result
                cursor.execute("""
                    UPDATE crawler_diseases
                    SET image_count = image_count + 1,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (disease_id,))
            else:
                # Insert new disease
                cursor.execute("""
                    INSERT INTO crawler_diseases (name, plant_types, common_symptoms, image_count)
                    VALUES (%s, %s, %s, 1)
                """, (
                    disease_name,
                    json.dumps([metadata.get("plant_type")]),
                    json.dumps(metadata.get("symptoms", []))
                ))
                
        except Exception as e:
            logger.error(f"Failed to update disease stats: {str(e)}")
    
    def get_total_images(self) -> int:
        """Get total number of images in knowledge base"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM crawler_images")
            count = cursor.fetchone()[0]
            return count
        except:
            return 0
        finally:
            if conn:
                self._return_connection(conn)
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Total images
            cursor.execute("SELECT COUNT(*) as count FROM crawler_images")
            total_images = cursor.fetchone()['count']
            
            # Total diseases
            cursor.execute("SELECT COUNT(*) as count FROM crawler_diseases")
            total_diseases = cursor.fetchone()['count']
            
            # Images by disease
            cursor.execute("""
                SELECT disease_name, COUNT(*) as count
                FROM crawler_images
                WHERE disease_name IS NOT NULL
                GROUP BY disease_name
                ORDER BY count DESC
                LIMIT 10
            """)
            top_diseases = [{"name": row['disease_name'], "count": row['count']} for row in cursor.fetchall()]
            
            return {
                "total_images": total_images,
                "total_diseases": total_diseases,
                "top_diseases": top_diseases
            }
            
        except Exception as e:
            logger.error(f"Failed to get stats: {str(e)}")
            return {
                "total_images": 0,
                "total_diseases": 0,
                "top_diseases": []
            }
        finally:
            if conn:
                self._return_connection(conn)
    
    def list_diseases(self) -> List[Dict]:
        """List all diseases in knowledge base"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT name, plant_types, image_count, avg_confidence
                FROM crawler_diseases
                ORDER BY image_count DESC
            """)
            
            diseases = []
            for row in cursor.fetchall():
                diseases.append({
                    "name": row['name'],
                    "plant_types": json.loads(row['plant_types']) if row['plant_types'] else [],
                    "image_count": row['image_count'],
                    "avg_confidence": row['avg_confidence']
                })
            
            return diseases
            
        except Exception as e:
            logger.error(f"Failed to list diseases: {str(e)}")
            return []
        finally:
            if conn:
                self._return_connection(conn)
    
    def get_disease_info(self, disease_name: str) -> Optional[Dict]:
        """Get detailed information about a disease"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT name, plant_types, common_symptoms, treatments, image_count
                FROM crawler_diseases
                WHERE name = %s
            """, (disease_name,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Get sample images
            cursor.execute("""
                SELECT image_path, confidence, description_en
                FROM crawler_images
                WHERE disease_name = %s
                ORDER BY confidence DESC
                LIMIT 5
            """, (disease_name,))
            
            sample_images = [
                {
                    "path": r['image_path'],
                    "confidence": r['confidence'],
                    "description": r['description_en']
                }
                for r in cursor.fetchall()
            ]
            
            return {
                "name": row['name'],
                "plant_types": json.loads(row['plant_types']) if row['plant_types'] else [],
                "common_symptoms": json.loads(row['common_symptoms']) if row['common_symptoms'] else [],
                "treatments": json.loads(row['treatments']) if row['treatments'] else [],
                "image_count": row['image_count'],
                "sample_images": sample_images
            }
            
        except Exception as e:
            logger.error(f"Failed to get disease info: {str(e)}")
            return None
        finally:
            if conn:
                self._return_connection(conn)
    
    def close(self):
        """Close connection pool"""
        if self.pool:
            self.pool.closeall()
            logger.info("PostgreSQL connection pool closed")
