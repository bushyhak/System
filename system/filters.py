import calendar
from datetime import date, timedelta, datetime
from django.utils.html import format_html
from django.templatetags.static import static
from django.contrib import admin


class DateRangeFilter(admin.SimpleListFilter):
    title = "Date Range"
    parameter_name = "date_range"

    def lookups(self, request, model_admin):
        return (
            ("today", "Today"),
            ("this_week", "This week"),
            ("this_month", "This month"),
            ("custom", "Custom"),
        )

    def queryset(self, request, queryset):
        if self.value() == "today":
            today = datetime.today().date()
            return queryset.filter(date=today)
        elif self.value() == "this_week":
            start_of_week = datetime.today().date() - timedelta(
                days=datetime.today().weekday()
            )
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(date__range=(start_of_week, end_of_week))
        elif self.value() == "this_month":
            today = datetime.today().date()
            start_of_month = date(today.year, today.month, 1)
            end_of_month = date(
                today.year, today.month, calendar.monthrange(today.year, today.month)[1]
            )
            return queryset.filter(date__range=(start_of_month, end_of_month))
        elif self.value() == "custom":
            start_date = request.GET.get("start_date", None)
            end_date = request.GET.get("end_date", None)
            if start_date and end_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                return queryset.filter(date__range=(start_date, end_date))


class StatusFilter(admin.SimpleListFilter):
    title = "Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return (
            ("complete", "Complete"),
            ("cancelled", "Cancelled"),
            ("pending", "Pending"),
        )

    def queryset(self, request, queryset):
        if self.value() == "complete":
            return queryset.filter(completed=True)
        elif self.value() == "cancelled":
            return queryset.filter(cancelled=True)
        elif self.value() == "pending":
            return queryset.filter(completed=False, cancelled=False)


def boolean_display(field_value: bool, options=("True", "False")):
    """Return HTML code with a True/False text and
    success/error icon based a boolean field value"""
    if field_value:
        icon_url = static("admin/img/icon-yes.svg")
        return format_html(f'{options[0]} <img src="{icon_url}" alt="{options[0]}">')
    else:
        icon_url = static("admin/img/icon-no.svg")
        return format_html(f'{options[1]} <img src="{icon_url}" alt="{options[1]}">')
