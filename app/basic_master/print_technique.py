from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.basic_master import bp
from app.basic_master.model import PrintTechnique, PrintTechniqueSchema
from werkzeug import secure_filename
import shutil
from pathlib import Path
from app import db, ma
import app
import json
import config
import os
from app.utils import allowed_file
UPLOAD_FOLDER = os.path.abspath(current_app.config['UPLOAD_FOLDER'])


@bp.route('/get/print_technique', methods=['GET'])
@login_required
def get_print_technique():
    if request.method == 'GET':

        data_schema = PrintTechniqueSchema(many=True)
        data = PrintTechnique.query.all()
        json_data = data_schema.dump(data)
        return jsonify(json_data)


@bp.route('/add/print_technique', methods=['POST'])
@login_required
def add_print_technique():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        if len(payload['name']) != 0:

            check_data = PrintTechnique.query.filter_by(name=payload['name'])
            if check_data.first():
                return jsonify({'message': 'Print Technique - '+check_data.first().name+' already exists.'})
            else:
                try:
                    new_data = PrintTechnique(
                        payload['name'])

                    db.session.add(new_data)
                    db.session.commit()
                    return jsonify({'success': 'Data Added'})

                except Exception as e:
                    print(str(e))
                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/edit/print_technique', methods=['POST'])
@login_required
def edit_print_technique():
    if request.method == 'POST':
        
        payload = request.json
        if payload['name'] is not None:

            check_data = PrintTechnique.query.filter_by(
                name=payload['name']).first()
            if check_data and check_data.name != payload['name']:
                return jsonify({'message': 'Print Technique - '+check_data.name+' already exists.'})
            else:
                try:
                    new_data = PrintTechnique.query.filter_by(
                        id=payload['id']).first()
                    new_data.name = payload['name']
                    db.session.commit()
                    return jsonify({'success': 'Data Updated'})

                except Exception as e:
                    print(str(e))

                    db.session.rollback()
                    db.session.close()
                    return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})


@bp.route('/delete/print_technique', methods=['POST'])
@login_required
def delete_print_technique():
    if request.method == 'POST':
        payload = request.json
        check_data = PrintTechnique.query.filter_by(id=payload['id'])
        if check_data.first():

            try:
                check_data.delete()
                db.session.commit()
                return jsonify({'success': 'Data deleted'})
            except Exception as e:
                db.session.rollback()
                db.session.close()
                return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
            # else:
            #     return jsonify({'message': 'Cannot delete data. Being used by other master.'})

        else:
            return jsonify({'message': 'Data does not exist.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})