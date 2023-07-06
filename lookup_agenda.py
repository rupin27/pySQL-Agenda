import sys
from db_table import db_table
from tables.sessions_table import Session
from tables.speakers_table import Speaker

try:
    column = sys.argv[1]
    search_val = " ".join(sys.argv[2:])

except IndexError as e:
    raise RuntimeError("Invalid command line arguments.") from e

# create session and speaker objects
session_object = Session(None, None, None, None, None, None, None)
speaker_object = Speaker(None, None, None, None, None)

# create session and speaker tables
session_table = db_table("sessions", { session_object.id: "integer PRIMARY KEY",
                                       session_object.parent_id: "integer",
                                       session_object.date: "string NOT NULL",
                                       session_object.time_start: "string NOT NULL",
                                       session_object.time_end: "string NOT NULL",
                                       session_object.title:"string NOT NULL",
                                       session_object.location: "string",
                                       session_object.description: "string",
                                      })

speaker_table = db_table("speakers", { speaker_object.name: "string NOT NULL",
                                       speaker_object.date: "string NOT NULL",
                                       speaker_object.time_start: "string NOT NULL",
                                       speaker_object.time_end: "string NOT NULL",
                                       speaker_object.session_id: "string NOT NULL",
                                     })

if column == 'speaker':
    # query the speaker table and print results
    speaker_data = speaker_table.select(["speakers", "date", "time_start", "time_end", "session_title"], {"speakers": search_val})
    for row in speaker_data:
        result_speakers = " ".join(["{}:\t{}\t{} - {}\t{}".format(row['speakers'], row['date'], row['time_start'], row['time_end'], row['session_title'])])
        print(result_speakers)

else:
    result_sessions = []
     # query the session table and related records from the speaker table
    parent_data = session_table.select(["id", "parent_id", "date", "time_start", "time_end", "title", "location"], {column: search_val})
    sub_data = [j for row in parent_data for j in session_table.select(["id", "parent_id","date", "time_start", "time_end", "title", "location"], {"parent_id": row["id"]})]

    # unordered results, increasing efficiency 
    # result_sessions = parent_data + sub_data

    # appending data keeping sub sessions directly below the parent sessions
    for val1 in parent_data:
        result_sessions.append(val1)
        for val2 in sub_data:
            if val1['id'] == val2['parent_id']:
                result_sessions.append(val2)
                
    # removing duplicates
    result_sessions = list(set(tuple(row.items()) for row in result_sessions))
    result_sessions = [dict(item) for item in result_sessions]

    for row in result_sessions:
        result = " ".join(["{}\t{} - {}\t{}\t{}".format(row['date'], row['time_start'], row['time_end'], row['title'], row['location'])])
        print(result)
        
