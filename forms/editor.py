from bs4 import BeautifulSoup as BS

class EditorForm():
	def __init__(self, _data = {}):
		self.template = 'static/editor.html'
		self.error = False
		self.data = _data
		self.soup = BS(open(self.template).read())

	def __str__(self):
		self._insert_data()
		if not self.error:
			return self.soup.prettify()
		else:
			raise Exception("Непонятно!")

	def _get_data_keys(self):
		try:
			return self.data[list(self.data.keys())[0]].keys()
		except (KeyError, IndexError) as e:
			return []

	def _make_hfooter(self, _element = 'header'):
		for key in self._get_data_keys():
			input_el = BS('<input type="text" name="%s" placeholder="%s">' % (key, key)).input
			self.soup.find(_element).insert(0,input_el)
		input_el = BS('<input type="button" value="Фильтр">').input
		self.soup.find(_element).insert(0,input_el)

	def _make_table(self, **kwargs):
		_table = BS('<table>').table
		_thead = BS('<thead>').thead
		_tr = BS('<tr>').tr
		for key in self._get_data_keys():
			_tr.insert(0,BS('<th>%s</th>' % key).th)
		_thead.insert(0,_tr)
		_tbody = BS('<tbody>').tbody
		for item_key in self.data.keys():
			_tr = BS('<tr>').tr
			for key in self._get_data_keys():
				_tr.insert(0,BS('<td>%s</td>' % self.data[item_key][key]).td)
			_tbody.insert(0,_tr)
		_table.insert(0,_tbody)
		_table.insert(0,_thead)
		self.soup.find('article').insert(0,_table)
	def _insert_data(self):
		self._make_hfooter('header')
		self._make_table()
		self._make_hfooter('footer')
