# EFL-Stops-Parser
A script for the Elite Football League to read play by plays exported from the sim engine to determine the amount of defensive "stops" every player in the league got.
The script does this by downloading each game of a season from the game index, then reading each line of the play by play downloaded to determine if the play ended in a defensive stop.
If the play ended in a stop, the script keeps track of it in a array and exports that array into a csv file after it has run through all of the games.
