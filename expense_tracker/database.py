# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from .compat import basestring
from .extensions import db
from sqlalchemy.ext.declarative import declared_attr

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(
    tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name), **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs
    )


class UserRelated(SurrogatePK):
    """A mixin that sub classes the SurrogatePK mixin and adds a user_id field as well as methods
    to query by said field"""

    # user_id = reference_col("users", nullable=True)
    @declared_attr
    def user_id(cls):
        return reference_col("users", nullable=True)

    @classmethod
    def get_one_by_user_id(cls, user_id):
        """Get single record by user ID."""
        if any(
                (
                        isinstance(user_id, basestring) and user_id.isdigit(),
                        isinstance(user_id, (int, float)),
                )
        ):
            return cls.query.filter(user_id == int(user_id)).first()
        return None

    @classmethod
    def get_many_by_user_id(cls, user_id):
        """Get single record by user ID."""
        if any(
                (
                        isinstance(user_id, basestring) and user_id.isdigit(),
                        isinstance(user_id, (int, float)),
                )
        ):
            return cls.query.filter(user_id == int(user_id)).all()
        return None
