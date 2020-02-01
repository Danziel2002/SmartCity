from smartCity import app
from flask import render_template, url_for, flash, redirect, request, jsonify
from smartCity import app, db, bcrypt
from smartCity.models import User, Post, Transport
from smartCity.routes import giveExp

@app.route("/findName")
def test():
    users = []
    name = str(request.args.get('name'))
    userList = User.query.filter(User.username.contains(name)).all()
    for user in userList:
        users.append(user.username)
    return jsonify({
        'users':users,
        })


@app.route('/getTransport')
def getTransport():
    vehicleId = str(request.args.get('vehicleId'))
    vehicle = Transport.query.filter(id == vehicleId).first()
    if vehicle == None:
        return jsonify({
            'vehicle' : "There is not a vehicle with this id"
            })
    else:
        giveExp(vehicle.price * 2)
        return jsonify({
            'vehicle' : vehicle.name
            })

@app.route('/giveXpToUser')
def giveXpToUser():
    userId = str(request.args.get('userId'))
    userInstance = User.query.filter(id == userId).first()
    userInstance.giveXp()
