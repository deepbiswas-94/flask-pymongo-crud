from bson.json_util import dumps
from flask import Flask
import json
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config.from_pyfile('../config.py')
bcryptObj = Bcrypt(app)
mongo = PyMongo(app)

def parse_json(data):
    return json.loads(dumps(data))

def employeeList():
    """ Getting a list of employees
        >>> mongo.db.employees.find()
        :Returns:
            - Return list of employees in JSON format
    """    
    employees = mongo.db.employees.find()
    test = [doc for doc in employees]
    finalResult = parse_json(test)
    return finalResult

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
        list = employeeList()
        newEmployeeId = len(list) + 1
        newData = {**data,'employee_id':newEmployeeId}
        response = mongo.db.employees.insert_one(newData)
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
    employee_exist_status = checkIfEmployeeExists({'employee_id': data['employee_id']})
    if employee_exist_status:                    
        response = mongo.db.employees.update_one(
            {'employee_id': data['employee_id']}, 
            {'$set': {'name': data['name'], 'email': data['email'], 'password': data['password']}})
        return response.acknowledged
    else:
        return False

def deleteEmployeeOp(data):
    """ Delete a Employee document 
        >>> mongo.db.employees.delete_one(id)
        :Parameters:
            - `data`:Dictionary containing id
        :Returns:
            - Return True if the delete was successful
    """        
    employee_exist_status = checkIfEmployeeExists({'employee_id': data['employee_id']})
    if employee_exist_status:        
        response = mongo.db.employees.delete_one({'employee_id': data['employee_id']})
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