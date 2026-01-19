#!/usr/bin/env python3
"""
Archive Legacy Code Script
===========================

Purpose: Archive the legacy gaara_ai_integrated/ directory to ZIP and remove it.
This script is part of Phase 1: Code Stabilization to clean up 150+ syntax errors
in deprecated code.

Usage:
    python scripts/archive_legacy.py [--dry-run] [--target-dir DIR]

Author: Global System v35.0
Date: 2026-01-17
"""

import argparse
import logging
import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class LegacyArchiver:
    """
    Archive legacy code directories to ZIP files.
    
    This class handles the archival of deprecated code directories,
    ensuring safe backup before deletion.
    
    Attributes:
        source_dir (Path): Directory to archive
        archive_dir (Path): Directory where archives are stored
        dry_run (bool): If True, simulate without making changes
    """
    
    def __init__(self, source_dir: str = "gaara_ai_integrated", 
                 archive_dir: str = ".", dry_run: bool = False):
        """
        Initialize the archiver.
        
        Args:
            source_dir: Path to directory to archive
            archive_dir: Path where ZIP archive will be created
            dry_run: If True, only simulate actions
        """
        self.source_dir = Path(source_dir)
        self.archive_dir = Path(archive_dir)
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.archive_name = f"legacy_archive_{self.timestamp}.zip"
        self.archive_path = self.archive_dir / self.archive_name
        
    def validate_source(self) -> bool:
        """
        Validate that source directory exists and is not empty.
        
        Returns:
            bool: True if source is valid, False otherwise
        """
        if not self.source_dir.exists():
            logger.error(f"Source directory does not exist: {self.source_dir}")
            return False
            
        if not self.source_dir.is_dir():
            logger.error(f"Source is not a directory: {self.source_dir}")
            return False
            
        # Check if directory has any content
        try:
            contents = list(self.source_dir.iterdir())
            if not contents:
                logger.warning(f"Source directory is empty: {self.source_dir}")
                return False
        except PermissionError:
            logger.error(f"Permission denied accessing: {self.source_dir}")
            return False
            
        logger.info(f"✓ Source directory validated: {self.source_dir}")
        return True
        
    def create_archive(self) -> Tuple[bool, int]:
        """
        Create ZIP archive of the source directory.
        
        Returns:
            Tuple[bool, int]: (Success status, Number of files archived)
        """
        if self.dry_run:
            logger.info(f"[DRY RUN] Would create archive: {self.archive_path}")
            # Count files for dry run
            file_count = sum(1 for _ in self.source_dir.rglob('*') if _.is_file())
            return True, file_count
            
        try:
            logger.info(f"Creating archive: {self.archive_path}")
            file_count = 0
            
            with zipfile.ZipFile(self.archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Walk through all files in source directory
                for file_path in self.source_dir.rglob('*'):
                    if file_path.is_file():
                        # Calculate relative path for archive
                        arcname = file_path.relative_to(self.source_dir.parent)
                        zipf.write(file_path, arcname)
                        file_count += 1
                        
                        if file_count % 100 == 0:
                            logger.info(f"  Archived {file_count} files...")
            
            logger.info(f"✓ Archive created: {self.archive_path}")
            logger.info(f"  Total files archived: {file_count}")
            return True, file_count
            
        except Exception as e:
            logger.error(f"Failed to create archive: {e}")
            return False, 0
            
    def verify_archive(self) -> bool:
        """
        Verify the integrity of the created archive.
        
        Returns:
            bool: True if archive is valid, False otherwise
        """
        if self.dry_run:
            logger.info("[DRY RUN] Would verify archive integrity")
            return True
            
        if not self.archive_path.exists():
            logger.error(f"Archive not found: {self.archive_path}")
            return False
            
        try:
            # Test ZIP integrity
            with zipfile.ZipFile(self.archive_path, 'r') as zipf:
                # Test all files in archive
                test_result = zipf.testzip()
                if test_result is not None:
                    logger.error(f"Corrupt file in archive: {test_result}")
                    return False
                    
                # Get archive statistics
                file_count = len(zipf.namelist())
                archive_size = self.archive_path.stat().st_size
                archive_size_mb = archive_size / (1024 * 1024)
                
                logger.info(f"✓ Archive verified successfully")
                logger.info(f"  Files in archive: {file_count}")
                logger.info(f"  Archive size: {archive_size_mb:.2f} MB")
                
            return True
            
        except zipfile.BadZipFile:
            logger.error(f"Archive is corrupted: {self.archive_path}")
            return False
        except Exception as e:
            logger.error(f"Failed to verify archive: {e}")
            return False
            
    def remove_source(self) -> bool:
        """
        Remove the source directory after successful archival.
        
        Returns:
            bool: True if removal successful, False otherwise
        """
        if self.dry_run:
            logger.info(f"[DRY RUN] Would remove directory: {self.source_dir}")
            return True
            
        try:
            logger.info(f"Removing source directory: {self.source_dir}")
            shutil.rmtree(self.source_dir)
            logger.info(f"✓ Source directory removed: {self.source_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove source directory: {e}")
            return False
            
    def archive(self) -> bool:
        """
        Execute the complete archival process.
        
        This is the main method that orchestrates:
        1. Validation
        2. Archive creation
        3. Verification
        4. Source removal
        
        Returns:
            bool: True if all steps successful, False otherwise
        """
        logger.info("=" * 60)
        logger.info("Legacy Code Archiver - Starting")
        logger.info("=" * 60)
        
        # Step 1: Validate source
        if not self.validate_source():
            logger.error("✗ Validation failed - Aborting")
            return False
            
        # Step 2: Create archive
        success, file_count = self.create_archive()
        if not success:
            logger.error("✗ Archive creation failed - Aborting")
            return False
            
        # Step 3: Verify archive
        if not self.verify_archive():
            logger.error("✗ Archive verification failed - Aborting")
            # Don't remove source if verification fails
            return False
            
        # Step 4: Remove source
        if not self.remove_source():
            logger.warning("⚠ Archive created but source removal failed")
            logger.warning(f"  Manual cleanup required: {self.source_dir}")
            return False
            
        logger.info("=" * 60)
        logger.info("✓ Archival completed successfully")
        logger.info(f"  Archive: {self.archive_path}")
        logger.info(f"  Files: {file_count}")
        logger.info("=" * 60)
        return True


def main() -> int:
    """
    Main entry point for the archive script.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description='Archive legacy code directory to ZIP and remove it',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Archive gaara_ai_integrated/ directory
  python scripts/archive_legacy.py
  
  # Dry run to see what would happen
  python scripts/archive_legacy.py --dry-run
  
  # Archive custom directory
  python scripts/archive_legacy.py --target-dir old_code/
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate actions without making changes'
    )
    
    parser.add_argument(
        '--target-dir',
        type=str,
        default='gaara_ai_integrated',
        help='Directory to archive (default: gaara_ai_integrated)'
    )
    
    args = parser.parse_args()
    
    # Create archiver instance
    archiver = LegacyArchiver(
        source_dir=args.target_dir,
        dry_run=args.dry_run
    )
    
    # Execute archival
    success = archiver.archive()
    
    # Return exit code
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
