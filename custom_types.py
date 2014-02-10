from sqlalchemy.types import TypeDecorator, CHAR
import uuid

class GUID(TypeDecorator):
    """ Platform independent GUID type.

    Uses uses CHAR(32), storing as str'ified
    hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return "%.32x" % value
        elif value and not isinstance(value, uuid.UUID):
            return "%.32x" % uuid.UUID(value)
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return uuid.UUID(value)
        else:
            return None
