from app.extensions import db

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    contact = db.Column(db.String(255), nullable=False)

    # foriegn key 
    Program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    # Course_id = db.Column(db.Integer,db.Foreignkey( 'courses.id'))
    

    # Relationships
    Program = db.relationship('Program', backref='students')
    Course = db.relationship('Course', backref='students')

    def __init__(self, first_name, last_name, email, contact):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"