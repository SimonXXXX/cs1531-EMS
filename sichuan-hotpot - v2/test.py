from flask import Flask,render_template, request, redirect, url_for, abort
from flask_login import LoginManager
from datetime import datetime
from EMS import EMS
from Session import Session
from Event import Course, Seminar
from User import Staff, Student, Guest
import pytest

system = EMS()

#Guest-user into system
def test_one_correct():
    e_mail = "stella0@unsw.net"
    username = "stella"
    password = "stella"
    guest = system.guest_register(e_mail, username, password)
    assert guest.get_name() == "stella"
    assert guest.get_password() == "stella"
    assert guest.get_email() == "stella0@unsw.net"

def test_one_error_1():
    with pytest.raises(Exception) as a:
        email = "crystal666"
        name = ""
        password = ""
        new = system.guest_register(email, name, password)
        assert a.errors['address_error'] == "Email address error!"
        assert a.errors['name_error'] == "Name cannot be empty!"
        assert a.errors['password_error'] == "Password cannot be empty!"

def test_one_error_2():
    with pytest.raises(Exception) as a:
        email = "hello@unsw.net"
        name = ""
        password = ""
        new = system.guest_register(email, name, password)
        assert a.errors['address_error'] == "Email address error!"
        assert a.errors['name_error'] == "Name cannot be empty!"
        assert new.get_email() == "hello@unsw.net"

def test_one_error_3():
    with pytest.raises(Exception) as a:
        e_mail = "genius@hell.com"
        username = "g e nius"
        password = "genius"
        new = system.guest_register(e_mail, username, password)
        assert a.errors['username_blank'] == "Blank cannot be included in the Username!"

#create new seminar
def test_two_correct():
    date_format = "%Y-%m-%d"
    name = "Dolly"
    zID = "5122462"
    email = "z5122462@unsw.net"
    password = "dolly"
    user_type = "trainer"
    new = Staff(name, zID, email, password, user_type)
    assert new.get_name() == "Dolly"
    assert new.get_password() == "dolly"


    s_name = "Dolly"
    s_capacity = 80
    s_location = "rosebery"
    s_startTime = datetime.strptime("2018-08-01", date_format)
    s_finishTime = datetime.strptime("2018-08-31", date_format)
    s_de_registerTime = datetime.strptime("2018-07-19", date_format)
    s_earlybird_finishTime = datetime.strptime("2018-07-18", date_format)
    register_fee = 5
    s_description = "helloWorld"
    event_type = "SEMINAR"
    poster_name = "Dolly"
    S = system.post_seminar(new, s_name, s_capacity, s_location, s_startTime, s_finishTime, s_de_registerTime, s_earlybird_finishTime, register_fee, s_description, event_type, poster_name)
    assert S.get_name() == "Dolly"
    assert S.get_finishTime() > S.get_startTime()
    assert S.get_startTime() > S.get_de_registerTime()
    assert str(S.get_name()) != ""
    assert str(S.get_capacity()) != ""

def test_two_error_1():
    with pytest.raises(Exception) as a:
        date_format = "%Y-%m-%d"
        name = "Molly"
        zID = "5122463"
        email = "51222463@unsw.net"
        password = "cooler"
        role = "trainer"
        new = Staff(name, zID, email, password, role)
        assert new.get_name() == "Molly"
        assert new.get_email() == "5122463@unsw.net"
        assert new.get_password() == "cooler"

        #seminar initialization
        s_name = "Molly is the best!"
        s_capacity = 30
        s_location = "mentmore"
        s_star_time = datetime.strptime("2018-08-01", date_format)
        s_finish_time = datetime.strption("2018-07-31", date_format)
        s_deregister_time = datetime.strptime("2018-07-30", date_format)
        s_early_bird_time = datetime.strptime("2018-07-29", date_format)
        s_fee = 0
        s_description = "hello, welcome to the activity"
        s_event_type = "SEMINAR"
        s_poster = "Molly"
        seminar = system.post_seminar(Dolly, s_name, s_capacity, s_location, s_start_time, s_finish_time, s_deregister_time, s_early_bird_time, s_fee, s_description, s_event_type, s_poster)

        assert seminar.get_name == "Molly is the best!"
        assert seminar.location == "mentmore"
        assert a.errors['capacity_error'] == "Capacity cannot be 0!"
        assert a.errors['sf_error'] == "Start_time & Finish_time Error!"

def test_two_error_2():
    with pytest.raises(Exception) as a:
        date_format = "%Y-%m-%d"
        name = "Holly"
        zID = "5122464"
        email = "51222464@unsw.net"
        password = "coolest"
        role = "trainer"
        new = Staff(name, zID, email, password, role)
        assert new.get_name() == "Holly"
        assert new.get_email() == "5122464@unsw.net"
        assert new.get_password() == "cooler"

        #seminar initialization
        s_name = ""
        s_capacity = 30
        s_location = "mentmore"
        s_star_time = datetime.strptime("2018-08-01", date_format)
        s_finish_time = datetime.strption("2018-08-31", date_format)
        s_deregister_time = datetime.strptime("2018-08-20", date_format)
        s_early_bird_time = datetime.strptime("2018-07-29", date_format)
        s_fee = 10
        s_description = "hello, welcome to the activity"
        s_event_type = "SEMINAR"
        s_poster = "Holly"
        seminar = system.post_seminar(Dolly, s_name, s_capacity, s_location, s_start_time, s_finish_time, s_deregister_time, s_early_bird_time, s_fee, s_description, s_event_type, s_poster)

        assert a.errors['name_error'] == "Event name cannot be empty!"
        assert a.errors['dr_error'] == "De_register_time Error!"

