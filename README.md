# Tournament-Database

Welcome! This project is for the Fullstack Nanodegree program from Udacity. It is a tournament database that follows the swiss tournament system.

Instructions

1. Make sure you install vagrant. For information on installation and set up, click on this link https://goo.gl/LacvLA (You will first have to log on to udacity).

2.Start Vagrant

 -Once you intalled vagrant and cloned this repo, open up a terminal and go to the vagrant directory

 -Once in there type in 'vagrant up'

 -The first time it make take some time (10 mins) but once it is complete type 'vagrant ssh'. This is so you can log in to virtual machine.

 3.Once logged in, type in 'cd /vagrant/tournament'
 	-Type in psql and then type '\i tournament.sql'(this will create the database and connect it to)

 4. Run the tests and enjoy!
 	-In terminal type in python tournament_test.py

 As a result, you will see:

 vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py 
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!



