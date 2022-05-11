from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from app.auth.decorators import admin_required
from app.task.forms import register_form, task_edit_form

from app.db import db
from app.db.models import Task

task = Blueprint('task', __name__, template_folder='templates')


@task.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')



@task.route('/task', methods=['GET'], defaults={"page": 1})
@task.route('/task/<int:page>', methods=['GET','POST'])
def browse_tasks(page):
    data = Task.query.filter_by(user_id=current_user.id)
    titles = [('name', 'Task Name'), ('message', 'Task Detail'), ('date', 'Date'),('user_id', "Creator ID")]
    edit_url = ('task.edit_task', [('task_id', ':id')])
    add_url = url_for('task.add_task')
    temp_url = ('task.temp_task', [('task_id', ':id')])
    delete_url = ('task.delete_task', [('task_id', ':id')])

    current_app.logger.info("Browse page loading")

    return render_template('browse_tasks.html', titles=titles, add_url=add_url, edit_url=edit_url,
                           delete_url=delete_url, temp_url=temp_url,
                           data=data, Task=Task, record_type="Task")

@task.route('/task/uncompleted/', methods=['GET'], defaults={"page": 1})
@task.route('/task/uncompleted/<int:page>', methods=['GET','POST'])
def browse_0_tasks(page):
    data = Task.query.filter_by(is_completed=0, user_id=current_user.id)
    titles = [('name', 'Task Name'), ('message', 'Task Detail'), ('date', 'Date'),('user_id', "Creator ID")]
    edit_url = ('task.edit_task', [('task_id', ':id')])
    add_url = url_for('task.add_task')
    temp_url = ('task.temp_task', [('task_id', ':id')])
    delete_url = ('task.delete_task', [('task_id', ':id')])

    current_app.logger.info("Browse page loading")

    return render_template('browse_uncompleted_tasks.html', titles=titles, add_url=add_url, edit_url=edit_url,
                           delete_url=delete_url, temp_url=temp_url,
                           data=data, Task=Task, record_type="Task")

@task.route('/task/completed/', methods=['GET'], defaults={"page": 1})
@task.route('/task/completed/<int:page>', methods=['GET','POST'])
def browse_1_tasks(page):
    data = Task.query.filter_by(is_completed=1, user_id=current_user.id)
    titles = [('name', 'Task Name'), ('message', 'Task Detail'), ('date', 'Date'),('user_id', "Creator ID")]
    edit_url = ('task.edit_task', [('task_id', ':id')])
    add_url = url_for('task.add_task')
    temp_url = ('task.temp_task', [('task_id', ':id')])
    delete_url = ('task.delete_task', [('task_id', ':id')])

    current_app.logger.info("Browse page loading")

    return render_template('browse_completed_tasks.html', titles=titles, add_url=add_url, edit_url=edit_url,
                           delete_url=delete_url, temp_url=temp_url,
                           data=data, Task=Task, record_type="Task")



@task.route('/task/<int:task_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    form = task_edit_form(obj=task)
    if form.validate_on_submit():
        task.message = form.message.data
        task.date = form.date.data
        task.name = form.name.data
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
        task = Task(name=form.name.data,message=form.message.data, date=form.date.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Congratulations, you just created a task', 'success')
        return redirect(url_for('task.browse_tasks'))

    return render_template('task_new.html', form=form)

@task.route('/task/<int:task_id>/complete', methods=['POST', 'GET'])
@login_required
def temp_task(task_id):
    task = Task.query.get(task_id)
    if task.is_completed == 1:
        task.is_completed = 0
    else:
        task.is_completed = 1
    db.session.commit()
    return redirect(url_for('task.browse_tasks'), 302)

@task.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task Deleted', 'success')
    return redirect(url_for('task.browse_tasks'), 302)
