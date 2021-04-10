from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.secret_key = b'uwu'

db = SQLAlchemy(app)


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String(100), unique=True)
    redirect_url = db.Column(db.String(2048))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        short_name = request.form["short_name"]
        redirect_url = request.form["redirect_url"]
        url = Urls.query.filter_by(short_name=short_name).first()
        if url is not None:
            flash("exists")
            return redirect("/")
        # new_url = Urls(
        #     short_name=short_name,
        #     redirect_url=redirect_url,
        # )
        # db.session.add(new_url)
        # db.session.commit()
        flash(f"{short_name}")
        return redirect("/")
    return render_template("home.html")


@app.route("/<short_name>/")
def short_link(short_name):
    if short_name is not None:
        url = Urls.query.filter_by(short_name=short_name).first()
        if url is not None:
            return redirect(url.redirect_url)
        return render_template("error.html")
    return render_template("error.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
