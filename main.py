"""
Linear Programming Optimizer - Main Entry Point

A modern web application for solving linear programming problems
with an intuitive interface.
"""

import os
from dotenv import load_dotenv
from lp_optimizer.app import create_app
from lp_optimizer.utils.logger import LPLogger, get_logger

# Load environment variables from .env file
load_dotenv()

# Initialize logging system
log_level = os.getenv("LOG_LEVEL", "DEBUG")
log_file = os.getenv("LOG_FILE", None)
LPLogger.setup(level=log_level, log_file=log_file)

# Get logger for main module
logger = get_logger("main")


def main():
    """Run the LP optimizer application"""
    logger.info("Starting LP Optimizer Application")
    logger.debug(f"Python path: {os.sys.executable}")
    logger.debug(f"Working directory: {os.getcwd()}")
    
    # Create the app
    logger.info("Creating Dash application...")
    app = create_app()
    logger.info("✅ Dash application created successfully")

    # Configure from environment
    debug = os.getenv("DASH_DEBUG", "True").lower() == "true"
    port = int(os.getenv("PORT", "8050"))
    
    logger.info(f"Configuration:")
    logger.info(f"  Debug mode: {debug}")
    logger.info(f"  Port: {port}")
    logger.info(f"  Host: 0.0.0.0")

    # Run the server
    logger.info("=" * 60)
    logger.info(f"🚀 Starting server on http://0.0.0.0:{port}")
    logger.info("=" * 60)
    
    try:
        app.run(debug=debug, host="0.0.0.0", port=port)
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
