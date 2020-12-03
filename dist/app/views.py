from app import app, db, session, login_mananger
from app.model import User, Vehicle, Driver, Department, Approver, Request, Assignment, CheckOff, History
from app.forms import UserForm, VehicleForm, DriverForm, DepartmentForm, ApproverForm, RequestForm, AssignmentForm, CheckOffForm, LoginForm
from flask import render_template, request, redirect, url_for, flash, jsonify, _request_ctx_stack, g
from flask_login import login_user, logout_user, current_user, login_required
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import jwt
from functools import wraps
import base64


# _____________________________ JWT Implementation ___________________________#


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(token, 'some-secret')

        except jwt.ExpiredSignature:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = payload
        return f(*args, **kwargs)

    return decorated


# _______________________ API ROUTES (endpoints) ____________________#


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            session['id'] = user.id
            login_user(user)

            username = user.firstname + " " + user.lastname
            payload = {'sub': user.id, 'name': username}
            token = jwt.encode(payload, 'some-secret', algorithm='HS256').decode('utf-8')

            data = {"token": token, "message": "Welcome "+user.firstname}
            return jsonify({"message": data['message'], "id": session['id'], "token": data['token']})

        return jsonify({"error": "Incorrect username or password"})


@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')


@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    session.pop('id', None)
    data = {"message": "See you soon!"}
    return jsonify({"message": data['message']})


@app.route('/api/user', methods=['GET', 'POST'])
@app.route('/api/user/<user_id>', methods=['GET', 'POST'])
def user(user_id=None):

    form = UserForm()

    if request.method == "POST" and form.validate_on_submit:
        if user_id is None:  # If user does not exist create user
            username = form.username.data
            password = form.password.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            dept = form.department.data
            job_title = form.job_title.data
            role = form.role.data

            user = User(username, password, firstname, lastname, email, dept, job_title, role)
            db.session.add(user)
            db.session.commit()

        else:  # If user exist provide option to update user
            user = User.query.filter_by(user_id=user_id).first()
            user.username = form.username.data
            user.firstname = form.firstname.data
            user.lastname = form.lastname.data
            user.email = form.email.data
            user.dept = form.department.data
            user.job_title = form.job_title.data
            user.role = form.role.data
            db.session.commit()

    elif request.method == "GET" and user_id is not None:
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('register.html', user=user)

    else:
        return render_template('register.html')


@app.route('/api/users', methods=['GET'])
def users():

    users = User.query.all()
    user_list = []

    for user in users:
        data = {
            'user_id': user.user_id,
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'dept': user.dept,
            'job_title': user.job_title,
            'role': user.role
        }
        user_list.append(data)
    return jsonify({'users': user_list})


@app.route('/api/driver/<driver_id>', methods=['GET'])
@app.route('/api/driver', methods=['POST'])
def driver(driver_id=None):

    form = DriverForm()

    if request.method == 'POST' and form.validate_on_submit:
        user_id = form.user_id.data
        licence_type = form.licence_type.data
        max_weight = form.max_weight.data
        issue_date = form.issue_date.data
        expiry_date = form.expiry_date.data
        issue_country = form.issue_date.data
        status = form.status.data
        manager = form.manager.data
        licence_front = form.licence_front.data
        licence_back = form.licence_back.data
        dl_front = secure_filename(licence_front.filename)
        dl_back = secure_filename(licence_back.filename)

        # set custom file name for reference which will be saved
        if dl_front.endswith('.' + "png"):
            front = "dl_" + user_id + "_" + "dl_front" + ".png"
        elif dl_front.endswith('.' + "jpg"):
            front = "dl_" + user_id + "_" + "dl_front" + ".jpg"

        if dl_back.endswith('.' + "png"):
            back = "dl_" + user_id + "_" + "dl_back" + ".png"
        elif dl_back.endswith('.' + "jpg"):
            back = "dl_" + user_id + "_" + "dl_back" + ".jpg"

        licence_front.save(os.path.join(app.config['UPLOAD_FOLDER'], front))
        licence_front.save(os.path.join(app.config['UPLOAD_FOLDER'], back))
        driver = Driver(user_id, licence_type, max_weight, issue_date, expiry_date, issue_country, status, manager, front, back)
        db.session.add(driver)
        db.session.commit()

        data = {"message": "Profile successfully Added"}
        return jsonify({"message": data['message']})
    else:
        driver = Driver.query.filter_by(user_id=driver_id).first()
        return jsonify({'driver': driver})


@app.route('/api/request', methods=['GET', 'POST'])
@app.route('/api/request/<request_id>', methods=['GET'])
def pool_request(request_id=None):

    form = RequestForm()

    if request.method == 'POST' and form.validate_on_submit:
        driver = form.driver.data
        request_date = datetime.now()
        date_from = form.date_from.data
        time_from = form.time_from.data
        date_to = form.date_to.data
        time_to = form.time_to.data
        reason = form.reason.data
        status = form.status.data
        approver = None
        approval_date = None

        vehicle_request = Request(driver, request_date, date_from, time_from, date_to, time_to, reason, status, approver, approval_date)
        db.session.add(vehicle_request)
        db.session.commit()
    elif request.method == 'GET' and request_id is not None:
        vehicle_request = Request.query.filter_by(request_id=request_id)
        return jsonify({'request': vehicle_request})
    else:
        render_template('pool_request.html')


@app.route('/api/requests', methods=['GET'])
def pool_requests():
    vehicle_requests = Request.query.all()
    request_list = []

    for req in vehicle_requests:
        data = {
            'request_id': req.vehicle_id,
            'driver': req.driver,
            'request_date': req.request_date,
            'date_from': req.date_from,
            'time_from': req.time_from,
            'date_to': req.date_to,
            'time_to': req.time_to,
            'reason': req.reason,
            'status': req.status,
            'approver': req.approver,
            'approval_date': req.approval_date
        }
        request_list.append(data)
    return jsonify({'requests': request_list})


@app.route('/api/vehicle/<regID>', methods=['GET', 'POST'])
@app.route('/api/vehicle', methods=['POST'])
def vehicle(regID=None):

    form = VehicleForm()

    if request.method == "POST" and form.validate_on_submit:
        if regID is None:
            reg_id = form.reg_id.make
            make = form.make.make
            model = form.model.make
            yr = form.yr.make
            colour = form.colour.make
            max_weight = form.max_weight.make
            registration = form.registration.make
            fitness = form.fitness.make
            status = form.status.make
            edited_by = form.edited_by.make  # Get current User
            date_added = datetime.now()
            edit_date = datetime.now()

            vehicle = Vehicle(reg_id, make, model, yr, colour, max_weight, registration, fitness, status, edited_by, date_added, edit_date)
            # Stage and commit changes
            db.session.add(vehicle)
            db.session.commit()
            # info for user
            # flash here
            return jsonify({"msg": "Vehicle added successfully!"})
        else:
            # Get Vehicle
            vehicle = Vehicle.query.filter_by(reg_id=regID).first()
            # Add Changes
            vehicle.reg_id = form.reg_id.make
            vehicle.make = form.make.make
            vehicle.model = form.model.make
            vehicle.yr = form.yr.make
            vehicle.colour = form.colour.make
            vehicle.max_weight = form.max_weight.make
            vehicle.registration = form.registration.make
            vehicle.fitness = form.fitness.make
            vehicle.status = form.status.make
            vehicle.edited_by = form.edited_by.make  # Get current User
            vehicle.edit_date = datetime.now()
            # Commit Changes
            db.session.commit()
            # info for user
            # flash here
            return jsonify({"msg": "Vehicle updated successfully!"})

    elif regID is not None:
        vehicle = Vehicle.query.filter_by(reg_id=regID).first()

        if vehicle is not None:
            return jsonify({'vehicle': vehicle})
        else:  # vehicle not in db
            return jsonify({"msg": "Vehicle not found!"})
    else:
        return "Add vehicle"


@app.route('/api/vehicles', methods=['POST'])
def vehicles():

    vehicles = Vehicle.query.all()
    vehicle_list = []

    for vehicle in vehicles:
        data = {
            'reg_id': vehicle.reg_id,
            'make': vehicle.make,
            'model': vehicle.model,
            'yr': vehicle.yr,
            'colour': vehicle.colour,
            'max_weight': vehicle.max_weight,
            'registration': vehicle.registration,
            'fitness': vehicle.fitness,
            'status': vehicle.status,
            'edited_by': vehicle.edited_by,  # Get User name form DB
            'date_added': vehicle.date_added,
            'edit_date': vehicle.edit_date
        }
        vehicle_list.append(data)
    return jsonify({'vehicles': vehicle_list})


@app.route('/api/assignment', methods=['GET', 'POST'])
@app.route('/api/assignments', methods=['GET'])
def assignment():
    return "assignment"


@app.route('/api/history/<reg_id>')
@app.route('/api/history/<driver_id>')
@app.route('/api/history')
def history(reg_id=None, driver_id=None):
    return "History"
