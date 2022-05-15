
from flask import render_template, request
import flask
from openvpn import app
from flask_login import login_required, current_user

import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
import googleapiclient.discovery

import redis as redis
from rq import Queue

from openvpn.tasks import initiate_vpn
from openvpn.googleapi import get_project, create_instance , reserve_static_ip,get_reserved_ip,list_reserveds,insert_firewall_rule

r = redis.Redis()
q = Queue(connection=r)


@app.route('/')
def index():
    print(app.config['ENV'])
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/vpn/<desired_project_id>')
def vpn(desired_project_id = 'example-project-id-123'):

    if 'credentials' not in flask.session:
        return flask.redirect('oauth.authorize')

    print(flask.session['credentials'])

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])


    job = q.enqueue(initiate_vpn, credentials , desired_project_id)

    return "the task is running to create project"


@app.route('/get_project')
def project():


    if 'credentials' not in flask.session:
        return flask.redirect('oauth.authorize')


    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])


    get_project(credentials)
    create_instance(credentials)
    return "An instance created"

@app.route('/reserve_ip')
def reserve_ip():

    if 'credentials' not in flask.session:
        return flask.redirect('oauth.authorize')


    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])


    reserve_static_ip(credentials)
    return "One ip is reserved"

@app.route('/get_reserved_ip')
def get_reversed_ip():

    if 'credentials' not in flask.session:
        return flask.redirect('oauth.authorize')


    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])


    get_reserved_ip(credentials)
    return "got reserved ip"

@app.route('/list_reserved_ips')
def list_reserved_ips():

    if 'credentials' not in flask.session:
        return flask.redirect('oauth.authorize')


    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])


    list_reserveds(credentials)
    return "got reserved ip"

@app.route('/insert_firewallrule')
def insert_firewallrule():

    if 'credentials' not in flask.session:
        return flask.redirect('oauth.authorize')


    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])


    insert_firewall_rule(credentials)
    return "firewall rule inserted"

