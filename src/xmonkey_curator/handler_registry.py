from .base_handler import BaseFileHandler
from .handlers import TextFileHandler, ElfFileHandler

HANDLER_REGISTRY = {
    'application/x-executable': ElfFileHandler,
    'text/plain': TextFileHandler,
    'text/markdown': TextFileHandler,
    'text/x-python': TextFileHandler,
    'text/x-java-source': TextFileHandler,
    'text/css:': TextFileHandler,
    'text/html': TextFileHandler,
    'application/json': TextFileHandler,
}

def register_handler(mime_type, handler_class):
    """Registers a new handler for a given MIME type."""
    HANDLER_REGISTRY[mime_type] = handler_class

def get_handler(mime_type):
    return HANDLER_REGISTRY.get(mime_type)
