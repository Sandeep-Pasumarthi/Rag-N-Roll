import os
import logging
import structlog
from structlog.processors import CallsiteParameter, CallsiteParameterAdder, TimeStamper


class CustomLogger:
    def __init__(self, log_dir="logs", log_file_name="server.jsonl", level=logging.INFO):
        self.base_path = os.getcwd()

        logs_dir = os.path.join(os.getcwd(), log_dir)
        os.makedirs(logs_dir, exist_ok=True)
        log_file_path = os.path.join(logs_dir, log_file_name)
        abs_log_path = os.path.abspath(log_file_path)

        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        if not any(
            isinstance(h, logging.FileHandler) and getattr(h, "baseFilename", "") == abs_log_path
            for h in root_logger.handlers
        ):
            fh = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
            fh.setLevel(level)
            fh.setFormatter(logging.Formatter("%(message)s"))
            root_logger.addHandler(fh)
        
        structlog.configure(
            processors=[
                structlog.processors.add_log_level,
                CallsiteParameterAdder(
                    parameters={
                        CallsiteParameter.FILENAME,
                        CallsiteParameter.PATHNAME,
                        CallsiteParameter.LINENO,
                        CallsiteParameter.FUNC_NAME,
                        CallsiteParameter.MODULE,
                    }
                ),
                TimeStamper(fmt="iso"),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(level),
            cache_logger_on_first_use=True,
        )
    
    def get_logger(self, name=None):
        """
        Returns a structlog logger. Pass a name (like __name__) to identify the module.
        """
        return structlog.get_logger(name)

LOGGER = CustomLogger()
