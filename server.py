import json
import sys

from http.server import HTTPServer, BaseHTTPRequestHandler, urllib
from threading import Thread
from time import sleep
from datetime import datetime

from database.data import data as db
from database.data import filter
# from database.users import calc_hash
# from database.users import set_auth_cookies, check_auth_cookies, del_auth_cookies
#
# from exceptions import LoginError, WrongPasswordError, WrongUsernameError
#
from forms.editor import EditorForm
# from forms.loginform import LoginForm
# from forms.lostform import LostForm
# from forms.searchform import SearchForm

class SmallDBRqHandler(BaseHTTPRequestHandler):
	def _get_cookies(self):
		rez = {}
		try:
			pairs = [_.split("=") for _ in self.headers['Cookie'].split('; ')]
			for pair in pairs:
				try:
					key, value = pair
					rez.update({key:urllib.parse.unquote_plus(value)})
				except ValueError:
					pass
			return rez
		except AttributeError:
			return {}

	def _get_referer(self):
		try:
			_host = self.headers['Host']
			rez = self.headers['Referer'].split(_host)[1]
		except (KeyError, AttributeError, IndexError):
			rez = ''
		return rez

	def _get_params(self):
		rez = {}
		try:
			rez.update(urllib.parse.parse_qs(self.path.split("?")[1]))
		except IndexError:
			pass
		print(rez)
		return rez

	def _send_cookies(self, cookies = {}):
		for cookie in cookies.keys():
			self.send_header('Set-Cookie', "%s=%s" % (cookie, urllib.parse.quote_plus(cookies[cookie])))

	def _load_file(self, name, context=None, content_type='text/html', cookies = {}):
		self.send_response(200)
		self._send_cookies(cookies)
		self.send_header('Content-type', content_type)
		self.end_headers()
		data = ''
		with open(name, 'rb') as _file:
			data = _file.read()
		if context:
			for key in context:
				data = data.replace(
					bytes(key, 'utf-8'),
					bytes(context[key], 'utf-8')
				)
		self.wfile.write(data)

	def _redirect(self, url, cookies = {}):
		"""редирект клиента с опциональным выставлением куков"""
		self.send_response(302)
		self.send_header('Location', url)
		self._send_cookies(cookies)
		self.end_headers()
		self.wfile.write(bytes('data', 'utf-8'))

	def _load_str(self, data, cookies = {}):
		self.send_response(200)
		self._send_cookies(cookies)
		self.end_headers()
		self.wfile.write(bytes(str(data), 'utf-8'))

	def _to_json(self, data):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(str.encode(json.dumps(data, indent = 4)))


	def do_GET(self):
		params = self._get_params()

		if self.path.endswith('png'):
			self._load_file(self.path.lstrip('/'), content_type='image/png')
		elif self.path.endswith('jpg'):
			self._load_file(self.path.lstrip('/'), content_type='image/jpeg')
		elif self.path.startswith('/static'):
			content_type = 'text/html'
			if self.path.endswith('jpg'):
				content_type = 'image/jpeg'
			elif self.path.endswith('css'):
				content_type = 'text/css'
			self._load_file(self.path.lstrip('/'), content_type=content_type)
		elif self.path  == '/':
			self._load_str(EditorForm(db))
		elif self.path.startswith('/workers'):
		 	self._load_str('<meta charset="utf-8"><pre>%s</pre>' % (workers))
		# elif self.path.startswith('/lost'):
		# 	self.show_lost_form()
		# elif params['is_auth'] and self.path.startswith('/rpd_main'):
		# 	self.show_search_form(params)
		# elif params['is_auth'] and self.path.startswith('/logout'):
		# 	if self.path.endswith('yes'):
		# 		self._redirect('/auth/', cookies = del_auth_cookies(params['login']))
		# 	else:
		# 		self.show_confirm_form(_forward = '/logout/yes', _return = params['referer'])
		else:
			self._redirect('/auth/')

	def do_POST(self):
		data = urllib.parse.parse_qs(
			self.rfile.read(
				int(self.headers.get('content-length'))
			).decode('utf-8')
		)
		print(self.path, data, file = sys.stderr)
		if self.path.startswith('/setfilter'):
			try:
				_filter = json.loads(data['data'][0])
			except (KeyError, IndexError) as e:
				_filter = {}
			self._load_str(EditorForm(filter(db, _filter)))
		elif self.path.startswith('/addrecord'):
			print(db)
			try:
				_insert = json.loads(data['data'][0])
			except (KeyError, IndexError) as e:
				_insert = {}
			print('>>>>', _insert)
			db.update({222:_insert})
			print(db)
			self._load_str(EditorForm(db))

if __name__ == '__main__':
	server = HTTPServer(('0.0.0.0', 8000), SmallDBRqHandler)
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		import pickle
		pickle.dump(data, open('database/data.dat', 'wb'))
		print("\nfinished\n")
		exit(1)
