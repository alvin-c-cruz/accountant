from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required
import json
from .models import Department
from .forms import DepartmentForm
from application.extensions import db


bp = Blueprint("department", __name__, template_folder="pages", url_prefix="/department")


@bp.route("/")
@login_required
def home():
    departments = Department.query.all()

    context = {
        "departments": departments
    }

    return render_template("department/home.html", **context)


@bp.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        form = DepartmentForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for('department.home'))

    else:
        form = DepartmentForm()

    context = {
        "form": form,
    }

    return render_template("department/form.html", **context)


@bp.route("/edit/<int:department_id>", methods=["POST", "GET"])
def edit(department_id):   
    if request.method == "POST":
        form = DepartmentForm()
        form.post(request.form)

        if form.validate_on_submit():
            form.save()
            return redirect(url_for('department.home'))

    else:
        department = Department.query.get(department_id)
        form = DepartmentForm(
            id=department.id,
            department_name=department.department_name
        )

    context = {
        "form": form,
    }

    return render_template("department/form.html", **context)


@bp.route("/delete/<int:department_id>", methods=["POST", "GET"])
def delete(department_id):   
    department = Department.query.get(department_id)
    if not department.is_related():
        db.session.delete(department)
        db.session.commit()
        flash(f"{department.department_name} has been deleted.", category="success")
    else:
        flash(f"Cannot delete {department.department_name} because it has related records.", category="error")

    return redirect(url_for('department.home'))


@bp.route("/_department_autocomplete", methods=['GET'])
def department_autocomplete():
    departments = [department.department_name for department in Department.query.order_by(Department.department_name).all()]
    return Response(json.dumps(departments), mimetype='application/json')