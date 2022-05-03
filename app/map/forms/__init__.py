from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class location_edit_form(FlaskForm):
    title = StringField('Location Name', [
        validators.DataRequired(),

    ], description="Name of the location")
    longitude = StringField('Longitude', [
        validators.DataRequired(),

    ], description="Longitude of the location")
    latitude = StringField('Latitude', [
        validators.DataRequired(),

    ], description="Latitude of the location")
    population = IntegerField('Population', [
        validators.DataRequired(),

    ], description="Population of the location")
    is_admin = BooleanField('Admin', render_kw={'value':'1'})
    submit = SubmitField()



class location_form(FlaskForm):
    title = StringField('Location Name', [
        validators.DataRequired(),

    ], description="Name of the location")
    longitude = StringField('Longitude', [
        validators.DataRequired(),

    ], description="Longitude of the location")
    latitude = StringField('Latitude', [
        validators.DataRequired(),

    ], description="Latitude of the location")
    population = IntegerField('Population', [
        validators.DataRequired(),

    ], description="Population of the location")
    submit = SubmitField()


class csv_upload(FlaskForm):
    file = FileField()
    submit = SubmitField()