from calendar import HTMLCalendar
from datetime import date, timedelta


def daterange_generator(start_date: date, end_date: date):
    """Generates dates between start_date and end_date (inclusive)."""
    for counter in range(
            int(
                (end_date - start_date).days
            ) + 1
    ):
        yield start_date + timedelta(counter)


class AvailabilityCalendar(HTMLCalendar):

    CLASS_BUSY = "busy"
    CLASS_FREE = "free"

    CLASSIC_HTML = '<table border="0" cellpadding="0" cellspacing="0" class="month">'  # noqa: E501
    BOOTSTRAP_HTML = '<table class="table table-bordered table-calendar">'

    def __init__(self, availability_data, use_bootstrap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.availability_data = availability_data
        self.use_bootstrap = use_bootstrap

    def formatday(self, theyear, themonth, day, weekday):
        # Generated single day cell
        # with formatting based on availability data
        if not day:
            return "<td class='{}'>{}</td>".format(
                self.cssclasses[weekday],
                ""
            )
        else:
            flag = self.CLASS_FREE if self.availability_data.get(
                    date(theyear, themonth, day)
            ) else self.CLASS_BUSY

            return "<td class='{}'>{}</td>".format(
                "{} {}".format(
                    self.cssclasses[weekday],
                    flag
                ),
                day
            )

    def formatweek(self, theyear, themonth, theweek):
        """
        Return a complete week as a table row.
        """
        s = ''.join(
            self.formatday(theyear, themonth, d, wd)
            for (d, wd)
            in theweek
        )
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(theyear, themonth, week))
            a('\n')
        a('</table>')
        a('\n')
        calendar_code = ''.join(v)
        if self.use_bootstrap:
            return calendar_code.replace(
                self.CLASSIC_HTML,
                self.BOOTSTRAP_HTML
                )
        return calendar_code
