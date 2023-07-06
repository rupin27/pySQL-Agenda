class Speaker:
    def __init__(self, name, date, time_start, time_end, session_id):

        # attributes of a speaker
        self.name = "speakers"
        self.date = "date"
        self.time_start = "time_start"
        self.time_end = "time_end"
        self.session_id = "session_title"
        # dictionary to store the speaker data
        
        self.data = {
            self.name: name,
            self.date: date,
            self.time_start: time_start,
            self.time_end: time_end,
            self.session_id: session_id
        }