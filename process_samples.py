#!/usr/bin/env python3
"""
Process all sample articles and generate HTML files.
"""

import os
import sys
import glob
import logging
from src.__main__ import create_pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_article(input_file, output_dir):
    """Process a single article file and generate HTML output."""
    basename = os.path.basename(input_file)
    name, _ = os.path.splitext(basename)
    output_file = os.path.join(output_dir, f"{name}.html")
    
    logger.info(f"Processing {input_file} -> {output_file}")
    
    pipeline = create_pipeline(output_file)
    
    try:
        with open(input_file, 'r') as f:
            pipeline.process(f)
        return True
    except Exception as e:
        logger.error(f"Error processing {input_file}: {e}")
        return False

def main():
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all .article files in the samples directory
    samples_dir = os.path.join(os.path.dirname(__file__), "samples")
    article_files = glob.glob(os.path.join(samples_dir, "*.article"))
    
    if not article_files:
        logger.error(f"No article files found in {samples_dir}")
        return 1
    
    logger.info(f"Found {len(article_files)} article files")
    
    # Process each article file
    success_count = 0
    for article_file in article_files:
        if process_article(article_file, output_dir):
            success_count += 1
    
    logger.info(f"Processed {success_count} of {len(article_files)} articles successfully")
    logger.info(f"Output files are in {output_dir}")
    
    return 0 if success_count == len(article_files) else 1

if __name__ == "__main__":
    sys.exit(main()) 