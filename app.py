from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import data_processing 


app = Flask(__name__)
# configures the database to be used
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# our class here is used for the ID name
# it is basically a table to be used for the flask website

class Todo(db.Model):
    # this is a column with it being an integer and the primary key of the table
    id = db.Column(db.Integer, primary_key=True)
# column for names
    name = db.Column(db.String(50), nullable=True)
# column for comments
    comments = db.Column(db.Text, nullable=True)
# this tells us when each column is created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
# all instances of class are defined as strings
    def __repr__(self):
        return '<Task %r>' % self.id
    
with app.app_context():
    db.create_all()

# Set 'home.html' as the new root homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        leaid = request.form['leaid']
        enrollment_data, district_totals_data, district_percentages_data = data_processing.load_data(leaid)
        ap_enrollment_data, district_ap_totals_data = data_processing.load_ap_data(leaid, district_totals_data)
        suspension_data, district_suspension_totals_data = data_processing.load_suspension_data(leaid, district_totals_data)
        return render_template('results.html', enrollment_data=enrollment_data, ap_data=ap_enrollment_data, suspension_data=suspension_data)
    return render_template('home.html')

    
    
@app.route('/about')
def about():
    return render_template('about.html')
# post and get methods refer to the HTTP methods used to send and receive data from a web server
@app.route('/sources')
def sources():
    return render_template('sources.html')
# methods POST and GET can be handled by the index function
@app.route('/index', methods=['POST', 'GET'])
def index():
    # first checks if the method is POST
    if request.method == 'POST':
        # extracts data from name
        sub_name = request.form['name']
        sub_comments = request.form['comments']
        # creates a new 'Todo' submission
        new_sub = Todo(name=sub_name, comments=sub_comments)

        try:
            # tries to add to new submission and commit the transaction
            db.session.add(new_sub)
            db.session.commit()
            # if submission is useful, redirects user to the homepage
            return redirect('/index')
        except:
            # else notifies user of error
            return 'There was an issue adding your submission'
    else:
        # retrieve tasks and orders by most newest
        subs = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', subs=subs)
    

# this part is about deleting an ID from the table
@app.route('/delete/<int:id>')
def delete(id):
    # retrieves submission to be deleted else it returns 404
    sub_to_delete = Todo.query.get_or_404(id)

    try:
        # commands tells database session to prepare to delete
        db.session.delete(sub_to_delete)
        # commits transaction, removing task from database
        db.session.commit()
        # redirected towards the homepage once sub is deleted
        return redirect('/index')
    except:
        # will notify user if they failed to delete the submission
        return 'There was a problem deleting that task'
    
# specifically designed to update any submission again taking in both GET and POST methods
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # once again, the submission must exist or else returns 404
    sub = Todo.query.get_or_404(id)
    # if method is POST, it knows that the submission was updated
    if request.method == 'POST':
        # new value is updated through the form
        sub.name= request.form['name']
        sub.comments = request.form['comments']
        try:
            # commits changes to the database
            db.session.commit()
            # returns to homepage if successful
            return redirect('/index')
        except:
            # if problem during commit, notifies the user
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', sub=sub)

   # new commit 
if __name__ == "__main__":
    app.run(debug=True)