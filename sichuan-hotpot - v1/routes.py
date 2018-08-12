from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from server import app, EventManageSystem
from datetime import datetime
from errorException import errorException, check_event_inputs, check_session_inputs, check_register_inputs

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = EventManageSystem.validate_login(email, password)
        if user != None:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', errorMessage = 'Please input right Username and Password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user = current_user)

@app.route('/guest_register', methods = ['GET', 'POST'])
def Guest_Register():
    errors = {}
    if request.method == 'POST':
        email = request.form['Email']
        username = request.form['Username']
        password = request.form['Password']
        try:
            errors = check_register_inputs(username, password, email)
            if errors:
                raise errorException(errors)
            else:
                EventManageSystem.guest_register(email, username, password)
                return render_template('base.html',message = "Register succeed")
        except errorException as E:
            return render_template('Guest_Register.html', errors = E.errors)
    return render_template('Guest_Register.html')


@app.route('/dashboard')
@login_required
def dashboard():
        if current_user.get_user_type() == "trainer":
            return render_template('dashboard.html', all_opening_event = EventManageSystem.get_OpeningEvent(),all_close_event = EventManageSystem.get_ClosedEvent(),curr_register_event = current_user.curr_RegisterEvent(),pass_register_event = current_user.pass_RegisterEvent(),opening_posted_event = current_user.curr_PostedEvent(),closed_posted_event = current_user.past_PostedEvent(),cancelled_posted_event = current_user.cancel_PostedEvent(), trainer = 1)
        else:
            return render_template('dashboard.html', all_opening_event = EventManageSystem.get_OpeningEvent(),all_close_event = EventManageSystem.get_ClosedEvent(),curr_register_event = current_user.curr_RegisterEvent(),pass_register_event = current_user.pass_RegisterEvent(), trainer = 0)

@app.route('/show_all_Event')
@login_required
def show_all_event():
    return render_template('show_all_event.html',all_opening_event = EventManageSystem.get_OpeningEvent(),all_close_event = EventManageSystem.get_ClosedEvent())


@app.route('/post_course',methods = ['GET', 'POST'])
@login_required
def post_course():
    errors = {}
    date_format = "%Y-%m-%d"
    if request.method == "POST":
        try:
            start_time = datetime.strptime(request.form['start_time'], date_format)
        except:
            errors['start_error'] = "The start_time is not valid"
            return render_template('post_course.html', errors = errors)
        try:
            finish_time = datetime.strptime(request.form['finish_time'], date_format)
        except:
            errors['finish_error'] = "The finish_time is not valid"
            return render_template('post_course.html', errors = errors)
        try:
            earlybird_finishTime = datetime.strptime(request.form['eb_finishTime'], date_format)
        except:
            errors['early_bird_error'] = "The Early_Bird_finishTime is not valid"
            return render_template('post_course.html', errors = errors)
        try:
            de_register_time = datetime.strptime(request.form['de_register_time'], date_format)
        except:
            errors['deregister_error'] = "The de_register_time is not valid"
            return render_template('post_course.html', errors = errors)


        try:
            errors = check_event_inputs(request.form.get('name'), request.form.get('capacity'), request.form.get('location'), start_time, finish_time, de_register_time, earlybird_finishTime)
            if errors:
                raise errorException(errors)
            else:
                newCourse = EventManageSystem.post_course(current_user, request.form.get('name'), request.form.get('capacity'), request.form.get('location'), start_time, finish_time, de_register_time, earlybird_finishTime,request.form.get('fee'),request.form.get('description'), "COURSE",current_user.get_name())
                course_id = newCourse.get_id()
                return redirect(url_for('course_page',id = course_id))
        except errorException as E:
            return render_template('post_course.html', errors = E.errors)
    return render_template('post_course.html', error = {})

@app.route('/post_seminar',methods = ['GET', 'POST'])
@login_required
def post_seminar():
    errors = {}
    date_format = "%Y-%m-%d"
    if request.method == "POST":
        try:
            start_time = datetime.strptime(request.form['start_time'], date_format)
        except:
            errors['start_error'] = "The start_time is not valid"
            return render_template('post_seminar.html', errors = errors)
        try:
            finish_time = datetime.strptime(request.form['finish_time'], date_format)
        except:
            errors['finish_error'] = "The finish_time is not valid"
            return render_template('post_seminar.html', errors = errors)
        try:
            earlybird_finishTime = datetime.strptime(request.form['eb_finishTime'], date_format)
        except:
            errors['early_bird_error'] = "The Early_Bird_finishTime is not valid"
            return render_template('post_seminar.html', errors = errors)
        try:
            de_register_time = datetime.strptime(request.form['de_register_time'], date_format)
        except:
            errors['deregister_error'] = "The de_register_time is not valid"
            return render_template('post_seminar.html', errors = errors)
        try:
            errors = check_event_inputs(request.form.get('name'), request.form.get('capacity'), request.form.get('location'), start_time, finish_time, de_register_time, earlybird_finishTime)
            if errors:
                raise errorException(errors)
            else:
                newSeminar = EventManageSystem.post_seminar(current_user, request.form.get('name'), request.form.get('capacity'), request.form.get('location'), start_time, finish_time, de_register_time, earlybird_finishTime, request.form.get('fee'),request.form.get('description'), "SEMINAR",current_user.get_name())
                seminar_id = newSeminar.get_id()
                return redirect(url_for('seminar_page',id = seminar_id))
        except errorException as E:
            return render_template('post_seminar.html', errors = E.errors)
    return render_template('post_seminar.html')

@app.route('/session_page/<session_id><seminar_id>',methods = ['GET','POST'])
@login_required
def session_page(session_id, seminar_id):
    errors = {}
    seminar = EventManageSystem.get_event_by_id(seminar_id)
    session = EventManageSystem.get_session_by_id(seminar, session_id)
    register_available = "able"
    
    if current_user.get_name() in session.get_all_attendees() or session.get_num_of_attendees() >= session.get_capacity():
        register_available = "unable"
    
    de_register_available = "able"
    if current_user.get_name() not in session.get_all_attendees():
        de_register_available = "unable"

    if request.method == 'POST':
        if request.form.get('Register'):
            if current_user.get_name() == session.get_speaker():
                try:
                    raise errorException("*registraton is not successful")
                except errorException as error:
                    errors['errror'] = E.errors
                    return render_template('session_page.html', Session = session, Seminar = seminar, register_available = register_available, de_register_available = de_register_available, errors = errors)
            EventManageSystem.register_session(current_user,session)
            return redirect(url_for('session_page', session_id = session_id, seminar_id = seminar_id))
        elif request.form.get("De-Register"):
            EventManageSystem.de_register_session(current_user, session)
            return redirect(url_for('session_page', session_id = session_id, seminar_id = seminar_id))
    return render_template('session_page.html', Session = session, Seminar = seminar, register_available = register_available, de_register_available = de_register_available, errors = {})

@app.route('/add_session/<id>',methods = ['GET','POST'])
@login_required
def add_session(id):
    errors = {}
    if request.method == 'POST':
        id_session = id
        session_name = request.form.get('name')
        session_speaker = request.form.get('speaker')
        speaker_type = request.form.get('speaker_type')
        session_capacity = request.form.get('capacity')
        try:
            errors = check_session_inputs(session_name, session_speaker, speaker_type, session_capacity, EventManageSystem.get_event_by_id(id_session))
            if errors:
                raise errorException(errors)
            else:
                now_session = EventManageSystem.post_session(EventManageSystem.get_event_by_id(id_session),\
                                        session_name, session_speaker,\
                                        speaker_type,session_capacity)
                return redirect(url_for('seminar_page',id = id_session, session_list = now_session))          
        except errorException as E:
            return render_template('add_session.html', errors = E.errors)
    return render_template('add_session.html', errors = {})


@app.route('/course_page/<id>',methods = ['GET', 'POST'])
@login_required
def course_page(id):
    course = EventManageSystem.get_event_by_id(id)

    register_available = "able"
    if course.judge_capacity() == False or course.get_status() is "CLOSED" or current_user.get_name() in course.get_all_attendees() or course.get_status() is "CANCELLED":
        register_available = "unable"

    de_register_available = "able"
    if course.get_de_registerTime() < datetime.now() or course.get_status() is "CLOSED"  or course.get_status() is "CANCELLED"  or current_user.get_name() not in course.get_all_attendees():
        de_register_available = "unable"

    cancel_available = "unable"
    if str(current_user.get_user_type()) == "trainer" and str(course.get_poster_name()) == str(current_user.get_name()):
        cancel_available = "able"

    register_eb = "able"
    if current_user.get_name() in course.get_all_attendees() or course.judge_capacity() is False:
        register_eb = "unable"

    if course.get_status() == "CANCELLED" or course.get_status() == "CLOSED":
        register_available = "unable"
        de_register_available = "unable"
        cancel_available = "unable"
        register_eb = "unable" 

    if request.method == 'POST':
        if request.form.get('Register') or request.form.get('eb'):
            if str(current_user.get_name()) == str(course.get_poster_name()):
                try:
                    raise errorException("*Convenor cannot register for your event")
                except errorException as G:
                    errors = G.errors
                    return render_template('course_page.html', Course = EventManageSystem.get_event_by_id(id), r_available = register_available, d_r_available = de_register_available, c_available = cancel_available, register_eb = register_eb, errors = errors)
            EventManageSystem.register_event(current_user, course)
            return redirect(url_for('course_page',id = id))
        elif request.form.get('De-Register'):
            EventManageSystem.de_register_event(current_user, course)
            return redirect(url_for('course_page',id = id))
        elif request.form.get('Cancel'):
            EventManageSystem.cancel_event(course)
            return redirect(url_for('dashboard'))
        if request.form.get('Show'):
            return render_template('All_attendees.html', Event = EventManageSystem.get_event_by_id(id))
        return render_template('course_page.html', Course = EventManageSystem.get_event_by_id(id), r_available = register_available, d_r_available = de_register_available, c_available = cancel_available, register_eb = register_eb,detail = 'FAIL')
    return render_template('course_page.html', Course = EventManageSystem.get_event_by_id(id), r_available = register_available, d_r_available = de_register_available, c_available = cancel_available,register_eb = register_eb)


@app.route('/seminar_page/<id>',methods= ['GET', 'POST'])
@login_required
def seminar_page(id):
    seminar = EventManageSystem.get_event_by_id(id)
    session_list = seminar.get_session()
    
    register_available = "able"
    if seminar.judge_capacity() is False or seminar.get_status() is "CLOSED"  or current_user.get_name() in seminar.get_all_attendees() or seminar.get_status() is "CANCELLED":
        register_available = "unable"

    de_register_available = "able"
    if seminar.get_status() is "CLOSED" or seminar.get_status() is "CANCELLED" or current_user.get_name() not in seminar.get_all_attendees():
        de_register_available = "unable"

    cancel_available = "able"
    if str(current_user.get_name()) != str(seminar.get_poster_name()):
        cancel_available = "unable"

    new_session_available = "able"
    if str(current_user.get_name()) != str(seminar.get_poster_name()):
        new_session_available = "unable"

    register_eb = "able"
    if current_user.get_name() in seminar.get_all_attendees() or seminar.judge_capacity() is False:
        register_eb = "unable"

    register_available_session = "unable"
    for session in session_list:
        for attendee in session.get_all_attendees():
            if str(attendee) == str(current_user.get_name()):
                register_available_session = "able"
                break

    guest_speaker_free = "unable"


    if seminar.get_status() == "CANCELLED" or seminar.get_status() == "CLOSED":
        register_available = "unable"
        de_register_available = "unable"
        cancel_available = "unable"
        new_session_available = "unable"
        register_eb = "unable"
        register_available_session = "unable"

    if request.method == 'POST':
        if request.form.get('Register') or request.form.get('eb'):
            if str(current_user.get_name()) == str(seminar.get_poster_name()):
                try:
                    raise errorException("*Convenor cannot register for your event")
                except errorException as G:
                    errors = G.errors
                    return render_template('seminar_page.html', Seminar = EventManageSystem.get_event_by_id(id), r_available = register_available, d_r_available = de_register_available, n_s_available = new_session_available, c_available = cancel_available, register_eb = register_eb, session_list = session_list, RAS = register_available_session, errors = errors, guest_speaker_free = guest_speaker_free)
            EventManageSystem.register_event(current_user, seminar)
            return redirect(url_for('seminar_page',id = id))
        elif request.form.get('De-Register'):
            EventManageSystem.de_register_event(current_user, seminar)
            return redirect(url_for('seminar_page',id = id))
        elif request.form.get('Cancel'):
            EventManageSystem.cancel_event(seminar)
            return redirect(url_for('dashboard'))
        if request.form.get('Add_session'):
            return redirect(url_for('add_session',id = id))
        if request.form.get('Show'):
            return render_template('All_attendees.html', Event = EventManageSystem.get_event_by_id(id))
        return render_template('seminar_page.html', Seminar = EventManageSystem.get_event_by_id(id), r_available = register_available, d_r_available = de_register_available, n_s_available = new_session_available, c_available = cancel_available, register_eb = register_eb, detail = 'FAIL', session_list = session_list, RAS = register_available_session, guest_speaker_free = guest_speaker_free)
    return render_template('seminar_page.html', Seminar = EventManageSystem.get_event_by_id(id), r_available = register_available, d_r_available = de_register_available, n_s_available = new_session_available, c_available = cancel_available, register_eb = register_eb, session_list = session_list, RAS = register_available_session, guest_speaker_free = guest_speaker_free)


