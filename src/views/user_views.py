#!/usr/bin/env python3
###############################################################################
# Author: Agustin Bassi
# Date: July 2020
# Copyright: Bankar
# Project: Bankar Python code challenge
# Brief: Project to test skill working with Python & REST APIs
###############################################################################

#########[ Imports ]########################################################### 

from flask import Blueprint, Response, abort, json, jsonify, request, url_for

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from ..shared.utils import Utils
from ..models.user_model import UserModel

#########[ Settings & Data ]###################################################

user_api = Blueprint('users', __name__)

#########[ Module main code ]##################################################

@user_api.route('/', methods=['GET'])
def get_all_users():
    # create response for all users
    response = {
        'users': list(map(
            lambda user: user.serialize(), UserModel.query.all()
            ))
    }
    # return the response with the status code
    return custom_response(response, 200)

@user_api.route('/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    # obtain the first user with the device_id
    user = UserModel.query.filter_by(id=user_id).first()
    # abort if no device found
    if user is None:
        return Utils.create_json_response({"error" : "not found"}, 404)
    # return the response with the status code
    return Utils.create_json_response({'user' : user.serialize()}, 200)

@user_api.route('/', methods=['POST'])
def create_user():

    def __validate_request_data():
        # at this place validates all required fields
        if  request.json is None or \
            not 'name' in request.json or \
            not 'age' in request.json:
            # TODO: Validate state as well
            return False
        
        if not Utils.validate_value(request.json['name'], allowed_types=[str], lenght=128) or \
            not Utils.validate_value(request.json['age'], allowed_types=[int], min_val=1, max_val=120):
            # TODO: Validate state as well
            return False

        return True

    # evaluates request data before to do anything
    if not __validate_request_data():
        return Utils.create_json_response({"error" : "bad request"}, 400)

    # if program reaches this section request data is OK
    user = UserModel(request.json)
    user.save()
    # return the response with the status code
    return Utils.create_json_response({'user' : user.serialize()}, 201)

@user_api.route('/<int:user_id>/', methods=['PUT'])
def update_user(user_id):

    def __validate_request_data():
        # at this place validates all required fields
        if  request.json is None or \
            (not 'name' in request.json and \
            not 'age' in request.json):
            # TODO: Validate state as well
            return False
        
        if not Utils.validate_value(request.json['name'], allowed_types=[str], lenght=128) or \
            not Utils.validate_value(request.json['age'], allowed_types=[int], min_val=1, max_val=120):
            # TODO: Validate state as well
            return False

        return True

    # obtain the first user with the device_id
    user = UserModel.query.filter_by(id=user_id).first()
    # abort if no device found
    if user is None:
        return Utils.create_json_response({"error" : "not found"}, 404)

    # evaluates request data before to do anything
    if not __validate_request_data():
        return Utils.create_json_response({"error" : "bad request"}, 400)
    
    user.update(request.json)
    # return the response with the status code
    return Utils.create_json_response({'user' : user.serialize()}, 200)

@user_api.route('/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    # obtain the first user with the device_id
    user = UserModel.query.filter_by(id=user_id).first()
    # abort if no device found
    if user is None:
        return Utils.create_json_response({"error" : "not found"}, 404)
    
    user.delete()
    # return the response with the status code
    return Utils.create_json_response({'message' : 'deleted'}, 204)

#########[ end of file ]#######################################################