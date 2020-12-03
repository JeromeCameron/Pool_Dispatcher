from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, IntegerField, DateTimeField, DateField, TimeField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email, Length, Regexp, Required
from datetime import datetime, time


class UserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confrim_password = PasswordField('Confirm Password', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    dept = StringField('Department', validators=[InputRequired()])
    job_title = StringField('Job Title', validators=[InputRequired()])
    role = StringField('Role', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class VehicleForm(FlaskForm):
    reg_id = StringField('Reg Plate No.', validators=[InputRequired(), Length(min=5, max=6), Regexp(u'(^[A-Z]{2}\d{4}$)|(^\d{4}[A-Z]{2}$)|(^\d{4}[A-Z]{1}$)')])
    make = StringField('Make', validators=[InputRequired()])
    model = StringField('Model', validators=[InputRequired()])
    yr = IntegerField('Year', validators=[Required()])
    colour = StringField('Colour', validators=[InputRequired()])
    max_weight = IntegerField('Max-Weight', validators=[Required()])
    registration = DateField('Registration', validators=[InputRequired()])
    fitness = DateField('Fitness', validators=[InputRequired()])
    status = StringField('Status', validators=[InputRequired()])


class DriverForm(FlaskForm):
    licence_type = StringField('Licence Class', validators=[InputRequired()])
    max_weight = IntegerField('Max Weight', validators=[Required()])
    issue_date = DateField('Original Issue Date', validators=[InputRequired()])
    expiry_date = DateField('Expiry Date', validators=[InputRequired()])
    issue_country = StringField('Issue Country', validators=[InputRequired()])
    status = StringField('Status', validators=[InputRequired()])
    manager = StringField('Manager', validators=[InputRequired()])
    licence_front = FileField('Front', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    licence_back = FileField('Back', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])


class DepartmentForm(FlaskForm):
    dept_name = StringField('Department', validators=[InputRequired()])
    section = StringField('Section', validators=[InputRequired()])


class ApproverForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[Required()])
    dept_id = IntegerField('Department ID', validators=[Required()])


class RequestForm(FlaskForm):
    driver = IntegerField('Driver ID', validators=[InputRequired()])
    # request_date = DateField('Request Date', validators=[InputRequired()])
    date_from = DateField('Date From', validators=[InputRequired()])
    time_from = DateTimeField('Time From', validators=[InputRequired()])
    date_to = DateField('Date To', validators=[InputRequired()])
    time_to = DateTimeField('Time To', validators=[InputRequired()])
    reason = TextAreaField('Reason', validators=[InputRequired()])
    status = StringField('Status', validators=[InputRequired()])
    approver = IntegerField('Approver', validators=[Required()])
    approval_date = DateTimeField('Approval Date', validators=[InputRequired()])


class AssignmentForm(FlaskForm):
    reg_id = IntegerField('Reg Plate No.', validators=[Required()])
    driver_id = IntegerField('Driver ID', validators=[Required()])
    request_id = IntegerField('Request ID', validators=[Required()])


class CheckOffForm(FlaskForm):
    request_id = IntegerField('Request ID', validators=[Required()])
    vehicle = StringField('Vehicle', validators=[InputRequired()])
    dt = DateField('Date', validators=[InputRequired()])
    tm = DateTimeField('Time', validators=[InputRequired()])
    check = StringField('Check', validators=[InputRequired()])
    mileage = IntegerField('Mileage', validators=[Required()])
    fuel_card = BooleanField('Fuel Card', validators=[InputRequired()])
    fuel = StringField('Fuel', validators=[InputRequired()])
    jack = BooleanField('Jack', validators=[InputRequired()])
    lug_tool = BooleanField('Lug Tool', validators=[InputRequired()])
    spare_wheel = BooleanField('Fuel Card', validators=[InputRequired()])
    condition = BooleanField('Condition', validators=[InputRequired()])
