from db import db


class UserModel(db.Model):
    __tablename__ = "Users"

    Id = db.Column(db.BIGINT, primary_key=True, autoincrement=True)
    UserName = db.Column(db.NVARCHAR(1000), nullable=False, unique=True)
    PassWord = db.Column(db.NVARCHAR(1000), nullable=False)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
