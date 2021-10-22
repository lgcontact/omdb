import urllib.request, urllib.parse, urllib.error
import sqlite3
import json
import ssl

api_key = "800a5c3b"
serviceurl = "http://www.omdbapi.com/?"

conn = sqlite3.connect('omdb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Omdbdump;')
cur.execute('''CREATE TABLE Omdbdump (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT, year TEXT, rated TEXT, released TEXT, runtime TEXT, genre TEXT, director TEXT, writer TEXT, actors TEXT, plotlong TEXT, language  TEXT, country TEXT, awards TEXT, poster URL, imdbrating REAL, rtrating REAL, mcrating REAL, imdbid TEXT, type TEXT, dvd TEXT, boxoffice TEXT, production TEXT, website URL
)
''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = cur.execute('''SELECT id, title, year FROM top50''')

rty = list()
for row in fh:
    #row = cur.fetchone()
    qtitle = str(row[1])
    qyear = str(row[2])

    #print(rty)
    print(qtitle)
    print(qyear)

    #parms sets up the query url: url concatenated with address and api key
    #query format https://www.omdbapi.com/?t=blade+runner&y=2018&plot=full&apikey=800a5c3b

    parms = dict()
    parms["t"] = qtitle
    parms["y"] = qyear
    parms["plot"] = "full"
    parms["apikey"] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    
    js = json.loads(data)
    if js['Response'] == 'False':
        print('==== Failure To Retrieve ====')
        print(data)
        continue
   
    title = js['Title']
    year = js['Year']
    rated = js['Rated']
    released = js['Released']
    runtime = js['Runtime']
    genre = js['Genre']
    director = js['Director']
    writer = js['Writer']
    actors = js['Actors']
    plotlong = js['Plot']
    language = js['Language']
    country = js['Country']
    awards = js['Awards']
    poster = js['Poster']
    imdbrating = js['imdbRating']
    mcrating = js['Metascore']
    imdbid = js['imdbID']
    type = js['Type']
    dvd = js['DVD']
    boxoffice = js['BoxOffice']
    production = js['Production']
    website = js['Website']
    try:
        rtrating = js['Ratings'][1]['Value']
    except:
        rtrating = 'N/A'
    
    print(title)
    print(imdbid)
    print(runtime)
    
    #the loop works until here -- with the following lines, it goes through once then stops...

    #cur.execute('''INSERT INTO Omdbdump (title, year, rated, released, runtime, genre, director, writer, actors, plotlong, language, country, awards, poster, imdbrating, rtrating, mcrating, imdbid, type, dvd, boxoffice, production, website) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (title, year, rated, released, runtime, genre, director, writer, actors, plotlong, language, country, awards, poster, imdbrating, rtrating, mcrating, imdbid, type, dvd, boxoffice, production, website) )
    #conn.commit()

print("Done")
