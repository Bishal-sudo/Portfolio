from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Initialize the app and database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Experience model
class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    years = db.Column(db.String(10), nullable=False)
    projects = db.Column(db.String(10), nullable=False)
    satisfaction = db.Column(db.String(10), nullable=False)

# Define the Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Home route
@app.route("/")
def home():
    experience = Experience.query.first()
    return render_template("index.html", experience=experience)

# Contact page route
@app.route("/contact")
def contact_page():
    return render_template("contact.html")

# Resume page route
@app.route("/resume")
def resume_page():
    return render_template("resume.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/blog")
def blog_page():
    return render_template("blog.html")

# Submit contact form
@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]

    contact_entry = Contact(name=name, email=email, message=message)
    db.session.add(contact_entry)
    db.session.commit()

    return render_template("submit-contact.html")

# Run the app
if __name__ == "__main__":
    # Ensure the database is created and seeded with initial data if needed
    with app.app_context():
        db.create_all()  # Create database tables
        if not Experience.query.first():
            # Add a default record if no experience data exists
            db.session.add(Experience(years="13+", projects="100+", satisfaction="99.9%"))
            db.session.commit()

      port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
