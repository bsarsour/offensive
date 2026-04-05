"""
  python generate_israeli_numbers.py
  python generate_israeli_numbers.py --prefix 052 --limit 1000
  python generate_israeli_numbers.py --prefix 054 --format intl --output my_numbers.txt
"""

import argparse
import os
import threading
from queue import Queue

# All valid Israeli mobile prefixes
MOBILE_PREFIXES = ["050", "051", "052", "053", "054", "055", "056", "057", "058"]


def format_number(prefix: str, suffix: str, fmt: str) -> str:
    """Format a number based on the chosen style."""
    if fmt == "local":
        # 05X-XXXXXXX
        return f"{prefix}-{suffix}"
    elif fmt == "intl":
        # +972-5X-XXXXXXX  (drop leading 0, add country code)
        return f"+972-{prefix[1:]}-{suffix}"
    elif fmt == "plain":
        # 05XXXXXXXXX (no separators)
        return f"{prefix}{suffix}"
    elif fmt == "intl_plain":
        # 9725XXXXXXXXX
        return f"972{prefix[1:]}{suffix}"
    return f"{prefix}{suffix}"


def generate_for_prefix(
    prefix: str,
    fmt: str,
    result_queue: Queue,
    limit: int = None,
) -> None:
    """Worker function: generate all numbers for one prefix and push to queue."""
    count = 0
    max_suffix = 10_000_000  # 7-digit suffix: 0000000 - 9999999

    for i in range(max_suffix):
        if limit and count >= limit:
            break
        suffix = f"{i:07d}"
        number = format_number(prefix, suffix, fmt)
        result_queue.put(number)
        count += 1

    result_queue.put(None)  # sentinel: this prefix is done


def writer_thread(
    result_queue: Queue,
    output_file: str,
    num_prefixes: int,
    print_sample: bool,
    sample_size: int,
) -> dict:
    """Collect numbers from the queue, write to file, optionally print samples."""
    stats = {"total": 0, "sample": []}
    done_count = 0

    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        while done_count < num_prefixes:
            item = result_queue.get()
            if item is None:
                done_count += 1
                continue
            f.write(item + "\n")
            stats["total"] += 1

            # Collect sample numbers for console display
            if print_sample and len(stats["sample"]) < sample_size:
                stats["sample"].append(item)

            if stats["total"] % 1_000_000 == 0:
                print(f"  ... {stats['total']:,} numbers written so far")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Generate Israeli mobile phone numbers using threads."
    )
    parser.add_argument(
        "--prefix",
        choices=MOBILE_PREFIXES,
        default=None,
        help="Generate only for this prefix (default: all prefixes)",
    )
    parser.add_argument(
        "--format",
        choices=["local", "intl", "plain", "intl_plain"],
        default="local",
        help=(
            "Number format:\n"
            "  local     = 05X-XXXXXXX (default)\n"
            "  intl      = +972-5X-XXXXXXX\n"
            "  plain     = 05XXXXXXXXX\n"
            "  intl_plain= 9725XXXXXXXXX"
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max numbers per prefix (default: all 10,000,000)",
    )
    parser.add_argument(
        "--output",
        default="israeli_mobile_numbers.txt",
        help="Output file path (default: israeli_mobile_numbers.txt)",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=20,
        help="Number of sample lines to print to console (default: 20)",
    )
    args = parser.parse_args()

    prefixes = [args.prefix] if args.prefix else MOBILE_PREFIXES
    result_queue: Queue = Queue(maxsize=200_000)  # bounded to control memory

    print("=" * 55)
    print("  Israeli Mobile Number Generator")
    print("=" * 55)
    print(f"  Prefixes  : {', '.join(prefixes)}")
    print(f"  Format    : {args.format}")
    print(f"  Limit/pfx : {args.limit or '10,000,000 (all)'}")
    print(f"  Output    : {args.output}")
    print(f"  Threads   : {len(prefixes)} generator + 1 writer")
    print("=" * 55)
    print("Generating...")

    # Launch one generator thread per prefix
    threads = []
    for prefix in prefixes:
        t = threading.Thread(
            target=generate_for_prefix,
            args=(prefix, args.format, result_queue, args.limit),
            daemon=True,
        )
        t.start()
        threads.append(t)

    # Writer runs in the main thread (I/O-bound, only one file handle needed)
    stats = writer_thread(
        result_queue=result_queue,
        output_file=args.output,
        num_prefixes=len(prefixes),
        print_sample=args.sample > 0,
        sample_size=args.sample,
    )

    for t in threads:
        t.join()

    # Print sample
    if stats["sample"]:
        print(f"\nSample output ({len(stats['sample'])} numbers):")
        print("-" * 30)
        for num in stats["sample"]:
            print(f"  {num}")
        print(f"  ... and {stats['total'] - len(stats['sample']):,} more")

    print("\n" + "=" * 55)
    print(f"  Done! {stats['total']:,} numbers saved to: {args.output}")
    file_size = os.path.getsize(args.output) / (1024 * 1024)
    print(f"  File size : {file_size:.1f} MB")
    print("=" * 55)


if __name__ == "__main__":
    main()
