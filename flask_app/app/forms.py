from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Required
from flask_wtf.file import FileField, FileRequired

# Address entry form
class AddressForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit Address')


# Photo entry form (file selector)
class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit Photo')

# surveyform
class SurveyForm(FlaskForm):
    dropdown = SelectField(u'Main Building', choices = [('Damaged', 'Damaged'), ('Undamaged', 'Undamaged')], validators = [DataRequired()])

    outer = SelectField(u'Outer Buildings', choices = [('Damaged', 'Damaged'), ('Undamaged', 'Undamaged')])

    exterior = SelectField(u'Exterior Damage', choices = [('Yes', '  Yes  '), ('No', '  No  ')])

    interior = SelectField(u'Interior Damage', choices = [('Yes', '  Yes  '), ('No', '  No  ')])

    singletext = StringField('Percentage of property damaged')

    multiple = SelectMultipleField(u'Type of Disaster', choices = [('Fire', 'Fire'), ('Flood', 'Flood'), ('Hurricane','Hurricane'), ('Earthquake','Earthquake'), ('Tornado','Tornado')])

    extranotes = StringField('Name of Disaster')

    submit = SubmitField('Submit Damage Form')
