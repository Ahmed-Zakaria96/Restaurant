from wtforms import Form, SelectField, StringField, PasswordField, validators

user_type_choices = ['Admin', 'Restaurant', 'Customer']

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.DataRequired()])
    user_type = SelectField('Type', choices=user_type_choices)
