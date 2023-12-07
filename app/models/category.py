from app.extensions import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)

    products = db.relationship('Product', back_populates='category')

    def __repr__(self):
        return f'<Category {self.name}>'
