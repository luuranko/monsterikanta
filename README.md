# Monsterikanta
Tietokantasovellus 2020, periodi IV

[Heroku](http://tsoha-monsterikanta.herokuapp.com/)

**Viimeisimmän commitin muutokset**
- Traitien ja Actionien lisääminen tai poistaminen ei enää tyhjennä uusia muutoksia monsteriin.
- Jos Actionin nimi on "Multiattack", se listataan ensimmäisenä. Muuten Traitit ja Actionit listataan aakkosjärjestyksessä.
- Turhiksi tulleita HTML-sivuja ja näkymiä poistettiin.

**Sovelluksen käyttöön liittyviä ongelmia**
- Traiteja ja Actioneja ei voi luoda monsterinluonnissa, vaan ne luodaan muokkausnäkymässä.
- Traiteja ja Actioneja ei voi muokata.

**Muita ongelmia**
- Monsterien listaussivun HTML on hakutoiminnon osalta toistaiseksi spagettia, koska toiminnon aikaansaaminen tuotti ongelmia.


[Käyttäjätarinoita](https://github.com/luuranko/monsterikanta/blob/master/documentation/userstory.md)

Monsterikanta on sovellus, jonka avulla voi luoda ja hallinnoida D&D 5e -pelisysteemiin pohjautuvia hirviöitä.
Tavoitteena ovat seuraavat toiminnallisuudet:
- [x] Käyttäjätunnusten luonti 
- [x] Sisään- ja uloskirjautuminen
- [x] Oman monsterin luominen ja muokkaaminen
- [x] Monsterien piirteet ja hyökkäykset, jotka luodaan
  - [ ] ...tai valitaan omasta valikoimasta 
- [x] Monsterin liittäminen yhteen tai useampaan ympäristöön
- [x] Oman ympäristön luominen ja muokkaaminen
- [ ] Tietokantakyselyt monstereista ja ympäristöistä niiden ominaisuuksien ja yhteyksien perusteella
- [ ] Oma katalogi ympäristöistä ja monstereista
- [x] Omien monsterien ja ympäristöjen asettaminen julkiseksi tai yksityiseksi niin, että kaikki käyttäjät voivat tarkastella julkisia monstereita ja ympäristöjä

[Tietokantakaavio](https://github.com/luuranko/monsterikanta/blob/master/tietokantakaavio.png)

*Tietokantakaavio on vanhentunut*

Tulevaisuuden lisätavoitteita:
- Käyttäjäsivut
- Piirteiden ja hyökkäysten muokkaaminen templaattimuotoon niin, että sama piirre tai hyökkäys voi olla useammalla monsterilla
