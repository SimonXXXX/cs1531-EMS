from datetime import datetime
from abc import ABC
from Session import Session
from flask_login import current_user

class Event(ABC):
    __id = -1
    
    def __init__(self, name, capacity, location, startTime, finishTime, de_registerTime, earlybird_finishTime, register_fee,description, event_type,poster_name):
        self._id = self.generate_id()
        self._name = name
        self._capacity = int(capacity)
        self._location = location
        self._startTime = startTime
        self._finishTime = finishTime
        self._de_registerTime = de_registerTime
        self._earlybird_finishTime = earlybird_finishTime
        self._description = description
        self._register_fee = register_fee
        self._event_type = event_type
        self._poster_name = poster_name
        self._attendees = []
        self._cancel = "no"
        if self._startTime < datetime.now():
            self._status = "CLOSED"
        else:
            self._status = "OPENING"

    def generate_id(self):
        Event.__id += 1
        return Event.__id

    def get_id(self):
        return str(self._id)

    def get_status(self):
        return self._status

    def get_sale_register_fee(self):
        return (int(self._register_fee))/2
    
    def get_name(self):
        return str(self._name)
    
    def get_capacity(self):
        return self._capacity
    
    def get_location(self):
        return self._location
    
    def get_startTime(self):
        return self._startTime
    
    def get_finishTime(self):
        return self._finishTime
    
    def get_de_registerTime(self):
        return self._de_registerTime
    
    def get_earlybird_finishTime(self):
        return self._earlybird_finishTime

    def get_register_fee(self):
        return self._register_fee

    def get_poster_name(self):
        return self._poster_name

    def get_description(self):
        return self._description

    def get_event_type(self):
        return self._event_type

    def get_attendees_num(self):
        return len(self._attendees)

    def get_all_attendees(self):
        return self._attendees

    def judge_capacity(self):
        attendees_num = len(self._attendees)
        if attendees_num < self._capacity:
            return True
        else:
            return False

    def new_attendees(self, user):
        self._attendees.append(user.get_name())

    def remove_attendees(self, user):
        self._attendees.remove(user.get_name())

    def change_status(self, status):
        self._status = status

class Course(Event):
    def __init__(self, name, capacity, location, startTime, finishTime, de_registerTime, earlybird_finishTime,register_fee,description, event_type, poster_name):
        super().__init__(name, capacity, location, startTime, finishTime, de_registerTime, earlybird_finishTime,register_fee,description, event_type, poster_name)

    def get_course_presenter(self):
        return current_user.get_name()


class Seminar(Event):
    def __init__(self, name, capacity, location, startTime, finishTime, de_registerTime, earlybird_finishTime, register_fee,description, event_type, poster_name):
        super().__init__(name, capacity, location, startTime, finishTime, de_registerTime, earlybird_finishTime,register_fee,description, event_type, poster_name)
        self._session = []

    def get_session(self):
        return self._session

    
    def new_session(self, session_name, session_speaker, speaker_type, capacity):
        session = Session(session_name, session_speaker, speaker_type, capacity)
        self._session.append(session)
    



    