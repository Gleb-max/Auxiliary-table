from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField("Job Title", validators=[DataRequired()])
    team_leader = IntegerField("Team Leader Id", validators=[DataRequired()])
    work_size = FloatField("Work Size", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    # start_date = DateField("Начало")
    # end_date = DateField("Окончание")
    department = IntegerField("Department", validators=[DataRequired()])
    category_id = IntegerField("Category Id", validators=[DataRequired()])
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField("Submit")
