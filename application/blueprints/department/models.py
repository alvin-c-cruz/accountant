from application.extensions import db


class Department(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    department_name = db.Column(db.String(255), unique=True)

    def __str__(self):
        return self.department_name
       
    def is_related(self):
        if self.transfer_ins:
            return True
        
        if self.transfer_outs:
            return True
