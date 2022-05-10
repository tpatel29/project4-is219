from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from app.auth.decorators import admin_required
from app.auth.forms import login_form, register_form, profile_form, security_form, user_edit_form
from app.db import db
from app.db.models import User
from app.db.models import Task

task = Blueprint('task', __name__, template_folder='templates')


@task.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@task.route('/taska')
@login_required
@admin_required
def browse_tasks():
    data = Task.query.all()
    titles = [('name', 'Task Name'), ('message', 'Task Detail'), ('date', 'Date')]
    edit_url = ('task.edit_task', [('task_id', ':id')])
    add_url = url_for('task.add_task')
    delete_url = ('task.delete_task', [('task_id', ':id')])
    # filter_by(name = 'some name', id = 5)
    current_app.logger.info("Browse page loading")

    return render_template('browse.html', titles=titles, add_url=add_url, edit_url=edit_url, delete_url=delete_url,
                           data=data, Task=Task, record_type="Tasks")


@task.route('/task/<int:task_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    form = task_edit_form(obj=task)
    if form.validate_on_submit():
        task.about = form.about.data
        task.is_admin = int(form.is_admin.data)
        db.session.add(task)
        db.session.commit()
        flash('Task Edited Successfully', 'success')
        current_app.logger.info("edited a task")
        return redirect(url_for('task.browse_tasks'))
    return render_template('task_edit.html', form=form)

@task.route('/task/new', methods=['POST', 'GET'])
@login_required
def add_task():
    form = register_form()
    if form.validate_on_submit():
        task = Task.query.filter_by(email=form.email.data).first()
        if task is None:
            task = Task(name=form.name.data,message=form.message.data, date=form.date.data )
            db.session.add(task)
            db.session.commit()
            flash('Congratulations, you just created a task', 'success')
            return redirect(url_for('auth.browse_tasks'))
        else:
            flash('Already Registered')
            return redirect(url_for('auth.browse_tasks'))
    return render_template('task_new.html', form=form)


@task.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task Deleted', 'success')
    return redirect(url_for('auth.browse_tasks'), 302)
