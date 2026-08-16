from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from prometheus_flask_exporter import PrometheusMetrics 
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from sqlalchemy import text


app = Flask(__name__)
metrics = PrometheusMetrics(app)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)

    poster = db.Column(db.String(255))
    background = db.Column(db.String(255))

    short_description = db.Column(db.Text)
    main_thoughts = db.Column(db.Text)

    soundtrack = db.Column(db.String(255))
    snack = db.Column(db.String(255))

    scenes = db.relationship(
        "Scene",
        backref="movie",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Scene(db.Model):
    __tablename__ = "scenes"

    id = db.Column(db.Integer, primary_key=True)

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey("movies.id"),
        nullable=False
    )

    title = db.Column(db.String(200))
    image = db.Column(db.String(255))
    description = db.Column(db.Text)

@app.route('/health')
def health_check():
    try:
        db.session.execute(text('SELECT 1'))
        return "Healthy", 200
    except Exception as e:
        return f"Unhealthy: {str(e)}", 500
    
@app.route("/")
def home():

    movies = Movie.query.all()

    return render_template(
        "home.html",
        movies=movies
    )

@app.route("/add", methods=["GET", "POST"])
def add_movie():

    if request.method == "POST":

        title = request.form["title"]
        poster = request.files["poster"]
        background = request.files["background"]
        poster_filename = secure_filename(poster.filename)
        background_filename = secure_filename(background.filename)

        poster.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            poster_filename)
            )

        background.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                background_filename)
                )
        slug = (
            title.lower()
            .replace(" ", "-")
            .replace("'", "")
        )

        movie = Movie(

        title=title,

        slug=slug,

        poster=f"/static/uploads/{poster_filename}",

        background=f"/static/uploads/{background_filename}",

        short_description=request.form["description"],

        main_thoughts=request.form["thoughts"],

        soundtrack=request.form["soundtrack"],

        snack=request.form["snack"]
        )

        db.session.add(movie)
        db.session.commit()

        return redirect(
            url_for(
            "add_scene",
            movie_id=movie.id)
            )

    return render_template("add_movie.html")

@app.route("/movie/<int:movie_id>/add-scene",
           methods=["GET", "POST"])
def add_scene(movie_id):

    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":

        image = request.files["image"]

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        scene = Scene(

            movie_id=movie.id,

            title=request.form["title"],

            image=f"/static/uploads/{filename}",

            description=request.form["description"]

        )

        db.session.add(scene)

        db.session.commit()

        return redirect(
            url_for(
                "movie",
                slug=movie.slug
            )
        )

    return render_template(

        "add_scene.html",

        movie=movie

    )

@app.route("/scene/<int:id>/delete")
def delete_scene(id):

    scene = Scene.query.get_or_404(id)

    movie_slug = scene.movie.slug

    db.session.delete(scene)

    db.session.commit()

    return redirect(
        url_for(
            "movie",
            slug=movie_slug
        )
    )

@app.route("/delete/<int:id>")
def delete_movie(id):

    movie = Movie.query.get_or_404(id)

    db.session.delete(movie)

    db.session.commit()

    return redirect(url_for("home"))


@app.route("/movie/<slug>")
def movie(slug):

    movie = Movie.query.filter_by(slug=slug).first()

    if movie is None:
        return "Movie not found", 404

    return render_template(
        "movie.html",
        movie=movie,
        scenes=movie.scenes
    )


with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(
    host="0.0.0.0",
    port=5000,
    debug=True)