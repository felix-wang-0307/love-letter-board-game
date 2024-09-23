# Love Letter Board Game
The implementation of a multiplayer card game called [Love Letter](https://en.wikipedia.org/wiki/Love_Letter_(card_game)).
## Implementation
Backend: 
- Implementing WebSocket Connection using Python FastAPI
- Adopt `typings` for type hints

Frontend (not implement yet):
React + AntDesign 

## Game Rules (Wikipedia)
- At the start of each round, one card is discarded face-down (four cards with three of them face-up if playing with two players; so the process of elimination cannot be used to prove which cards are left for the round), one card is dealt to each player and the rest are deposited face-down in the middle to form a draw deck.
- During each player's turn, one card is drawn from the deck and the player gets to play either that card or the card already in their hand.
- After processing the effect described on the played card, the next player to the left gets a turn.
- This process is repeated until either the deck runs out, in which case the player holding the highest-value card wins the round, or all players but one are eliminated, in which case the last player still in play wins the round.
- Once a round ends, the winner of the round receives a favor token. All cards are collected and shuffled, and play continues with a new round, with the winner of the previous round taking the first turn.
- The game ends when one player has obtained a predetermined number of favor tokens (from 3 to 7, depending on the number of players), winning the game for that player.
