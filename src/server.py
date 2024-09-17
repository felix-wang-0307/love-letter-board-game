# server.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from user.ConnectionManager import ConnectionManager
from user.User import User
from game.GameRoom import GameRoom
from game.Game import Game
from player.Player import Player
import uuid
from typing import Dict

app = FastAPI()
manager = ConnectionManager()
game_rooms: Dict[str, GameRoom] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for user connections.
    """
    user = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await handle_client_message(user, data)
    except WebSocketDisconnect:
        await manager.disconnect(user.user_id)
    except Exception as e:
        print(f"Error with user {user.user_id}: {e}")
        await manager.disconnect(user.user_id)

async def handle_client_message(user: User, data: dict):
    """
    Handles incoming messages from users.

    Args:
        user (User): The user who sent the message.
        data (dict): The message data.
    """
    message_type = data.get('type')
    if message_type == 'create_room':
        room_id = str(uuid.uuid4())[:8]
        game_room = GameRoom(room_id)
        game_rooms[room_id] = game_room
        await game_room.add_user(user)
        await user.send_message({
            'type': 'room_created',
            'room_id': room_id
        })
    elif message_type == 'join_room':
        room_id = data.get('room_id')
        game_room = game_rooms.get(room_id)
        if game_room:
            await game_room.add_user(user)
            await user.send_message({
                'type': 'room_joined',
                'room_id': room_id
            })
        else:
            await user.send_message({
                'type': 'error',
                'message': 'Room not found.'
            })
    elif message_type == 'leave_room':
        if user.current_room:
            await user.current_room.remove_user(user)
            await user.send_message({
                'type': 'room_left',
                'room_id': user.current_room.room_id
            })
    elif message_type == 'start_game':
        if user.current_room:
            await user.current_room.start_game()
    # Handle other message types...


if __name__ == "__main__":
    # simulate the frontend connection and message sending
    import asyncio

    # Mock User class (since we're not considering connections)
    class MockUser:
        def __init__(self, user_id, name):
            self.user_id = user_id
            self.name = name
            self.messages = []

        async def send_message(self, message):
            print(f"Message to {self.name}: {message}")
            self.messages.append(message)
        
    # Create mock users
    user1 = MockUser(user_id="1", name="Alice")
    user2 = MockUser(user_id="2", name="Bob")
    user3 = MockUser(user_id="3", name="Charlie")

    # Create players from mock users
    player1 = Player(user=user1)
    player2 = Player(user=user2)
    player3 = Player(user=user3)

    # Create a game with the players
    game = Game(players=[player1, player2, player3])

    async def main():
        # Initialize the game
        await game.initialize()

        # Simulate the game loop
        game.ongoing = True
        while game.ongoing:
            current_player = game.player_in_turn()
            print(f"\nCurrent player: {current_player.user.name}")
            print(f"Hand: {[card.name for card in current_player.hand]}")
            
            # Get player input for the card to play
            played_card_index = int(input("Enter the index of the card to play: "))
            played_card = current_player.hand[played_card_index]

            target_info = {}
        
            if played_card.name in ["Guard", "Baron", "Priest", "King"]:
                target_player_id = input("Enter the target player ID: ")
                target_info['target_player_id'] = target_player_id
                if played_card.name == "Guard":
                    target_card_value = input("Enter the card value to guess: ")
                    target_info['target_card_value'] = target_card_value


            # Player plays the card
            await game.handle_player_action(
                player_id=current_player.user.user_id,
                played_card_index=played_card_index,
                target_info=target_info
            )
            
            # Check if the game has ended
            if not game.ongoing:
                winners = game.determine_winner()
                print(f"Game ended. Winner(s): {[p.user.name for p in winners]}")
                break
            
            await game.next_turn()

        # After the game ends, you can inspect scores or start a new round

    # Run the async main function
    asyncio.run(main())

