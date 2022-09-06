from app import app
from models.Employee import employeeList,insertEmployee,updateEmployee,deleteEmployeeOp
from flask import jsonify, request,g
from flask_expects_json import expects_json
from jsonschema import ValidationError
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager

jwt = JWTManager(app)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
    },
    'required': ['name','email', 'password']
}

def getEmployees():
    """ calling Employee model for list of employees
        :Returns:
            - Return list of employees in JSON format
    """       
    try:    
        list = employeeList() 
    except Exception as e:
        return jsonify('Something went wrong'), 200
    else:
        return jsonify(list), 200        

@expects_json(schema)
def addOrUpdateEmployee():
    """ Preparing update or insert operation for Employee and calling model function
        :Returns:
            - Insert or update operation status
    """        
    _json = request.json
    if 'employee_id' in _json:
        employee_id = _json['employee_id']
        if employee_id and request.method == 'POST':
            try:                
                status = updateEmployee(_json)
            except:
                resp = jsonify('Employee update failed')
                resp.status = 200                            
            else:
                if status == True:
                    resp = jsonify('Employee updated successfully!')
                    resp.status = 200
                else:
                    resp = jsonify('Employee update failed')
                    resp.status = 200                
        else:
            return not_found()
    else:
        if request.method == 'POST':
            try:                
                status = insertEmployee(_json)
            except:
                resp = jsonify('Employee adding failed')
                resp.status = 200
            else:                
                if status == True:
                    resp = jsonify('Employee added successfully')
                    resp.status = 200
                else:
                    resp = jsonify('Employee adding failed')
                    resp.status = 200
        else:
            return not_found()
    return resp
    
def deleteEmployee():
    """ Preparing delete operation for Employee and calling model function
        :Returns:
            - Delete operation status
    """            
    _json = request.json
    employee_id = _json['employee_id']
    if employee_id and request.method == 'POST':        
        try:
            status = deleteEmployeeOp(_json)
        except:
            resp = jsonify('Employee delete failed')
            resp.status = 200
        else:            
            if status == True:
                resp = jsonify('Employee deleted successfully!')
                resp.status = 200
            else:
                resp = jsonify('Employee delete failed')
                resp.status = 200
    else:
        return not_found()
    return resp

@app.errorhandler(404)
def not_found(error=None):
    """ Invalid URL error handler for API
        :Returns:
            - Status and Message in json format
    """                
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(400)
def bad_request(error):
    """ Invalid Request Params error handler for create or update operation
        :Returns:
            - Status and Message in json format
    """                    
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return jsonify({'message': original_error.message})
    # handle other "Bad Request"-errors
    return error