from datetime import datetime, timedelta


class DTManager():
    """
    Static class that provides method to handle python's datetime objects
    """

    def string_to_datetime(string_date: str, expanded: bool = True) -> datetime:
        """
        Converts a string to a datetime object

        Args:
            string_date (str): The date represented as a string
            expanded (bool): If true the date includes the time, if false it does not

        Returns
            datetime: A dateobject of the string provided
        """

        if expanded:
            return datetime.strptime(string_date, "%Y-%m-%d %H:%M")
        else:
            return datetime.strptime(string_date, "%Y-%m-%d")

    def datetime_to_string(dt: datetime, expanded: bool = True) -> str:
        """
        Converts a datetime object to a string

        Args:
            dt (datetime): The date represented as a datetime object
            expanded (bool): If true the date includes the time, if false it does not
        
        Returns
            str: A string of the datetime object
        """

        if expanded:
            return datetime.strftime(dt, "%Y-%m-%d %H:%M")
        else:
            return datetime.strftime(dt, "%Y-%m-%d")

    def date_difference(start: datetime, end: datetime) -> int:
        """
        Calculates the difference between start and end dates

        Args:
            start (datetime): The starting date and time
            end (datetime): The end date and time
        
        Returns:
            int: The units are one unit for one 30 minute interval
        """

        difference: int = 0

        delta_difference: timedelta = end - start
        difference += delta_difference.days * 48
        difference += int(delta_difference.seconds / 1800)

        return difference

    def convert_to_utc(local_dt: datetime, offset: int = 0) -> datetime:
        """
        Converts the local date and time to UTC

        Args:
            local_dt (datetime): The local date and time
            offset (int): The offset from UTC of the local timezone
        
        Returns:
            datetime: The UTC date and time
        """

        return local_dt - timedelta(hours=offset)

    def convert_from_utc(utc_dt: datetime, offset: int = 0) -> datetime:
        """
        Converts the UTC date and time to local

        Args:
            utc_dt (datetime): The UTC date and time
            offset (int): The offset from UTC of the local timezone
        
        Returns:
            datetime: The local date and time
        """

        return utc_dt + timedelta(hours=offset)
    
    def get_today_str(offset: int = 0) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def get_interval_utc(date: str = "today", offset: int = 0) -> tuple:
        """
        Gets the UTC start and ene time for a local date

        Args:
            date (str): The local date; defaults to today
            offset (int): The offset from UTC of the local timezone
        
        Returns:
            tuple: Contains two strings which represent the start and end date and time in UTC
        """

        if date == "today":
            date_dt: datetime = DTManager.convert_from_utc(datetime.now(), offset)
            date = date_dt.strftime("%Y-%m-%d")

        start_utc = DTManager.convert_to_utc(datetime.strptime(date, "%Y-%m-%d"), offset)
        end_utc = start_utc + timedelta(days=1)

        return (start_utc, end_utc)
