from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import logging

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=date.today())

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")


list = Users.query.all()


@app.route('/registration', methods=["POST", "GET"])
def blog():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        for user in list:
            if user.email == email:
                return render_template("registration.html", error="Пользователь с таким email уже существует")
            elif user.name == name:
                return render_template("registration.html", error="Пользователь с таким именем уже существует")

        try:
            u = Users(email=request.form['email'], psw=request.form['psw'], date=datetime.utcnow())
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], old=request.form['old'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
            print("Post already get ")

            return render_template("data.html")
        except Exception as e:
            print(e)
    return render_template("registration.html")


@app.route('/enter', methods=["POST", "GET"])
def enter():
    if request.method == "POST":

        try:
            email = request.form['email']
            psw = request.form['psw']

            for user in list:
                if user.email == email:
                    print(psw)
                    if user.psw == psw:
                        user_id = user.id
                        app.logger.info("User founded!" + str(user_id))
                        return redirect('/id/' + str(user_id))
                    else:
                        app.logger.info("invalid password")
                        return render_template("enter.html", err='Invalid password')

            return render_template("enter.html", err='User is not found')

        except Exception as ex:
            app.logger.error(ex)
    return render_template("enter.html")


User = Users.query.all()
Profile = Profiles.query.all()


@app.route(f'/id/<int:user_id>')
def about(user_id):
    user = User[user_id - 1]
    profile = Profile[user_id - 1]
    return render_template("id.html", name=profile.name, old=str(profile.old),
                           city=profile.city, email=user.email)


@app.route('/contacts')
def contacts():
    return render_template("contacts.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
