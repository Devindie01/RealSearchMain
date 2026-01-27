# Import all the models, so that Base has them before being
# imported by Alembic or used to create_all()
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.property import Property  # noqa