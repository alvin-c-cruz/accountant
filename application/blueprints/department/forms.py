from dataclasses import dataclass
from application.extensions import db
from .models import Department


@dataclass
class DepartmentForm:
    id: int = None
    department_name: str = ""

    errors = {}

    def get(self, department_id):
        department = Department.query.get(department_id)

        if department:
            self.id = department.id
            self.department_name = department.department_name

        return department
    
    def save(self):
        if self.id is None:
            # Add a new record
            new_department = Department(department_name=self.department_name)
            db.session.add(new_department)
        else:
            # Update an existing record
            department = Department.query.get(self.id)
            if department:
                department.department_name = self.department_name
        db.session.commit()
   
    def post(self, request_form):
        self.id = request_form.get('department_id')
        self.department_name = request_form.get('department_name')

    def validate_on_submit(self):
        if not self.department_name:
            self.errors["department_name"] = "Please type department name."
        else:
            existing_department = Department.query.filter(Department.department_name == self.department_name, Department.id != self.id).first()
            if existing_department:
                self.errors["department_name"] =  "Department name already exists. Please choose a different one."

        if not self.errors:
            return True
        else:
            return False        
    