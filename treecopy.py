from pathlib import Path
import click
import pyperclip
import pathspec

class DirectoryTree:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.gitignore_spec = self._load_gitignore()

    def _load_gitignore(self) -> pathspec.PathSpec | None:
        """Load .gitignore patterns if the file exists.
        
        Returns:
            pathspec.PathSpec | None: A PathSpec object containing the gitignore patterns,
                                    or None if the file doesn't exist or has errors
        """
        try:
            gitignore_path = self.root_dir / '.gitignore'
            if gitignore_path.exists():
                with open(gitignore_path) as f:
                    return pathspec.PathSpec.from_lines(
                        pathspec.patterns.GitWildMatchPattern,
                        f.readlines()
                    )
        except IOError as e:
            click.echo(f"Warning: Could not read .gitignore file: {e}", err=True)
        except pathspec.PatternError as e:
            click.echo(f"Warning: Invalid pattern in .gitignore: {e}", err=True)
        except Exception as e:
            click.echo(f"Warning: Unexpected error processing .gitignore: {e}", err=True)
        return None

    def should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored based on default patterns and .gitignore rules."""
        # Default patterns to always ignore
        if path.name in {'.git', '__pycache__', 'node_modules', '.env'}:
            return True
        
        if self.gitignore_spec is not None:
            try:
                # Get relative path from root directory for gitignore matching
                rel_path = str(path.relative_to(self.root_dir))
                return self.gitignore_spec.match_file(rel_path)
            except ValueError as e:
                click.echo(f"Warning: Error processing path {path}: {e}", err=True)
                return False
        return False

    def _generate_tree(self, directory: Path, prefix: str = "", is_last: bool = True) -> str:
        """Generate tree structure for a directory and its contents."""
        name = directory.name + '/' if directory.is_dir() else directory.name
        tree = f"{prefix}{'└── ' if is_last else '├── '}{name}\n"

        if directory.is_dir():
            try:
                # Filter and sort directory contents
                items = [
                    item for item in sorted(directory.iterdir())
                    if not self.should_ignore(item)
                ]
                
                # Process each item
                for i, item in enumerate(items):
                    is_last_item = i == len(items) - 1
                    new_prefix = prefix + ('    ' if is_last else '│   ')
                    tree += self._generate_tree(
                        item,
                        prefix=new_prefix,
                        is_last=is_last_item
                    )
            except PermissionError as e:
                click.echo(f"Warning: Permission denied accessing {directory}: {e}", err=True)
            except Exception as e:
                click.echo(f"Warning: Error processing directory {directory}: {e}", err=True)
        
        return tree

    def generate(self) -> str:
        """Generate the complete tree structure starting from root."""
        try:
            tree = f"{self.root_dir.name}/\n"
            
            # Filter and sort root directory contents
            items = [
                item for item in sorted(self.root_dir.iterdir())
                if not self.should_ignore(item)
            ]
            
            # Generate tree for each root item
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                tree += self._generate_tree(item, is_last=is_last)
            
            return tree
        except PermissionError as e:
            click.echo(f"Error: Permission denied accessing root directory: {e}", err=True)
            return ""
        except Exception as e:
            click.echo(f"Error: Failed to generate directory tree: {e}", err=True)
            return ""

@click.command()
@click.argument('path', type=click.Path(exists=True, path_type=Path))
@click.option('--clipboard/--no-clipboard', default=True, help='Copy to clipboard')
def cli(path: Path, clipboard: bool):
    """Generate a tree structure of the specified directory and optionally copy to clipboard."""
    try:
        tree_generator = DirectoryTree(path)
        tree = tree_generator.generate()
        
        if not tree:
            return

        # Print the tree
        click.echo(tree)
        
        # Copy to clipboard if requested
        if clipboard:
            try:
                pyperclip.copy(tree)
                click.echo("Tree structure copied to clipboard!", err=True)
            except pyperclip.PyperclipException:
                click.echo("Failed to copy to clipboard - clipboard access denied", err=True)
            except Exception as e:
                click.echo(f"Failed to copy to clipboard: {e}", err=True)
    
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    cli()