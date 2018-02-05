from flask import Flask
from flask_restful import Resource, Api


def get_app(resources) -> Flask:
    """
    Get a configured Flask application.
    param resources: A list or dictionary of  (``Resource``, "/resource/path")
    """
    app = Flask(__name__)
    api = Api(app)

    if isinstance(resources, dict):
        resources = resources.items()
    for path, resource in resources:
        if isinstance(resource, Resource:
            app.add_resource(resource, path)
        elif isinstance()
        else:
            raise ValueError(
                f"Resource is unrecognized resource class {type(resource)}}."
            )

    return app
