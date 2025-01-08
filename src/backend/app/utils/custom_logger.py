import logging


class CustomLogger:
    """
    A custom logger class that prevents propagation and uses a single stream handler.

    This class helps avoid duplicate log messages and maintains a consistent logging format.
    """

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initializes the logger with a name and optional logging level.

        Args:
            name (str): The name of the logger instance.
            level (int, optional): The logging level. Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.propagate = True
        self.logger.setLevel(level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def __getattr__(self, name):
        """
        Forwards all logging methods (debug, info, warning, etc.) to the internal logger.
        """
        return getattr(self.logger, name)