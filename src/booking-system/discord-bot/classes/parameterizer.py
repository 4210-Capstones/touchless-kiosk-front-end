import re


class Parameterizer:
    def check_date(date: str) -> bool:
        reg_ex = r'^(0[1-9]|1[0-2]|[1-9])[-](0[1-9]|[12][0-9]|3[01]|[1-9])[-](\d{4})$'
        match = re.match(reg_ex, date)

        if match:
            return False
        else:
            return True

    def check_time(time: str) -> bool:
        reg_ex = r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
        match = re.match(reg_ex, time)

        if match:
            return False
        else:
            return True

    def reformat_date(date: str) -> str:
        date_list = date.split("-")

        return f"{date_list[2]}-{date_list[0]}-{date_list[1]}"
