#1
import mechanicalsoup
import pandas as pd
import sqlite3
# შევქმნათ openai ობიექტი და გავხსნათ URL
openai = mechanicalsoup.StatefulBrowser()
openai.open("https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions")
# "Distribution" სვეტის შიგთავსი
th = openai.page.find_all("th", attrs={"class": "table-rh"})
# tidy up and slice off non-table elements
distro = [value.text.replace("\n", "") for value in th]
distro = distro[:95]
# ცხრილის მონაცემები
td = openai.page.find_all("td")
# tidy up and slice off non-table elements
columns = [value.text.replace("\n", "") for value in td]
columns = columns[6:1051]
column_names = ["Founder",
                "Maintainer",
                "Initial_Release_Year",
                "Current_Stable_Version",
                "Security_Updates",
                "Release_Date",
                "System_Distribution_Commitment",
                "Forked_From",
                "Target_Audience",
                "Cost",
                "Status"]
dictionary = {"Distribution": distro}
# სვეტების სახელების და შიგთავსის ლექსიკონში შეტანა
#ენუმერაცია-ჩამონათვალი
for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::11]
#ლექსიკონის გარდაქმნა DataFrame-ად
df = pd.DataFrame(data = dictionary)
# create new database and cursor
connection = sqlite3.connect("linux_distro.db")
cursor = connection.cursor()
#მონაცემთა ბაზის ცხრილის შექმნა
cursor.execute("create table linux (Distro, " + ",".join(column_names)+ ")")
for i in range(len(df)):
    cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i]) #iloc=integer location
# "linux_distro.db"-ში მონაცემების შენახვა
connection.commit()
connection.close()



#2
import urllib.request
from bs4 import BeautifulSoup as bs
import re #regular expression
import pandas as pd
page=urllib.request.urlopen("https://docs.python.org/3/library/random.html")
soup=bs(page)
names=soup.body.findAll('dt')
function_names=re.findall('id="random.\w+', str(names))
#item[4:]პირველი ოთხი სიმბოლოს მოშორება
function_names=[item[4:] for item in function_names]
description=soup.body.findAll('dd')
function_usage=[]
for item in description:
    item=item.text
    item=item.replace('\n', ' ')
    function_usage.append(item)
data=pd.DataFrame({'function name': function_names, 'function usage': function_usage})
print(data)


#3
import sqlite3
dbase=sqlite3.connect('gta.sqlite')
gta=dbase.cursor()
gta.execute('''create table if not exists gta(
                year integer,
                name text,
                city text

    )''')
list=[
      (1997, "GTA",'New Guernsey'),
      (1999, "GTA", "USA"),
      (2001, "GTA III","Liberty City"),
      (2002, "GTA:Vice City", "Vice City"),
      (2004, "GTA: San Andreas", "San Andreas"),
      (2008, "GTA IV", "Liberty City")
      ]

gta.executemany("insert into gta values (?,?,?)", list)
for row in gta.execute("select * from gta"):
    print(row)
print('**************')
gta.execute("select * from gta where city=:c", {"c":"Liberty City"})
gta_search=gta.fetchall()
print(gta_search)
gta.execute("""create table cities (
                gta_city text,
                real_city text    
    )""")
gta.execute("insert into cities values(?,?)", ("Liberty City", "New York"))
gta.execute("select * from cities where gta_city=:c",{"c":"Liberty City"})
cities_search=gta.fetchall()
print(cities_search)
print("*********")
for i in gta_search:
#გვინდა, რომ ჩავანაცვლოთ New York-თ ის მნიშვნელობები, რომლებიც უტოლდება #Liberty City-ს,
#სხვა შემთხევაში მივიღოთ შედეგები იტერაციის შედეგად.
#["New York" if value =="Liberty City" else value for value in i]
#ჩანაწერი Liberty City მდებარეობს 0 სტრიქონის და 0 სვეტის კვეთაზე, ხოლო New York #მდებარეობს 0 სტრიქონის და 1 სვეტის კვეთაზე.
   loop= [cities_search[0][1] if value==cities_search[0][0] else value for value in i]
   print(loop)
dbase.close()



#4
from flask import Flask, jsonify, request
app=Flask(__name__)
books=[
    {
     'name': 'Creativity, Inc',
     'price': 7.99,
     'isbn': 9764847372
     },
    {
     'name': 'Sapiens',
     'price': 6.99,
     'isbn': 9787433621
     }
]

@app.route('/books')
def get_books():
    return jsonify({'books':books})
@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value={}
    for book in books:
        if book["isbn"] == isbn:
            return_value={
                'name':book["name"],
                'price':book["price"]
                }
    return jsonify(return_value)
app.run(port=5000)



#5
from flask import Flask, make_response, jsonify, request
import dataset
app=Flask(__name__)
db=dataset.connect('sqlite:///api.db')
books={
       '1':{
           "id":"1",
           "name":"Elon Musk",
           "author":"Ashlee Vance"
           },
       '2':{
           "id":"2",
           "name":"Steve Jobs",
           "author":"Walter Isaacson"
           }
       }
table=db['books']
table.insert({
    "book_id":"1",
    "name":"Elon Musk",
    "author":"Ashlee Vance"
    })
table.insert({
    "book_id":"2",
    "name":"Steve Jobs",
    "author":"Walter Isaacson"
    })
def fetch_db(book_id):
    return table.find_one(book_id=book_id)
def fetch_db_all():
    return table.all()
@app.route('/api/books', methods=['GET', 'PUT'])
def api_books():
    if request.method=='GET':
        return make_response(jsonify(books), 200)
if __name__=='__main__':
    app.run()


#6
from requests_html import HTML, HTMLSession
session=HTMLSession()
r=session.get('https://coreyms.com/')
articles=r.html.find('article')
for article in articles:
    headline = article.find('article', 'h1', 'a').text
    print(headline)
    summary = article.find('div', class_='entry-content').p.text
    print(summary)
    try:
        vid_src = article.find('iframe', class_='youtube-player').attrs['src']
        vid_id = vid_src.split('/')[4]
        vid_id = vid_id.split('?')[0]
        yt_link = f'https://youtube.com/watch?v={vid_id}'
    except Exception as e:
        yt_link = None
    print(yt_link)
    print()


#7
from flask import Flask, jsonify
app=Flask(__name__)
courses=[{
      "Description":"Python in AI",
      "course_id":"0",
      "name":"Python AI Certificate",
      "site":"btu.edu.ge"
      },
     {
      "Description":"CCNA",
      "course_id":"1",
      "name":"CCNA Certificate",
      "site":"netacad.com"
      },
     {
      "Description":"Linux",
      "course_id":"2",
      "name":"Linux Certificate",
      "site":"netdevgroup.com"
 }]
@app.route('/')
def index():
    return "Python, CCNA, Linux, OpenAI"
@app.route("/courses", methods=['GET'])
def get():
    return jsonify({'Courses':courses})
@app.route("/courses/<int:course_id>", methods=['GET'])
def get_course(course_id):
    return jsonify({'course':courses[course_id]})
@app.route("/courses", methods=['POST'])
def create():
    course={"Description":"SQLserver",
    "course_id":"3",
    "name":"SQLserver Certificate",
    "site":"mygreatlearning.com"}
    courses.append(course)
    return jsonify({'Created':course})
if __name__=="__main__":
    app.run(debug=True)
#პასუხი:
#cmd-ში გავუშვათ შემდეგი ბრძანება: curl -i -H *Content-Type: Application/json* -X POST http://127.0.0.1:5000/courses

#8
import requests
from bs4 import BeautifulSoup
url='https://realpython.github.io/fake-jobs/'
html=requests.get(url)
tesla=BeautifulSoup(html.content, 'html.parser')
results=tesla.find('div', id='ResultsContainer') #gadavxedot
job_title=results.find_all('h2', class_='title is-5')
for job in job_title:
    print(job.text)

#9
def outer_func(msg):
    message=msg
    def inner_func():
        print(message)
    return inner_func()

a = outer_func('hello')
a()


#10
def html_tag(tag):
    def wrap_text(msg):
        print('<{0}>{1}</{0}>'.format(tag, msg))
    return wrap_text
print_h1=html_tag('h1')
print_h1('TeslaAL')
print_h1('btuAL')
print_p=html_tag('p')
print_p('PythonAI')

#11
from flask import Flask, jsonify
app=Flask(__name__)
courses=[{
      "Description":"Python in AI",
      "course_id":"0",
      "name":"Python AI Certificate",
      "site":"btu.edu.ge"
      },
     {
      "Description":"CCNA",
      "course_id":"1",
      "name":"CCNA Certificate",
      "site":"netacad.com"
      },
     {
      "Description":"Linux",
      "course_id":"2",
      "name":"Linux Certificate",
      "site":"netdevgroup.com"
 }]
@app.route('/')
def index():
    return "Python, CCNA, Linux, OpenAI"
@app.route("/courses", methods=['GET'])
def get():
    return jsonify({'Courses':courses})
@app.route("/courses/<int:course_id>", methods=['GET'])
def get_course(course_id):
    return jsonify({'course':courses[course_id]})
# @app.route("/courses", methods=['POST'])
# def create():
#     course={"Description":"SQLserver",
#     "course_id":"3",
#     "name":"SQLserver Certificate",
#     "site":"mygreatlearning.com"}
#     courses.append(course)
#     return jsonify({'Created':course})
@app.route("/courses/<int:course_id>", methods=['PUT'])
def course_update(course_id):
    courses[course_id]['Description']="TESLA OS"
    return jsonify({'course':courses[course_id]})
@app.route("/courses/<int:course_id>", methods=['DELETE'])
def delete(course_id):
    courses.remove(courses[course_id])
    return jsonify({'result':True})
if __name__=="__main__":
    app.run(debug=True)
#პასუხი:
#cmd-ში გავუშვათ: curl -i -H *Content-Type: Application/json* -X DELETE http://127.0.0.1:5000/courses/2


#12
import mechanicalsoup
soup=mechanicalsoup.StatefulBrowser()
soup.open('http://coreyms.com')
for article in soup.page.find_all('article'):
    headline=article.find('article', 'h1', 'a') #gadaamowme
    print(headline)
    summary=article.find('div', class_='entry-content').p.text
    print(summary)
    try:
        vid_src=article.find('iframe', class_='youtube-player')['src']
        vid_id=vid_src.split('/')[4]
        vid_id=vid_id.split('?')[0]
        yt_link=f'https://youtube.com/watch?v={vid_id}'
    except Exception as e:
        yt_link=None
    print(yt_link)
    print()



#13
from flask import Flask, jsonify
app=Flask(__name__)
courses=[{
      "Description":"Python in AI",
      "course_id":"0",
      "name":"Python AI Certificate",
      "site":"btu.edu.ge"
      },
     {
      "Description":"CCNA",
      "course_id":"1",
      "name":"CCNA Certificate",
      "site":"netacad.com"
      },
     {
      "Description":"Linux",
      "course_id":"2",
      "name":"Linux Certificate",
      "site":"netdevgroup.com"
 }]
@app.route('/')
def index():
    return "Python, CCNA, Linux, OpenAI"
@app.route("/courses", methods=['GET'])
def get():
    return jsonify({'Courses':courses})
@app.route("/courses/<int:course_id>", methods=['GET'])
def get_course(course_id):
    return jsonify({'course':courses[course_id]})
if __name__=="__main__":
    app.run(debug=True)


#14
from bs4 import BeautifulSoup
import requests
source = requests.get("https://coreyms.com").text
soup = BeautifulSoup(source, "lxml")
for article in soup.find_all("article"):
    headline = article.h1.a.text
    print(headline)
    summary = article.find("div", class_ = "entry-content").p.text
    print(summary)
    print()

    try:
        src = article.find("iframe", class_="youtube-player")["src"]
        id = src.split("/")[4]
        id = id.split("?")[0]
        yt_link = f"https://youtube.com/watch?v={id}"
    except Exception as e:
        yt_link = None
    print(yt_link)
    print()


#x
from flask import Flask, jsonify
app=Flask(__name__)
courses=[{
      "Description":"Python in AI",
      "course_id":"0",
      "name":"Python AI Certificate",
      "site":"btu.edu.ge"
      },
     {
      "Description":"CCNA",
      "course_id":"1",
      "name":"CCNA Certificate",
      "site":"netacad.com"
      },
     {
      "Description":"Linux",
      "course_id":"2",
      "name":"Linux Certificate",
      "site":"netdevgroup.com"
 }]

@app.route('/')
def index():
    return "Python, CCNA, Linux, OpenAI"

@app.route("/courses", methods=['GET'])
def get():
    return jsonify({'Courses':courses})

@app.route("/courses/<int:course_id>", methods=['GET'])
def get_course(course_id):
    return jsonify({'course':courses[course_id]})

@app.route("/courses/<int:course_id>", methods=['PUT'])
def course_update(course_id):
    courses[course_id]['Description']="BTULinux"
    return jsonify({'course':courses[course_id]})

if __name__=="__main__":
    app.run(debug=True)
# პასუხი:
# cmd-ში გავუშვათ შემდეგი ბრძანება: curl -i -H *Content-Type: Application/json* -X PUT http://127.0.0.1:5000/courses/2
