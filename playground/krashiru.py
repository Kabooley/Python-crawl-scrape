"""
セッションの維持方法:
	ms_main(): mechanicalsoup.StatefulBrowser()でステートフルブラウザでの操作
	rq_main(): RequestsのCoockieセッション
認証情報
スクレイピング

"""
import os
import logging

import mechanicalsoup
import requests

URL = "https://accounts.kurashiru.com/accounts/v1/login?client_key=R5Punhzan6JIHL7zIOXV&return_to=https%3A%2F%2Fwww.kurashiru.com%2Fkurashiru_idp_callback"

def ms_main():
	browser = mechanicalsoup.StatefulBrowser()
	browser.open(URL)
	
	# logged in?
	assert 'accounts/v1/login?' in browser.get_url()


	"""
	form要素は一つしかない模様
	"form.SessionsNew-form"

	その要素の子要素以下に、
	"input#login_email", "input#login_password"
	"""

	browser.select_form('form.SessionsNew-form')

	# めんどくなった～
	# なんてことはなく、結局要素のidかclass名かnameなどで指定することになるので
	# とくに真新しさは感じなかったな～
	"""
	>>> import mechanicalsoup
	>>> browser = mechanicalsoup.StatefulBrowser()
	>>> browser.open("https://accounts.kurashiru.com/accounts/v1/login?client_key=R5Punhzan6JIHL7zIOXV&return_to=https%3A%2F%2Fwww.kurashiru.com%2Fkurashiru_idp_callback")
	<Response [200]>

	>>> browser.url
	'https://accounts.kurashiru.com/accounts/v1/login?client_key=R5Punhzan6JIHL7zIOXV&return_to=https%3A%2F%2Fwww.kurashiru.com%2Fkurashiru_idp_callback'

	>>> browser.select_form('form.SessionsNew-form')
	<mechanicalsoup.form.Form object at 0x7f3110afb700>
	>>> browser['login[email]'] = ""
	>>> browser['login[password]'] = ""

	>>> browser.submit_selected()
	<Response [200]>
	"""

# Requestsを使ってCookieセッションを維持する方法でログイン状態を維持するのを試してみる
def rq_main():
	cookie_name = "session_id"
	s = requests.session()
	login_data = {
		"email": "",
		"password": ""
	}

	res = s.post('https://accounts.kurashiru.com/accounts/v1/login?client_key=R5Punhzan6JIHL7zIOXV&return_to=https%3A%2F%2Fwww.kurashiru.com%2Fkurashiru_idp_callback', data = login_data)
	res.raise_for_status()

	