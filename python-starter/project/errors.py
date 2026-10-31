# === INPUT ERRORS ===
class InvalidInputError(Exception): pass
class InvalidStateError(InvalidInputError): pass
class InvalidSymbolError(InvalidInputError): pass
class MalformedInputError(InvalidInputError): pass
