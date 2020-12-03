from . import db, login_mananger
from datetime import datetime, time
from werkzeug.security import generate_password_hash


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    dept = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Options(Super, Admin, Driver, Approver)

    def __init__(self, user_id, username, password, firstname, lastname, email, dept, job_title, role):
        self.user_id = user_id
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.dept = dept
        self.job_title = job_title
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        try:
            return unicode(self.user_id)
        except NameError:
            return str(self.user_id)

    def __repr__(self):
        return '<User %r>' % (self.username)


@login_mananger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Vehicle(db.Model):

    __tablename__ = 'vehicles'

    reg_id = db.Column(db.String(6), primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    yr = db.Column(db.Integer, nullable=False)
    colour = db.Column(db.String(50), nullable=False)
    max_weight = db.Column(db.Integer, nullable=False)
    registration = db.Column(db.DateTime, nullable=False)
    fitness = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Available")  # Options(Available, Garage, Reserved, Assigned)
    edited_by = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now())
    edit_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    assignment = db.relationship('Assignment', backref=db.backref('vehicle_assignment'), uselist=False)
    history = db.relationship('History', backref=db.backref('vehicle_history'))

    def __init__(self, reg_id, make, model, yr, colour, max_weight, registration, fitness, status, edited_by, date_added, edit_date):
        self.reg_id = reg_id
        self.make = make
        self.model = model
        self.yr = yr
        self.colour = colour
        self.max_weight = max_weight
        self.registration = registration
        self.fitness = fitness
        self.status = status
        self.edited_by = edited_by
        self.date_added = date_added
        self.edited_by = edit_date


class Driver(db.Model):

    __tablename__ = 'drivers'

    user_id = db.Column(db.Integer, primary_key=True)
    licence_type = db.Column(db.String(20), nullable=False)
    max_weight = db.Column(db.Integer, nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    issue_country = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False) # Options(Pending, Approved, Declined, Suspended)
    manager = db.Column(db.Integer, nullable=False)  # might not need this if an set approvers for each dept
    licence_front = db.Column(db.String(80), nullable=False)
    licence_back = db.Column(db.String(80), nullable=False)

    def __init__(self, user_id, licence_type, max_weight, issue_date, expiry_date, issue_country, status, manager, licence_front, licence_back):
        self.user_id = user_id
        self .licence_type = licence_type
        self.max_weight = max_weight
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.issue_country = issue_country
        self.status = status
        self.manager = manager
        self.licence_front = licence_front
        self.licence_back = licence_back


class Department(db.Model):

    __tablename__ = 'departments'

    dept_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_name = db.Column(db.String(250), nullable=False)
    section = db.Column(db.String(30), nullable=False)

    def __init__(self, dept_id, dept_name, section):
        self.dept_id = dept_id
        self.dept_name = Department
        self.section = section


class Approver(db.Model):

    __tablename__ = 'approvers'

    approver_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.dept_id'), nullable=False)

    def __init__(self, approver_id, user_id, dept_id):
        self.approver_id = approver_id
        self.user_id = user_id
        self.dept_id = dept_id


class Request(db.Model):

    __tablename__ = 'requests'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver = db.Column(db.Integer, db.ForeignKey('drivers.user_id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.now())
    date_from = db.Column(db.DateTime, nullable=False)
    time_from = db.Column(db.Time, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    time_to = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")  # Options(Pending, Approved, Disapproved, Manger Approval)
    # approval
    approver = db.Column(db.Integer)
    approval_date = db.Column(db.DateTime)

    def __init__(self, request_id, driver, request_date, date_from, time_from, date_to, time_to, reason, status, approver, approval_date):
        self.request_id = request_id
        self.driver = driver
        self.request_date = request_date
        self.date_from = date_from
        self.time_from = time_from
        self.date_to = date_to
        self.time_to = time_to
        self.reason = reason
        self.status = status
        self.appover = approver
        self.approval_date = approval_date


class Assignment(db.Model):

    __tablename__ = 'assignments'

    reg_id = db.Column(db.String(6), db.ForeignKey('vehicles.reg_id'), primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.user_id'), unique=True, nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.request_id'), nullable=False)
    assign_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    assign_time = db.Column(db.Time, nullable=False, default=datetime.now())
    assigner = db.Column(db.Integer)

    def __init__(self, reg_id, driver_id, request_id, assign_date, assigner):
        self.reg_id = reg_id
        self.driver_id = driver_id
        self.request_id = request_id
        self.assign_date = assign_date
        self.assigner = assigner


class CheckOff(db.Model):

    __tablename__ = 'checkOff'

    check_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.request_id'), nullable=False)
    vehicle = db.Column(db.String(6), db.ForeignKey('vehicles.reg_id'), nullable=False)
    dt = db.Column(db.DateTime, nullable=False, default=datetime.now())
    tm = db.Column(db.Time, nullable=False, default=datetime.now())
    check = db.Column(db.String(5), nullable=False)  # Options(In, Out)
    mileage = db.Column(db.Integer, nullable=False)
    fuel_card = db.Column(db.Boolean, nullable=False)
    fuel = db.Column(db.String(20), nullable=False)  # Options(Full, Three Quarters, Half, Quarter, Empty)
    jack = db.Column(db.Boolean, nullable=False)
    lug_tool = db.Column(db.Boolean, nullable=False)
    spare_wheel = db.Column(db.Boolean, nullable=False)
    condition = db.Column(db.String(20), nullable=False)  # Options(Good, Dirty, Fair)

    def __init__(self, check_id, request_id, vehicle, dt, tm, check, mileage, fuel_card, fuel, jack, lug_tool, spare_wheel, condition):
        self.check_id = check_id
        self.request_id = request_id
        self.vehicle = vehicle
        self.dt = dt
        self.tm = tm
        self.check = check
        self.mileage = mileage
        self.fuel_card = fuel_card
        self.fuel = fuel
        self.jack = jack
        self.lug_tool = lug_tool
        self.spare_wheel = spare_wheel
        self.condition = condition


class History(db.Model):

    __tablename__ = 'history'

    history_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.request_id'), nullable=False)
    vehicle = db.Column(db.String(6), db.ForeignKey('vehicles.reg_id'), nullable=False)
    dt = db.Column(db.DateTime, nullable=False)
    tm = db.Column(db.Time, nullable=False)
    check = db.Column(db.String(5), nullable=False)  # Options(In, Out)
    approved_by = db.Column(db.Integer, nullable=False)
    assigned_by = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)

    def __init__(self, history_id, request_id, vehicle, dt, tm, ckeck, approved_by, assigned_by, note):
        self.history_id = history_id
        self.request_id = request_id
        self.vehicle = vehicle
        self.dt = dt
        self.tm = tm
        self.check = check
        self.approved_by = approved_by
        self.assigned_by = assigned_by
        self.note = note
