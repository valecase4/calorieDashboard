from datetime import datetime, timedelta
from werkzeug.routing import BaseConverter

def get_current_date(format="Italy"):
    """
    Return the current date in dd-mm-yyyy format by default
    """
    if format=="default":
        return datetime.today().strftime("%Y-%m-%d")
    return datetime.today().strftime("%d-%m-%Y")


# Verify the correctness of the route date
class RegexConverter(BaseConverter):
    def __init__(self, map, *items):
        super().__init__(map)
        self.regex = items[0]