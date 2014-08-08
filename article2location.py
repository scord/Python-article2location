import json
import urllib2
from bs4 import BeautifulSoup
import sys

def locations():
	f = open("countries.json")
	data = json.load(f)
	return data

def subject(url):
	ls = locations()
	a = article(url)

	for l in ls:
		a = a.replace(l['name'], l['name'].replace(" ", ""))
		a = a.replace(l['capital'], l['capital'].replace(" ", ""))
		a = a.replace(l['demonym'], l['demonym'].replace(" ", ""))
		a = a.replace(l['region'], l['region'].replace(" ", ""))
		a = a.replace(l['subregion'], l['subregion'].replace(" ", ""))

		for s in l['altSpellings']:
			a = a.replace(s, s.replace(" ", ""))

	a = a.lower()

	counts = wordCount(a)

	topscore = 0
	toplocation = ""

	for x in ls:
		l = makeLowercase(x)
		score = 0

		if l['name'].replace(" ", "") in counts:
			score += 3 * counts[l['name'].replace(" ", "")]
		if l['capital'].replace(" ", "") in counts:
			score += 2 * counts[l['capital'].replace(" ", "")]
		if l['demonym'].replace(" ","") in counts:
			score += 3 * counts[l['demonym'].replace(" ","")]
		if l['region'].replace(" ", "") in counts:
			score += counts[l['region'].replace(" ", "")]
		if l['subregion'].replace(" ", "") in counts:
			score += counts[l['subregion'].replace(" ", "")]

		smallWords = ["in","is","as","to","at","be","of","it","mr","ms","by","me","my","no","mp","la","on"]

		for spelling in l['altSpellings']:
			if len(spelling) >= 2 and spelling not in smallWords:
				if spelling in counts:
					score += 2* counts[spelling.replace(" ", "")]

		if score > topscore:

			topcountry = x['name']
			topscore = score

	return topcountry

def makeLowercase(location):
	l = {}
	l['name'] = location['name'].lower()
	l['capital'] = location['capital'].lower()
	l['demonym'] = location['demonym'].lower()
	l['region'] = location['region'].lower()
	l['subregion'] = location['subregion'].lower()
	l['altSpellings'] = location['altSpellings']

	for i in range(len(l['altSpellings'])):
        l['altSpellings'][i] = l['altSpellings'][i].lower()

	return l

def wordCount(s):
	for c in set(',.[]\"\'/-'):
		s = s.replace(c, " ")
	counts = {}
	for word in s.split():
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1

	return counts

def article(url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page)
	ps = soup.find_all('p')
	text = []
	for p in ps:
		text.append(p.getText())

	text.append(soup.find('h1').getText())
	text.append(url)

	return " ".join(text)



print subject(sys.argv[1])
