import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird - Multi Character", layout="centered")

# Mã nguồn HTML / CSS / JS của Game
game_html = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flappy Bird Game</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
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
        canvas { display: block; background: #70c5ce; }
    </style>
</head>
<body>

<div id="game-container">
    <canvas id="birdCanvas" width="360" height="640"></canvas>
</div>

<script>
const canvas = document.getElementById('birdCanvas');
const ctx = canvas.getContext('2d');

// --- ÂM THANH 8-BIT ---
const AudioContext = window.AudioContext || window.webkitAudioContext;
const audioCtx = new AudioContext();

function playSound(type) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
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
        osc.start(now); osc.stop(now + 0.1);
    } else if (type === 'score') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, now);
        osc.frequency.setValueAtTime(659.25, now + 0.08);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.2);
        osc.start(now); osc.stop(now + 0.2);
    } else if (type === 'hit') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, now);
        osc.frequency.linearRampToValueAtTime(40, now + 0.15);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0.01, now + 0.15);
        osc.start(now); osc.stop(now + 0.15);
    }
}

// --- TRẠNG THÁI GAME ---
let gameState = 'START'; // START, CHARACTERS, PLAYING, GAMEOVER
let score = 0;
let highScore = localStorage.getItem('fb_highscore') || 0;
let frames = 0;
let selectedSkin = 0;

// DANH SÁCH NHÂN VẬT
const CHARACTERS = [
    { id: 0, name: 'CỔ ĐỂN', color: '#f8d038' },
    { id: 1, name: 'BĂNG BĂNG', color: '#f8ea38' },
    { id: 2, name: 'NÓN LÁ', color: '#509848' },
    { id: 3, name: 'HOÀNG GIA', color: '#8838d0' },
    { id: 4, name: 'KỲ LÂN BIỂN', color: '#38a8b8' }
];

// Nút chọn nhân vật trong Menu
const charBtn = { x: 80, y: 380, w: 200, h: 45 };

// --- HÀM VẼ CÁC NHÂN VẬT PIXEL ---
function drawPixelBird(x, y, skinId, scale = 2) {
    ctx.save();
    ctx.translate(x, y);
    const p = scale;

    if (skinId === 0) { // 1. Chim Vàng Gốc
        ctx.fillStyle = '#4a403a'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#f8d038'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#f8b000'; ctx.fillRect(-6*p, 2*p, 10*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -6*p, 7*p, 6*p);
        ctx.fillStyle = '#4a403a'; ctx.fillRect(3*p, -4*p, 2*p, 3*p);
        ctx.fillStyle = '#f85820'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    } 
    else if (skinId === 1) { // 2. Chim Băng Băng (Headband & Mỏ Hồng)
        ctx.fillStyle = '#4a403a'; ctx.fillRect(-8*p, -7*p, 16*p, 13*p);
        ctx.fillStyle = '#f8ea38'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        // Băng đô hồng
        ctx.fillStyle = '#e82878'; ctx.fillRect(-7*p, -7*p, 14*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-4*p, -7*p, 2*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -4*p, 7*p, 5*p);
        ctx.fillStyle = '#4a403a'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        // Mỏ hồng đậm
        ctx.fillStyle = '#e82878'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, 0*p, 4*p, 3*p);
    } 
    else if (skinId === 2) { // 3. Chim Đội Nón Lá Green
        ctx.fillStyle = '#303030'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#509848'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        // Nón xanh lá
        ctx.fillStyle = '#78c038'; ctx.fillRect(-5*p, -10*p, 10*p, 4*p);
        ctx.fillRect(-7*p, -7*p, 14*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#303030'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        // Mỏ cam lá
        ctx.fillStyle = '#f87820'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 3) { // 4. Chim Vương Miện Tím
        ctx.fillStyle = '#302040'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#8838d0'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        // Vương miện hồng
        ctx.fillStyle = '#f858a8'; ctx.fillRect(-6*p, -10*p, 11*p, 4*p);
        ctx.fillRect(-7*p, -8*p, 2*p, 2*p); ctx.fillRect(-2*p, -8*p, 2*p, 2*p); ctx.fillRect(3*p, -8*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#302040'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#f89020'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#f878c0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 4) { // 5. Kỳ Lân Biển (Unicorn Blue)
        ctx.fillStyle = '#203840'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#38a8b8'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        // Sừng kỳ lân tím
        ctx.fillStyle = '#c048d0'; ctx.fillRect(3*p, -11*p, 3*p, 5*p);
        ctx.fillStyle = '#f878e8'; ctx.fillRect(4*p, -9*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#203840'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#306870'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#78e0f0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }

    ctx.restore();
}

// --- ĐỐI TƯỢNG CHIM ---
const bird = {
    x: 60, y: 250, radius: 12, gravity: 0.25, jumpForce: -4.6, velocity: 0,
    draw() {
        ctx.save();
        ctx.translate(this.x, this.y);
        let rotation = Math.min(Math.PI / 4, Math.max(-Math.PI / 4, (this.velocity / 10)));
        ctx.rotate(rotation);
        ctx.restore();

        drawPixelBird(this.x, this.y, selectedSkin, 1.8);
    },
    update() {
        this.velocity += this.gravity;
        this.y += this.velocity;
        if (this.y - this.radius <= 0) { this.y = this.radius; this.velocity = 0; }
        if (this.y + this.radius >= canvas.height - 80) {
            this.y = canvas.height - 80 - this.radius;
            triggerGameOver();
        }
    },
    jump() { this.velocity = this.jumpForce; playSound('jump'); },
    reset() { this.y = 250; this.velocity = 0; }
};

// --- QUẢN LÝ ỐNG CỐNG ---
const pipes = {
    items: [], gap: 125, width: 52, speed: 2,
    draw() {
        this.items.forEach(p => {
            ctx.fillStyle = '#73bf2e'; ctx.strokeStyle = '#000'; ctx.lineWidth = 2;
            ctx.fillRect(p.x, 0, this.width, p.top);
            ctx.strokeRect(p.x, 0, this.width, p.top);
            ctx.fillRect(p.x, p.bottom, this.width, canvas.height - 80 - p.bottom);
            ctx.strokeRect(p.x, p.bottom, this.width, canvas.height - 80 - p.bottom);
        });
    },
    update() {
        if (frames % 100 === 0) {
            let maxTop = canvas.height - 80 - this.gap - 50;
            let minTop = 50;
            let top = Math.floor(Math.random() * (maxTop - minTop + 1)) + minTop;
            this.items.push({ x: canvas.width, top: top, bottom: top + this.gap, passed: false });
        }
        this.items.forEach((p, index) => {
            p.x -= this.speed;
            if (bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.width &&
               (bird.y - bird.radius < p.top || bird.y + bird.radius > p.bottom)) {
                triggerGameOver();
            }
            if (p.x + this.width < bird.x && !p.passed) {
                p.passed = true; score++; playSound('score');
                if (score > highScore) { highScore = score; localStorage.setItem('fb_highscore', highScore); }
            }
            if (p.x + this.width < 0) this.items.splice(index, 1);
        });
    },
    reset() { this.items = []; }
};

function drawGround() {
    ctx.fillStyle = '#ded895'; ctx.fillRect(0, canvas.height - 80, canvas.width, 80);
    ctx.strokeStyle = '#000'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(0, canvas.height - 80); ctx.lineTo(canvas.width, canvas.height - 80); ctx.stroke();
    ctx.fillStyle = '#73bf2e'; ctx.fillRect(0, canvas.height - 80, canvas.width, 14);
}

// --- MÀN HÌNH CHỌN NHÂN VẬT ---
function drawCharacterSelect() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#fff'; ctx.strokeStyle = '#000'; ctx.lineWidth = 3;
    ctx.font = '24px Courier New'; ctx.textAlign = 'center';
    ctx.strokeText('CHỌN NHÂN VẬT', canvas.width / 2, 70);
    ctx.fillText('CHỌN NHÂN VẬT', canvas.width / 2, 70);

    // Vẽ lưới các nhân vật (2 cột x 3 hàng)
    CHARACTERS.forEach((char, i) => {
        let col = i % 2;
        let row = Math.floor(i / 2);
        let cx = 90 + col * 180;
        let cy = 160 + row * 130;

        // Ô khung nhân vật
        ctx.fillStyle = (selectedSkin === i) ? '#f8d038' : '#2a2a2a';
        ctx.strokeStyle = '#fff'; ctx.lineWidth = (selectedSkin === i) ? 4 : 2;
        ctx.fillRect(cx - 65, cy - 45, 130, 90);
        ctx.strokeRect(cx - 65, cy - 45, 130, 90);

        // Vẽ nhân vật đại diện
        drawPixelBird(cx, cy - 10, i, 2);

        // Tên nhân vật
        ctx.fillStyle = (selectedSkin === i) ? '#000' : '#fff';
        ctx.font = '12px Courier New';
        ctx.fillText(char.name, cx, cy + 30);
    });

    // Nút Bắt đầu
    ctx.fillStyle = '#73bf2e'; ctx.fillRect(80, 530, 200, 50);
    ctx.strokeStyle = '#fff'; ctx.strokeRect(80, 530, 200, 50);
    ctx.fillStyle = '#fff'; ctx.font = '20px Courier New';
    ctx.fillText('BẮT ĐẦU CHƠI', canvas.width / 2, 562);
}

// --- GIAO DIỆN UI MENU / GAMEOVER ---
function drawUI() {
    ctx.fillStyle = '#fff'; ctx.strokeStyle = '#000'; ctx.lineWidth = 3;
    if (gameState === 'START') {
        ctx.font = '28px Courier New'; ctx.textAlign = 'center';
        ctx.strokeText('FLAPPY BIRD', canvas.width / 2, 180);
        ctx.fillText('FLAPPY BIRD', canvas.width / 2, 180);

        // Vẽ nhân vật đang chọn
        drawPixelBird(canvas.width / 2, 250, selectedSkin, 2.5);

        ctx.font = '15px Courier New';
        ctx.strokeText('Nhấn SPACE / CHẠM để chơi', canvas.width / 2, 330);
        ctx.fillText('Nhấn SPACE / CHẠM để chơi', canvas.width / 2, 330);

        // Nút Mở Menu Nhân Vật
        ctx.fillStyle = '#f85820'; ctx.fillRect(charBtn.x, charBtn.y, charBtn.w, charBtn.h);
        ctx.strokeRect(charBtn.x, charBtn.y, charBtn.w, charBtn.h);
        ctx.fillStyle = '#fff'; ctx.font = '16px Courier New';
        ctx.fillText('NHÂN VẬT 🎭', canvas.width / 2, charBtn.y + 28);

    } else if (gameState === 'CHARACTERS') {
        drawCharacterSelect();
    } else if (gameState === 'PLAYING') {
        ctx.font = '36px Courier New'; ctx.textAlign = 'center';
        ctx.strokeText(score, canvas.width / 2, 60);
        ctx.fillText(score, canvas.width / 2, 60);
    } else if (gameState === 'GAMEOVER') {
        ctx.font = '30px Courier New'; ctx.textAlign = 'center';
        ctx.strokeText('GAME OVER', canvas.width / 2, 180);
        ctx.fillText('GAME OVER', canvas.width / 2, 180);

        drawPixelBird(canvas.width / 2, 220, selectedSkin, 2);

        ctx.font = '18px Courier New';
        ctx.strokeText(`Điểm: ${score}`, canvas.width / 2, 280);
        ctx.fillText(`Điểm: ${score}`, canvas.width / 2, 280);
        ctx.strokeText(`Cao nhất: ${highScore}`, canvas.width / 2, 310);
        ctx.fillText(`Cao nhất: ${highScore}`, canvas.width / 2, 310);

        ctx.font = '14px Courier New';
        ctx.strokeText('Chạm hoặc Bấm SPACE chơi lại', canvas.width / 2, 370);
        ctx.fillText('Chạm hoặc Bấm SPACE chơi lại', canvas.width / 2, 370);
    }
}

function triggerGameOver() {
    if (gameState !== 'GAMEOVER') { playSound('hit'); gameState = 'GAMEOVER'; }
}

function loop() {
    ctx.fillStyle = '#70c5ce'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    if (gameState === 'PLAYING') {
        bird.update(); pipes.update(); frames++;
    }
    pipes.draw(); drawGround();
    if (gameState !== 'START' && gameState !== 'CHARACTERS') bird.draw();
    drawUI();
    requestAnimationFrame(loop);
}

// XỬ LÝ CLICK / TOUCH
function handleInteraction(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const clickX = clientX - rect.left;
    const clickY = clientY - rect.top;

    if (gameState === 'START') {
        // Kiểm tra xem người dùng có bấm vào nút NHÂN VẬT không
        if (clickX >= charBtn.x && clickX <= charBtn.x + charBtn.w &&
            clickY >= charBtn.y && clickY <= charBtn.y + charBtn.h) {
            gameState = 'CHARACTERS';
            return;
        }
        gameState = 'PLAYING'; bird.jump();
    } 
    else if (gameState === 'CHARACTERS') {
        // Chọn nhân vật trong bảng
        CHARACTERS.forEach((char, i) => {
            let col = i % 2; let row = Math.floor(i / 2);
            let cx = 90 + col * 180; let cy = 160 + row * 130;
            if (clickX >= cx - 65 && clickX <= cx + 65 && clickY >= cy - 45 && clickY <= cy + 45) {
                selectedSkin = i;
            }
        });
        // Bấm nút BẮT ĐẦU CHƠI
        if (clickX >= 80 && clickX <= 280 && clickY >= 530 && clickY <= 580) {
            bird.reset(); pipes.reset(); score = 0; frames = 0;
            gameState = 'PLAYING'; bird.jump();
        }
    } 
    else if (gameState === 'PLAYING') {
        bird.jump();
    } 
    else if (gameState === 'GAMEOVER') {
        bird.reset(); pipes.reset(); score = 0; frames = 0;
        gameState = 'PLAYING';
    }
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        e.preventDefault();
        if (gameState === 'CHARACTERS') {
            gameState = 'PLAYING'; bird.jump();
        } else {
            handleInteraction(-100, -100);
        }
    }
});

canvas.addEventListener('mousedown', (e) => handleInteraction(e.clientX, e.clientY));
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    const touch = e.touches[0];
    handleInteraction(touch.clientX, touch.clientY);
});

loop();
</script>
</body>
</html>
"""

# Hiển thị Game lên ứng dụng Streamlit
components.html(game_html, height=660)
