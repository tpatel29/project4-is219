from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *



class register_form(FlaskForm):
    name = StringField('Task Title', [
        validators.DataRequired(),

    ], description="You need to signup with an email")

    message = StringField('Task Details', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    date = DateTimeField('Deadline', [
        validators.DataRequired(),


    ], description="Create a password ")
    submit = SubmitField()


class task_edit_form(FlaskForm):
    name = StringField('Task Title', [
        validators.DataRequired(),

    ], description="You need to signup with an email")

    message = StringField('Task Details', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),

    ], description="Create a password ")
    date = DateTimeField('Deadline', [
        validators.DataRequired(),

    ], description="Create a password ")
    submit = SubmitField()

