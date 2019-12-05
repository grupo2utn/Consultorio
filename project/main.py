from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import db, Horario, DiaAtencion,Profesional, AtencionProfesional, Turnos, Paciente, Especialidad, EspecialidadProfesional
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
    user = current_user.id
    lista = request.form.getlist('horasAingresar')
    for hora in lista:
        b = Horario.query.filter_by(id=hora).first()
        bandera = AtencionProfesional.query.filter_by(id_Profesional=user,id_Dia=dia,id_Horario=hora).first()
        if not bandera:                          
            new_atencion = AtencionProfesional(id_Profesional=user,id_Dia=dia,id_Horario=hora)
            db.session.add(new_atencion)
    db.session.commit()  
    return redirect(url_for('main.profile'))


@main.route('/profile/atencion')
@login_required
def profile_atencion(): 
    user = current_user.id 
    ate = AtencionProfesional.query.filter_by(id_Profesional=user).order_by(AtencionProfesional.id_Dia, AtencionProfesional.id_Horario).all()
    o = []
    for i in ate:
        h = Horario.query.filter_by(id=i.id_Horario).first()
        d = DiaAtencion.query.filter_by(id=i.id_Dia).first()
        o.append([i.id, d.descripcion, h.hora_inicio])
    return render_template('profile.html', ate=ate, o=o)


@main.route('/profile/atencion', methods=['POST'])
@login_required
def profile_atencion_POST(): 
    lista = request.form.getlist('ch')
    for a in lista:
        atencion = AtencionProfesional.query.filter_by(id=a[0]).first()
        if atencion:
            db.session.delete(atencion)
    db.session.commit()  
    return redirect(url_for('main.profile'))

@main.route('/profile/turnos')
@login_required
def profile_turnos(): 
    user = current_user.id 
    tur = Turnos.query.filter_by(id_Profesional=user).order_by(Turnos.id_Dia, Turnos.id_Horario).all()
    x = []
    for i in tur:
        h = Horario.query.filter_by(id=i.id_Horario).first()
        d = DiaAtencion.query.filter_by(id=i.id_Dia).first()
        p = Paciente.query.filter_by(id=i.id_Paciente).first()
        x.append([i.id, p.nombre, p.apellido, p.dni, p.email, p.telefono, i.descripcion, d.descripcion, h.hora_inicio])
    return render_template('profile.html', tur=tur, x=x)

@main.route('/profile/turnos', methods=['POST'])
@login_required
def profile_turnos_POST(): 
    lista = request.form.getlist('tu')
    for a in lista:
        turno = Turnos.query.filter_by(id=a[0]).first()
        if turno:
            db.session.delete(turno)
    db.session.commit()  
    return redirect(url_for('main.profile'))


@main.route('/profile/miturnos')
@login_required
def profile_miturnos(): 
    user = current_user.id 
    mitur = Turnos.query.filter_by(id_Paciente=user).order_by(Turnos.id_Dia, Turnos.id_Horario).all()
    w = []
    for i in mitur:
        h = Horario.query.filter_by(id=i.id_Horario).first()
        d = DiaAtencion.query.filter_by(id=i.id_Dia).first()
        p = Profesional.query.filter_by(id=i.id_Profesional).first()
        w.append([i.id, p.nombre, p.apellido ,p.email, i.descripcion, d.descripcion, h.hora_inicio])
    return render_template('profile.html', mitur=mitur, w=w)

@main.route('/profile/miturnos', methods=['POST'])
@login_required
def profile_miturnos_POST(): 
    lista = request.form.getlist('tu')
    for a in lista:
        turno = Turnos.query.filter_by(id=a[-4:]).first()
        if turno:
            db.session.delete(turno)
    db.session.commit()  
    return redirect(url_for('main.profile'))

