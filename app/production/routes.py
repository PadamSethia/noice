from flask import Blueprint
from flask import render_template, redirect, url_for, request, session, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app.production import bp
from app import db, ma
from app.production.prod_model import Production, ProductionSchema,  ProductionReportSchema, ProductionMaterialsSchema, ProductionMaterials
import json
import os
from app.utils import allowed_file
import sqlalchemy.exc
from werkzeug import secure_filename
import shutil
from pathlib import Path
from datetime import datetime

UPLOAD_FOLDER = os.path.abspath(current_app.config['UPLOAD_FOLDER'])


@bp.route('/new', methods=['GET'])
@login_required
def new_transaction():
    return render_template('production/new.html')


@bp.route('/get', methods=['GET'])
@login_required
def get_transaction():

    schema = ProductionSchema(many=True)
    mat_Schema = ProductionMaterialsSchema(many=True)
    data = Production.query.all()
    mat_data = ProductionMaterials.query.filter_by(id=1).first()
    json_data = schema.dumps(data)
    return jsonify(json_data)

@bp.route('/get/<id>', methods=['GET'])
@login_required
def get_transaction_by_id(id):

    schema = ProductionSchema(many=True)
    data = Production.query.filter_by(id = int(id))
    json_data = schema.dumps(data)
    return jsonify(json_data)

@bp.route('/get/report/<id>', methods=['GET'])
@login_required
def get_transaction_report(id):

    schema = ProductionReportSchema()
    data = Production.query.filter_by(id = int(id)).first()
    json_data = schema.dumps(data)
    return jsonify(json_data)

@bp.route('/get/last/', methods=['GET'])
@login_required
def get_transaction_last():
    try:
        data = Production.query.order_by(Production.id.desc()).first().id
        return jsonify({'new_id' : int(data+1)})
    except Exception as e:
        return jsonify({'new_id' : int(1)})
@bp.route('/delete/<id>', methods=['POST'])
@login_required
def delete_transaction(id):
    try:
        data = Production.query.filter_by(id=id)
        data.delete()
        db.session.commit()
        return jsonify({'success': 'Data Added'})
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something unexpected happened' , 'error' : str(e)})
        


@bp.route('/view/<id>', methods=['GET'])
@login_required
def view_transaction(id):
    return render_template('transaction/view.html', pp_no=id)

@bp.route('/edit/<id>', methods=['GET'])
@login_required
def edit_transaction(id):
    return render_template('transaction/edit.html', pp_no=id)


@bp.route('/update/<id>', methods=['POST'])
@login_required
def update_transaction(id):
    if request.method == 'POST':
        print(request.form)
        payload = json.loads(request.form['data'])
        print(payload)
        file = request.files

        if payload:
            try:
                trans = Production.query.filter_by(id=int(id)).first()

                if len(file) != 0:
                    file = request.files['image']
                    try:
                        if file and allowed_file(file.filename):
                            filename = secure_filename(file.filename)
                            foldertemp = os.path.join(
                                UPLOAD_FOLDER, 'transaction_report')

                            if os.path.exists(foldertemp):
                                filetemp = os.path.join(
                                    foldertemp, filename)
                                file.save(filetemp)
                                setattr(trans, 'image', filetemp)
                            else:

                                os.makedirs(foldertemp)

                                filetemp = os.path.join(
                                    foldertemp, filename)
                                file.save(filetemp)
                                setattr(trans, 'image', filetemp)
                        else:
                            return jsonify({'message': 'Image file not supported.'})

                    except KeyError as e:
                        print(str(e))
                        pass

                    except Exception as e:
                        print(str(e))

                temp_date = payload['date'].split('-')
                start_date = datetime(
                    int(temp_date[0]), int(temp_date[1]), int(temp_date[2]))
                trans.flag = payload['status']
                trans.finished_goods_code = payload['finished_goods_code']
                trans.quantity = payload['quantity']
                trans.report = payload['report']
                trans.date = start_date

                db.session.commit()

                return jsonify({'success': 'Data Added'})

            except sqlalchemy.exc.IntegrityError as e:
                print('Here' + str(e))
                db.session.rollback()
                db.session.close()
                return jsonify({'message': 'Duplicate entry for values.'})

            except Exception as e:
                print('Here' + str(e))
                db.session.rollback()
                db.session.close()
                return jsonify({'message': 'Something unexpected happened. Check logs', 'log': str(e)})
        else:
            return jsonify({'message': 'Empty Data.'})

    else:
        return jsonify({'message': 'Invalid HTTP method . Use POST instead.'})
