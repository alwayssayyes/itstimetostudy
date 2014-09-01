from flask import render_template, request, session, url_for, redirect, jsonify

from datetime import datetime
from time import time
from app import app, facebook
import pusher


# app.secret_key = 'development key'

# @app.route('/')
# def start():
# 	return redirect(url_for('loginn'))

# @app.route('/loginn')
# def loginn():
# 	return facebook.authorize(callback=url_for('facebook_authorized', next=request.args.get('next') or request.referrer or None, _external=True))

# @app.route('/login/authorized')
# @facebook.authorized_handler
# def facebook_authorized(resp):
# 	if resp is None:
# 		return 'Access denied: reason=%s error=%s' % (
# 			request.args['error_reason'],
# 			request.args['error_description']
# 		)
# 	session['oauth_token'] = (resp['access_token'], '')
# 	me = facebook.get('/me')
# 	return str(me.data)

# @facebook.tokengetter
# def get_facebook_oauth_token():
# 	return session.get('oauth_token')

@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	if 'id' in request.form:
		id = request.form.get('id')
		session['username']= id
		data = {'success':True, 'msg':'login success!!'}
		return jsonify(data)
	else:
		return jsonify(success=False)

@app.route('/pusher/auth', methods=['POST'])
def push_auth():
	p = pusher.Pusher(
  		app_id='86075',
  		key='62d7b66cdbddfe53f2fa',
  		secret='21652834c633831866be'
	)

	socket_id = request.form.get('socket_id')
	channel_name = request.form.get('channel_name')
	username = session['username']

	channel_data = {'user_info' : {'username' :username}}
	channel_data['user_id'] = username
	response = p[channel_name].authenticate(socket_id,channel_data)

	return jsonify(response) 

@app.route('/send_msg', methods = ['POST'])
def send():
	p = pusher.Pusher(
	  app_id='86075',
	  key='62d7b66cdbddfe53f2fa',
	  secret='21652834c633831866be'
	)

	
	msg = request.form.get('msg_data')
	t = time()
	st = datetime.fromtimestamp(t).strftime('%Y-%m-%d %H-%M-%S')
	username = session['username']
	
	
	p['presence-lsy'].trigger('new_msg', {"msg":msg, 'username' : username, "time":st} )

	return jsonify(success=True)
