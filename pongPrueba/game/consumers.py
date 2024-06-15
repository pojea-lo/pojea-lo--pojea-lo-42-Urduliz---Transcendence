# game/consumers.py
import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'pong_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Initialize game state
        self.game_state = self.get_initial_game_state()
        await self.send_game_state()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'move_paddle':
            player = text_data_json['player']
            direction = text_data_json['direction']
            self.update_paddle_position(player, direction)
        elif action == 'restart':
            self.restart_game()

        # Update the game state
        self.update_ball_position()
        self.check_collisions()
        await self.send_game_state()

    async def send_game_state(self):
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'game_state': self.game_state
        }))

    def get_initial_game_state(self):
        return {
            'ball_position': [400, 200],
            'ball_velocity': [5, 4],
            'paddle1_position': 150,
            'paddle2_position': 150,
            'player1_score': 0,
            'player2_score': 0,
            'showing_win_screen': False
        }

    def update_paddle_position(self, player, direction):
        paddle_speed = 10
        if player == 'player1':
            if direction == 'up':
                self.game_state['paddle1_position'] = max(0, self.game_state['paddle1_position'] - paddle_speed)
            elif direction == 'down':
                self.game_state['paddle1_position'] = min(300, self.game_state['paddle1_position'] + paddle_speed)
        elif player == 'player2':
            if direction == 'up':
                self.game_state['paddle2_position'] = max(0, self.game_state['paddle2_position'] - paddle_speed)
            elif direction == 'down':
                self.game_state['paddle2_position'] = min(300, self.game_state['paddle2_position'] + paddle_speed)

    def update_ball_position(self):
        if self.game_state['showing_win_screen']:
            return

        ball = self.game_state['ball_position']
        velocity = self.game_state['ball_velocity']

        ball[0] += velocity[0]
        ball[1] += velocity[1]

        # Ball collision with top or bottom
        if ball[1] <= 0 or ball[1] >= 400:
            velocity[1] = -velocity[1]

        self.game_state['ball_position'] = ball
        self.game_state['ball_velocity'] = velocity

    def check_collisions(self):
        ball = self.game_state['ball_position']
        velocity = self.game_state['ball_velocity']

        if ball[0] <= 0:
            if self.game_state['paddle1_position'] < ball[1] < self.game_state['paddle1_position'] + 100:
                velocity[0] = -velocity[0]
            else:
                self.game_state['player2_score'] += 1
                self.reset_ball()

        if ball[0] >= 800:
            if self.game_state['paddle2_position'] < ball[1] < self.game_state['paddle2_position'] + 100:
                velocity[0] = -velocity[0]
            else:
                self.game_state['player1_score'] += 1
                self.reset_ball()

        self.game_state['ball_velocity'] = velocity

    def reset_ball(self):
        self.game_state['ball_position'] = [400, 200]
        self.game_state['ball_velocity'] = [-self.game_state['ball_velocity'][0], random.choice([-4, 4])]
        if self.game_state['player1_score'] >= 5 or self.game_state['player2_score'] >= 5:
            self.game_state['showing_win_screen'] = True

    def restart_game(self):
        self.game_state = self.get_initial_game_state()
