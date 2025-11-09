from ..extensions import db
from .users import BaseModel

class Images(BaseModel):
    img = db.Column(db.LargeBinary, nullable=False)
    title = db.Column(db.String(100), nullable=False, default='좋아요!!!')
    name = db.Column(db.String(200), nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Image {self.name}>'