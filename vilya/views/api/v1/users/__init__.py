# -*- coding: utf-8 -*-

from __future__ import absolute_import
from quixote.errors import TraversalError
from vilya.views.api.utils import json_body, jsonize, http_status
from vilya.models.user import User
from vilya.views.api.utils import RestAPIUI


class UsersUI(RestAPIUI):
    _q_exports = []
    _q_methods = ['get', 'post']

    def get(self, request):
        return []

    def post(self, request):
        user = request.user
        name = request.get_form_var('name', '')
        password = request.get_form_var('password', '')
        description = request.get_form_var('description', '')
        email = request.get_form_var('email', '')
        if user:
            new_user = User.create(name=name,
                                   password=password,
                                   description=description,
                                   email=email)
            return new_user.to_dict() if new_user else {}
        return {}

    def _q_lookup(self, request, name):
        user = User.get(name=name)
        if user:
            return UserUI(user)
        raise TraversalError


class UserUI(RestAPIUI):
    _q_exports = []
    _q_methods = ['get', 'post']

    def __init__(self, user=None):
        self.user = user

    def get(self, request):
        user = self.user if self.user else request.user
        if not user:
            return {}
        return user.to_dict()

    @jsonize
    @json_body
    @http_status(201)
    def _post(self, request):
        return self.post(request)

    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        user = User.get(name=name)
        if user and user.validate_password(password):
            user.set_session(request)
            return user.to_dict()
        return {}
