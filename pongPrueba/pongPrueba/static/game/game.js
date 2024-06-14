document.addEventListener('DOMContentLoaded', (event) => {
    const canvas = document.getElementById('pongCanvas');
    const context = canvas.getContext('2d');

    const paddleWidth = 10, paddleHeight = 100;
    const ballSize = 10;
    const paddleSpeed = 10;

    let ballX = canvas.width / 2;
    let ballY = canvas.height / 2;
    let ballSpeedX = 5, ballSpeedY = 4;
    let player1Y = (canvas.height - paddleHeight) / 2;
    let player2Y = (canvas.height - paddleHeight) / 2;

    let player1Up = false, player1Down = false;
    let player2Up = false, player2Down = false;

    let player1Score = 0, player2Score = 0;
    const winningScore = 5;
    let showingWinScreen = false;

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

    function drawScore() {
        context.fillStyle = 'white';
        context.font = '300px Arial';
        context.textAlign = 'center';
        context.fillText(player1Score, canvas.width / 4, canvas.height / 2 + 100);
        context.fillText(player2Score, 3 * canvas.width / 4, canvas.height / 2 + 100);
    }

    function drawWinScreen() {
        context.fillStyle = 'white';
        context.font = '30px Arial';
        context.textAlign = 'center';
        if (player1Score >= winningScore) {
            context.fillText("Player 1 Wins!", canvas.width / 2, canvas.height / 2);
        } else if (player2Score >= winningScore) {
            context.fillText("Player 2 Wins!", canvas.width / 2, canvas.height / 2);
        }
        context.fillText("Click to Restart", canvas.width / 2, canvas.height / 2 + 50);
    }

    function resetBall() {
        if (player1Score >= winningScore || player2Score >= winningScore) {
            showingWinScreen = true;
        }
        ballX = canvas.width / 2;
        ballY = canvas.height / 2;
        ballSpeedX = -ballSpeedX;
    }

    function moveEverything() {
        if (showingWinScreen) {
            return;
        }

        ballX += ballSpeedX;
        ballY += ballSpeedY;

        if (ballY <= 0 || ballY >= canvas.height) {
            ballSpeedY = -ballSpeedY;
        }

        if (ballX <= 0) {
            if (ballY > player1Y && ballY < player1Y + paddleHeight) {
                ballSpeedX = -ballSpeedX;
            } else {
                player2Score++;
                resetBall();
            }
        }

        if (ballX >= canvas.width) {
            if (ballY > player2Y && ballY < player2Y + paddleHeight) {
                ballSpeedX = -ballSpeedX;
            } else {
                player1Score++;
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
        
        if (!showingWinScreen) {
            drawScore();
        } else {
            context.clearRect(0, 0, canvas.width, canvas.height);
            drawWinScreen();
        }
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

    canvas.addEventListener('click', (event) => {
        if (showingWinScreen) {
            player1Score = 0;
            player2Score = 0;
            showingWinScreen = false;
        }
    });

    function gameLoop() {
        moveEverything();
        drawEverything();
        requestAnimationFrame(gameLoop);
    }

    gameLoop();
});
