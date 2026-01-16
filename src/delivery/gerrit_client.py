"""
Gerrit client for pushing code.
"""
import logging
import subprocess
from pathlib import Path
from typing import Optional

from git import Repo
from git.exc import GitCommandError

from ..config.settings import DeliveryConfig
from ..manifest.models import Project
from ..transformer.branch_transformer import BranchTransformer
from ..transformer.repo_transformer import RepoTransformer

logger = logging.getLogger(__name__)


class GerritClient:
    """Client for pushing code to Gerrit."""

    def __init__(
        self,
        config: DeliveryConfig,
        branch_transformer: Optional[BranchTransformer] = None,
        repo_transformer: Optional[RepoTransformer] = None,
    ) -> None:
        """
        Initialize Gerrit client.

        Args:
            config: Delivery configuration
            branch_transformer: Optional branch name transformer
            repo_transformer: Optional repository name transformer
        """
        self.config = config
        self.branch_transformer = branch_transformer or BranchTransformer(
            add_date_suffix=config.branch_transform
        )
        self.repo_transformer = repo_transformer or RepoTransformer(
            alias=config.repo_alias
        )

    def _get_gerrit_url(self, project_name: str) -> str:
        """
        Get Gerrit URL for a project.

        Args:
            project_name: Project name/path

        Returns:
            Full Gerrit URL for the project
        """
        # Transform repository name if alias is configured
        transformed_name = self.repo_transformer.transform(project_name)

        # Construct Gerrit URL
        gerrit_base = self.config.gerrit_url.rstrip("/")
        if self.config.auth_method == "ssh":
            # SSH URL format: ssh://user@host:port/path
            if "@" in gerrit_base:
                return f"{gerrit_base}/{transformed_name}"
            else:
                # Assume username from config or use default
                username = self.config.username or "git"
                return f"ssh://{username}@{gerrit_base.replace('ssh://', '').replace('http://', '').replace('https://', '')}/{transformed_name}"
        else:
            # HTTP URL format: http://host/path
            return f"{gerrit_base}/{transformed_name}"

    def push_project(
        self, project: Project, local_repo_path: Path, dry_run: bool = False
    ) -> bool:
        """
        Push a project to Gerrit.

        Args:
            project: Project to push
            local_repo_path: Local path to the project repository
            dry_run: If True, only simulate without actually pushing

        Returns:
            True if push succeeded, False otherwise
        """
        if not local_repo_path.exists():
            logger.error(f"Repository path does not exist: {local_repo_path}")
            return False

        try:
            repo = Repo(str(local_repo_path))

            # Get transformed branch name
            target_branch = self.branch_transformer.transform_revision(
                project.revision
            )
            if not target_branch:
                logger.warning(
                    f"Project {project.name} has no revision, skipping"
                )
                return False

            # Check if branch exists locally
            try:
                branch = repo.heads[target_branch]
            except (IndexError, AttributeError):
                # Try to find branch by revision
                try:
                    commit = repo.commit(project.revision)
                    # Create branch from commit if needed
                    branch = repo.create_head(target_branch, commit)
                except Exception as e:
                    logger.error(
                        f"Failed to find or create branch {target_branch} for {project.name}: {e}"
                    )
                    return False

            # Get Gerrit URL
            gerrit_url = self._get_gerrit_url(project.name)

            # Configure remote
            remote_name = "gerrit"
            if remote_name in repo.remotes:
                repo.delete_remote(remote_name)

            # Set up authentication
            if self.config.auth_method == "ssh":
                # SSH key should be configured in ~/.ssh/config or via SSH_AUTH_SOCK
                repo.create_remote(remote_name, url=gerrit_url)
            else:
                # HTTP authentication
                if self.config.username and self.config.password:
                    # Embed credentials in URL
                    from urllib.parse import urlparse, urlunparse

                    parsed = urlparse(gerrit_url)
                    netloc = f"{self.config.username}:{self.config.password}@{parsed.netloc}"
                    auth_url = urlunparse(
                        (
                            parsed.scheme,
                            netloc,
                            parsed.path,
                            parsed.params,
                            parsed.query,
                            parsed.fragment,
                        )
                    )
                    repo.create_remote(remote_name, url=auth_url)
                else:
                    repo.create_remote(remote_name, url=gerrit_url)

            if dry_run:
                logger.info(
                    f"[DRY RUN] Would push {project.name} branch {target_branch} to {gerrit_url}"
                )
                return True

            # Push to Gerrit
            logger.info(
                f"Pushing {project.name} branch {target_branch} to {gerrit_url}"
            )
            push_info = repo.remote(remote_name).push(
                f"{branch}:refs/heads/{target_branch}", force=False
            )

            # Check push result
            if push_info and push_info[0].flags & push_info[0].ERROR:
                logger.error(
                    f"Failed to push {project.name}: {push_info[0].summary}"
                )
                return False

            logger.info(f"Successfully pushed {project.name}")
            return True

        except GitCommandError as e:
            logger.error(f"Git error pushing {project.name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error pushing {project.name}: {e}")
            return False
