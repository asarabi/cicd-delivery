"""
Command-line interface for delivery tool.
"""
import argparse
import logging
import sys
from pathlib import Path

from ..config.settings import ConfigLoader
from ..delivery.orchestrator import DeliveryOrchestrator


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration.

    Args:
        verbose: If True, enable debug logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> int:
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Deliver code from manifest to Gerrit"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="Path to configuration file (YAML)",
    )
    parser.add_argument(
        "-w",
        "--work-dir",
        type=Path,
        help="Working directory for operations (default: temp directory)",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Simulate without actually pushing to Gerrit",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(verbose=args.verbose)

    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        logger.info(f"Loading configuration from {args.config}")
        config_loader = ConfigLoader(args.config)
        manifest_config, delivery_config = config_loader.load()

        # Create orchestrator
        orchestrator = DeliveryOrchestrator(
            manifest_config=manifest_config,
            delivery_config=delivery_config,
            work_dir=args.work_dir,
        )

        # Execute delivery
        logger.info("Starting delivery process...")
        result = orchestrator.execute(dry_run=args.dry_run)

        # Print results
        print("\n" + "=" * 60)
        print("Delivery Summary")
        print("=" * 60)
        print(f"Total projects in manifest: {result.total_projects}")
        print(f"Projects after filtering: {result.filtered_projects}")
        print(f"Successfully pushed: {result.successful}")
        print(f"Failed: {result.failed}")
        print(f"Skipped: {result.skipped}")

        if result.failed_projects:
            print(f"\nFailed projects:")
            for project in result.failed_projects:
                print(f"  - {project}")

        if result.skipped_projects:
            print(f"\nSkipped projects:")
            for project in result.skipped_projects:
                print(f"  - {project}")

        print("=" * 60 + "\n")

        # Return exit code
        return 0 if result.failed == 0 else 1

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
