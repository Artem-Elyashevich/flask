from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

ex = Flask(__name__, template_folder='templates')

ex.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog1.db'
ex.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ex.app_context().push()

database = SQLAlchemy(ex)

class Users(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100))

    def __repr__(self):
        return f"User {self.name}"

@ex.route('/base', methods=["POST", "GET"])
def main():
    if request.method == 'POST':
        try:
            print("Post")
            name = request.form['name']
            user = Users(name)
            print(f"{name}\n")


            database.session.add(user)
            database.commit()

            print("End post")
        except:
            #database.session.rollback()
            print('Error')
    return render_template('base.html')

if __name__ == "__main__":
    database.init_app(ex)
    with ex.app_context():
        database.create_all()
    ex.run(debug=True)