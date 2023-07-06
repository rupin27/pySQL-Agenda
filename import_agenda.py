import sys
import xlrd
from db_table import db_table
from tables.sessions_table import Session
from tables.speakers_table import Speaker

try:
    import_file = xlrd.open_workbook(sys.argv[1])
    import_page = import_file.sheet_by_index(0)
except FileNotFoundError as e:
    raise RuntimeError("Failed to open or access the Excel file.") from e

# create instances of Session and Speaker objects
session_object = Session(None, None, None, None, None, None, None)
speaker_object = Speaker(None, None, None, None, None)

# create the sessions table in the database
session_table = db_table("sessions", { session_object.id: "integer PRIMARY KEY",
                                       session_object.parent_id: "integer",
                                       session_object.date: "string NOT NULL",
                                       session_object.time_start: "string NOT NULL",
                                       session_object.time_end: "string NOT NULL",
                                       session_object.title:"string NOT NULL",
                                       session_object.location: "string",
                                       session_object.description: "string",
                                     })

# create the speakers table in the database
speaker_table = db_table("speakers", { speaker_object.name: "string NOT NULL",
                                       speaker_object.date: "string NOT NULL",
                                       speaker_object.time_start: "string NOT NULL",
                                       speaker_object.time_end: "string NOT NULL",
                                       speaker_object.session_id: "string NOT NULL",
                                     })

parent_session = 0
session_data = []
speaker_data = []

# iterate over the rows in the Excel sheet starting from row 15
for row in range(15, import_page.nrows):
    id = row - 14
    date = str(import_page.cell_value(rowx = row, colx = 0))
    time_start = str(import_page.cell_value(rowx = row, colx = 1))
    time_end = str(import_page.cell_value(rowx = row, colx = 2))
    session = str(import_page.cell_value(rowx = row, colx = 3)).replace("'", "''").strip()
    session_title = str(import_page.cell_value(rowx = row, colx = 4)).replace("'", "''").strip()
    location = str(import_page.cell_value(rowx = row, colx = 5)).replace("'", "''").strip()
    description = str(import_page.cell_value(rowx = row, colx = 6)).replace("'", "''").strip()
    speaker = str(import_page.cell_value(rowx = row, colx = 7)).replace("'", "''").strip()

    if speaker:
        # split the speaker names separated by "; "
        alist = speaker.split("; ")
        for name in alist:
            # create a Speaker object for each speaker name
            speaker_object = Speaker(name, date, time_start, time_end, session_title)
            speaker_data.append(speaker_object.data)

    if session == "Session":
        # create a Session object for a session row
        session_object = Session(-1, date, time_start, time_end, session_title, location, description)
        session_data.append(session_object.data)
        parent_session = id

    elif session == "Sub":
        # create a Session object for a subsession row
        session_object = Session(parent_session, date, time_start, time_end, session_title, location, description)
        session_data.append(session_object.data)

# insert the session data into the sessions table
session_table.insert_many(session_data)
# insert the session data into the speakers table
speaker_table.insert_many(speaker_data)