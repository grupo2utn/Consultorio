from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
from project.models import db, Paciente, Profesional, DiaAtencion, Horario, Especialidad,AtencionProfesional,Turnos

turno=Blueprint('turno',__name__)

@turno.route('/turnoPaciente/atencion_especialidad')
@login_required
def paciente_elegirEsp():
    user = current_user.id
    especialidad = Especialidad.query.all()
    return render_template('turnoPaciente.html', especialidad=especialidad)

@turno.route('/turnoPaciente/atencion_especialidad',methods=['POST'])
@login_required
def paciente_elegirEsp_post():
    global esp
    esp=request.form.get('esp')
    return redirect(url_for('turno.paciente_elegirProf'))

@turno.route('/turnoPaciente/atencion_profesional')
@login_required
def paciente_elegirProf():
    espe=Especialidad.query.filter(Especialidad.id==esp).first()
    profesional=Profesional.query.filter(Profesional.especialidad.contains(espe)).all()
    return render_template('turnoPaciente.html', profesional=profesional)

@turno.route('/turnoPaciente/atencion_profesional',methods=['POST'])
@login_required
def paciente_elegirProf_post():
    global prof
    prof=request.form.get('pro')
    return redirect(url_for('turno.paciente_elegirDiaYHora'))

@login_required
@turno.route('/turnoPaciente/atencion_dia')
def paciente_elegirDiaYHora():
    dias=DiaAtencion.query.all()
    horas=Horario.query.all()
    ate = AtencionProfesional.query.filter_by(id_Profesional=prof).order_by(AtencionProfesional.id_Dia, AtencionProfesional.id_Horario).all()
    o = []
    for i in ate:
        h = Horario.query.filter_by(id=i.id_Horario).first()
        d = DiaAtencion.query.filter_by(id=i.id_Dia).first()
        ban = Turnos.query.filter_by(id_Profesional=prof, id_Horario=h.id, id_Dia=d.id).first()
        if not ban:
            o.append([i.id_Dia, i.id_Horario, d.descripcion, h.hora_inicio, i.id])
    return render_template('turnoPaciente.html',o=o)

@turno.route('/turnoPaciente/atencion_dia_hora',methods=['POST'] )
@login_required
def paciente_elegirDiaYHora_Post():
    global dia, hora, h, d
    tur= request.form.get('tur')
    obs = request.form.get('obs')
    new_turno= Turnos(id_Profesional=prof,id_Dia=tur[1],id_Horario=tur[4],id_Paciente=current_user.id, descripcion= obs )
    db.session.add(new_turno)
    db.session.commit()
    return redirect(url_for('turno.paciente_registro'))


@turno.route('/turnoPaciente/turnoRegistrado')
@login_required
def paciente_registro():
    registro='Registrado correctamente'
    return render_template('turnoPaciente.html',profesionalTurno=registro)
