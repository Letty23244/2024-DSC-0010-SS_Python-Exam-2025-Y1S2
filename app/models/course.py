from app.extensions import db

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key= True)
    nameOfCourse = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    course_unit = db.Column(db.String(50), nullable=False)

   

    # foriegn key 
    Program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    
    def __init__(self, name_of_course, Schedule, Course_unit):
        self.nameOfCourse = name_of_course
        self.schedule = Schedule
        self.course_unit = Course_unit
       

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"