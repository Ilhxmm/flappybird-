const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const overlay = document.getElementById('gameOverlay');
const retryButton = document.getElementById('retryButton');
const scoreElement = document.getElementById('score');
const startScreen = document.getElementById('startScreen');
const startButton = document.getElementById('startButton');

const WIN_WIDTH = canvas.width;
const WIN_HEIGHT = canvas.height;
const PIPE_WIDTH = 70;
const PIPE_GAP = 150;
const BIRD_WIDTH = 50;  // Updated width
const BIRD_HEIGHT = 40; // Updated height
const GRAVITY = 0.5;
const FLAP_STRENGTH = -10;
const PIPE_SPEED = 5;

// Load images
const birdImage = new Image();
birdImage.src = 'https://i.postimg.cc/6yTjy0R8/bird.png'; // Updated URL
const backgroundImage = new Image();
backgroundImage.src = 'https://i.postimg.cc/n9FWRfC2/background.png';
const pipeImage = new Image();
pipeImage.src = 'https://i.postimg.cc/YjMTqYbF/pipe.png';

let bird = {
    x: 50,
    y: WIN_HEIGHT / 2,
    velocity: 0,
    width: BIRD_WIDTH,
    height: BIRD_HEIGHT
};

let pipes = [{ x: WIN_WIDTH, height: Math.random() * (WIN_HEIGHT - 150) + 50, passed: false }];
let score = 0;
let gameStarted = false;
let isFlapping = false; // To track if the bird is flapping

function drawBackground() {
    ctx.drawImage(backgroundImage, 0, 0, WIN_WIDTH, WIN_HEIGHT);
}

function drawBird() {
    ctx.drawImage(birdImage, bird.x, bird.y, bird.width, bird.height);
}

function drawPipe(pipe) {
    // Draw top pipe
    ctx.drawImage(pipeImage, pipe.x, 0, PIPE_WIDTH, pipe.height);
    // Draw bottom pipe
    ctx.drawImage(pipeImage, pipe.x, pipe.height + PIPE_GAP, PIPE_WIDTH, WIN_HEIGHT - pipe.height - PIPE_GAP);
}

function drawScore() {
    ctx.font = '30px Arial'; // Set font size and type
    ctx.fillStyle = 'yellow'; // Set text color to yellow
    ctx.textAlign = 'right'; // Align text to the right
    ctx.fillText(`Score: ${score}`, WIN_WIDTH - 20, 40); // Position text at the top-right
}

function updateBird() {
    bird.velocity += GRAVITY;
    bird.y += bird.velocity;
    
    // Keep bird within canvas boundaries
    if (bird.y < 0) bird.y = 0;
    if (bird.y + bird.height > WIN_HEIGHT) bird.y = WIN_HEIGHT - bird.height;

    // Reset flap state after applying the flap strength
    if (isFlapping) {
        bird.velocity = FLAP_STRENGTH;
        isFlapping = false;
    }
}

function updatePipes() {
    for (const pipe of pipes) {
        pipe.x -= PIPE_SPEED;
        if (pipe.x + PIPE_WIDTH < 0) {
            pipes.shift();
            pipes.push({
                x: WIN_WIDTH,
                height: Math.random() * (WIN_HEIGHT - 150) + 50,
                passed: false
            });
            score++;
        }
    }
}

function checkCollision() {
    for (const pipe of pipes) {
        if (bird.x + bird.width > pipe.x && bird.x < pipe.x + PIPE_WIDTH) {
            if (bird.y < pipe.height || bird.y + bird.height > pipe.height + PIPE_GAP) {
                return true;
            }
        }
    }
    return bird.y < 0 || bird.y + bird.height > WIN_HEIGHT;
}

function gameLoop() {
    drawBackground();
    drawBird();
    for (const pipe of pipes) {
        drawPipe(pipe);
    }

    updateBird();
    updatePipes();

    drawScore(); // Call the function to draw the score

    if (checkCollision()) {
        endGame();
        return;
    }

    requestAnimationFrame(gameLoop);
}

function endGame() {
    overlay.classList.remove('hidden');
    scoreElement.textContent = `Final Score: ${score}`; // Display final score on overlay
}

function resetGame() {
    bird = { x: 50, y: WIN_HEIGHT / 2, velocity: 0, width: BIRD_WIDTH, height: BIRD_HEIGHT };
    pipes = [{ x: WIN_WIDTH, height: Math.random() * (WIN_HEIGHT - 150) + 50, passed: false }];
    score = 0;
    scoreElement.textContent = `Score: ${score}`;
    overlay.classList.add('hidden');
    startScreen.classList.remove('hidden');
    gameStarted = false;
}

function startGame() {
    startScreen.classList.add('hidden');
    gameStarted = true;
    gameLoop();
}

retryButton.addEventListener('click', resetGame);
startButton.addEventListener('click', startGame);

// Handle mouse and touch events
canvas.addEventListener('mousedown', (e) => {
    e.preventDefault(); // Prevent default behavior
    if (gameStarted) {
        isFlapping = true;
    }
});

canvas.addEventListener('touchstart', (e) => {
    e.preventDefault(); // Prevent default behavior
    if (gameStarted) {
        isFlapping = true;
    }
});
