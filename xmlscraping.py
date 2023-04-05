import requests 
from bs4 import BeautifulSoup
from xml.dom import minidom
from xml.dom.minidom import getDOMImplementation
import os
import re
import string

root = minidom.Document()
impl = getDOMImplementation()
xml = root.createElement('root') 
root.appendChild(xml)
headers ={
'User-Agent':
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'}
base_url ='https://digital-aarena.com/cat/last/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1/%D9%85%D8%B4%D8%A7%D8%B1%D9%8A%D8%B9-%D8%A7%D9%84%D8%B9%D9%85%D9%84%D8%A7%D8%AA-%D8%A7%D9%84%D8%B1%D9%82%D9%85%D9%8A%D9%87/'
for page in range (1 , 339):
	pages_url = base_url + 'page/' + str(page) + '/'
	req = requests.get(pages_url)
	soup =BeautifulSoup(req.content , 'lxml')
	currency_data = soup.find_all('h2' , class_='post-title')
	links_list=[]
	print('saving page: ' + str(page))
	for item in currency_data:
		for link in item.find_all('a' ,href =True ):
			links_list.append(link['href'])
	currency_df=[]
	for alink in links_list:
	     req2 = requests.get(alink , headers = headers )
	     soup = BeautifulSoup(req2.content ,'lxml')
	     name_of_curr = soup.find('h1' , class_='post-title entry-title')
	     question1 = soup.find(text=re.compile("ما ه"))
	     question2 = soup.find(text=re.compile("أين تكمن"))
	     if question1 is None or question2 is None:
	     	continue
	     link_for_curr=alink
	     curr_rate = str(soup.find(text=re.compile("تحتل")))
	     curr_rate_number = re.findall(r'\d+', curr_rate)
	     currency_pics_list = soup.find_all("img", {"class" : "aligncenter"})
	     try:
	     	currency_pic1 = currency_pics_list[0]
	     	currency_photo1_url = currency_pic1['src']
	     except:
	     	currency_photo1_url = 'NO existed photo'
	     try:
	     	currency_pic2 = currency_pics_list[1]
	     	currency_photo2_url = currency_pic2['src']
	     except: 
	     	currency_photo2_url ='NO existed photo'

	     answer1=[]
	     element2 = soup.find_all('h3')[1]
	     nextSiblings2 = element2.find_next_siblings(limit = 10)
	     for y in nextSiblings2:
	         if y.text[0:3]=='أين':
		         break
	         else:
		         answer1.append(y.text)
	     ans1_final = " ".join([str(textil) for textil in answer1])

	     #the below part is for text 2 answer
	     answer2=[]
	     element = soup.find_all('h3')[2]

	     nextSiblings = element.find_next_siblings('p')

	     for i in nextSiblings:
	         if i.text[0:4]=='تحتل':
		         break
	         else:
		         answer2.append(i.text)
	     ans2_final = " ".join([str(texto) for texto in answer2])
	      
	   #Save Data at XML foramt
	   
	     record = root.createElement('rec')
	     
	     #CurrencyName
	     recordChild = root.createElement('currencyName')     
	     text = root.createTextNode(name_of_curr.text.strip())
	     recordChild.appendChild(text)
	     record.appendChild(recordChild)
	     
	     #CurrnecyDesc
	     recordChild = root.createElement('currencyDesc')     
	     text = root.createTextNode(question1)
	     recordChild.appendChild(text)
	     record.appendChild(recordChild)     
	     
	     #textOne
	     recordChild = root.createElement('textOne')
	     text = root.createTextNode(ans1_final)#!TODO REPLACE LATER
	     recordChild.appendChild(text)
	     record.appendChild(recordChild)          
	     
	     #questionTwo
	     recordChild = root.createElement('CurrencyImportance')     
	     text = root.createTextNode(question2)#!TODO REPLACE LATER
	     recordChild.appendChild(text)
	     record.appendChild(recordChild) 
	     
	     #textTwo
	     recordChild = root.createElement('textTwo')     
	     text = root.createTextNode(ans2_final)#!TODO REPLACE LATER
	     recordChild.appendChild(text)
	     record.appendChild(recordChild)  
	     
	     #currency_rate
	     recordChild = root.createElement('CurrencyRate')     
	     text = root.createTextNode(str(curr_rate_number))#!TODO REPLACE LATER
	     recordChild.appendChild(text)
	     record.appendChild(recordChild)  
	     
	      #imageUrl
	     recordChild = root.createElement('imageOneUrl')     
	     text = root.createTextNode(currency_photo1_url)
	     recordChild.appendChild(text)
	     record.appendChild(recordChild) 
	     
	     #imageUrl
	     recordChild = root.createElement('imageTwoUrl')     
	     text = root.createTextNode(currency_photo2_url)
	     recordChild.appendChild(text)
	     record.appendChild(recordChild)   
		        
	      #pageUrl
	     recordChild = root.createElement('PageUrl')     
	     text = root.createTextNode(link_for_curr)
	     recordChild.appendChild(text)
	     record.appendChild(recordChild) 
	     
	     xml.appendChild(record)
	  
	     xml_str = root.toprettyxml(indent ="\t") 
	  
	save_path_file = "WorldCurrData.xml"
	  
	with open(save_path_file, "w") as f:
		f.write(xml_str)      
     
     

