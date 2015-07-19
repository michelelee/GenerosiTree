
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Donor, Donation, Org, Campaign
import json
from twilio.rest import TwilioRestClient
import twilio
import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
caller=os.environ['TWILIO_PHONE']
receiver=os.environ['GRANTEE']

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

@app.route('/go_to_org')
def go_to_org():
    """Routes to organization page."""
    return render_template('org_landing.html')
    
@app.route('/donate', methods=['POST'])
def get_donation():
    # stripe.api_key = "sk_test_frMFHRq8QkHkwAl028zWBmag"
    # if request.form['value'] == '50':
    return render_template('thank_you.html')

@app.route('/org_landing', methods=['GET', 'POST'])
def show_org_land():
    org_name = Org.query.filter_by(org_name='The Org').first()
    campaign = Campaign.query.filter_by(campaign_name='Coding for Kids').first()
    return render_template('org_landing.html', org_name=org_name, 
        # campaign1=campaign1, campaign2=campaign2, campaign3=campaign3
        )

@app.route('/message_input', methods=['POST'])
def send_text():
    try:
        body = request.form['message']
        caller=os.environ['TWILIO_PHONE']
        receiver=os.environ['GRANTEE']
        client = twilio.rest.TwilioRestClient(account_sid, auth_token)
        message = client.messages.create(body=body,
        to=receiver,
        from_=caller)
    except twilio.TwilioRestException as e:
        print e
    return render_template('org_landing.html')

# @app.route('/received_messages', methods=['POST']) 
# def receive_texts(ACCOUNT_SID=account_sid, AUTH_TOKEN=auth_token):
#     client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)   
#     message = client.messages.get('SM9ab8d5a6fd7b72387de6c869f529ccbc') 
#     text_body = message.body
#     print text_body
#     return render_template('org_landing.html', messages="a message") 

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
    DebugToolbarExtension(app)

    app.run()
