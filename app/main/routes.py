from flask import Blueprint, render_template
from flask import render_template, redirect, url_for, request, session , jsonify
from flask_login import login_user, logout_user, current_user , login_required
from app.main import bp
from app.model import User , Role
from app import db



@bp.route('/' , methods=['GET' , 'POST'])
@bp.route('/home' , methods=['GET' , 'POST'])
@login_required
def home():
    return redirect(url_for('reports.view_reports'))


@bp.route('/overview' , methods=['GET' , 'POST'])
@login_required
def overview():
    return render_template('base/overview.html')



# # Sentry verification

# @bp.route('/debug-sentry')
# def trigger_error():
#     division_by_zero = 1 / 0
#     return render_template('base/base.html', title=('Home'))