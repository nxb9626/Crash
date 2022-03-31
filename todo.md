- scope was a bit too big so

- giving up on timed input
    - adapting based on nubmer of moves into the game. not as fun but I can't expect anyone playing agasint this to actually be able to play against it timed.
    - model building doesn't have it so not can't really do anything other than online learning to get that, or playing timed games against self, which sin't viable
    
- minimax a bit too slow to allow for deeper searches, 3 moves ahead doesn't seem to be far enough
    - checking for repeat boards was good, but not enough
    - minimax ab pruning
    - multithread it

- building "model" against previously played games in the lichesss database
    - basically running the utility function against each move of each game, and based on the players elo and whether they won the game increasing the value of that metric at that move in the game
        - is horribly over simplified way of thinking about the game but it kinda needs to be as the scope of this is not feasible otherwise
