import pydantic
from typing import Union
from flask import Flask, jsonify
from flask import request
from flask.views import MethodView

from models import AdvertisementModel, Session

app = Flask("app")


class HTTPError(Exception):
    def __init__(self, status_code: int, message: Union[str, list, dict]):
        self.status_code = status_code
        self.message = message


class CreateAdModel(pydantic.BaseModel):
    title: str
    description: str
    owner: str


class AdvertisementView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = session.query(AdvertisementModel).filter(AdvertisementModel.id == ad_id).first()
            if ad_id != AdvertisementModel.id:
                raise HTTPError(400, 'error')
            return jsonify({
                'id': ad.id,
                'title': ad.title,
                'created_at': ad.created_at,
                'description': ad.description,
                'owner': ad.owner,
            })

    def post(self):
        json_data = dict(request.json)
        try:
            json_data_validate = CreateAdModel(**json_data).dict()
        except pydantic.ValidationError as er:
            raise HTTPError(400, 'error')

        with Session() as session:
            ads = AdvertisementModel(**json_data_validate)
            session.add(ads)
            session.commit()
            return jsonify({
                'id': ads.id,
                'title': ads.title,
                'owner': ads.owner,
                'description': ads.description,
            })

    def delete(self, ad_id: str):
        try:
            with Session() as session:
                ad = session.query(AdvertisementModel).filter(AdvertisementModel.id == ad_id).first()
                session.delete(ad)
                session.commit()
                return jsonify({
                    'status': 'success'
                })
        except pydantic.ValidationError as er:
            raise HTTPError(400, 'error')


advertisement_view = AdvertisementView.as_view("advertisement_view")

app.add_url_rule("/advertisements", view_func=advertisement_view, methods=["POST"])
app.add_url_rule("/advertisements/<int:user_id>", view_func=advertisement_view, methods=["GET", "DELETE"])

app.run()