class Session:
    def __init__(self, parent_id, date, time_start, time_end, session_title, location, description):
        # attributes of a session
        self.id = "id"
        self.parent_id = "parent_id"
        self.date = "date"
        self.time_start = "time_start"
        self.time_end = "time_end"
        self.title = "title"
        self.location = "location"
        self.description = "description"
        # dictionary to store the session data
        self.data = {
            self.parent_id: parent_id,
            self.date: date,
            self.time_start: time_start,
            self.time_end: time_end,
            self.title: session_title,
            self.location: location,
            self.description: description,
        }