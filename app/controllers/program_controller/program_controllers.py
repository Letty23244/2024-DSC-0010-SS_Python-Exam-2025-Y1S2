from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST,   HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR
from app.models.program_model import Program
from app.extensions import db



# programs Blueprint
programs = Blueprint('programs',__name__, url_prefix='/api/v1/programs')

#Creating a program
@programs.route('/create', methods =['POST'])
def createProgram():
    
    #Storing Request Values
    data = request.json
    name_of_program = data.get('name')
    duration = data.get('duration')
    semester = data.get('semester')
    

    #Validation of the incoming requests

    if not name_of_program or not duration or not semester  :
        return jsonify({
            'error':"All Fields are required"
        }),HTTP_400_BAD_REQUEST
    
    if Program.query.filter_by(name_of_program=name_of_program).first() is not None:
        return jsonify({
            'error':'name of the program  is already in  use'
        }),HTTP_409_CONFLICT
    
    try:
        # Creating a new program
        new_program = Program(
            name_of_program=name_of_program,
            duration=duration,
            semester=semester
            
        )
        db.session.add(new_program)
        db.session.commit()

        Program_name = new_program.get_full_name()

        return jsonify({
            'message': Program_name + 'has been successfully created',
            'program':{
                'id': new_program.id,
                'first_name':new_program.name_of_program,
                'last_name':new_program.duration,
                'contact':new_program.semester
            }
        }),HTTP_201_CREATED
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR
    



       # Update the programs
@programs.route('/edit/<int:id>', methods =['PUT', 'PATCH'])
def updateprograms(id):

    try:

        data = request.get_json()
        programs = Program.query.get(id)

        if not Program :
            return jsonify ({
                'error':"program not found"
            }),HTTP_404_NOT_FOUND
        
        programs.name = data.get('name', programs.name)
        programs.semester = data.get('schedule', programs.semester)
        programs.duration = data.get('course_unit', programs.duration)
       

        db.session.commit()

        return jsonify({
            'message': f"The courses id of {id} is updated successfully",
            'program':{
                'id': programs.id,
                'name':programs.name,
                'duration': programs.duration,
                'semester': programs.semester,
                
            }
        }), HTTP_200_OK
    
    except Exception as e:
        return jsonify ({
            'error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR