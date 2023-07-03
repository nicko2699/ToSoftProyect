from flask_wtf import FlaskForm
from sqlalchemy.sql.sqltypes import String
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, IntegerField, FieldList
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Ingrese su usuario", validators=[DataRequired("Campo obligatorio")])
    password = PasswordField("Ingrese su contraseña", validators=[DataRequired("Campo obligatorio")])
    remember_me = BooleanField("Recuerdame")
    submit = SubmitField("Iniciar Sesión")

class SignUpForm(FlaskForm):
    name = StringField("Ingrese su nombre", validators=[DataRequired("Campo obligatorio")])
    last_names = StringField("Ingrese sus apellidos", validators=[DataRequired("Campo obligatorio")])
    username = StringField("Ingrese su usuario", validators=[DataRequired("Campo obligatorios")])
    password = PasswordField("Ingrese su contraseña", validators=[DataRequired("Campo obligatorio")])
    password2 = PasswordField('Repita la contraseña' , validators=[DataRequired("Campo obligatorio"), EqualTo('password')])
    email = EmailField("Ingrese su correo electrónico", validators=[DataRequired("Campo obligatorio")])
    address = StringField("Ingrese su dirección", validators=[DataRequired("Campo obligatorio")])
    phone = IntegerField("Ingrese su número telefonico", validators=[DataRequired("Campo obligatiorio")])
    submit = SubmitField(" Registrar ")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor ingrese otro nombre de usuario')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor ingrese otro correo electronico')

class EditUserForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired("Campo obligatorio")])
    last_names = StringField("Apellidos", validators=[DataRequired("Campo obligatorio")])
    username = StringField("Usuario", validators=[DataRequired("Campo obligatorios")])
    email = EmailField("Correo Electrónico", validators=[DataRequired("Campo obligatorio")])
    address = StringField("Dirección", validators=[DataRequired("Campo obligatorio")])
    phone = IntegerField("Número telefónico", validators=[DataRequired("Campo obligatiorio")])
    submit = SubmitField(" Confirmar ")

class orderServForm(FlaskForm):

    typeService = StringField("Ingrese el tipo de servicio", validators=[DataRequired("Campo obligatorio")])
    submit = SubmitField(" Confirmar orden ")

class orderWorkForm(FlaskForm):

    typeWork = StringField("Ingrese el tipo de trabajo", validators=[DataRequired("Campo obligatorio")])
    budget = StringField("Ingrese el presupuesto estimado", validators=[DataRequired("Campo obligatorio")])
    workDuration = StringField("Ingrese el tiempo estimado para realizar el trabajo", validators=[DataRequired("Campo obligatorio")])
    technician = StringField("Asigne un técnico", validators=[DataRequired("Campo obligatorio")])
    submit = SubmitField(" Confirmar orden ")
