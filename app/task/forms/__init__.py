from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *

class register_form(FlaskForm):
    name = StringField('Task Title', [
        validators.DataRequired(),

    ], description="This is the Name of the Task")

    message = StringField('Task Details', [
        validators.DataRequired(),

    ], description="Description of the Task")
    date = DateField('Deadline', [
        validators.DataRequired(),

    ], description="Deadline")
    submit = SubmitField()


class task_edit_form(FlaskForm):
    name = StringField('Task Title', [
        validators.DataRequired(),

    ], description="This is the Name of the Task")

    message = StringField('Task Details', [
        validators.DataRequired(),

    ], description="Description of the Task")
    date = DateField('Deadline', [
        validators.DataRequired(),

    ], description="Deadline")
    submit = SubmitField()

