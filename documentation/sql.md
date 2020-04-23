
### Create Table -lauseet

```sqlite3
CREATE TABLE account (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	admin BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	CHECK (admin IN (0, 1))
)

CREATE TABLE monster (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	public BOOLEAN NOT NULL, 
	mtype VARCHAR(144) NOT NULL, 
	size VARCHAR(144) NOT NULL, 
	cr VARCHAR(144) NOT NULL, 
	weakto VARCHAR(750), 
	resist VARCHAR(750), 
	descrip VARCHAR(5000), 
	hp INTEGER NOT NULL, 
	ac INTEGER NOT NULL, 
	stre INTEGER NOT NULL, 
	dex INTEGER NOT NULL, 
	con INTEGER NOT NULL, 
	inte INTEGER NOT NULL, 
	wis INTEGER NOT NULL, 
	cha INTEGER NOT NULL, 
	sens VARCHAR(500) NOT NULL, 
	spd VARCHAR(100) NOT NULL, 
	saves VARCHAR(144), 
	skills VARCHAR(750), 
	immun VARCHAR(750), 
	coimmun VARCHAR(750), 
	l_points INTEGER, 
	account_id INTEGER NOT NULL, 
	account_name VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id), 
	CHECK (public IN (0, 1)), 
	FOREIGN KEY(account_id) REFERENCES account (id)
)

CREATE TABLE enviro (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(144) NOT NULL, 
	public BOOLEAN NOT NULL, 
	etype VARCHAR(200) NOT NULL, 
	descrip VARCHAR(5000) NOT NULL, 
	account_id INTEGER NOT NULL, 
	account_name VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id), 
	CHECK (public IN (0, 1)), 
	FOREIGN KEY(account_id) REFERENCES account (id)
)

CREATE TABLE trait (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(60) NOT NULL, 
	usage VARCHAR(60) NOT NULL, 
	content VARCHAR(1000) NOT NULL, 
	monster_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(monster_id) REFERENCES monster (id)
)

CREATE TABLE action (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(60) NOT NULL, 
	usage VARCHAR(60) NOT NULL, 
	content VARCHAR(1000) NOT NULL, 
	atype INTEGER NOT NULL, 
	monster_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(monster_id) REFERENCES monster (id)
)

CREATE TABLE reaction (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(60) NOT NULL, 
	content VARCHAR(1000) NOT NULL, 
	monster_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(monster_id) REFERENCES monster (id)
)

CREATE TABLE legendary (
	id INTEGER NOT NULL, 
	date_created DATETIME, 
	date_modified DATETIME, 
	name VARCHAR(60) NOT NULL, 
	cost INTEGER NOT NULL, 
	content VARCHAR(1000) NOT NULL, 
	monster_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(monster_id) REFERENCES monster (id)
)

CREATE TABLE enviromonster (
	enviro_id INTEGER NOT NULL, 
	monster_id INTEGER NOT NULL, 
	PRIMARY KEY (enviro_id, monster_id), 
	FOREIGN KEY(enviro_id) REFERENCES enviro (id), 
	FOREIGN KEY(monster_id) REFERENCES monster (id)
)
```

### Käyttötapauksiin liittyvät SQL-kyselyt

Käyttäjän luominen: `INSERT INTO account (date_created, date_modified, name, username, password, admin) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Tester', 'test', 'test', 0);`

Etusivu, haetaan viimeisimpänä muokattu monsteri (listan ensimmäinen valitaan Pythonissa): `SELECT Monster.id, Monster.name, Monster.date_modified FROM Account LEFT JOIN Monster ON Account.id = Monster.account_id WHERE Monster.account_id = 1 ORDER BY Monster.date_modified DESC;`
Etusivu, haetaan viimeisimpänä muokattu ympäristö (listan ensimmäinen valitaan Pythonissa): `SELECT Enviro.id, Enviro.name, Enviro.date_modified FROM Account LEFT JOIN Enviro ON Account.id = Enviro.account_id WHERE Enviro.account_id = ? ORDER BY Enviro.date_modified DESC;`

Monsterien listaussivu, haetaan lista käyttäjistä ja heidän monsterimääristään: `SELECT Account.name, COUNT(Monster.id) AS monster FROM Account LEFT JOIN Monster ON Account.id = Monster.account_id GROUP BY Account.name ORDER BY monster DESC;`
Monsterien listaussivu, haetaan lista näytettävistä monstereista: `SELECT * FROM monster WHERE monster.account_id = 1 OR monster.public = 1;`

Monsterin luominen: `INSERT INTO monster (date_created, date_modified, name, public, mtype, size, cr, weakto, resist, descrip, hp, ac, stre, dex, con, inte, wis, cha, sens, spd, saves, skills, immun, coimmun, l_points, account_id, account_name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Test Monster', 1, 'Aberration', 'Tiny', '0', '', '', '(Description to be added.)', 1, 10, 10, 10, 10, 10, 10, 10, 'passive Perception 10', '30 ft.', '', '', '', '', '3', 1, 'Tester');`
Traitin luominen: `INSERT INTO trait (date_created, date_modified, name, usage, content, monster_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Test Trait', '', 'Testing.', 1);`
Actionin luominen: `INSERT INTO action (date_created, date_modified, name, usage, content, atype, monster_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Melee Test', '', 'Melee Weapon Attack: +0 to hit, reach 5 ft., one target. Hit: 0 (0d0 + 0) bludgeoning damage.', '2', 1);`
Reactionin luominen: `INSERT INTO reaction (date_created, date_modified, name, content, monster_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Test Reaction', 'Testing.', 1);`
Legendary Actionin luominen: `INSERT INTO legendary (date_created, date_modified, name, cost, content, monster_id) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Test Legendary Action', 1, 'Testing.', 1);`

Monsterin oma sivu, monsterin hakeminen: `SELECT * FROM monster WHERE monster.id = 1;`
Monsterin oma sivu, Traitien hakeminen: `SELECT Trait.id, Trait.name, Trait.usage, Trait.content FROM Monster LEFT JOIN Trait ON Monster.id = Trait.monster_id WHERE Trait.monster_id = 1 ORDER BY LOWER(Trait.name);`
Monsterin oma sivu, Actionien hakeminen: `SELECT Action.id, Action.name, Action.usage, Action.content, Action.atype FROM Monster LEFT JOIN Action ON Monster.id = Action.monster_id WHERE Action.monster_id = 1 ORDER BY Action.atype ASC, LOWER(Action.name);`
Monsterin oma sivu, Reactionien hakeminen: `Reaction.id, Reaction.name, Reaction.content FROM Monster LEFT JOIN Reaction ON Monster.id = Reaction.monster_id WHERE Reaction.monster_id = 1 ORDER BY LOWER(Reaction.name);`
Monsterin oma sivu, Legendary Actionien hakeminen: `SELECT Legendary.id, Legendary.name, Legendary.cost, Legendary.content FROM Monster LEFT JOIN Legendary ON Monster.id = Legendary.monster_id WHERE Legendary.monster_id = 1 ORDER BY LOWER(Legendary.name);`

Monsterin julkisuuden vaihtaminen yksityiseksi: `UPDATE monster SET date_modified=CURRENT_TIMESTAMP, public=0 WHERE monster.id = 1;`

Monsterin muokkaaminen, monsterin tiedot: `UPDATE monster SET date_modified=CURRENT_TIMESTAMP, mtype='Monstrosity', size='Large', cr='4', descrip='This is a description', hp=100, ac=15, dex=18, sens='passive Perception 15', skills='Perception +5, Stealth +6', l_points=0 WHERE monster.id = 1;`
Monsterin muokkaaminen, edelliset Traitit poistetaan: `DELETE FROM trait WHERE trait.monster_id = 1;`
Monsterin muokkaaminen, edelliset Actionit poistetaan: `DELETE FROM action WHERE action.monster_id = 1;`
Monsterin muokkaaminen, edelliset Reactionit poistetaan: `DELETE FROM reaction WHERE reaction.monster_id = 1;`
Monsterin muokkaaminen, edelliset Legendary Actionit poistetaan: `DELETE FROM legendary WHERE legendary.monster_id = 1;`
Monsterin muokkaamisessa nykyisten Traitien, Actionien, Reactionien ja Legendary Actionien luomiseen käytetään samoja lauseita kuin yleensäkin niiden luomisessa.

Ympäristön luominen: `INSERT INTO enviro (date_created, date_modified, name, public, etype, descrip, account_id, account_name) VALUES (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Testipaikka', 0, 'Arctic', '(Description to be added.)', 1, 'Tester');`

Ympäristön oma sivu, ympäristön hakeminen: `SELECT * FROM enviro WHERE enviro.id = 1;`
Ympäristön oma sivu, paikallisten monstereiden hakeminen: `SELECT Monster.id, Monster.name, Monster.public FROM Enviro JOIN EnviroMonster ON EnviroMonster.enviro_id = Enviro.id JOIN Monster ON Monster.id = EnviroMonster.monster_id WHERE EnviroMonster.enviro_id = 1 ORDER BY Monster.name;`
Ympäristön oma sivu, ei-paikallisten monstereiden hakeminen: `SELECT Monster.id, Monster.name FROM Monster WHERE id NOT IN (SELECT Monster.id FROM Enviro JOIN EnviroMonster ON EnviroMonster.enviro_id = Enviro.id JOIN Monster ON Monster.id = EnviroMonster.monster_id WHERE EnviroMonster.enviro_id = 1) AND Monster.account_id = 1 ORDER BY Monster.name;`

Ympäristön julkisuuden vaihtaminen julkiseksi: `UPDATE enviro SET date_modified=CURRENT_TIMESTAMP, public=1 WHERE enviro.id =1;`

Ympäristön muokkaaminen: `UPDATE enviro SET date_modified=CURRENT_TIMESTAMP, etype='Desert', descrip='This is a description.' WHERE enviro.id = 1;`

Monsterin lisääminen ympäristöön: `INSERT INTO enviromonster (enviro_id, monster_id) VALUES (1, 1);`
Monsterin poistaminen ympäristöstä: `DELETE FROM enviromonster WHERE enviromonster.enviro_id=1 AND enviromonster.monster_id=1;`

Ympäristöjen listaussivu, käyttäjien ympäristömäärän hakeminen: `SELECT Account.name, COUNT(Enviro.id) AS enviro FROM Account LEFT JOIN Enviro ON Account.id = Enviro.account_id GROUP BY Account.name ORDER BY enviro DESC;`
Ympäristöjen listaussivu, ympäristöjen hakeminen: `SELECT enviro.id AS enviro_id, enviro.date_created AS enviro_date_created, enviro.date_modified AS enviro_date_modified, enviro.name AS enviro_name, enviro.public AS enviro_public, enviro.etype AS enviro_etype, enviro.descrip AS enviro_descrip, enviro.account_id AS enviro_account_id, enviro.account_name AS enviro_account_name FROM enviro WHERE enviro.account_id = ? OR enviro.public = 1;`

Ympäristön poistaminen: `DELETE FROM enviro WHERE enviro.id = 1`
Monsterin poistaminen: `DELETE FROM monster WHERE monster.id = 1`

Admin, käyttäjien listaaminen: `SELECT * FROM account WHERE account.admin = 0;`
Admin, käyttäjän poistaminen: `DELETE FROM account WHERE account.id=1;`
