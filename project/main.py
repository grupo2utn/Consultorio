from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import db, Horario, DiaAtencion,Profesional

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    if current_user is Profesional:
        a = current_user.EspecialidadProfesional
    return render_template('profile.html', name=current_user.nombre)


@main.route('/profile/dias')
@login_required
def profile_dias():
    dias = DiaAtencion.query.all()
    horas = Horario.query.all()
    return render_template('profile.html', dias=dias, horas=horas)



@main.route('/profile/dias', methods=['GET','POST'])
@login_required
def profile_diasPOST():
    if request.method == 'POST':
        list = []
        list = request.form.getlist('dias')
    return render_template('profile.html')

