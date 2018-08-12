from abc import ABC
from flask_login import UserMixin

class User(UserMixin, ABC):
    __id = -1
    def __init__(self, name, zID, email_address, password, user_type):
        self._id = self._generate_id()
        self._name = name
        self._zID = zID
        self._password = password
        self._user_type = user_type
        self._email = email_address
        self._RegisterEvent = []
        self._session = []
        self._message = ""

    def _generate_id(self):
        User.__id += 1
        return User.__id
    
    def get_id(self):
        return str(self._id)    
    
    def get_name(self):

        return self._name

    def get_zID(self):
        return self._zID

    def get_password(self):
        return str(self._password)

    def get_email(self):
        return self._email

    def get_user_type(self):
        return str(self._user_type)

    def add_new_event(self, Event):
        self._RegisterEvent.append(Event)

    def remove_event(self, Event):
        self._RegisterEvent.remove(Event)

    def curr_RegisterEvent(self):
        openingEvent = []
        index = 0
        while index < len(self._RegisterEvent):
            if self._RegisterEvent[index].get_status() == "OPENING":
                openingEvent.append(self._RegisterEvent[index])
            index += 1
        return openingEvent

    def pass_RegisterEvent(self):
        closedEvent = []
        index = 0
        while index < len(self._RegisterEvent):
            if self._RegisterEvent[index].get_status() == "CLOSED":
                closedEvent.append(self._RegisterEvent[index])
            index += 1
        return closedEvent

    def send_message(self, msg):
        self._message = msg

    def get_message(self):
        return self._message

class Staff(User):
    def __init__(self, name, zID, email_address, password, user_type):
        super().__init__(name, zID, email_address, password, user_type)
        self._PostedEvent = []

    def post_event(self, event):
        self._PostedEvent.append(event)

    def get_PostedList(self, event):
        return self._PostedEvent

    def curr_PostedEvent(self):
        currPostedEvent = []
        index = 0
        while index < len(self._PostedEvent):
            if self._PostedEvent[index].get_status() == "OPENING":
                currPostedEvent.append(self._PostedEvent[index])
            index += 1
        return currPostedEvent
    
    def past_PostedEvent(self):
        passPostedEvent = []
        index = 0
        while index < len(self._PostedEvent):
            if self._PostedEvent[index].get_status() == "CLOSED":
                passPostedEvent.append(self._PostedEvent[index])
            index += 1
        return passPostedEvent

    def cancel_PostedEvent(self):
        cancelPostedEvent = []
        index = 0
        while index < len(self._PostedEvent):
            if self._PostedEvent[index].get_status() == "CANCELLED":
                cancelPostedEvent.append(self._PostedEvent[index])
            index += 1
        return cancelPostedEvent

class Student(User):
    def __init__(self, name, zID, email_address, password, user_type):
           super().__init__(name, zID, email_address, password, user_type)

class Guest(User):
    def __init__(self, name, zID, email_address, password, user_type):
           super().__init__(name, zID, email_address, password, user_type)    

    