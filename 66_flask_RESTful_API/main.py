from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=['GET'])
def get_random():
    if 'GET' == request.method:
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        random_id = random.randint(0, len(all_cafes))
        random_cafe = db.get_or_404(Cafe, random_id)
        return jsonify(
            id=random_cafe.id,
            name=random_cafe.name,
            map_url=random_cafe.map_url,
            img_url=random_cafe.img_url,
            location=random_cafe.location,
            seats=random_cafe.seats,
            has_toilet=random_cafe.has_toilet,
            has_wifi=random_cafe.has_wifi,
            has_sockets=random_cafe.has_sockets,
            can_take_calls=random_cafe.can_take_calls,
            coffee_price=random_cafe.coffee_price
        )


@app.route("/all", methods=['GET'])
def get_all():
    if 'GET' == request.method:
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        all_cafes_result = []
        for this_cafe in all_cafes:
            all_cafes_result.append(dict(
                id=this_cafe.id,
                name=this_cafe.name,
                map_url=this_cafe.map_url,
                img_url=this_cafe.img_url,
                location=this_cafe.location,
                seats=this_cafe.seats,
                has_toilet=this_cafe.has_toilet,
                has_wifi=this_cafe.has_wifi,
                has_sockets=this_cafe.has_sockets,
                can_take_calls=this_cafe.can_take_calls,
                coffee_price=this_cafe.coffee_price
            ))
        return jsonify(all_cafes_result)


@app.route("/search", methods=['GET'])
def search():
    search_location = request.args.get('loc')
    if 'GET' == request.method:
        all_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == search_location)).scalars().all()
        cafes_result = []
        # for cafe_id in range(len(all_cafes)):
        #     this_cafe = db.get_or_404(Cafe, cafe_id + 1)
        #     if this_cafe.location == search_location:
        for this_cafe in all_cafes:
            cafes_result.append(dict(
                id=this_cafe.id,
                name=this_cafe.name,
                map_url=this_cafe.map_url,
                img_url=this_cafe.img_url,
                location=this_cafe.location,
                seats=this_cafe.seats,
                has_toilet=this_cafe.has_toilet,
                has_wifi=this_cafe.has_wifi,
                has_sockets=this_cafe.has_sockets,
                can_take_calls=this_cafe.can_take_calls,
                coffee_price=this_cafe.coffee_price
            ))
        if not cafes_result:
            return jsonify({"error": {"Not Found": "sorry..."}})
        return jsonify(cafes_result)

# HTTP GET - Read Record


# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add():
    if "POST" == request.method:
        # db.session.add(Cafe(**request.form.to_dict()))
        db.session.add(Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            has_sockets=bool(request.form.get("has_sockets")),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        ))
        db.session.commit()
        return jsonify({"response": {"success": "added..."}})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id):
    if 'PATCH' == request.method:
        # cafe = db.get_or_404(Cafe, cafe_id, description="sorry, cafe not found")
        if cafe := db.session.get(Cafe, cafe_id):
            cafe.coffee_price = request.args.get('new_price')
            db.session.commit()
            return jsonify({"response": {"success": "added..."}}), 200
        else:
            return jsonify({"response": {"error": "sorry, cafe not found..."}}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def report_closed(cafe_id):
    if 'DELETE' == request.method:
        if "TopSecretAPIKey" == request.args.get('api_key'):
            if cafe := db.session.get(Cafe, cafe_id):
                db.session.delete(cafe)
                db.session.commit()
                return jsonify({"response": {"success": "deleted..."}}), 200
            else:
                return jsonify({"response": {"error": "sorry, cafe not found..."}}), 404
        else:
            return jsonify({"response": {"error": "sorry, wrong key..."}}), 403


if __name__ == '__main__':
    app.run(debug=True)
