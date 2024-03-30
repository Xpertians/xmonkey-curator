from .base_handler import BaseFileHandler
from .handlers import TextFileHandler, ElfFileHandler, PythonFileHandler
from .handlers import PerlFileHandler, CplusFileHandler, JavaFileHandler
from .handlers import RustFileHandler, RubyFileHandler, ObjectivecFileHandler
from .handlers import JvmFileHandler, OctetStreamFileHandler
from .handlers import SharedLibFileHandler, ArchiveLibFileHandler
from .handlers import MachOSFileHandler


HANDLER_REGISTRY = {
    # Plan Text and String
    'text/plain': TextFileHandler,
    'text/x-makefile': TextFileHandler,
    'text/markdown': TextFileHandler,
    'text/css': TextFileHandler,
    'text/html': TextFileHandler,
    'text/xml': TextFileHandler,
    'text/csv': TextFileHandler,
    'application/pls+xml': TextFileHandler,
    'application/x-mpegurl': TextFileHandler,
    'application/json': TextFileHandler,
    'text/x-tex': TextFileHandler,
    'text/vtt': TextFileHandler,
    'text/x-asm': TextFileHandler,
    'text/x-m4': TextFileHandler,
    'text/x-shellscript': TextFileHandler,
    'text/cache-manifest': TextFileHandler,
    'text/javascript': TextFileHandler,
    'application/javascript': TextFileHandler,
    'application/json': TextFileHandler,
    'application/x-sh': TextFileHandler,
    'application/x-tex': TextFileHandler,
    'application/x-texinfo': TextFileHandler,
    'application/xml': TextFileHandler,
    'application/postscript': TextFileHandler,
    'application/cu-seeme': TextFileHandler,
    'application/x-msdownload': TextFileHandler,
    # Pygments based extraction
    'text/x-c': CplusFileHandler,
    'text/x-c++': CplusFileHandler,
    'text/x-python': PythonFileHandler,
    'application/x-python-code': PythonFileHandler,
    'text/x-script.python': PythonFileHandler,
    'text/x-perl': PerlFileHandler,
    'text/x-java-source': JavaFileHandler,
    'application/java-vm': JvmFileHandler,
    'text/rust': RustFileHandler,
    'text/x-rust': RustFileHandler,
    'application/rls-services+xml': RustFileHandler,
    'text/ruby': RubyFileHandler,
    'text/x-ruby': RubyFileHandler,
    'text/x-objective-c': ObjectivecFileHandler,
    # Library Specific
    'application/octet-stream': OctetStreamFileHandler,
    'application/x-executable': ElfFileHandler,
    'application/x-sharedlib': SharedLibFileHandler,
    'application/x-archive': ArchiveLibFileHandler,
    'application/x-mach-binary': MachOSFileHandler,
}


def register_handler(mime_type, handler_class):
    """Registers a new handler for a given MIME type."""
    HANDLER_REGISTRY[mime_type] = handler_class


def get_handler(mime_type):
    return HANDLER_REGISTRY.get(mime_type)
