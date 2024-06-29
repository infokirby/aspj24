from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so


#User DB class
class Users(db.Model):
    phoneNo: so.Mapped[int] = so.mapped_column(primary_key = True)
    name: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, unique=True)
    passwordHash: so.Mapped[str] = so.mapped_column(sa.String(256))

    orders: so.WriteOnlyMapped['Order'] = so.relationship(back_populates= 'customer')

    def __repr__(self):
        return f"User: {self.name}"


