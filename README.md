# plangrid_rock_paper_scissors

The tests are doctests. They are run automatically, but to get the output of the tests, simply run "python rps.py -v".

To play give a game history file, and the names of two players via the command line like so: "python rps.py /tmp/history stephan joe". It will then prompt you to enter the prefix of rock, paper, or scissors.

If you would like to play my ai opponent give the name "mafaldo" as one of the players. e.g. "python rps.py /tmp/history stephan mafaldo". Mafaldo chooses moves proportional to the number of times the other player would have lost to them in the game history.

