# Monsterikanta
Tietokantasovellus 2020, periodi IV

[Sovellus Herokussa](http://tsoha-monsterikanta.herokuapp.com/)

**Viimeisimmät muutokset**
- Ympäristöjen listaussivulla on nyt hakutoiminto, jolla voi filtteröidä ympäristön nimen, tyypin ja luojan perusteella. Lisäksi nämä tulokset voi halutessaan filtteröidä myös sen mukaan, ovatko ympäristöt juuri itse tehtyjä, vai nimenomaan muiden käyttäjien tekemiä.
- Rivinvaihdot säilyvät nyt monsterien ja ympäristöjen kuvauksissa ja monsterien Traitien kuvauksissa.
  - Tämä sallii kauniimman muotoilun kuvauksiin ja Spellcasting-Traitin asianmukaisen muotoilun.
- Käyttäjän nimi, käyttäjänimi ja salasana eivät voi enää olla pelkkiä välimerkkejä.

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
- [ ] Hakutoiminnallisuuksia: Monstereita ja Ympäristöjä voi hakea eri ominaisuuksien perusteella
- [x] Omien monsterien ja ympäristöjen asettaminen julkiseksi tai yksityiseksi niin, että kaikki käyttäjät voivat tarkastella julkisia monstereita ja ympäristöjä

[Tietokantakaavio](https://github.com/luuranko/monsterikanta/blob/master/tietokantakaavio.png)

*Tietokantakaavio on vanhentunut*

**Tulevia lisäyksiä**
- Hakutoiminnon laajentaminen
  - Monsterien haku nimen, tyypin, haastetason, legendaarisuusstatuksen, luojan nimen tai sen perusteella, onko monsterilla tietyn nimistä Traitia, Actionia, Reactionia tai Legendary Actionia
  - Ympäristöjen haku monsterien määrän tai sen perusteella, onko ympäristöön liitetty tietyn nimistä monsteria
  - Hakutulosten järjestäminen erinäisten piirteiden tai luomisajan perusteella
- Varmistusikkuna, kun ollaan poistamassa monsteria, ympäristöä tai käyttäjää
- Sivutus pitkissä listauksissa
- Ability Score modifierien näyttäminen
- Salasanojen suojaaminen
- Monsterien kopioiminen
- Traitit, Actionit, Reactionit ja Legendary Actionit monesta moneen -yhteydelle monsterien kanssa, templaattimuotoisiksi
- Käyttäjäsivut, joilla listataan kaikki käyttäjän tekemät (julkiset) monsterit ja ympäristöt
