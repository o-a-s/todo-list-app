import logging
import logging.handlers
import queue
import atexit

class CustomLogger:
    """
    A custom logger class that prevents propagation and uses a single stream handler.

    This class helps avoid duplicate log messages and maintains a consistent logging format.
    """
    _instance = None
    _initialized = False
    _queue = None
    _listener = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name: str, level: int = logging.INFO):
        """
        Initializes the logger with a name and optional logging level.

        Args:
            name (str): The name of the logger instance.
            level (int, optional): The logging level. Defaults to logging.INFO.
        """
        if self._initialized:
            return
        
        self._initialized = True
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        self.logger.propagate = False
        
        # Create a queue to hold log messages
        if CustomLogger._queue is None:
            CustomLogger._queue = queue.Queue(maxsize=1000)
        
            # Create a QueueHandler
            queue_handler = logging.handlers.QueueHandler(CustomLogger._queue)
            self.logger.addHandler(queue_handler)
            
            # Create a StreamHandler for output
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(module)s - %(message)s")
            stream_handler.setFormatter(formatter)
        
            # Create and start queue listener
            CustomLogger._listener = logging.handlers.QueueListener(
                CustomLogger._queue, 
                stream_handler,
                respect_handler_level=True
                )
            CustomLogger._listener.start()
            
            atexit.register(self.shutdown)

    def __getattr__(self, name):
        """
        Forwards all logging methods (debug, info, warning, etc.) to the internal logger.
        """
        return getattr(self.logger, name)
    
    @classmethod
    def shutdown(cls):
        """
        Stops the QueueListner and performs cleanup
        """
        if cls._listener is not None:
            cls._listener.stop()
            cls._listener = None
            cls._queue = None
            cls._initialized = False