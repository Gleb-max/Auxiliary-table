from data.jobs import Job
from data import db_session
from data.users import User
from forms.job import JobForm
from forms.login import LoginForm
from data.constants import DB_NAME
from werkzeug.exceptions import abort
from forms.register import RegisterForm
from data.departments import Department
from forms.department import DepartmentForm
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_required, logout_user, current_user, login_user


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_KEY"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def all_jobs():
    session = db_session.create_session()
    jobs = []
    if current_user.is_authenticated:
        jobs = session.query(Job)
    return render_template("index.html", jobs=jobs)


@app.route("/departments")
def all_departments():
    session = db_session.create_session()
    departments = []
    if current_user.is_authenticated:
        departments = session.query(Department)
    return render_template("departments.html", departments=departments)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html",
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", title="Регистрация",
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template("register.html", title="Регистрация",
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect("/")
    return render_template("register.html", title="Register", form=form)


@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Job()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.department_id = form.department.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        current_user.jobs.append(job)
        session.merge(current_user)
        session.commit()
        return redirect("/")
    return render_template("addjob.html", title="Adding a Job", form=form)


@app.route("/jobs/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    form = JobForm()
    if request.method == "GET":
        session = db_session.create_session()
        job = session.query(Job).filter(
            Job.id == job_id, ((Job.leader == current_user) | (current_user.id == 1))
        ).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.department.data = job.department_id
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        job = session.query(Job).filter(
            Job.id == job_id, ((Job.leader == current_user) | (current_user.id == 1))
        ).first()
        if job:
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.department_id = form.department.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            session.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("addjob.html", title="Edit a Job", form=form)


@app.route("/job_delete/<int:job_id>", methods=["GET", "POST"])
@login_required
def job_delete(job_id):
    session = db_session.create_session()
    job = session.query(Job).filter(
        Job.id == job_id, ((Job.leader == current_user) | (current_user.id == 1))
    ).first()
    if job:
        session.delete(job)
        session.commit()
    else:
        abort(404)
    return redirect("/")


@app.route("/add_department", methods=["GET", "POST"])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief_id = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        session.add(department)
        session.commit()
        return redirect("/departments")
    return render_template("adddepartment.html", title="Adding a Department",
                           form=form)


@app.route("/departments/<int:department_id>", methods=["GET", "POST"])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    if request.method == "GET":
        session = db_session.create_session()
        department = session.query(Department).filter(
            Department.id == department_id, ((Department.chief == current_user) | (current_user.id == 1))
        ).first()
        if department:
            form.title.data = department.title
            form.chief.data = department.chief_id
            form.members.data = department.members
            form.email.data = department.email
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        department = session.query(Department).filter(
            Department.id == department_id, ((Department.chief == current_user) | (current_user.id == 1))
        ).first()
        if department:
            department.title = form.title.data
            department.chief_id = form.chief.data
            department.members = form.members.data
            department.email = form.email.data
            session.commit()
            return redirect("/departments")
        else:
            abort(404)
    return render_template("adddepartment.html", title="Edit a Department", form=form)


@app.route("/department_delete/<int:department_id>", methods=["GET", "POST"])
@login_required
def department_delete(department_id):
    session = db_session.create_session()
    department = session.query(Department).filter(
        Department.id == department_id, ((Department.chief == current_user) | (current_user.id == 1))
    ).first()
    if department:
        session.delete(department)
        session.commit()
    else:
        abort(404)
    return redirect("/departments")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init(DB_NAME)
    app.run()


if __name__ == "__main__":
    main()
