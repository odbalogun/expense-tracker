from expense_tracker.extensions import ma

from .models import Expense, Period


class ExpenseSchema(ma.ModelSchema):
    class Meta:
        model = Expense
        fields = ("id", "period_id", "name", "budgeted_price", "actual_price", "date_created", "date_last_updated",
                  "status", "priority", "note", "user_id")


class PeriodSchema(ma.ModelSchema):
    class Meta:
        model = Period
        fields = ("id", "month", "year", "user_id")


expense_schema = ExpenseSchema()
period_schema = PeriodSchema()