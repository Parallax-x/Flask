from flask import Flask, jsonify, request
from flask.views import MethodView
from pydantic import ValidationError
from models import Session, Advert
from sqlalchemy.exc import IntegrityError
from schema import CreateAdvert, UpdateAdvert

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.message})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def validate_json(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


def get_advert_by_id(advert_id: int):
    advert = request.session.get(Advert, advert_id)
    if advert is None:
        raise HttpError(404, "advert not found")
    return advert


def add_advert(advert: Advert):
    try:
        request.session.add(advert)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "advert already exists")


class AdvertView(MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, advert_id):
        advert = get_advert_by_id(advert_id)
        return jsonify(advert.dict)

    def post(self):
        json_data = validate_json(CreateAdvert, request.json)
        advert = Advert(**json_data)
        add_advert(advert)
        return jsonify(advert.dict)

    def patch(self, advert_id):
        advert = get_advert_by_id(advert_id)
        json_data = validate_json(UpdateAdvert, request.json)
        for field, value in json_data.items():
            setattr(advert, field, value)
        add_advert(advert)
        return jsonify(advert.dict)

    def delete(self, advert_id):
        advert = get_advert_by_id(advert_id)
        self.session.delete(advert)
        self.session.commit()
        return jsonify({'status': 'deleted'})


advert_view = AdvertView.as_view("advert_view")

app.add_url_rule("/advert/", view_func=advert_view, methods=["POST"])
app.add_url_rule("/advert/<int:advert_id>/", view_func=advert_view, methods=["GET", "PATCH", "DELETE"])

if __name__ == '__main__':
    app.run()
