import sqlite3

from classes.datetime_manager import DTManager as dtm


class DBManager():
    """
    Manages connections and queries to the database
    """

    def __init__(self, connection_path):
        self.path: str                          = connection_path
        self.connection: sqlite3.Connection     = None
        self.cursor: sqlite3.Cursor             = None

    def connect(self) -> bool:
        """
        Establishes a connection to the database if not already connected

        Returns:
            bool: True if the connection was succesfully established; False if the connection already exist or if the connection failed
        """

        # Checks if there isn't an already existing connections
        if self.connection is not None or self.cursor is not None:
            return False
        else:
            # Attempts to connect to the database
            try:
                self.connection = sqlite3.connect(self.path)
                self.cursor = self.connection.cursor()
                return True
            # If the connection fails then sets the connection and cursor to None
            except Exception as e:
                self.connection = None
                self.cursor = None
                return False
    
    def shutdown(self) -> None:
        """
        Safely closes the connection to the database

        Returns
            None
        """

        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None

    def setup(self) -> bool:
        """
        Set ups the database using a premade schema. THIS REWRITES THE CURRENT DATABASE!!!

        Returns:
            bool: True if the database was set up properly; False if the set up failed
        """

        try:
            with open("./database/sql/booker_schema.sql") as sql:
                schema = sql.read()
            self.cursor.executescript(schema)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
        
        # try:
        #     with open("./database/sql/service.sql") as sql:
        #         schema = sql.read()
        #     self.cursor.executescript(schema)
        #     self.connection.commit()
        # except Exception as e:
        #     self.connection.rollback()
        #     return False
    
    def add_service(self, room_number: str, room_name: str) -> bool:
        """
        Creates a SQL insert statement for the room table

        Args:
            room_number (str): Number of the Room
            room_name   (str): Name of the Room/Service

        Returns:
            bool: True if the SQL insert was inserted succesfully; False if the SQL insert failed
        """

        if self.connection is None or self.cursor is None:
            return False
        
        query = "INSERT INTO Service(S_RoomNumber, S_Name) VALUES(?,?)"

        try:
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute(query, (room_number, room_name))
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            return False
    
    def add_booking(self, start_date: str, end_date: int, user_id: str, name: str, room_number: str) -> bool:
        """
        Creates a SQL insert statement for the booking table

        Args:
            start_date  (str): The start date of the booking
            end_date    (str): The end date of the booking
            user_id     (str): The id of the owner of the booking
            name        (str): The name of the owner of the booking
            room_number (str): The room number of the room where the booking is taking place

        Returns:
            bool: True if the SQL insert was inserted succesfully; False if the SQL insert failed
        """

        if self.connection is None or self.cursor is None:
            return False
        
        query = "INSERT INTO Booking(B_StartDate, B_EndDate, B_UserID, B_Name, B_RoomNumber) VALUES(?,?,?,?,?)"

        try:
            self.connection.execute("PRAGMA foreign_keys = ON")
            self.cursor.execute(query, (start_date, end_date, user_id, name, room_number))
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            self.connection.rollback()
            return False
    
    def find_bookings(self, date: str = "today", offset: int = 0, room_number: str = "MATH 352", expanded: bool = True) -> list:
        """
        Finds all the bookings on a certain day in a certain room

        Args:
            date        (str):  The date the booking search takes place
            offset      (int):  The offset for the timezone of the user 
            room_number (str):  Room number for booking search
            expanded    (bool): Returns all booking information if true and only start and end date if false

        Returns:
            list: List of tuples containing information about the bookings
        """

        rows = None

        interval_dt = dtm.get_interval_utc(date, offset)

        start_str: str = dtm.datetime_to_string(interval_dt[0])
        end_str: str = dtm.datetime_to_string(interval_dt[1])
        expanded_str: str = "*" if expanded else "B_StartDate, B_EndDate"

        query = f"""
            SELECT {expanded_str}
            FROM Booking
            WHERE B_RoomNumber = ?
            AND B_StartDate >= ? 
            AND B_StartDate < ?
        """

        try:
            self.cursor.execute(query, (room_number, start_str, end_str))
            rows = self.cursor.fetchall()
        except Exception as e:
            pass

        return rows

    def find_my_bookings(self, user_id: str) -> list:
        """
        Finds all the users bookings regardless of room

        Args:
            user_id     (str): ID for the user

        Returns:
            list: All user's booking information separated into tuples
        """

        rows = None

        query = """
            SELECT *
            FROM Booking
            WHERE B_UserID = ?
        """

        try:
            self.cursor.execute(query, (user_id,))
            rows = self.cursor.fetchall()
        except Exception as e:
            pass

        return rows