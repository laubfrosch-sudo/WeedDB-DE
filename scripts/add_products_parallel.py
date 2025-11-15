"""
Parallel batch processing for adding multiple products to WeedDB.

This script processes multiple products concurrently using asyncio,
with configurable concurrency limits to avoid overwhelming the target website.

Features:
- Parallel processing with semaphore-based rate limiting
- Progress tracking with tqdm
- Comprehensive error handling and retry logic
- Detailed logging and reporting
- Graceful shutdown on interruption

Usage:
    python3 add_products_parallel.py <product_names_file> [options]

Options:
    --concurrency N    : Max concurrent requests (default: 3)
    --timeout N        : Timeout per product in seconds (default: 120)
    --yes              : Skip confirmation prompts
    --log-level LEVEL  : Logging level (DEBUG, INFO, WARNING, ERROR)

Example:
    python3 add_products_parallel.py products.txt --concurrency 5 --yes
"""

import asyncio
import sys
import os
import signal
import json
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import subprocess
import argparse
from pathlib import Path

try:
    from tqdm.asyncio import tqdm
except ImportError:
    print("❌ tqdm not installed. Run: pip3 install tqdm")
    sys.exit(1)

# Logging will be added after initial testing
# from logger import get_logger, setup_global_logging

# Constants
DEFAULT_CONCURRENCY = 3
DEFAULT_TIMEOUT = 120
LOG_DIR = Path(__file__).parent.parent / "data" / "logs"

@dataclass
class ProductResult:
    """Result of processing a single product"""
    name: str
    success: bool
    duration: float
    error_message: Optional[str] = None
    product_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class BatchResult:
    """Summary of batch processing results"""
    total_products: int
    successful: int
    failed: int
    total_duration: float
    concurrency: int
    timestamp: str
    results: List[ProductResult]

    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "results": [r.to_dict() for r in self.results]
        }

class ParallelBatchProcessor:
    """Handles parallel processing of product additions"""

    def __init__(self, concurrency: int = DEFAULT_CONCURRENCY, timeout: int = DEFAULT_TIMEOUT):
        self.concurrency = concurrency
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(concurrency)
        self.shutdown_event = asyncio.Event()

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n⚠️  Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_event.set()

    async def process_product(self, product_name: str, progress_bar: tqdm) -> ProductResult:
        """Process a single product with semaphore limiting"""
        if self.shutdown_event.is_set():
            return ProductResult(product_name, False, 0.0, "Shutdown requested")

        async with self.semaphore:
            if self.shutdown_event.is_set():
                return ProductResult(product_name, False, 0.0, "Shutdown requested")

            start_time = time.time()

            try:
                # Run add_product.py as subprocess
                process = await asyncio.create_subprocess_exec(
                    'python3', 'add_product.py', product_name,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=Path(__file__).parent
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(),
                        timeout=self.timeout
                    )
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    return ProductResult(
                        product_name, False, time.time() - start_time,
                        f"Timeout after {self.timeout}s"
                    )

                duration = time.time() - start_time
                success = process.returncode == 0

                error_msg = None
                if not success and stderr:
                    error_msg = stderr.decode().strip()

                # Try to extract product ID from stdout
                product_id = None
                if success and stdout:
                    output = stdout.decode()
                    # Look for "ID: <number>" pattern
                    import re
                    match = re.search(r'ID:\s*(\d+)', output)
                    if match:
                        product_id = int(match.group(1))

                progress_bar.update(1)
                progress_bar.set_description(f"Processing: {product_name[:20]}...")

                return ProductResult(
                    product_name, success, duration, error_msg, product_id
                )

            except Exception as e:
                duration = time.time() - start_time
                return ProductResult(
                    product_name, False, duration,
                    f"Unexpected error: {str(e)}"
                )

    async def process_batch(self, product_names: List[str]) -> BatchResult:
        """Process all products in parallel"""
        start_time = time.time()
        timestamp = datetime.now().isoformat()

        print(f"🚀 Starting parallel batch processing...")
        print(f"   📊 Products: {len(product_names)}")
        print(f"   ⚡ Concurrency: {self.concurrency}")
        print(f"   ⏱️  Timeout per product: {self.timeout}s")
        print(f"   📅 Started: {timestamp}")
        print()

        # Create progress bar
        with tqdm(total=len(product_names), desc="Processing products") as progress_bar:
            # Create tasks for all products
            tasks = [
                self.process_product(name, progress_bar)
                for name in product_names
            ]

            # Run all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions that occurred
        processed_results: List[ProductResult] = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ProductResult(
                    product_names[i], False, 0.0,
                    f"Task exception: {str(result)}"
                ))
            elif isinstance(result, ProductResult):
                processed_results.append(result)
            else:
                # Fallback for unexpected types
                processed_results.append(ProductResult(
                    product_names[i], False, 0.0,
                    f"Unexpected result type: {type(result)}"
                ))

        # Calculate summary
        total_duration = time.time() - start_time
        successful = sum(1 for r in processed_results if r.success)
        failed = len(processed_results) - successful

        batch_result = BatchResult(
            len(product_names), successful, failed, total_duration,
            self.concurrency, timestamp, processed_results
        )

        return batch_result

def read_product_names(filename: str) -> List[str]:
    """Read product names from file, ignoring comments and empty lines"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        products = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            products.append(line)

        return products

    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

def save_batch_report(result: BatchResult, output_file: Optional[str] = None) -> None:
    """Save detailed batch processing report"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_path = LOG_DIR / f"batch_report_{timestamp}.json"
    else:
        output_file_path = Path(output_file)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

    print(f"📄 Report saved to: {output_file}")

def print_summary(result: BatchResult) -> None:
    """Print human-readable summary of batch results"""
    print("\n" + "="*60)
    print("📊 BATCH PROCESSING SUMMARY")
    print("="*60)
    print(f"Total Products:     {result.total_products}")
    print(f"Successful:         {result.successful}")
    print(f"Failed:            {result.failed}")
    print(".1f")
    print(".1f")
    print(".1f")
    print(f"Concurrency:        {result.concurrency}")
    print(f"Timestamp:          {result.timestamp}")
    print("="*60)

    if result.failed > 0:
        print("\n❌ FAILED PRODUCTS:")
        for res in result.results:
            if not res.success:
                print(f"   • {res.name}: {res.error_message}")

    print("\n✅ SUCCESS!")

def main():
    parser = argparse.ArgumentParser(
        description="Parallel batch processing for WeedDB products",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 add_products_parallel.py products.txt
  python3 add_products_parallel.py products.txt --concurrency 5 --yes
  python3 add_products_parallel.py products.txt --timeout 180 --log-level DEBUG
        """
    )

    parser.add_argument('filename', help='File containing product names')
    parser.add_argument('--concurrency', type=int, default=DEFAULT_CONCURRENCY,
                       help=f'Max concurrent requests (default: {DEFAULT_CONCURRENCY})')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                       help=f'Timeout per product in seconds (default: {DEFAULT_TIMEOUT})')
    parser.add_argument('--yes', action='store_true',
                       help='Skip confirmation prompts')
    parser.add_argument('--output', help='Output file for detailed report')

    args = parser.parse_args()

    # Validate arguments
    if args.concurrency < 1:
        print("❌ Concurrency must be at least 1")
        sys.exit(1)

    if args.timeout < 10:
        print("❌ Timeout must be at least 10 seconds")
        sys.exit(1)

    # Read product names
    product_names = read_product_names(args.filename)
    if not product_names:
        print("❌ No valid product names found in file")
        sys.exit(1)

    # Show confirmation
    if not args.yes:
        print(f"📋 Ready to process {len(product_names)} products with concurrency {args.concurrency}")
        print("Products to process:")
        for i, name in enumerate(product_names[:5], 1):
            print(f"  {i}. {name}")
        if len(product_names) > 5:
            print(f"  ... and {len(product_names) - 5} more")

        response = input("\nContinue? (y/N): ").lower().strip()
        if response not in ('y', 'yes'):
            print("❌ Aborted by user")
            sys.exit(0)

    # Create processor and run batch
    processor = ParallelBatchProcessor(args.concurrency, args.timeout)

    try:
        result = asyncio.run(processor.process_batch(product_names))

        # Print summary and save report
        print_summary(result)
        save_batch_report(result, args.output)

        # Exit with appropriate code
        if result.failed > 0:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()