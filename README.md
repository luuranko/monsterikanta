# Monsterikanta
Tietokantasovellus 2020, periodi IV

[Sovellus Herokussa](http://tsoha-monsterikanta.herokuapp.com/)

Monsterikanta on sovellus, jonka avulla voi luoda ja hallinnoida D&D 5e -pelisysteemiin pohjautuvia hirviöitä.

**Viimeisimmät muutokset**
- Yksinkertaiset käyttäjäsivut lisätty.
  - Käyttäjäsivuilla näkyvät käyttäjän luomishetki, luomusten määrät ja listaus luomuksista (muut käyttäjät näkevät vain julkiset luomukset).
  - Omalle käyttäjäsivulle pääsee yläpalkin My Page-linkistä.
  - Admin voi nyt poistaa käyttäjän vain kyseisen käyttäjän käyttäjäsivulta, ja sovellus näyttää varmistusikkunan ennen poistamista, jotta vahinkopoistoja ei tapahtuisi.
  - Muiden käyttäjien käyttäjäsivuille pääsee
    - etusivun Ranking-listauksesta nimeä painamalla
    - monsterien tai ympäristöjen listauksessa luojan nimeä painamalla
    - adminina All Users -sivulta
- Monsterien ja ympäristöjen listaussivuilla voi nyt painaa luomuksen nimen kohdalta linkkiä, joka vie luomuksen omalle sivulle. Tämä mahdollistaa monsterisivujen avaamisen uusille välilehdille kätevästi.
- Legendary Actionit järjestetään nyt pelkän aakkosjärjestyksen sijaan ensisijaisesti niiden käyttöhintojen mukaan, sitten aakkosjärjestyksessä, jotta suurihintaisemmat näytettäisiin viimeiseksi.
- Etusivun rankingit näyttävät käyttäjät nyt oikein: vain ne käyttäjät, joilla on julkisia luomuksia, järjestettynä monsterien määrän (laskeva), ympäristöjen määrän (laskeva), ja nimen (nouseva) mukaan.

**Tunnettuja ongelmia**
- Traitit ja Actionit (ja mahdollisesti myös Reactionit ja Legendary Actionit) eivät järjesty kaikissa tapauksissa samalla tavalla, kuin virallisissa lähteissä. Tämä johtuu siitä, että statblockit on suunniteltu järjestämään ne intuitiivisesti niin, että vähiten käytössä olevat asiat ovat viimeisenä. Sovelluksen järjestysalgoritmit yrittävät jäljitellä tätä priorisointia tiettyyn pisteeseen asti, mutta parempi intuitiivisuus saataisiin aikaan vain antamalla käyttäjälle hallinta piirteiden järjestyksestä. Tämä toiminto saatetaan lisätä aikanaan.

**Tulevaisuuden lisätavoitteita**
- Mahdollisuus merkitä monta monsteria "kirjanmerkillä" ja näyttää kaikkien merkittyjen monsterien statblockit samassa näkymässä
- Käyttäjäsivujen kaunistaminen ja toiminnallisuuden laajentaminen, esimerkiksi sivutus pitkiä listauksia varten
- Hakutoiminnon laajentaminen
  - Monsterien haku sen perusteella, onko monsterilla tietyn nimistä Traitia, Actionia, Reactionia tai Legendary Actionia
  - Ympäristöjen haku monsterien määrän tai sen perusteella, onko ympäristöön liitetty tietyn nimistä monsteria
  - Hakutulosten järjestäminen erinäisten piirteiden tai luomisajan perusteella
- Ability Score modifierien näyttäminen monsterinluonnissa ja muokkaussivulla
- Salasanojen suojaaminen
- Traitit, Actionit, Reactionit ja Legendary Actionit monesta moneen -yhteydelle monsterien kanssa, templaattimuotoisiksi
- Käyttäjälle vapaa hallinta siitä, missä järjestyksessä Traitit, Actionit, Reactionit ja Legendary Actionit listataan monsterin statblockissa.

[Käyttäjätarinoita](https://github.com/luuranko/monsterikanta/blob/master/documentation/userstory.md)*(Puutteellinen uusien lisäysten jälkeen)*

[Sovelluksen käyttöohje](https://github.com/luuranko/monsterikanta/blob/master/documentation/guide.md)*(Puutteellinen uusien lisäysten jälkeen)*

[Asennusohje](https://github.com/luuranko/monsterikanta/blob/master/documentation/installation.md)

[Tietokantarakenne ja SQL-kyselyt](https://github.com/luuranko/monsterikanta/blob/master/documentation/sql.md)*(Puutteellinen uusien lisäysten jälkeen)*

[Tietokantakaavio](https://github.com/luuranko/monsterikanta/blob/master/documentation/tietokantakaavio.png)
