from app.extensions import db

class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.String(20), nullable = False)
    
    def __init__(self, name, duration, semester):
        self.name = name
        self.duration = duration
        self.semester = semester

    def get_full_name(self):
        return f"{self.name} {self.semester}"



