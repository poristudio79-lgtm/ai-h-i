<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flappy Bird Game</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #1a1a1a;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: 'Courier New', Courier, monospace;
            user-select: none;
        }
        #game-container {
            position: relative;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border-radius: 8px;
            overflow: hidden;
        }
        canvas {
            display: block;
            background: #70c5ce;
        }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="birdCanvas" width="360" height="640"></canvas>
</div>

<script>
const canvas = document.getElementById('birdCanvas');
const ctx = canvas.getContext('2d');

// --- HỆ THỐNG ÂM THANH 8-BIT (WEB AUDIO API) ---
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

function playSound(type) {
    if (audioCtx.state === 'suspended') {
        audioCtx.resume();
    }
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    const now = audioCtx.currentTime;

    if (type === 'jump') {
        osc.type = 'square';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.1);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.1);
        osc.start(now);
        osc.stop(now + 0.1);
    } else if (type === 'score') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, now);
        osc.frequency.setValueAtTime(659.25, now + 0.08);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
        osc.start(now);
        osc.stop(now + 0.2);
    } else if (type === 'hit') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.linearRampToValueAtTime(40, now + 0.15);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.15);
        osc.start(now);
        osc.stop(now + 0.15);
    }
}

// --- BIẾN TRẠNG THÁI GAME ---
let gameState = 'START'; // START, PLAYING, GAMEOVER
let score = 0;
let highScore = localStorage.getItem('fb_highscore') || 0;
let frames = 0;

// --- ĐỐI TƯỢNG CHIM ---
const bird = {
    x: 60,
    y: 250,
    radius: 12,
    gravity: 0.25,
    jumpForce: -4.6,
    velocity: 0,

    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);

        // Góc xoay theo vận tốc
        let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (this.velocity / 10)));
        ctx.rotate(rotation);

        // Thân chim
        ctx.fillStyle = '#f7d547';
        ctx.beginPath();
        ctx.arc(0, 0, this.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#000';
        ctx.stroke();

        // Mắt
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(4, -4, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#000';
        ctx.beginPath();
        ctx.arc(5, -4, 1.5, 0, Math.PI * 2);
        ctx.fill();

        // Mỏ
        ctx.fillStyle = '#f35b04';
        ctx.beginPath();
        ctx.arc(6, 2, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    },

    update() {
        this.velocity += this.gravity;
        this.y += this.velocity;

        // Va chạm trần
        if (this.y - this.radius <= 0) {
            this.y = this.radius;
            this.velocity = 0;
        }

        // Va chạm đất
        if (this.y + this.radius >= canvas.height - 80) {
            this.y = canvas.height - 80 - this.radius;
            triggerGameOver();
        }
    },

    jump() {
        this.velocity = this.jumpForce;
        playSound('jump');
    },

    reset() {
        this.y = 250;
        this.velocity = 0;
    }
};

// --- QUẢN LÝ ỐNG CỐNG ---
const pipes = {
    items: [],
    gap: 120,
    width: 52,
    speed: 2,

    draw() {
        this.items.forEach(p => {
            ctx.fillStyle = '#73bf2e';
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 2;

            // Ống trên
            ctx.fillRect(p.x, 0, this.width, p.top);
            ctx.strokeRect(p.x, 0, this.width, p.top);

            // Ống dưới
            ctx.fillRect(p.x, p.bottom, this.width, canvas.height - 80 - p.bottom);
            ctx.strokeRect(p.x, p.bottom, this.width, canvas.height - 80 - p.bottom);
        });
    },

    update() {
        // Tạo ống mới mỗi 100 khung hình
        if (frames % 100 === 0) {
            let maxTop = canvas.height - 80 - this.gap - 50;
            let minTop = 50;
            let top = Math.floor(Math.random() * (maxTop - minTop + 1)) + minTop;

            this.items.push({
                x: canvas.width,
                top: top,
                bottom: top + this.gap,
                passed: false
            });
        }

        this.items.forEach((p, index) => {
            p.x -= this.speed;

            // Kiểm tra va chạm với chim
            if (
                bird.x + bird.radius > p.x &&
                bird.x - bird.radius < p.x + this.width &&
                (bird.y - bird.radius < p.top || bird.y + bird.radius > p.bottom)
            ) {
                triggerGameOver();
            }

            // Ghi điểm khi vượt qua ống
            if (p.x + this.width < bird.x && !p.passed) {
                p.passed = true;
                score++;
                playSound('score');
                if (score > highScore) {
                    highScore = score;
                    localStorage.setItem('fb_highscore', highScore);
                }
            }

            // Xóa ống ngoài màn hình
            if (p.x + this.width < 0) {
                this.items.splice(index, 1);
            }
        });
    },

    reset() {
        this.items = [];
    }
};

// --- MẶT ĐẤT VÀ NỀN ---
function drawGround() {
    ctx.fillStyle = '#ded895';
    ctx.fillRect(0, canvas.height - 80, canvas.width, 80);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, canvas.height - 80);
    ctx.lineTo(canvas.width, canvas.height - 80);
    ctx.stroke();

    // Họa tiết cỏ trên mặt đất
    ctx.fillStyle = '#73bf2e';
    ctx.fillRect(0, canvas.height - 80, canvas.width, 14);
}

// --- GIAO DIỆN (UI) ---
function drawUI() {
    ctx.fillStyle = '#fff';
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 3;

    if (gameState === 'START') {
        ctx.font = '28px Courier New';
        ctx.textAlign = 'center';
        ctx.strokeText('FLAPPY BIRD', canvas.width / 2, 200);
        ctx.fillText('FLAPPY BIRD', canvas.width / 2, 200);

        ctx.font = '16px Courier New';
        ctx.strokeText('Nhấn SPACE hoặc CHẠM để chơi', canvas.width / 2, 300);
        ctx.fillText('Nhấn SPACE hoặc CHẠM để chơi', canvas.width / 2, 300);
    } else if (gameState === 'PLAYING') {
        ctx.font = '36px Courier New';
        ctx.textAlign = 'center';
        ctx.strokeText(score, canvas.width / 2, 60);
        ctx.fillText(score, canvas.width / 2, 60);
    } else if (gameState === 'GAMEOVER') {
        ctx.font = '30px Courier New';
        ctx.textAlign = 'center';
        ctx.strokeText('GAME OVER', canvas.width / 2, 180);
        ctx.fillText('GAME OVER', canvas.width / 2, 180);

        ctx.font = '18px Courier New';
        ctx.strokeText(`Điểm: ${score}`, canvas.width / 2, 250);
        ctx.fillText(`Điểm: ${score}`, canvas.width / 2, 250);

        ctx.strokeText(`Cao nhất: ${highScore}`, canvas.width / 2, 280);
        ctx.fillText(`Cao nhất: ${highScore}`, canvas.width / 2, 280);

        ctx.font = '14px Courier New';
        ctx.strokeText('Chạm hoặc bấm SPACE để chơi lại', canvas.width / 2, 350);
        ctx.fillText('Chạm hoặc bấm SPACE để chơi lại', canvas.width / 2, 350);
    }
}

function triggerGameOver() {
    if (gameState !== 'GAMEOVER') {
        playSound('hit');
        gameState = 'GAMEOVER';
    }
}

// --- VÒNG LẶP CHÍNH (GAME LOOP) ---
function loop() {
    // 1. Vẽ nền Canvas
    ctx.fillStyle = '#70c5ce';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Cập nhật & Vẽ đối tượng
    if (gameState === 'PLAYING') {
        bird.update();
        pipes.update();
        frames++;
    }

    pipes.draw();
    drawGround();
    bird.draw();
    drawUI();

    requestAnimationFrame(loop);
}

// --- XỬ LÝ SỰ KIỆN ĐIỀU KHIỂN ---
function handleInput() {
    if (gameState === 'START') {
        gameState = 'PLAYING';
        bird.jump();
    } else if (gameState === 'PLAYING') {
        bird.jump();
    } else if (gameState === 'GAMEOVER') {
        bird.reset();
        pipes.reset();
        score = 0;
        frames = 0;
        gameState = 'PLAYING';
    }
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        e.preventDefault();
        handleInput();
    }
});

canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    handleInput();
});

canvas.addEventListener('mousedown', (e) => {
    handleInput();
});

// Chạy game
loop();
</script>

</body>
</html>
