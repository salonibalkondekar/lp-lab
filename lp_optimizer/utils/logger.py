"""
Centralized logging configuration for LP Optimizer application.
Provides color-coded logging for different components and severity levels.
"""

import logging
import sys
from typing import Optional
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Custom formatter with color coding for different log levels and components."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    
    COMPONENT_COLORS = {
        'MAIN': '\033[94m',       # Blue
        'APP': '\033[96m',        # Light Cyan
        'UI': '\033[95m',         # Light Magenta
        'CALLBACK': '\033[93m',   # Light Yellow
        'SOLVER': '\033[92m',     # Light Green
        'AI': '\033[91m',         # Light Red
        'VIZ': '\033[97m',        # White
    }
    
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    def format(self, record):
        # Get component from logger name
        component = record.name.split('.')[0].upper() if '.' in record.name else 'SYSTEM'
        
        # Get colors
        level_color = self.COLORS.get(record.levelname, self.RESET)
        component_color = self.COMPONENT_COLORS.get(component, self.RESET)
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S.%f')[:-3]
        
        # Build the formatted message
        formatted = (
            f"{self.BOLD}{level_color}[{record.levelname:8}]{self.RESET} "
            f"{timestamp} "
            f"{self.BOLD}{component_color}[{component:8}]{self.RESET} "
            f"{record.getMessage()}"
        )
        
        # Add exception info if present
        if record.exc_info:
            formatted += f"\n{level_color}{self.formatException(record.exc_info)}{self.RESET}"
        
        return formatted


class LPLogger:
    """Centralized logger factory for LP Optimizer application."""
    
    _loggers = {}
    _initialized = False
    
    @classmethod
    def setup(cls, level: str = "DEBUG", log_file: Optional[str] = None):
        """
        Initialize the logging system.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path to write logs to
        """
        if cls._initialized:
            return
        
        # Set up root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, level.upper()))
        
        # Remove any existing handlers
        root_logger.handlers.clear()
        
        # Console handler with color formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter())
        root_logger.addHandler(console_handler)
        
        # File handler if specified (without colors)
        if log_file:
            file_handler = logging.FileHandler(log_file, mode='a')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)
        
        cls._initialized = True
        
        # Log initialization
        logger = cls.get_logger("logger")
        logger.info("=" * 60)
        logger.info("LP OPTIMIZER LOGGING SYSTEM INITIALIZED")
        logger.info(f"Log level: {level}")
        logger.info(f"Log file: {log_file if log_file else 'Console only'}")
        logger.info("=" * 60)
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger with the specified name.
        
        Args:
            name: Logger name (e.g., 'app', 'ui.input_panel', 'callback.solve')
        
        Returns:
            Configured logger instance
        """
        if not cls._initialized:
            cls.setup()
        
        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)
        
        return cls._loggers[name]
    
    @classmethod
    def log_function_entry(cls, logger: logging.Logger, func_name: str, **kwargs):
        """Helper to log function entry with parameters."""
        params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        logger.debug(f"→ Entering {func_name}({params if params else ''})")
    
    @classmethod
    def log_function_exit(cls, logger: logging.Logger, func_name: str, result=None):
        """Helper to log function exit with result."""
        if result is not None:
            logger.debug(f"← Exiting {func_name} with result: {result}")
        else:
            logger.debug(f"← Exiting {func_name}")
    
    @classmethod
    def log_callback_registration(cls, logger: logging.Logger, callback_name: str, 
                                 inputs: list, outputs: list, states: list = None):
        """Helper to log callback registration details."""
        logger.info(f"📌 Registering callback: {callback_name}")
        logger.debug(f"  Inputs: {inputs}")
        logger.debug(f"  Outputs: {outputs}")
        if states:
            logger.debug(f"  States: {states}")
    
    @classmethod
    def log_component_creation(cls, logger: logging.Logger, component_name: str, 
                              component_id: str = None):
        """Helper to log UI component creation."""
        if component_id:
            logger.info(f"🔧 Creating component: {component_name} (ID: {component_id})")
        else:
            logger.info(f"🔧 Creating component: {component_name}")
    
    @classmethod
    def log_error_with_context(cls, logger: logging.Logger, error: Exception, 
                               context: str):
        """Helper to log errors with context."""
        logger.error(f"❌ Error in {context}: {type(error).__name__}: {str(error)}")
        logger.debug("Stack trace:", exc_info=True)


# Convenience function for quick logger access
def get_logger(name: str) -> logging.Logger:
    """Quick access to get a logger."""
    return LPLogger.get_logger(name)


# Initialize on import with default settings
LPLogger.setup(level="DEBUG")