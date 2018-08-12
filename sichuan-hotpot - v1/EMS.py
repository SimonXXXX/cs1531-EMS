import csv
from User import Staff, Student, Guest
from Event import Course, Seminar
from datetime import datetime

class EMS:
    def __init__(self):
        self._SeminarList = []
        self._CourseList = []
        self._user = []
        with open('user.csv') as file:
            readCSV = csv.reader(file, delimiter=',')
            next(readCSV)
            for info in readCSV:
                if info[4] == 'trainee':
                    self._user.append(Student(info[0],info[1],info[2],info[3],info[4]))
                elif info[4] == 'trainer':
                    self._user.append((Staff(info[0],info[1],info[2],info[3],info[4])))
                print(info[2],info[3])

    def validate_login(self, email, password):
        for user in self._user:
            if user.get_email() == email and user.get_password() == password:
                return user
        return None

    def guest_register(self, e_mail, username, password):
        guest = Guest(username, "GUEST", e_mail, password, "guest")
        self._user.append(guest)
        return guest

    def get_SeminarEvent(self):
        return self._SeminarList
    
    def get_CourseEvent(self):
        return self._CourseList

    def add_user(self, user):
        self._user.append(user)

    def add_seminar(self, seminar):
        self._SeminarList.append(seminar)

    def add_course(self, course):
        self._CourseList.append(course)
    def get_all_user(self):
        return self._user

    def get_allEvent(self):
        self._event = self._SeminarList + self._CourseList
        return self._event
    
    def get_OpeningEvent(self):
        self._event = self._SeminarList + self._CourseList
        OpeningEvent = []
        index = 0
        while index < len(self._event):
            if self._event[index]._status is "OPENING":
                OpeningEvent.append(self._event[index])
            index += 1
        return OpeningEvent

    def get_ClosedEvent(self):
        self._event = self._SeminarList + self._CourseList
        ClosedEvent = []
        index = 0
        while index < len(self._event):
            if self._event[index]._status is "CLOSED":
                ClosedEvent.append(self._event[index])
            index += 1
        return ClosedEvent

    
    def get_user_by_id(self, user_id):
        for user in self._user:
            if int(user.get_id()) == int(user_id):
                return user
        return False

    def get_event_by_id(self, event_id):
        for event in self._SeminarList:
            if int(event.get_id()) == int(event_id):
                return event
        for event in self._CourseList:
            if int(event.get_id()) == int(event_id):
                return event
        return False


    def register_event(self, user, event):
        if event in self.get_OpeningEvent():
            event.new_attendees(user)
            user.add_new_event(event)


    def de_register_event(self, user, event):
        if event in user.curr_RegisterEvent():
            event.remove_attendees(user)
            user.remove_event(event)


    def register_session(self, user, session):
        session.new_attendee(user)

    def de_register_session(self, user, session):
        session.remove_attendee(user)
    

    def cancel_event(self, event):
        event.change_status("CANCELLED")
        index = 0
        for user in self._user:
            for attendee in  event.get_all_attendees():
                if str(attendee) == str(user.get_name()):
                    user.send_message(("Sorry, {0} has been cancelled".format(event.get_name())))
        while index < len(self._user):
            if event in self._user[index].curr_RegisterEvent():
                self._user[index].remove_event(event)
            index += 1

    def post_course(self, user, name, capacity, 
                    location, startTime, finishTime, de_registerTime, earlybird_finishTime,register_fee,description, event_type, poster_name):
        if user.get_user_type() == "trainer":
            new_course = Course(name, capacity, location, startTime, finishTime, de_registerTime, earlybird_finishTime, register_fee,description, event_type, poster_name)
            self.add_course(new_course)
            user.post_event(new_course)
            return new_course

    def post_seminar(self, user, name, capacity, 
                    location, startTime, finishTime, de_registerTime, earlybird_finishTime,register_fee,description, event_type, poster_name):
        if user.get_user_type() == "trainer":
            new_seminar = Seminar(name, capacity, location, startTime, finishTime, de_registerTime, earlybird_finishTime, register_fee,description, event_type, poster_name)
            self.add_seminar(new_seminar)
            user.post_event(new_seminar)
            return new_seminar  
 

    def post_session(self, seminar, name, speaker, speaker_type, capacity):
        seminar.new_session(name, speaker, speaker_type, capacity)


    def get_session_by_id(self, Seminar, session_id):
        
        for session in Seminar.get_session():
            if int(session.get_id()) == int(session_id):
                return session
        return False


