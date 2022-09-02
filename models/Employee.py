from app import mongo
from bson.json_util import dumps
from bson.objectid import ObjectId

def employeeList():
    """ Getting a list of employees
        >>> mongo.db.employees.find()
        :Returns:
            - Return list of employees in JSON format
    """    
    employees = mongo.db.employees.find()
    resp = dumps(employees)
    return resp

def insertEmployee(data):
    """ Insert a Employee document 
        >>> mongo.db.employees.insert_one(name,email)
        :Parameters:
            - `data`:Dictionary containing insert data
        :Returns:
            - Return True if operation succeeded
    """
    employee_exist_status = checkIfEmployeeExists({'email': data['email']})
    if not employee_exist_status:                
        response = mongo.db.employees.insert_one(data)
        return response.acknowledged
    else:
        return False

def updateEmployee(data):
    """ Update Single a Employee document 
        >>> mongo.db.employees.update_one(id,name,email)
        :Parameters:
            - `data`:Dictionary containing update data
        :Returns:
            - Return True if operation succeeded
    """    
    response = mongo.db.employees.update_one(
        {'_id': ObjectId(data['_id']['$oid']) if '$oid' in data['_id'] else ObjectId(data['_id'])}, 
        {'$set': {'name': data['name'], 'email': data['email'], 'password': data['password']}})
    return response.acknowledged

def deleteEmployeeOp(data):
    """ Delete a Employee document 
        >>> mongo.db.employees.delete_one(id)
        :Parameters:
            - `data`:Dictionary containing id
        :Returns:
            - Return True if the delete was successful
    """        
    employee_exist_status = checkIfEmployeeExists({'_id': ObjectId(data['_id'])})
    if employee_exist_status:        
        response = mongo.db.employees.delete_one({'_id': ObjectId(data['_id'])})
        return response.acknowledged
    else:
        return False

def checkIfEmployeeExists(data):
    """ Check if a Employee data exists based on parameters
        >>> mongo.db.employees.find_one(data)
        :Parameters:
            - `data`:containing search params
        :Returns:
            - Return True if data exists
    """            
    employee_exist_status = mongo.db.employees.find_one(data)
    return True if employee_exist_status!=None else False