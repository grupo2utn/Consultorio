from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import db, Paciente, Profesional, DiaAtencion, Horario, Especialidad, EspecialidadProfesional


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Profesional.query.filter_by(email=email).first()
    if not user:
        user = Profesional.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Por favor revise los datos ingresados y pruebe nuevamente.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    apellido = request.form.get('apellido')
    dni = request.form.get('dni')
    telefono = request.form.get('telefono')

    paciente = Paciente.query.filter_by(email=email).first()

    if paciente:
        flash('El Mail ya se encuentra en nuestros registros')
        return redirect(url_for('auth.signup'))

    new_user = Paciente(email=email, nombre=name, apellido=apellido, dni=dni, telefono=telefono, password=generate_password_hash(password, method='sha256')  )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/signupProf')
def signupProf():

    dias = DiaAtencion.query.all()
    horas = Horario.query.all()
    especialidad = Especialidad.query.all()
    return render_template('signupProf.html', dias= dias, horas=horas, especialidad=especialidad)

@auth.route('/signupProf', methods=['POST'])
def signupProf_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    apellido = request.form.get('apellido')
    matricula = request.form.get('matricula')
    esp = request.form.get('esp')

    profesional = Profesional.query.filter_by(email=email).first()

    if profesional:
        flash('El Mail ya se encuentra en nuestros registros')
        return redirect(url_for('auth.signup'))

    new_user = Profesional(email=email, nombre=name, apellido=apellido, matricula=matricula, password=generate_password_hash(password, method='sha256')  )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/newperfil')
def newperfil():
    return render_template('newperfil.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))