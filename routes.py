from app import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from models import Task

import forms

@app.route("/")
@app.route("/index")
def index():
    tasks = Task.query.all()
    return render_template("index.html",  tasks=tasks)

@app.route("/add", methods=["POST", "GET"])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        task = Task(title = form.title.data)
        db.session.add(task)
        db.session.commit()
        flash('Tarea añadida a la base de datos')
        return redirect(url_for("index"))
    return render_template("add.html", form=form)

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = Task.query.get(task_id)
    form = forms.AddTaskForm()
    
    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            db.session.commit()
            flash("La tarea ha sido actualizada")
            return redirect(url_for("index"))
        form.title.data = task.title
        return render_template('edit.html', form=form, task_id=task_id)
    else:
        flash("No se encontró la tarea")
    return redirect(url_for('index'))

@app.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete(task_id):
    task = Task.query.get(task_id)
    form = forms.DeleteTaskForm()
    
    if task:
        if form.validate_on_submit():
           
            db.session.delete(task)
            db.session.commit()
            flash("La tarea ha sido eliminada")
            return redirect(url_for("index"))
       
        return render_template('delete.html', form=form, task_id=task_id, title=task.title)
    else:
        flash("No se encontró la tarea")
    return redirect(url_for('index'))

    
    
    