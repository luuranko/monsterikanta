# Monsterikanta
Tietokantasovellus 2020, periodi IV

[Heroku](http://tsoha-monsterikanta.herokuapp.com/)

**Viimeisimmät muutokset**
- Monsterin Traitit, Actionit, Reactionit ja Legendary Actionit voi nyt luoda jo heti alussa, eikä vasta muokkaustilassa.
- Rakennetta remontoitiin niin, että muokkaustilassa ei tapahdu ylimääräisiä redirecteja. Tämän vuoksi uudet tai poistetut edellämainitut lapsioliot eivät päivity ennen, kuin kaikki muokkaukset on vahvistettu.
- Bootstrappia otettiin laajemmin käyttöön ulkoasussa.

**Sovelluksen käyttöön liittyviä ongelmia**
- Tiettyjä (hyvin harvinaisia) merkkijonoja ei tule käyttää monsterin tiedoissa. Tämä ei kuitenkaan luultavasti ole ongelma käytännössä, mutta voi olla haavoittuvuus. Näiden merkkijonojen käyttämistä ei vielä toistaiseksi estetä sovelluksessa.

[Käyttäjätarinoita](https://github.com/luuranko/monsterikanta/blob/master/documentation/userstory.md)

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
