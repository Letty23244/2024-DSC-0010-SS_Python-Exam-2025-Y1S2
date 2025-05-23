from flask import Blueprint, request, jsonify

from app.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT ,HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from app.models.course import Course
from app.extensions import db

# course Blueprint
courses = Blueprint('courses',__name__, url_prefix='/api/v1/courses')

#Creating a student
@courses.route('/create', methods =['POST'])
def createCourse():
    
    #Storing Request Values
    data = request.json
    nameOfCourse = data.get('nameofcourse')
    schedule = data.get('schedule')
    course_unit = data.get('course_unit')
    

    #Validation of the incoming requests

    if not nameOfCourse or not schedule or not course_unit  :
        return jsonify({
            'error':"All Fields are required"
        }),HTTP_400_BAD_REQUEST
    
    if Course.query.filter_by(nameOfCourse=nameOfCourse).first() is not None:
        return jsonify({
            'error':'name of the course   is already in  use'
        }),HTTP_409_CONFLICT
    
    try:
        # Creating a new course
        new_course = Course(
            nameOfCourse=nameOfCourse,
            schedule=schedule,
            course_unit=course_unit
            
        )
        db.session.add(new_course)
        db.session.commit()

        Program_name = new_course.get_full_name()

        return jsonify({
            'message': Program_name + 'has been successfully created',
            'course':{
                'id': new_course.id,
                'nameofcourse':new_course.nameOfCourse,
                'schedule':new_course.schedule,
                'course_unit':new_course.course_unit
            }
        }),HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    
  