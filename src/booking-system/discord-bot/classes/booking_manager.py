from datetime import datetime

from database.python.db_manager import DBManager
from classes.datetime_manager import DTManager as dtm

MAX_BOOKING_TIME = 8


class BookingManager():
    """
    Handles all the booking logic and conflicts
    """

    def check_booking(start: datetime, end: datetime, reserved_slots: list) -> int:
        """
        Checks if the booking is valid

        Args:
            start (datetime): The start date and time
            end (datetime): The end date and time
            reserved_slots (list):
        
        Returns:
            int: Status code for the method execution status
                0: successful
                -1: the start date is after or equal to the end date
                -2: the duartion of the booking exceeds 4 hours
                -3: the room does not exist
                -4: the booking conflicts with other bookings
        """

        if BookingManager.check_timeframe(start, end):
            return -1

        if BookingManager.check_duration(start, end):
            return -2

        if BookingManager.check_room(start, end):
            return -3

        if BookingManager.check_conflict(start, end, reserved_slots):
            return -4

        return 0

    def check_timeframe(start: datetime, end: datetime) -> bool:
        """
        Checks if the start date and end date are in a valid booking format

        Args:
            start (datetime): The start date and time
            end (datetime): The end date and time

        Returns:
            bool: True if valid booking format; False if not valid booking format
        """

        return start >= end

    def check_duration(start: datetime, end: datetime) -> bool:
        """
        Checks if the duration of the booking does not exceed 4 hours

        Args:
            start (datetime): The start date and time
            end (datetime): The end date and time

        Returns:
            bool: True if duration is less than 4 hours; False if duration is more than 4 hours 
       """

        difference: int = dtm.date_difference(start, end)

        return MAX_BOOKING_TIME < difference
    
    def check_room(dbm: DBManager, room_number: str) -> bool:
        """
        WIP
        """
        return False

    def check_conflict(start: datetime, end: datetime, reserved_slots: list) -> bool:
        """
        Checks if user's booking conflicts with already reserved bookings

        Args:
            start (datetime): The start date and time
            end (datetime): The end date and time
            reserved_slots (list): list of reserved bookings
        
        Returns:
            bool: True if there is no conflict; False if there is a time conflic
        """

        for slots in reserved_slots:
            res_start: datetime = dtm.string_to_datetime(slots[0])
            res_end: datetime = dtm.string_to_datetime(slots[1])

            if res_start <= start < res_end:
                return True
            elif res_start < end <= res_end:
                return True

        return False

    def get_availability(reserved_slots: list, date: str = "today", offset: int = 0) -> list:
        """
        Gets the available time slots (30 minute interval) for the stated date

        Args:
            reserved_slots (list): The SQL query result represented a list of tuples
            date (str): 
            offset (int)

        """

        interval: tuple = dtm.get_interval_utc(date, offset)
        schedule: list = [0] * 48

        for slots in reserved_slots:
            res_start: datetime = dtm.string_to_datetime(slots[0])
            res_end: datetime = dtm.string_to_datetime(slots[1])

            start: int = dtm.date_difference(interval[0], res_start)
            end: int = dtm.date_difference(interval[0], res_end)

            for i in range(start, end):
                schedule[i] = 1

        return schedule
