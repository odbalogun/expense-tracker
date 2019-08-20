"""
Expense models
"""
import datetime as dt
import calendar
from expense_tracker.database import (
    Column,
    db,
    Model,
    reference_col,
    relationship,
    UserRelated
)


class Expense(UserRelated, Model):
    """
    Class for expense line items
    """
    __tablename__ = "expense"

    name = Column(db.String(100), nullable=False)
    budgeted_price = Column(db.Integer, default=0)
    actual_price = Column(db.Integer, nullable=True)
    date_created = Column(db.DateTime, default=dt.datetime.utcnow)
    status = Column(db.String(20), default='open')
    date_last_updated = Column(db.DateTime, nullable=True)
    priority = Column(db.String(20), default='normal')
    note = Column(db.Text, nullable=False)
    period_id = reference_col('periods', nullable=True)

    period = relationship("Period", backref="expense")
    user = relationship("User", backref="expense")


class Period(UserRelated, Model):
    """
    Represents a unique (per user)
    """
    __tablename__ = "periods"

    month = Column(db.Integer, nullable=False)
    year = Column(db.Integer, nullable=False)

    user = relationship("User", backref="periods")

    def __str__(self):
        return "{}, {}".format(self.month, self.year)

    @property
    def get_short_name(self):
        return calendar.month_abbr[self.month]

    @property
    def get_name(self):
        return calendar.month_name[self.month]