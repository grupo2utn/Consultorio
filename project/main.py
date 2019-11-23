from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Horario, DiaAtencion,Profesional, AtencionProfesional
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    bmail = current_user.email
    user = Profesional.query.filter_by(email=bmail).first()
    name = current_user.nombre
    
    if not user:
        a = "Paciente"
    else:
        a = "Profesional"
    return render_template('profile.html', name= name, a=a)

@main.route('/profile')
def signup():
    return render_template('profile.html')


@main.route('/profile/dias')
@login_required
def profile_dias():    
    dias = DiaAtencion.query.all()
    horas = Horario.query.all()
    return render_template('profile.html', dias=dias, horas=horas)

@main.route('/profile/dias', methods=['POST'])
@login_required
def profile_dias_POST():  
    dia = request.form.get('dia')
    c = DiaAtencion.query.filter_by(id=dia).first()
    user = current_user.id
    a = Profesional.query.filter_by(id=user).first()
    lista = request.form.getlist('horasAingresar')
    for hora in lista:
        b = Horario.query.filter_by(id=hora).first()                          
        new_atencion = AtencionProfesional(id_Profesional=user,id_Dia=dia,id_Horario=hora)
        db.session.add(new_atencion)

    db.session.commit()  
    return redirect(url_for('main.index'))
