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

	def _make_hfooter(self, _element = 'header', _button = "Фильтр"):
		for key in self._get_data_keys():
			input_el = self.soup.new_tag("input", name_=key, placeholder=key)
			self.soup.find(_element).append(input_el)
		input_el = self.soup.new_tag("input", type="button", value=_button)
		self.soup.find(_element).append(input_el)

	def _make_table(self, **kwargs):
		_table = self.soup.new_tag("table")
		_thead = self.soup.new_tag("thead")
		_tr = self.soup.new_tag("tr")
		for key in self._get_data_keys():
			_tr.append(BS('<th>%s</th>' % key).th)
		_thead.insert(0,_tr)
		_tbody = self.soup.new_tag("tbody")
		for item_key in self.data.keys():
			_tr = self.soup.new_tag("tr")
			for key in self._get_data_keys():
				_tr.append(BS('<td>%s</td>' % self.data[item_key][key]).td)
			_tbody.append(_tr)
		_table.append(_thead)
		_table.append(_tbody)
		self.soup.find('article').insert(0,_table)

	def _insert_data(self):
		self._make_hfooter('header')
		self._make_table()
		self._make_hfooter('footer', 'Добавить')
