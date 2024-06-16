import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.game_task = asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        self.game_task.cancel()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['type'] == 'move' and self.game_in_progress:
            if data['player'] == 1:
                if data['direction'] == 'up':
                    self.player1Up = True
                    self.player1Down = False
                elif data['direction'] == 'down':
                    self.player1Up = False
                    self.player1Down = True
                elif data['direction'] == 'stop':
                    self.player1Up = False
                    self.player1Down = False
            elif data['player'] == 2:
                if data['direction'] == 'up':
                    self.player2Up = True
                    self.player2Down = False
                elif data['direction'] == 'down':
                    self.player2Up = False
                    self.player2Down = True
                elif data['direction'] == 'stop':
                    self.player2Up = False
                    self.player2Down = False
        elif data['type'] == 'restart':
            await self.restart_game()  # Llamada asíncrona a restart_game

    async def game_loop(self):
        try:
            while True:
                if self.game_in_progress:
                    self.move_everything()
                    await self.send_game_state()
                await asyncio.sleep(0.03)  # 30 ms delay for ~33 FPS
        except asyncio.CancelledError:
            pass


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paddleWidth = 10
        self.paddleHeight = 100
        self.ballSize = 10
        self.paddleSpeed = 10
        self.scoreLeft = 0
        self.scoreRight = 0
        self.game_in_progress = True  # Bandera para controlar si el juego está en curso
        self.reset_ball()

        self.player1Y = (400 - self.paddleHeight) / 2
        self.player2Y = (400 - self.paddleHeight) / 2

        self.player1Up = False
        self.player1Down = False
        self.player2Up = False
        self.player2Down = False
        
    def reset_ball(self):
        self.ballX = 400
        self.ballY = 300
        if self.scoreRight > self.scoreLeft:
            self.ballSpeedX = 6  # Si el jugador derecho tiene más puntos, saca hacia la izquierda
        else:
            self.ballSpeedX = -6  # Si el jugador izquierdo tiene más puntos o igual, saca hacia la derecha
        self.ballSpeedY = 5

    def move_everything(self):
        if not self.game_in_progress:
            return
        
        self.ballX += self.ballSpeedX
        self.ballY += self.ballSpeedY

        if self.ballY <= 0 or self.ballY >= 400:
            self.ballSpeedY = -self.ballSpeedY

        if self.ballX <= 0:
            if self.ballY > self.player1Y and self.ballY < self.player1Y + self.paddleHeight:
                self.ballSpeedX = -self.ballSpeedX
            else:
                self.scoreRight += 1
                if self.scoreRight >= 1:
                    asyncio.create_task(self.handle_game_end("Jugador Derecho"))
                else:
                    self.reset_ball()

        if self.ballX >= 800:
            if self.ballY > self.player2Y and self.ballY < self.player2Y + self.paddleHeight:
                self.ballSpeedX = -self.ballSpeedX
            else:
                self.scoreLeft += 1
                if self.scoreLeft >= 1:
                    asyncio.create_task(self.handle_game_end("Jugador Izquierdo"))
                else:
                    self.reset_ball()

        if self.player1Up and self.player1Y > 0:
            self.player1Y -= self.paddleSpeed
        if self.player1Down and self.player1Y < 400 - self.paddleHeight:
            self.player1Y += self.paddleSpeed
        if self.player2Up and self.player2Y > 0:
            self.player2Y -= self.paddleSpeed
        if self.player2Down and self.player2Y < 400 - self.paddleHeight:
            self.player2Y += self.paddleSpeed

    async def handle_game_end(self, winner):
        self.game_in_progress = False  # Detener el juego
        message = f'<div class="game-end-message">{winner} ha ganado el juego! Haga clic para reiniciar.</div>'
        await self.send(text_data=json.dumps({'type': 'game_end', 'message': message}))
        self.game_task.cancel()  # Cancelar el loop del juego
        await self.send_game_state()

 
    async def send_game_state(self):
        game_state = {
            'player1Y': self.player1Y,
            'player2Y': self.player2Y,
            'ballX': self.ballX,
            'ballY': self.ballY,
            'scoreLeft': self.scoreLeft,
            'scoreRight': self.scoreRight,
            'game_in_progress': self.game_in_progress, 
        }
        await self.send(text_data=json.dumps(game_state))
    
    async def restart_game(self):
        self.scoreLeft = 0
        self.scoreRight = 0
        self.game_in_progress = True
        self.reset_ball()
        self.game_task = asyncio.create_task(self.game_loop()) # Reiniciar la tarea del juego
