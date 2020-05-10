import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Job(SqlAlchemyBase):
    __tablename__ = "jobs"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    department_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("departments.id"), nullable=True)
    leader = orm.relation("User")
    department = orm.relation("Department")
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String)
    start_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("category.id"))
    categories = orm.relation("Category",
                              secondary="jobs_to_category",
                              backref="jobs")

    def __str__(self):
        return f"<Job> id: {self.id} team_leader: [{self.leader}] job: {self.job}"

    def __repr__(self):
        return self.__str__()
