"""
Orchestrator for the delivery workflow.
"""
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ..config.settings import ConfigLoader, DeliveryConfig, ManifestConfig
from ..delivery.gerrit_client import GerritClient
from ..manifest.downloader import ManifestDownloader
from ..manifest.filter import filter_projects_by_revision
from ..manifest.models import Project
from ..manifest.parser import ManifestParser
from ..transformer.branch_transformer import BranchTransformer
from ..transformer.repo_transformer import RepoTransformer

logger = logging.getLogger(__name__)


@dataclass
class DeliveryResult:
    """Result of delivery operation."""

    total_projects: int
    filtered_projects: int
    successful: int
    failed: int
    skipped: int
    failed_projects: List[str]
    skipped_projects: List[str]


class DeliveryOrchestrator:
    """Orchestrator for the delivery workflow."""

    def __init__(
        self,
        manifest_config: ManifestConfig,
        delivery_config: DeliveryConfig,
        work_dir: Optional[Path] = None,
    ) -> None:
        """
        Initialize orchestrator.

        Args:
            manifest_config: Manifest configuration
            delivery_config: Delivery configuration
            work_dir: Working directory for operations
        """
        self.manifest_config = manifest_config
        self.delivery_config = delivery_config
        self.work_dir = work_dir

        # Initialize transformers
        self.branch_transformer = BranchTransformer(
            add_date_suffix=delivery_config.branch_transform
        )
        self.repo_transformer = RepoTransformer(alias=delivery_config.repo_alias)

        # Initialize Gerrit client
        self.gerrit_client = GerritClient(
            config=delivery_config,
            branch_transformer=self.branch_transformer,
            repo_transformer=self.repo_transformer,
        )

    def execute(
        self, project_paths: Optional[dict[str, Path]] = None, dry_run: bool = False
    ) -> DeliveryResult:
        """
        Execute the delivery workflow.

        Args:
            project_paths: Optional mapping of project names to local paths.
                          If None, assumes projects are in work_dir.
            dry_run: If True, simulate without actually pushing

        Returns:
            DeliveryResult with operation statistics
        """
        logger.info("Starting delivery workflow")

        # Step 1: Download manifest
        logger.info("Downloading manifest...")
        downloader = ManifestDownloader(self.manifest_config, self.work_dir)
        try:
            manifest_path = downloader.download()
            logger.info(f"Manifest downloaded to {manifest_path}")
        except Exception as e:
            logger.error(f"Failed to download manifest: {e}")
            raise

        # Step 2: Parse manifest
        logger.info("Parsing manifest...")
        parser = ManifestParser(manifest_path)
        try:
            all_projects = parser.parse()
            logger.info(f"Parsed {len(all_projects)} projects from manifest")
        except Exception as e:
            logger.error(f"Failed to parse manifest: {e}")
            raise

        # Step 3: Filter projects (exclude hash revisions)
        logger.info("Filtering projects...")
        filtered_projects = filter_projects_by_revision(all_projects)
        logger.info(
            f"Filtered to {len(filtered_projects)} projects with branch/tag revisions"
        )

        # Step 4: Push projects to Gerrit
        logger.info("Pushing projects to Gerrit...")
        result = DeliveryResult(
            total_projects=len(all_projects),
            filtered_projects=len(filtered_projects),
            successful=0,
            failed=0,
            skipped=0,
            failed_projects=[],
            skipped_projects=[],
        )

        for project in filtered_projects:
            # Get local repository path
            if project_paths and project.name in project_paths:
                local_path = project_paths[project.name]
            elif self.work_dir:
                # Assume project is in work_dir with path from manifest
                local_path = self.work_dir / project.path
            else:
                logger.warning(
                    f"No path specified for project {project.name}, skipping"
                )
                result.skipped += 1
                result.skipped_projects.append(project.name)
                continue

            if not local_path.exists():
                logger.warning(
                    f"Project path does not exist: {local_path}, skipping"
                )
                result.skipped += 1
                result.skipped_projects.append(project.name)
                continue

            # Push project
            success = self.gerrit_client.push_project(
                project, local_path, dry_run=dry_run
            )

            if success:
                result.successful += 1
            else:
                result.failed += 1
                result.failed_projects.append(project.name)

        # Cleanup
        try:
            downloader.cleanup()
        except Exception as e:
            logger.warning(f"Failed to cleanup: {e}")

        logger.info(
            f"Delivery completed: {result.successful} successful, "
            f"{result.failed} failed, {result.skipped} skipped"
        )

        return result
