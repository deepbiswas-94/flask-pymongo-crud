from curses.ascii import EM
from flask import Blueprint
from controllers.EmployeeController import getEmployees,deleteEmployee,addOrUpdateEmployee

router = Blueprint('router',__name__,url_prefix='/employee')

router.route('list',methods=['GET'])(getEmployees)
router.route('delete',methods=['POST'])(deleteEmployee)
router.route('addOrUpdate',methods=['POST'])(addOrUpdateEmployee)