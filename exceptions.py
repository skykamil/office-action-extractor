class ExtractionError(Exception):
    pass

class FileAccessError(ExtractionError):
    pass

class UnsupportedFileFormatError(ExtractionError):
    pass

class CorruptedFileError(ExtractionError):
    pass

class EmptyDocumentError(ExtractionError):
    pass