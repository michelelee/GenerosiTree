
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Donor, Donation, Org, Campaign
# from text import send_text
import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """This is the page an org. or campaign sees after login. The organization can
    see their current stream of donations - visualized by tables/gallery style. The
    organization is able to send a text message to all users regarding stated goals."""

    return render_template('homepage.html')


@app.route('/donor_landing', methods=['POST'])
def show_donor_landing():
    """This will route the donor to the donor landing page"""
    
    return render_template('donor_landing.html')


@app.route('/org_landing', methods=['GET', 'POST'])
def show_org_land():
    org_name = Org.query.filter_by(org_name='The Org').first()
    campaign = Campaign.query.filter_by(campaign_name='Coding for Kids').first()
    return render_template('org_landing.html', org_name=org_name, 
        # campaign1=campaign1, campaign2=campaign2, campaign3=campaign3
        )



@app.route("/donations_over_time", methods = ['GET'])
def get_donations_over_time_data():

    donation_objects = Donation.query.all()

    donations = []

    for donation in donation_objects:
        a = donation.__dict__
        if '_sa_instance_state' in a:
            a.pop('_sa_instance_state')
        donations.append(a)

    donations.sort()

    return jsonify(donations = donations)

@app.route("/donations_by_demographic", methods = ['GET'])
def get_donations_by_demographic():

    donor_objects = Donor.query.all()

    donors = []

    for donor in donor_objects:
        a = donor.__dict__
        donor_id = donor.donor_id
        donations = Donation.query.filter(donor_id == donor_id).all()
        donation_amt = 0
        for donation in donations:
            donation_amt += donation.donation_amt
        a["donation_amt"] = donation_amt
        if '_sa_instance_state' in a:
            a.pop('_sa_instance_state')
        donors.append(a)

    # print donors

    return jsonify(donors = donors)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
 
    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()

