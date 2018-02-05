"""
tpk_web.resources.rest - This package contains all the REST API views.

These views are designed for starting up, or making singular interactions
with the database. Anything requiring polling or fast updates should be
implemented with WebSockets in ``wsocket`` module.
"""
from functools import wraps
from typing import Dict

from flask import request
from flask_restful import marshal, marshal_with, Resource
from flask_sqlalchemy import Model
from werkzeug.exceptions import BadRequest, NotFound

from tpk_web.database import db


def json_data(func):
    """
    Take the incoming ``request.json`` and put it into the handler kwargs.

    Raises ``BadRequest`` if no json is found or the content is bad.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        # We only support JSON, so if we don't find any in the incoming request
        # a BadRequest is returned when force=True is passed to ``get_json``.
        request_json = request.get_json(force=True)

        kwargs['data'] = request_json
        return func(*args, **kwargs)

    return wrapped


class CreateViewAllResource(Resource):
    """
    Resource designed to create a new resource in the backend,
    or view all resources of a certain type.

    Accepts HTTP GET, and POST.
    """
    @property
    def db_model(self) -> Model:
        """
        The database model containing the requested data, or incoming data.
        """
        raise NotImplementedError

    @property
    def marshal_incoming(self) -> Dict:
        """
        A Mapping of field names represented as strings and flask_restful.fields
        """
        raise NotImplementedError

    @property
    def marshal_outgoing(self) -> Dict:
        """
        A Mapping of field names represented as strings and flask_restful.fields
        """
        raise NotImplementedError

    @marshal_with(marshal_outgoing)
    def get(self):
        """
        Return all instances (rows) of ``self.db_model``.
        This returns a list of ``self.db_model`` serialized as JSON objects.
        """
        return self.db_model.query.all()

    @json_data
    def post(self, data=None):
        """
        Create a new instance of ``self.db_model``.
        This effectively inserts a new row.

        :param data: An object representing ``db_model`` deserialized from JSON.
        """
        new_model = self.db_model(marshal(data, self.marshal_incoming))

        db.session.add(new_model)
        db.session.commit()


class UpdateViewSingleResource(Resource):
    """
    Resource designed to update a single resource in the backend,
    or view that resource of a certain type.

    Accepts HTTP GET, PUT, and DELETE.
    """
    @property
    def db_model(self) -> Model:
        """
        The database model containing the requested data, or incoming data.
        """
        raise NotImplementedError

    @property
    def marshal_incoming(self) -> Dict:
        """
        A Mapping of field names represented as strings and flask_restful.fields
        """
        raise NotImplementedError

    @property
    def marshal_outgoing(self) -> Dict:
        """
        A Mapping of field names represented as strings and flask_restful.fields
        """
        raise NotImplementedError

    @marshal_with(marshal_outgoing)
    def get(self, model_id):
        """
        Return an instance (row) of ``self.db_model`` with the id ``model_id``.

        :param model: The database row ID.
        """
        return self.db_model.query.get(model_id)

    # TODO: What if we want to perform actions, other than updating the model?
    @json_data
    def put(self, model_id, data=None):
        """
        Update an instance of ``self.db_model``.

        :param model: The database row ID.
        :param data: An object representing ``db_model`` deserialized from JSON.
        """
        model_to_update = self.db_model.query.get(model_id)
        for field, value in marshal(data, self.marshal_incoming).items():
            setattr(model_to_update, field, value)

        db.session.commit()

    def delete(self, model_id):
        """
        Remove an instance of ``self.db_model``.

        :param model: The database row ID.
        """
        model_instance = self.db_model.get(model_id)
        if model instance is not None:
            model_instance.delete()
            db.session.commit()

        else:
            raise NotFound()


# Register resources here, if you want to use it in the aggregated resources.
registered_resources = {

}
