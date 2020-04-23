## Asennusohje

**Tarvitut asennukset**
- Python 3.5 tai uudempi
  - pip
  - venv
- git
- heroku-cli ja tunnukset Herokuun
- postgresql

##### Paikallinen asennus ja käyttö

Kloonaa projekti (tai paina projektin sivulla "Clone or download"-nappia ja lataa ZIP):
``` 
git clone --recursive https://github.com/luuranko/monsterikanta
```

Kansiossa monsterikanta käynnistä venv: 
``` 
python3 -m venv venv
source venv/bin/activate```

Asennukset:
```pip install -r requirements.txt```

Käynnistä ohjelma:
```python run.py```

Luo Admin-tunnukset (name, username ja password voivat olla jotkin muutkin, mutta admin-arvon pitää olla 1 tai true):
``` 
sqlite3 application/monsters.db
insert into account(name, username, password, admin) values ('admin', 'admin', 'admin', 1);
```

##### Heroku

Kun olet ladannut kansion paikallisen käytön ensimmäisen askelen mukaan, siirry kansioon ja luo projekti herokussa (voit käyttää jotain muuta nimeä kuin monsterikanta):
``` heroku create monsterikanta
git remote add heroku https://git.heroku.com/monsterikanta.git
git add .
git commit -m"ensimmäinen commit"
git push heroku master```

Admin-tunnuksen luonti Herokussa olevaan sovellukseen:
``` heroku pg:psql
insert into account(name, username, password, admin) values('admin', 'admin', 'admin', true);```
