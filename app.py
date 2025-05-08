import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration using environment variables
db_user = os.getenv('DB_USER', 'postgres')  # Default to 'postgres' if not set
db_password = os.getenv('DB_PASSWORD','admin')  # Default to 'admin' if not set
db_host = os.getenv('DB_HOST', 'my-postgres')  # Default to 'localhost' if not set
db_name = os.getenv('DB_NAME', 'dbuser')  # Default to 'user' if not set

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    comment = db.Column(db.String(100))

# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('full.html')  # Default route

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        comment = request.form.get('comment')
        new_user = User(name = name, comment = comment)
        db.session.add(new_user)
        db.session.commit()
        return render_template('thanks.html', content1 = name, content2 = comment)
        if not name or not comment:
            return render_template('feedback.html', error='Please fill out all fields.')
        print(f"Feedback received from {name}: {comment}")
        return render_template('feedback.html', success=True)
    return render_template('feedback.html')

# Route to list users
@app.route('/users')
def list_users():
    users = User.query.all()
    return "<br>".join([f"{user.name} ({user.comment})" for user in users])


@app.route('/guestbook', methods=['GET', 'POST'])
def guest():
    if request.method == 'POST':
        name = request.form.get('guest-name')
        email = request.form.get('guest-email')
        comment = request.form.get('guest-comment')
        return render_template('thanks.html', content1 = name, content2 = email, content3 = comment)
        if not name or not comment:
            return render_template('guest.html', error='Please fill out all fields.')
        print(f"Feedback received from {name} : {email} : {comment}")
        return render_template('guest.html', success=True)
    return render_template('guest.html')


@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
