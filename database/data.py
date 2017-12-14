import pickle
import re

try:
	data = pickle.load(open('database/data.dat', 'rb'))
except:
	data = {
		1:{
			"материал":"М01",
			"тип":"d=57",
			"кол-во":"7м",
			"есть/закуп":"есть",
			"автор заказа":{
				"ФИО":"Иванов",
				"Т/Н":"1"
			},
			"дата заказа":"2017.12.11",
		},
		11:{
			"материал":"М01",
			"тип":"d=22",
			"кол-во":"5м",
			"есть/закуп":"нет",
			"автор заказа":{
				"ФИО":"Иванов",
				"Т/Н":"1"
			},
			"дата заказа":"2017.11.1",
		},
		111:{
			"материал":"М01",
			"тип":"d=22",
			"кол-во":"7м",
			"есть/закуп":"нет",
			"автор заказа":{
				"ФИО":"Пертов",
				"Т/Н":"1"
			},
			"дата заказа":"2017.11.11",
		},
	}
	pickle.dump(data, open('database/data.dat', 'wb'))

def filter(db = {}, _filter = {}):
	rez = {}
	for key in db:
		accept = len(_filter)
		for field in _filter:
			_str = _filter[field].strip()
			_re = r'.*(%s).*' % _str
			print(field, type(_str), _re, accept)
			if _str != '' and re.match(_re, str(db[key][field])):
				accept -= 1
		print (accept)
		if accept == len(_filter):
			rez.update({key:db[key]})
	return rez
