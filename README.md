#SwissTournamentStrategy
##About:
Python mini project with PostgreSQL connection to apply the SwissPairing strategy for multi-player games.

##How to Run:
###Clone/Download repository and from within the directory execute the following commands

-->vagrant up
-->vagrant ssh
-->cd /vagrant/tournament

###Create Database and Table/View definitions
-->psql "To connect to db"
=>Execute each of the sql statements in tournament.sql file one at a time 
-->\q  "To disconnect from db"

###Run the tournament_test.py file to check the proper implementation of the requirements
-->python tournament_test.py

###Expected Result:
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!




