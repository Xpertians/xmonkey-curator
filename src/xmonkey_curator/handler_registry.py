from .base_handler import BaseFileHandler
from .handlers import TextFileHandler, ElfFileHandler, PythonFileHandler
from .handlers import PerlFileHandler, CplusFileHandler, JavaFileHandler
from .handlers import RustFileHandler, RubyFileHandler, ObjectivecFileHandler


HANDLER_REGISTRY = {
    'application/x-executable': ElfFileHandler,
    # Plan Text and String
    'text/plain': TextFileHandler,
    'text/markdown': TextFileHandler,
    'text/css:': TextFileHandler,
    'text/html': TextFileHandler,
    'text/css': TextFileHandler,
    'text/x-asm': TextFileHandler,
    'text/cache-manifest': TextFileHandler,
    'application/json': TextFileHandler,
    'application/x-sh': TextFileHandler,
    'application/x-texinfo': TextFileHandler,
    'application/xml': TextFileHandler,
    'application/cu-seeme': TextFileHandler,
    'application/x-msdownload': TextFileHandler,
    # CTags based extraction
    'text/x-c': CplusFileHandler,
    'text/x-python': PythonFileHandler,
    'application/x-python-code': PythonFileHandler,
    'text/x-perl': PerlFileHandler,
    'text/x-java-source': JavaFileHandler,
    'text/rust': RustFileHandler,
    'text/x-rust': RustFileHandler,
    'text/ruby': RubyFileHandler,
    'text/x-ruby': RubyFileHandler,
    'text/x-objective-c': ObjectivecFileHandler,
}


def register_handler(mime_type, handler_class):
    """Registers a new handler for a given MIME type."""
    HANDLER_REGISTRY[mime_type] = handler_class


def get_handler(mime_type):
    return HANDLER_REGISTRY.get(mime_type)
