"""
All Test Info
1) Bad Password for Login
2) Bad Email for Login
3) Bad Email for Registration
4) Bad confirmation password for Registration
5) Bad password (requirements) for Registration
6) Already registered
7) Successful login
8) Successful registration
9) No access to users not logined in
10) access to user that is logged in
11) Check Add a task button
12) Edit a task Sucessfully
13) Delete a task Sucessfully
14) Mark a task complete Sucessfully       123
15) Mark a task incomplete Sucessfully
16) Create a task Sucessfully
17) Invalid edit of task name for task
18) Invalid edit of task detail for task
19) Invalid edit of task date for task
20) Completeing a task takes you to Completed Task page
21) Uncompleteing a task takes you to uncompleted Task page
22) Able to change your Email
23) Bad password confirmation for changing password
24) Bad email for changing email
25) Log out Sucessfully
"""
"""Testing the Calculator"""
import pytest
from app.db.models import User


def test_bad_login_pass(client):
    response = client.post("/login", data={"email": "tester@gmail.com", "password": "wrongPassword"},
                           follow_redirects=True)
    print(response.data)
    assert b"Invalid username or password" in response.data


def test_bad_login_email(client):
    response = client.post("/login", data={"email": "wrongEmail@gmail.com", "password": "Password123"},
                           follow_redirects=True)
    assert b"Invalid username or password" in response.data


def test_bad_regis_email(client):
    response = client.post("/register", data={"email": "", "password": "Password123", "confirm": "Password123"},
                           follow_redirects=True)
    if b'This field is required' not in response.data:
        print(response.data)
    assert b'This field is required' in response.data


def test_bad_regis_confirm(client):
    response = client.post("/register",
                           data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password"},
                           follow_redirects=True)

    assert b'Passwords must match' in response.data

#
# def test_bad_regis_pass(client):
#     response = client.post("/register", data={"email": "whatarethoses@gmail.com", "password": "123", "confirm": "123"},
#                            follow_redirects=True)
#     assert b'Password must be between 6 and 35 characters' in response.data


def test_already_regis(client):
    response = client.post("/register",
                           data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},
                           follow_redirects=True)
    response = client.post("/register",
                           data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},
                           follow_redirects=True)
    assert b'Already Registered' in response.data


def test_success_login(client):
    response = client.post("/register",
                           data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},
                           follow_redirects=True)
    response = client.post("/login",
                           data={"email": "tester@gmail.com", "password": "Password123"},
                           follow_redirects=True)
    assert b'Welcome' in response.data


def test_success_regis(client):
    response = client.post("/register",
                           data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},
                           follow_redirects=True)
    assert b'Congratulations, you are now a registered user' in response.data


def test_deny_dashboard_assess(client, application):
    with application.app_context():
        client.post("/login", data={"email": "tes@gmail.com", "password": "Password123"}, follow_redirects=True)
        client.get("/logout", follow_redirects=True)
        response = client.get("/dashboard", follow_redirects=True)
        assert b'Please log in to access this page' in response.data


def test_allow_dashboard_assess(client, application):
    with application.app_context():
        response = client.post("/register",
                               data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},
                               follow_redirects=True)
        client.post("/login", data={"email": "tester@gmail.com", "password": "Password123"}, follow_redirects=True)
        response = client.get("/dashboard", follow_redirects=True)
        assert b'Dashboard' in response.data

def test_add_task_button(client):
    client.post("/register",data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},follow_redirects=True)
    response = client.post("/login",data={"email": "tester@gmail.com", "password": "Password123"},follow_redirects=True)
    assert b'Add A Task' in response.data

def test_add_task_button(client):
    client.post("/register",data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},follow_redirects=True)
    response = client.post("/login",data={"email": "tester@gmail.com", "password": "Password123"},follow_redirects=True)
    assert b'Add A Task' in response.data

def test_add_task_succ(client):
    client.post("/register",data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},follow_redirects=True)
    response = client.post("/login",data={"email": "tester@gmail.com", "password": "Password123"},follow_redirects=True)
    response = client.post("/task/new", data={"name": "test", "message": "test", "date": "2022-05-06"},follow_redirects=True)
    assert b'Congratulations, you just created a task' in response.data

def test_edit_task_succ(client):
    client.post("/register",data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},follow_redirects=True)
    response = client.post("/login",data={"email": "tester@gmail.com", "password": "Password123"},follow_redirects=True)
    response = client.post("/task/new", data={"name": "test", "message": "test", "date": "2022-05-06"},follow_redirects=True)
    response = client.post("/task/1/edit", data={"name": "test", "message": "test", "date": "2022-05-06"},follow_redirects=True)
    assert b'Task Edited Successfully' in response.data

def test_delete_task_succ(client):
    client.post("/register",data={"email": "tester@gmail.com", "password": "Password123", "confirm": "Password123"},follow_redirects=True)
    response = client.post("/login",data={"email": "tester@gmail.com", "password": "Password123"},follow_redirects=True)
    response = client.post("/task/new", data={"name": "test", "message": "test", "date": "2022-05-06"},follow_redirects=True)
    response = client.post("/task/1/delete",follow_redirects=True)
    assert b'Task Deleted' in response.data
