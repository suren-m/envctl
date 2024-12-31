import typer
import brew
import core
from core.logger import logger

cli = typer.Typer()
mac_app = typer.Typer()
cli.add_typer(mac_app, name="mac")

@mac_app.command("sync")
def sync(
    items: str = typer.Option("all", "--items", "-i", 
                    help="What to sync: all,config,tools,vim (comma-separated)"),
    backup: bool = typer.Option(True, "--backup/--no-backup", "-b/-nb", 
                    help="Whether to backup existing configs before sync")
    ):
    """
    Sync specified items (config files, tools, vim) with optional backup
    """
    try:
        sync_items = core.utils.validate_sync_items(items)
        logger.info(f"Starting sync for: {', '.join(sync_items)}")
        
        if backup:
            logger.info("Backing up existing configs")
            core.backup_configs()
        else:
            logger.info("Skipping backup")
        
        if "all" in sync_items:
            brew.install()
            #config.sync()
            return
            
        # Individual syncs
        # if "vim" in sync_items:
        #     vim.sync()
        # if "tools" in sync_items:
        #     tools.sync()
        # if "config" in sync_items:
        #     config.sync()
            
        logger.info("Sync completed successfully")
            
    except Exception as e:
        logger.error(f"Error during sync: {e}", exc_info=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    try:
        logger.info('Starting...')
        core.ensure_directory('.envctl')
        cli()
    except Exception as e:
        logger.error(f'Error during execution: {e}', exc_info=True)
        raise typer.Exit(1)