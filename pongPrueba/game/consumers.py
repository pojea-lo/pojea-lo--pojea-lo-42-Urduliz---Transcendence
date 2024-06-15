import json

from channels.generic.websocket import WebsocketConsumer


class PongConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        self.send(text_data=json.dumps({
            'message': text_data_json['message'],
            'player1Y': text_data_json['player1Y'],
            'player2Y': text_data_json['player2Y'],
            'ballX': text_data_json['ballX'],
            'ballY': text_data_json['ballY'],
            'player1Score': text_data_json['player1Score'],
            'player2Score': text_data_json['player2Score'],
        }))