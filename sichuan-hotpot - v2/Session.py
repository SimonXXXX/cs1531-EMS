from flask_login import current_user
class Session:
    __id = -1
    def __init__(self, name, speaker, speaker_type, capacity):
        self._id = self.generate_id()
        self._name = name
        self._speaker = speaker
        self._type = speaker_type
        self._capacity = capacity
        self._attendees = []    

    def generate_id(self):
        Session.__id += 1
        return Session.__id

    def get_id(self):
        return str(self._id)

    def get_name(self):
        return self._name

    def get_speaker(self):
        return self._speaker

    def get_speaker_type(self):
        return self._type

    def get_capacity(self):
        return int(self._capacity)

    def get_num_of_attendees(self):
        return int(len(self._attendees))

    def get_all_attendees(self):
        return self._attendees

    def new_attendee(self,user):
        self._attendees.append(user.get_name())
    
    def remove_attendee(self,user):
        self._attendees.remove(user.get_name())