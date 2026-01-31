"""
FILE: image_crawler/crawler.py | PURPOSE: Async image crawler with pooling
OWNER: ML Team | RELATED: data_collection | LAST-AUDITED: 2026-01-31

Image Crawler - Gaara Scan AI v4.3.1
Search and download plant disease images from multiple sources.
Features: Connection pooling, rate limiting, retry logic, async I/O.
"""

import httpx
import asyncio
import logging
from pathlib import Path
from typing import List, Optional, Dict
import hashlib
from datetime import datetime, timezone
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class RateLimiter:
    """Token bucket rate limiter for controlling request rate."""

    def __init__(self, rate: float = 5.0, burst: int = 10):
        """
        Initialize rate limiter.

        Args:
            rate: Requests per second
            burst: Maximum burst size
        """
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_update = asyncio.get_event_loop().time()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary."""
        async with self._lock:
            now = asyncio.get_event_loop().time()
            elapsed = now - self.last_update
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate
                await asyncio.sleep(wait_time)
                self.tokens = 0
            else:
                self.tokens -= 1


class ImageCrawler:
    """
    Intelligent async image crawler with connection pooling.

    Features:
    - Connection pooling for efficient HTTP connections
    - Rate limiting to avoid overwhelming servers
    - Retry logic with exponential backoff
    - Concurrent downloads with semaphore control
    """

    def __init__(
        self,
        download_dir: str = "data/images",
        max_connections: int = 10,
        rate_limit: float = 5.0,
        max_retries: int = 3
    ):
        """
        Initialize crawler.

        Args:
            download_dir: Directory to save downloaded images
            max_connections: Maximum concurrent connections
            rate_limit: Requests per second limit
            max_retries: Maximum retry attempts
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = httpx.Timeout(30.0, connect=10.0)
        self.max_connections = max_connections
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None
        self._rate_limiter = RateLimiter(rate=rate_limit, burst=max_connections)
        self._semaphore = asyncio.Semaphore(max_connections)
        self._stats: Dict[str, int] = {
            "downloaded": 0,
            "failed": 0,
            "skipped": 0
        }

    @asynccontextmanager
    async def _get_client(self):
        """Get or create HTTP client with connection pooling."""
        if self._client is None or self._client.is_closed:
            limits = httpx.Limits(
                max_connections=self.max_connections,
                max_keepalive_connections=self.max_connections // 2
            )
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                limits=limits,
                follow_redirects=True,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
                    )
                }
            )
        yield self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    def get_stats(self) -> Dict[str, int]:
        """Get download statistics."""
        return self._stats.copy()
        
    async def search_and_download(
        self,
        query: str,
        max_images: int = 50,
        languages: List[str] = ["en", "ar"],
        sources: List[str] = ["google", "bing"]
    ) -> List[str]:
        """
        Search and download images
        
        Args:
            query: Search query
            max_images: Maximum number of images
            languages: Languages for search
            sources: Image sources
            
        Returns:
            List of downloaded image paths
        """
        logger.info(f"Starting image search for: {query}")
        
        # Collect image URLs from all sources
        image_urls = []
        
        for source in sources:
            try:
                if source == "google":
                    urls = await self._search_google(query, max_images // len(sources))
                elif source == "bing":
                    urls = await self._search_bing(query, max_images // len(sources))
                elif source == "unsplash":
                    urls = await self._search_unsplash(query, max_images // len(sources))
                else:
                    logger.warning(f"Unknown source: {source}")
                    continue
                
                image_urls.extend(urls)
                logger.info(f"Found {len(urls)} images from {source}")
                
            except Exception as e:
                logger.error(f"Failed to search {source}: {str(e)}")
                continue
        
        # Remove duplicates
        image_urls = list(set(image_urls))[:max_images]
        
        # Download images concurrently with rate limiting
        tasks = [self._download_image(url) for url in image_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        downloaded_paths = []
        for result in results:
            if isinstance(result, Exception):
                self._stats["failed"] += 1
            elif result:
                downloaded_paths.append(str(result))
                self._stats["downloaded"] += 1

        logger.info(
            f"Downloaded {len(downloaded_paths)} images "
            f"(failed: {self._stats['failed']})"
        )
        return downloaded_paths
    
    async def _search_google(self, query: str, max_results: int) -> List[str]:
        """
        Search Google Images (mock implementation)
        
        Note: In production, use Google Custom Search API
        """
        # Mock implementation - returns empty list
        # TODO: Implement Google Custom Search API integration
        logger.info(f"Google search for: {query} (mock)")
        return []
    
    async def _search_bing(self, query: str, max_results: int) -> List[str]:
        """
        Search Bing Images (mock implementation)
        
        Note: In production, use Bing Image Search API
        """
        # Mock implementation - returns empty list
        # TODO: Implement Bing Image Search API integration
        logger.info(f"Bing search for: {query} (mock)")
        return []
    
    async def _search_unsplash(self, query: str, max_results: int) -> List[str]:
        """
        Search Unsplash (mock implementation)
        
        Note: In production, use Unsplash API
        """
        # Mock implementation - returns empty list
        # TODO: Implement Unsplash API integration
        logger.info(f"Unsplash search for: {query} (mock)")
        return []
    
    async def _download_image(self, url: str) -> Optional[Path]:
        """
        Download image with connection pooling, rate limiting, and retry.

        Args:
            url: Image URL

        Returns:
            Path to downloaded image, or None if failed
        """
        async with self._semaphore:  # Limit concurrent downloads
            await self._rate_limiter.acquire()  # Rate limiting

            for attempt in range(self.max_retries):
                try:
                    async with self._get_client() as client:
                        response = await client.get(url)
                        response.raise_for_status()

                        # Validate content type
                        content_type = response.headers.get("Content-Type", "")
                        if not content_type.startswith("image/"):
                            self._stats["skipped"] += 1
                            logger.debug(f"Skipped non-image: {url}")
                            return None

                        # Generate filename from URL hash
                        url_hash = hashlib.md5(url.encode()).hexdigest()
                        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                        filename = f"{ts}_{url_hash}.jpg"
                        filepath = self.download_dir / filename

                        # Save image
                        filepath.write_bytes(response.content)
                        logger.info(f"Downloaded: {filepath}")
                        return filepath

                except httpx.HTTPStatusError as e:
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        logger.warning(
                            f"Retry {attempt + 1}/{self.max_retries} "
                            f"for {url}: {e}"
                        )
                        await asyncio.sleep(wait_time)
                        continue
                    logger.error(
                        f"Failed after {self.max_retries} attempts: {url}"
                    )
                    return None

                except httpx.TimeoutException:
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Timeout, retry {attempt + 1}: {url}")
                        await asyncio.sleep(wait_time)
                        continue
                    logger.error(f"Timeout after {self.max_retries} attempts: {url}")
                    return None

                except Exception as e:
                    logger.error(f"Failed to download {url}: {e}")
                    return None

        return None
