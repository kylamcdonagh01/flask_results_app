from app import app, db, views, models, admin
from flask import redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
from .forms import LoginForm
from flask_admin.contrib.sqla import ModelView
from .models import User, Competitor, Race, CompetitorRace
import sqlalchemy
from datetime import date
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
login_manager = LoginManager()
import os

login_manager.init_app(app)
app.secret_key = os.getenv("SECRET_KEY", "default-secret")
app.permanent_session_lifetime = timedelta(minutes=5) #store session data for 5 minutes

class AdminModelView(ModelView):
    def is_accessible(self):
        #only the admin is allowed to access the admin page, this would be the race judges
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self, name, **kwargs):
        #redirect user to login page if theyre not authorised users
        return redirect(url_for('login'))

#separate view for CompetitorRace table so that admin can enter competitors results properly
class CompetitorRaceAdmin(ModelView): 
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    
    form_columns = ['competitor', 'race', 'result']

    column_labels = {
        'competitor': 'Competitor ID',
        'race': 'Race Number',
        'result': 'Race Result'
    }
    column_searchable_list = ['competitor.first_name', 'race.description']  #make competitor and race names searchable
    column_sortable_list = ['competitor.first_name', 'race.description', 'result']

#admin views
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Competitor, db.session))
admin.add_view(AdminModelView(Race, db.session))
admin.add_view(CompetitorRaceAdmin(CompetitorRace, db.session, name='Competitor Races'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #returns None if the ID is not valid

@app.route("/settings")
@login_required
def settings():
    pass

@app.route("/")
def home():
    home={'description':'Welcome to the Race Results application. Here you can view the competitors and their results from each race! Sign into your account see your saved races and competitors. Make sure to check the upcoming races for dates and times of your next race.'}
    return render_template("index.html", title='Home', home=home)

@app.route("/competitors")
def competitors():
    return render_template("competitors.html", competitor=Competitor.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('account')) #take user to their account page
        else:
            #errror for incorrect details
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        #errror message if theyre not logged in
        flash("You are not logged in")
        return redirect(url_for("login"))
    
@app.route("/logout")
@login_required
def logout():
    #user has the option to log out if they want to
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

@app.route('/results')
def results():
    races = Race.query.filter_by(status=True).all() #only show races that have been completed (and therfore have results)
    return render_template('results.html', races=races)

@app.route('/race/<int:race_id>/show_results')
def show_race_results(race_id):
    race = Race.query.get_or_404(race_id)
    results = CompetitorRace.query.filter_by(race_id=race_id).all()
    return render_template('race_results.html', race=race, results=results)

@app.route('/next')
def next_races():
    #querying races with a date in the future (upcoming)
    upcoming_races = Race.query.filter(Race.race_date > date.today()).all()
    return render_template('next.html', races=upcoming_races)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/save_race/<int:race_id>', methods=['POST'])
@login_required
def save_race(race_id):
    user = current_user
    race = Race.query.get(race_id)
    if race not in user.saved_races:
        user.saved_races.append(race)
        db.session.commit()
    return redirect(url_for('account'))

@app.route('/unsave_race/<int:race_id>', methods=['POST'])
@login_required
def unsave_race(race_id):
    user = current_user
    race = Race.query.get(race_id)
    if race in user.saved_races:
        user.saved_races.remove(race)
        db.session.commit()
    return redirect(url_for('account'))

@app.route('/save_competitor/<int:competitor_id>', methods=['POST'])
@login_required
def save_competitor(competitor_id):
    user = current_user
    competitor = Competitor.query.get(competitor_id)
    if competitor not in user.saved_competitors:
        user.saved_competitors.append(competitor)
        db.session.commit()
    return redirect(url_for('account'))

@app.route('/unsave_competitor/<int:competitor_id>', methods=['POST'])
@login_required
def unsave_competitor(competitor_id):
    user = current_user
    competitor = Competitor.query.get(competitor_id)
    if competitor in user.saved_competitors:
        user.saved_competitors.remove(competitor)
        db.session.commit()
    return redirect(url_for('account'))

@app.route('/competitor_results/<int:competitor_id>')
def show_competitor_results(competitor_id):
    competitor = Competitor.query.get_or_404(competitor_id)
    results = CompetitorRace.query.filter_by(competitor_id=competitor_id).all()
    return render_template('competitor_results.html', competitor=competitor, results=results)

@app.route('/results/<int:competitor_id>')
def get_results(competitor_id):
    # Fetch results for the competitor
    results = CompetitorRace.query.filter_by(competitor_id=competitor_id).all()
    return render_template('results_partial.html', results=results)

@app.errorhandler(401)
def unauthorised_error(e):
    return render_template('401.html', message="Please log in first"), 401

if __name__ == "__main__":
    app.run(debug=True)