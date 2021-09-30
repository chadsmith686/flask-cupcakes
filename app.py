from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "secret"

connect_db(app)

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON with all cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON about one particular cupcake"""
    cc = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cc.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake, and returns the JSON of that cupcake"""
    
    new_cc = Cupcake(
        flavor=request.json['flavor'],
        size=request.json['size'],
        rating=request.json['rating'],
        image=request.json['image' or None]
    )

    db.session.add(new_cc)
    db.session.commit()
    return (jsonify(cupcake=new_cc.serialize()), 201)