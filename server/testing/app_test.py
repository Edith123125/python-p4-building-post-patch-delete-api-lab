import json
from os import environ
import re

from flask import request

from app import app
from models import db, Bakery, BakedGood

class TestApp:
    '''Flask application in flask_app.py'''

    def test_creates_baked_goods(self):
        '''can POST new baked goods through "/baked_goods" route.'''

        with app.app_context():
            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if af:
                db.session.delete(af)
                db.session.commit()

            response = app.test_client().post(
                '/baked_goods',
                json={  # Use JSON payload
                    "name": "Apple Fritter",
                    "price": 2,
                    "bakery_id": 5,
                }
            )

            af = BakedGood.query.filter_by(name="Apple Fritter").first()

            assert response.status_code == 201  
            assert response.content_type == 'application/json'
            assert af is not None
            assert af.id

    def test_updates_bakeries(self):
        '''can PATCH bakeries through "/bakeries/<int:id>" route.'''

        with app.app_context():
            mb = Bakery.query.filter_by(id=1).first()
            if not mb:
                mb = Bakery(name="ABC Bakery")
                db.session.add(mb)
                db.session.commit()

            response = app.test_client().patch(
                f'/bakeries/{mb.id}',
                json={  # Use JSON format
                    "name": "Your Bakery",
                }
            )

            updated_mb = db.session.get(Bakery, mb.id) 

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert updated_mb.name == "Your Bakery"

    def test_deletes_baked_goods(self):
        '''can DELETE baked goods through "/baked_goods/<int:id>" route.'''

        with app.app_context():
            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if not af:
                af = BakedGood(
                    name="Apple Fritter",
                    price=2,
                    bakery_id=5,
                )
                db.session.add(af)
                db.session.commit()

            response = app.test_client().delete(f'/baked_goods/{af.id}')

            deleted_af = db.session.get(BakedGood, af.id)  

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert deleted_af is None  
