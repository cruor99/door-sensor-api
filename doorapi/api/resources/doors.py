from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from doorapi.models import Doors
from doorapi.extensions import ma, db
from doorapi.commons.pagination import paginate


class DoorSchema(ma.ModelSchema):
    class Meta:
        model = Doors
        sqla_session = db.session


class DoorResource(Resource):
    """
    Single door event resource
    """

    def get(self, door_id):
        schema = DoorSchema()
        event = Doors.query.get_or_404(door_id)
        return {"event": schema.dump(event).data}

    def put(self, door_id):
        schema = DoorSchema(partial=True)
        event = Doors.query.get_or_404(door_id)
        event, errors = schema.load(request.json, instance=event)
        if errors:
            return errors, 422

        return {"msg": "door event updated", "event": schema.dump(event).data}

    def delete(self, door_id):
        event = Doors.query.get_or_404(door_id)
        db.session.delete(event)
        db.session.commit()

        return {"msg": "door event deleted"}


class DoorList(Resource):
    """
    Creation and get_all of door events
    """

    def get(self):
        schema = DoorSchema(many=True)
        query = Doors.query
        return paginate(query, schema)

    def post(self):
        schema = DoorSchema()
        print(request.json)
        event, errors = schema.load(request.json)
        if errors:
            return errors, 422

        db.session.add(event)
        db.session.commit()

        return {"msg": "door event created", "event": schema.dump(event).data}, 201
