document.addEventListener('DOMContentLoaded', (event) => {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    const paddleWidth = 10, paddleHeight = 100;
    const ballSize = 10;
    const paddleSpeed = 10;

    let ballX = canvas.width / 2;
    let ballY = canvas.height / 2;
    let ballSpeedX = 6, ballSpeedY = 5;
    let player1Y = (canvas.height - paddleHeight) / 2;
    let player2Y = (canvas.height - paddleHeight) / 2;

    let player1Up = false, player1Down = false;
    let player2Up = false, player2Down = false;

    function drawRect(x, y, width, height, color) {
        context.fillStyle = color;
        context.fillRect(x, y, width, height);
    }

    function drawCircle(x, y, radius, color) {
        context.fillStyle = color;
        context.beginPath();
        context.arc(x, y, radius, 0, Math.PI * 2, true);
        context.closePath();
        context.fill();
    }

    function drawNet() {
        for (let i = 0; i < canvas.height; i += 15) {
            drawRect(canvas.width / 2 - 1, i, 2, 10, 'white');
        }
    }

    function resetBall() {
        ballX = canvas.width / 2;
        ballY = canvas.height / 2;
        ballSpeedX = -ballSpeedX;
    }

    function moveEverything() {
        ballX += ballSpeedX;
        ballY += ballSpeedY;

        if (ballY <= 0 || ballY >= canvas.height) {
            ballSpeedY = -ballSpeedY;
        }

        if (ballX <= 0) {
            if (ballY > player1Y && ballY < player1Y + paddleHeight) {
                ballSpeedX = -ballSpeedX;
            } else {
                resetBall();
            }
        }

        if (ballX >= canvas.width) {
            if (ballY > player2Y && ballY < player2Y + paddleHeight) {
                ballSpeedX = -ballSpeedX;
            } else {
                resetBall();
            }
        }

        if (player1Up && player1Y > 0) {
            player1Y -= paddleSpeed;
        }
        if (player1Down && player1Y < canvas.height - paddleHeight) {
            player1Y += paddleSpeed;
        }
        if (player2Up && player2Y > 0) {
            player2Y -= paddleSpeed;
        }
        if (player2Down && player2Y < canvas.height - paddleHeight) {
            player2Y += paddleSpeed;
        }
    }

    function drawEverything() {
        drawRect(0, 0, canvas.width, canvas.height, 'black');
        drawNet();
        drawRect(0, player1Y, paddleWidth, paddleHeight, 'white');
        drawRect(canvas.width - paddleWidth, player2Y, paddleWidth, paddleHeight, 'white');
        drawCircle(ballX, ballY, ballSize, 'white');
    }

    document.addEventListener('keydown', (event) => {
        switch (event.key) {
            case 'w':
                player1Up = true;
                break;
            case 's':
                player1Down = true;
                break;
            case 'ArrowUp':
                player2Up = true;
                break;
            case 'ArrowDown':
                player2Down = true;
                break;
        }
    });

    document.addEventListener('keyup', (event) => {
        switch (event.key) {
            case 'w':
                player1Up = false;
                break;
            case 's':
                player1Down = false;
                break;
            case 'ArrowUp':
                player2Up = false;
                break;
            case 'ArrowDown':
                player2Down = false;
                break;
        }
    });

    function gameLoop() {
        moveEverything();
        drawEverything();
        requestAnimationFrame(gameLoop);
    }

    gameLoop();
});
