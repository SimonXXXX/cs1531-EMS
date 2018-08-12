from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from server import app, EventManageSystem
from datetime import datetime

class errorException(Exception):
    def __init__(self, errors):
        Exception.__init__(self)
        self.errors = errors
def check_register_inputs(name, password, email):
    errors = {}
    if str(name) == "":
        try:
            raise errorException("Name cannot be empty!")
        except errorException as A:
            errors['name_error'] = A.errors
    
    if str(password) == "":
        try:
            raise errorException("Password cannot be empty!")
        except errorException as B:
            errors['password_error'] = B.errors

    if str(email) == "":
        try:
            raise errorException("Email cannot be empty!")
        except errorException as C:
            errors['mail_error'] = C.errors

    test_email = False
    for character in email:
        if str(character) == "@":
            test_email = True
            break
    if test_email == False:
        try:
            raise errorException("Email address Error!")
        except errorException as D:
            errors['address_error'] = D.errors
    
    test_blank = False
    for character in name:
        if str(character) == " ":
            test_blank = True
            break
    if test_blank == True:
        try:
            raise errorException("Blank cannot be included in the Username!")
        except errorException as E:
            errors['username_blank'] = E.errors

    return errors

def check_event_inputs(name, capacity,location, start_time, finish_time, de_register_time, earlybird_finishTime):
    errors = {}
    if start_time > finish_time or start_time < datetime.now():
        try:
            raise errorException("Start_time & Finish_time Error!")
        except errorException as A:
            errors['sf_error'] = A.errors

    if de_register_time > start_time or de_register_time < datetime.now():
        try:
            raise errorException("De_register_time Error!")
        except errorException as B:
            errors['dr_error'] = B.errors

    if earlybird_finishTime > start_time or earlybird_finishTime < datetime.now():
        try:
            raise errorException("EarlyBird finish time Error!")
        except errorException as C:
            errors['eb_error'] = C.errors

    if str(name) == "":
        try:
            raise errorException("Event name cannot be empty!")
        except errorException as D:
            errors['name_error'] = D.errors
    
    if int(capacity) == 0 or str(capacity) == "":
        try:
            raise errorException("Capacity cannot be 0!")
        except errorException as E:
            errors['capacity_error'] = E.errors

    if str(location) == "":
        try:
            raise errorException("Location cannot be empty!")
        except errorException as F:
            errors['location_error'] = F.errors
    return errors


def check_session_inputs(session_name, session_speaker, speaker_type, session_capacity, Seminar):
    errors = {}
    if str(session_name) == "":
        try:
            raise errorException("Session_name cannot be empty!")
        except errorException as A:
            errors['sn_error'] = A.errors

    if str(session_speaker) == "":
        try:
            raise errorException("Speaker_name cannot be empty!")
        except errorException as B:
            errors['sp_error'] = B.errors

    if str(speaker_type) == "":
        try:
            raise errorException("Speaker_type cannot be empty!")
        except errorException as C:
            errors['type_error'] = C.errors

    if int(session_capacity) == 0 or str(session_capacity) == "":
        try:
            raise errorException("Capacity cannot be 0!")
        except errorException as D:
            errors['capacity_error'] = D.errors

    if str(speaker_type) == "Non-UNSW guest-speaker":
        test = False
        for user in EventManageSystem.get_all_user():
            if str(user.get_name()) == str(session_speaker):
                test = True
                break
        if test == False:
            try:
                raise errorException("Guest speaker must register in EMS!")
            except errorException as E:
                errors['guest_speaker'] = E.errors
    
    if int(Seminar.get_capacity()) < int(session_capacity):
        try:
            raise errorException("Session's capacity cannot be larger than Seminar's capacity!")
        except errorException as F:
            errors['capacity_num'] = F.errors
    
    Sum = 0
    for s in Seminar.get_session():
        Sum += s.get_capacity()
    if (Sum + int(session_capacity)) > Seminar.get_capacity():
        try:
            raise errorException("There is no such more seats for this session")
        except errorException as G:
            errors['no_seats'] = G.errors
    
    return errors

