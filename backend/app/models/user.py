from .. import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Columns types 
# https://docs.sqlalchemy.org/en/20/core/types.html

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
