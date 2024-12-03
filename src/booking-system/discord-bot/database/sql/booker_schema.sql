DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Service;


CREATE TABLE Service (
    S_RoomNumber    TEXT,
    S_Name          TEXT,

    PRIMARY KEY(S_RoomNumber)
);

CREATE TABLE Booking (
    B_StartDate     TEXT,
    B_EndDate       TEXT,
    B_UserID        TEXT,
    B_Name          TEXT,
    B_RoomNumber    TEXT,

    PRIMARY KEY(B_UserID, B_StartDate, B_RoomNumber),
    FOREIGN KEY(B_RoomNumber) REFERENCES Service(S_RoomNumber)
);
