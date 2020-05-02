# Monsterikanta
Tietokantasovellus 2020, periodi IV

[Sovellus Herokussa](http://tsoha-monsterikanta.herokuapp.com/)

**Viimeisimmät muutokset (kurssin deadlinen jälkeen tehtyjä)**
- Sekä omia että muiden tekemiä monstereita voi nyt kopioida.
- Monsterin statblockin voi vapaaehtoisesti muuttaa vaakasuuntaiseen näkymään, jos se on tarpeeksi pitkä, että muutos näyttäisi järkevältä.

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
- [x] Hakutoiminnallisuuksia: monstereita ja ympäristöjä voi hakea eri ominaisuuksien perusteella
- [x] Omien monsterien ja ympäristöjen asettaminen julkiseksi tai yksityiseksi niin, että kaikki käyttäjät voivat tarkastella julkisia monstereita ja ympäristöjä

[Tietokantakaavio](https://github.com/luuranko/monsterikanta/blob/master/documentation/tietokantakaavio.png)

**Tulevaisuuden lisätekemistä**
- Hakutoiminnon laajentaminen
  - Useamman vaihtoehdon valitseminen valikoista (esim. valitsee sekä Aberration että Beast -tyyppien monsterit ja hakutulokset näyttävät ne monsterit jotka kuuluvat jompaankumpaan kategoriaan)
  - Monsterien haku sen perusteella, onko monsterilla tietyn nimistä Traitia, Actionia, Reactionia tai Legendary Actionia
  - Ympäristöjen haku monsterien määrän tai sen perusteella, onko ympäristöön liitetty tietyn nimistä monsteria
  - Hakutulosten järjestäminen erinäisten piirteiden tai luomisajan perusteella
- Varmistusikkuna, kun ollaan poistamassa käyttäjää
- Ability Score modifierien näyttäminen monsterinluonnissa ja muokkaussivulla
- Salasanojen suojaaminen
- Traitit, Actionit, Reactionit ja Legendary Actionit monesta moneen -yhteydelle monsterien kanssa, templaattimuotoisiksi
- Käyttäjäsivut, joilla listataan kaikki käyttäjän tekemät (julkiset) monsterit ja ympäristöt
