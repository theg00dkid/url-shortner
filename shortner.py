from flask import Flask, request, redirect, render_template, flash, render_template_string
from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

app.secret_key = b'uwu'


Base = declarative_base()


class Urls(Base):
    __tablename__ = "shortlinks"

    id = Column(Integer, Sequence("short_urls_seq"), primary_key=True)
    short_name = Column("short_name", String, unique=True)
    redirect_url = Column("redirect_url", String)


engine = create_engine("sqlite:///urls.db")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route("/<short_name>/")
def short_link(short_name):
    if short_name is not None:
        url = session.query(Urls).filter_by(short_name=short_name).first()
        if url is not None:
            return redirect(url.redirect_url)
        return redirect("/")
    return redirect("/")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        short_name = request.form["short_name"]
        redirect_url = request.form["redirect_url"]
        url = session.query(Urls).filter_by(short_name=short_name).first()
        if url is not None:
            flash("exists")
            return redirect("/")
        new_url = Urls(
            short_name=short_name,
            redirect_url=redirect_url,
        )
        session.add(new_url)
        session.commit()
        session.close()
        flash(f"{short_name}")
        return redirect("/")
    # return render_template("home.html")
    return render_template_string("""

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>URL Shortner</title>
    <script src="https://code.iconify.design/1/1.0.7/iconify.min.js"></script>
    <style>
        body, html {
  background-color: #EBECF0;
}

body, p, input, select, textarea, button {
  font-family: 'Montserrat', sans-serif;
  letter-spacing: -0.2px;
  font-size: 16px;
}

div, p {
  color: #BABECC;
  text-shadow: 1px 1px 1px #FFF;
}

form {
  padding: 16px;
  width: 320px;
  margin: 0 auto;
}

.segment {
  padding: 32px 0;
  text-align: center;
}

button, input {
  border: 0;
  outline: 0;
  font-size: 16px;
  border-radius: 320px;
  padding: 16px;
  background-color: #EBECF0;
  text-shadow: 1px 1px 0 #FFF;
}

label {
  display: block;
  margin-bottom: 24px;
  width: 100%;
}

input {
  margin-right: 8px;
  box-shadow: inset 2px 2px 5px #BABECC, inset -5px -5px 10px #FFF;
  width: 100%;
  box-sizing: border-box;
  transition: all 0.2s ease-in-out;
  appearance: none;
  -webkit-appearance: none;
}

input:focus {
  box-shadow: inset 1px 1px 2px #BABECC, inset -1px -1px 2px #FFF;
}

button {
  color: #61677C;
  font-weight: bold;
  box-shadow: -5px -5px 20px #FFF, 5px 5px 20px #BABECC;
  transition: all 0.2s ease-in-out;
  cursor: pointer;
  font-weight: 600;
}

button:hover {
  box-shadow: -2px -2px 5px #FFF, 2px 2px 5px #BABECC;
}

button:active {
  box-shadow: inset 1px 1px 2px #BABECC, inset -1px -1px 2px #FFF;
}

button .icon {
  margin-right: 8px;
}

button.unit {
  border-radius: 8px;
  line-height: 0;
  width: 48px;
  height: 48px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  margin: 0 8px;
  font-size: 19.2px;
}

button.unit .icon {
  margin-right: 0;
}

button.red {
  display: block;
  width: 100%;
  color: #AE1100;
}

.input-group {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.input-group label {
  margin: 0;
  flex: 1;
}
    </style>
</head>

<body>

<form method="POST">
  
  <div class="segment">
    <h1>URL Shortner</h1>
  </div>
  
  <label>
    <input type="text" placeholder="Link to Short" name="redirect_url" required/>
  </label>
  <label>
    <input type="text" placeholder="Short Name" name="short_name" required/>
  </label>
  <button class="red" type="submit"><i class="icon iconify" data-icon="el:link"></i> Short Link!</button>
<br>
<br>
    <div>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
        <p class=flashes>
            {% for message in messages %}
            {% if message == "exists" %}
            This short name already exists, please try another name.
            {% else %}

            <div class="segment">
                <a href="/{{ message }}" target="_blank"><button class="unit" type="button"><i class="icon iconify" data-icon="mdi:web"></i></button></a>
                <button class="unit" type="button"><i class="icon iconify" data-icon="fluent:copy-24-filled" data-inline="false"></i></button>
                <!-- <button class="unit" type="button"><i class="icon iconify" data-icon="ion-md-settings" data-inline="false"></i></button> -->
            </div>

            {% endif %}
            {% endfor %}
        </p>
        {% endif %}
        {% endwith %}
    </div>
  
</form>

</body>

</html>

        """)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
