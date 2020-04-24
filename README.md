# Monsterikanta
Tietokantasovellus 2020, periodi IV

[Heroku](http://tsoha-monsterikanta.herokuapp.com/)

**Viimeisimmät muutokset**
- Monsterinluonti ja muokkaustila suojelevat keskeneräisiä muutoksia virheiden varalta paremmin
  - Jos syöttää numeroa vaativaan kenttään tekstiä, sovellus ilmoittaa virheestä ilman, että luodut Traitit ja muut ominaisuudet katoavat
  - Haitallisten merkkien (£ ja ¤) syöttäminen ei ole enää mahdollista Traitien ja muiden ominaisuuksien kenttiin.

**Sovelluksen käyttöön liittyviä ongelmia**
- Monsterien etsiminen koon perusteella: hakunapin uudelleenpainaminen sulkee hakutulokset eikä korvaa edellisiä tuloksia uusilla.

[Käyttäjätarinoita](https://github.com/luuranko/monsterikanta/blob/master/documentation/userstory.md)

[Sovelluksen käyttöohje](https://github.com/luuranko/monsterikanta/blob/master/documentation/guide.md)

[Asennusohje](https://github.com/luuranko/monsterikanta/blob/master/documentation/installation.md)

[Tietokantarakenne ja SQL-kyselyt](https://github.com/luuranko/monsterikanta/blob/master/documentation/sql.md)

Monsterikanta on sovellus, jonka avulla voi luoda ja hallinnoida D&D 5e -pelisysteemiin pohjautuvia hirviöitä.
Tavoitteena ovat seuraavat toiminnallisuudet:
- [x] Käyttäjätunnusten luonti 
- [x] Sisään- ja uloskirjautuminen
- [x] Oman monsterin luominen ja muokkaaminen
- [x] Monsterien piirteet ja hyökkäykset, jotka luodaan
- [x] Monsterin liittäminen yhteen tai useampaan ympäristöön
- [x] Oman ympäristön luominen ja muokkaaminen
- [ ] Hakutoiminnallisuuksia: Monstereita ja Ympäristöjä voi hakea eri ominaisuuksien ja yhteyksien perusteella
- [x] Omien monsterien ja ympäristöjen asettaminen julkiseksi tai yksityiseksi niin, että kaikki käyttäjät voivat tarkastella julkisia monstereita ja ympäristöjä

[Tietokantakaavio](https://github.com/luuranko/monsterikanta/blob/master/tietokantakaavio.png)

*Tietokantakaavio on vanhentunut*

Tulevaisuuden lisätavoitteita:
- Käyttäjäsivut
- Piirteiden ja hyökkäysten muokkaaminen templaattimuotoon niin, että sama piirre tai hyökkäys voi olla useammalla monsterilla
