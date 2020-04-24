from flask_restful import Resource, Api
from flask import Flask, Response, json, jsonify, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class Mahasiswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(10), unique =True)
    nama = db.Column(db.String(100))
    alamat = db.Column(db.Text(512))

    def __init__(self, nim, nama, alamat):
        self.nim = nim
        self.nama = nama
        self.alamat = alamat

    @staticmethod
    def get_all_users():
        return Mahasiswa.query.all()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'nim', 'nama', 'alamat')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/mahasiswa/", methods=["GET"])
def get_user():
    all_users = Mahasiswa.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route("/mahasiswa/<int:id>/", methods=["GET"])
def one_user(id):
    user = Mahasiswa.query.get(id)
    result = user_schema.dump(user)
    return jsonify(result)


@app.route("/mahasiswa/", methods=["POST"])
def create_user():
    if not request.json or not 'nim ' in request.json or not 'nama' in request.jsonand and not 'alamat' in request.json:
        abort(5555)

    user = Mahasiswa(request.json['nim'], request.json['nama'], request.json['alamat'])
    db.session.add(user)
    db.session.commit()

    result = user_schema.dump(user)
    return jsonify(result)


@app.route("/mahasiswa/<int:id>/", methods=["PUT"])
def update_user(id):
    if not request.json or not 'nim ' in request.json or not 'nama' in request.jsonand and not 'alamat' in request.json:
        abort(5555)

    user = Mahasiswa.query.get(id)
    user.nim = request.json['nim']
    user.nama = request.json['nama']
    user.alamat = request.json['alamat']
    db.session.commit()

    return user_schema.jsonify(user)


@app.route("/mahasiswa/<int:id>/", methods=["DELETE"])
def delete_user(id):
    user = Mahasiswa.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run()