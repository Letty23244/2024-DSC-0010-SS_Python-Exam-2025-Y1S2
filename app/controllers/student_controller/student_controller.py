
from flask import Blueprint, request, jsonify
HTTP_409_CONFLICT = 409
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from app.models.Student_model import Student
from app.extensions import db
# Student Blueprint
students = Blueprint('students',__name__, url_prefix='/api/v1/students')

#Creating a student
@students.route('/create', methods =['POST'])
def createStudent():
    
    
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    contact = data.get('contact')

    #Validation of the incoming requests

    if not first_name or not last_name or not email or not contact :
        return jsonify({
            'error':"All Fields are required"
        }),HTTP_400_BAD_REQUEST
    
    if Student.query.filter_by(email=email).first() is not None:
        return jsonify({
            'error':'Email Address is already in  use'
        }),HTTP_409_CONFLICT
    
    try:
        # Creating a new student
        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact=contact
        )
        db.session.add(new_student)
        db.session.commit()

        user_name = new_student.get_full_name()

        return jsonify({
            'message': user_name + 'has been successfully created',
            'student':{
                'id': new_student.id,
                'first_name':new_student.first_name,
                'last_name':new_student.last_name,
                'contact':new_student.contact
            }
        }),HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR

# Getting all Students
@students.get('/all')
def getAllStudents():

    try:
        all_students = Student.query.all()

        students_data = []

        for student in all_students:
            students_info ={
                'id':student.id,
                'first_name':student.first_name,
                'last_name':student.last_name,
                'email':student.email,
                'contact':student.contact
            }
            students_data.append(students_info)

        return jsonify({
            'message':"All students retrieved successfully",
            'total_students':len(students_data),
            'students':students_data
        }),HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR


# Getting student by id
@students.get('student/<int:id>')
def getStudentById(id):
    try:
        student = Student.query.filter_by(id=id).first()

        if not student:
            return jsonify({
                'error':"Student not found"
            }),HTTP_404_NOT_FOUND
        
        return jsonify({
            'message': "Student details retrieved successfully",
            'student':{
                'id': student.id,
                'first_name':student.first_name,
                'last_name':student.last_name,
                'contact':student.contact,
                'email':student.email
            }
        }),HTTP_200_OK
    
    except Exception as e:
        return jsonify({
            'error':str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
# Update the student 
@students.route('/edit/<int:id>', methods =['PUT', 'PATCH'])
def updateStudent(id):

    try:

        data = request.get_json()
        student = Student.query.get(id)

        if not student :
            return jsonify ({
                'error':"Student not found"
            }),HTTP_404_NOT_FOUND
        
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.contact = data.get('contact', student.contact)

        db.session.commit()

        return jsonify({
            'message': f"The student id of {id} is updated successfully",
            'student':{
                'id': student.id,
                'first_name':student.first_name,
                'last_name': student.last_name,
                'contact': student.contact,
                'email': student.email
            }
        }), HTTP_200_OK
    
    except Exception as e:
        return jsonify ({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    

# Delete the student
@students.route('delete/<int:id>', methods=['DELETE'])
def deleteStudent(id):
    try:
        student = Student.query.get(id)

        if not student :
            return jsonify ({
                'error':"Product not found"
            }),HTTP_404_NOT_FOUND
        else :
            # Delete associated students
            db.session.delete(student)
            db.session.commit()

            return jsonify({
                'message': "Student deleted successfully"
            }),HTTP_200_OK
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
