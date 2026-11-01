import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird - Multi Character", layout="centered")

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
    <canvas id="birdCanvas" width="480" height="640"></canvas>
</div>

<script>
const canvas = document.getElementById('birdCanvas');
const ctx = canvas.getContext('2d');

// --- HỆ THỐNG ÂM THANH 8-BIT ---
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
let selectedSkin = 1; // Mặc định là OHINH (Vàng gốc)

// 6 NHÂN VẬT THEO HÌNH MẪU
const CHARACTERS = [
    { id: 0, name: 'GBI', color: '#e82878' },
    { id: 1, name: 'OHINH', color: '#f8d038' },
    { id: 2, name: 'HOI BINK', color: '#509848' },
    { id: 3, name: 'KHON', color: '#8838d0' },
    { id: 4, name: 'BINH', color: '#38a8b8' },
    { id: 5, name: 'NARWHAL', color: '#20b2aa' }
];

// --- HÀM VẼ CÁC NHÂN VẬT PIXEL ---
function drawPixelBird(x, y, skinId, scale = 2) {
    ctx.save();
    ctx.translate(x, y);
    const p = scale;

    if (skinId === 0) { // 1. GBI (Băng đô hồng & mỏ hồng)
        ctx.fillStyle = '#4a403a'; ctx.fillRect(-8*p, -7*p, 16*p, 13*p);
        ctx.fillStyle = '#f8ea38'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#e82878'; ctx.fillRect(-7*p, -7*p, 14*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-4*p, -7*p, 2*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -4*p, 7*p, 5*p);
        ctx.fillStyle = '#4a403a'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#e82878'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, 0*p, 4*p, 3*p);
    } 
    else if (skinId === 1) { // 2. OHINH (Chim vàng gốc)
        ctx.fillStyle = '#4a403a'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#f8d038'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#f8b000'; ctx.fillRect(-6*p, 2*p, 10*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -6*p, 7*p, 6*p);
        ctx.fillStyle = '#4a403a'; ctx.fillRect(3*p, -4*p, 2*p, 3*p);
        ctx.fillStyle = '#f85820'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    } 
    else if (skinId === 2) { // 3. HOI BINK (Chim nón xanh)
        ctx.fillStyle = '#303030'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#509848'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#78c038'; ctx.fillRect(-5*p, -10*p, 10*p, 4*p); ctx.fillRect(-7*p, -7*p, 14*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#303030'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#f87820'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 3) { // 4. KHON (Chim tím vương miện)
        ctx.fillStyle = '#302040'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#8838d0'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#f858a8'; ctx.fillRect(-6*p, -10*p, 11*p, 4*p);
        ctx.fillRect(-7*p, -8*p, 2*p, 2*p); ctx.fillRect(-2*p, -8*p, 2*p, 2*p); ctx.fillRect(3*p, -8*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#302040'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#f89020'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#f878c0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 4) { // 5. BINH (Đầu chim unicorn lam)
        ctx.fillStyle = '#203840'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#38a8b8'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#c048d0'; ctx.fillRect(3*p, -11*p, 3*p, 5*p);
        ctx.fillStyle = '#f878e8'; ctx.fillRect(4*p, -9*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#203840'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#306870'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#78e0f0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 5) { // 6. NARWHAL (Kỳ lân biển cá voi)
        ctx.fillStyle = '#103038'; ctx.fillRect(-10*p, -4*p, 20*p, 10*p);
        ctx.fillStyle = '#20b2aa'; ctx.fillRect(-9*p, -3*p, 18*p, 8*p);
        ctx.fillStyle = '#e0f8f8'; ctx.fillRect(-9*p, 1*p, 18*p, 4*p);
        // Sừng dài phía trước
        ctx.fillStyle = '#e0e0e0'; ctx.fillRect(7*p, -7*p, 2*p, 6*p); ctx.fillRect(8*p, -9*p, 2*p, 3*p);
        // Đuôi cá
        ctx.fillStyle = '#20b2aa'; ctx.fillRect(-13*p, -6*p, 4*p, 6*p); ctx.fillRect(-13*p, 2*p, 4*p, 6*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(1*p, -3*p, 5*p, 5*p);
        ctx.fillStyle = '#103038'; ctx.fillRect(3*p, -2*p, 2*p, 3*p);
    }

    ctx.restore();
}

// --- ĐỐI TƯỢNG CHIM ---
const bird = {
    x: 80, y: 250, radius: 12, gravity: 0.25, jumpForce: -4.6, velocity: 0,
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
    items: [], gap: 130, width: 56, speed: 2,
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

// --- BẢNG CHỌN NHÂN VẬT CHUẨN 100% THEO HÌNH ---
function drawCharacterMenu() {
    // 1. Nền popup xanh nhạt có viền đen đậm
    let panelX = 30, panelY = 40, panelW = 420, panelH = 550;
    
    ctx.fillStyle = '#bdebf2';
    ctx.fillRect(panelX, panelY, panelW, panelH);
    ctx.strokeStyle = '#2b484f';
    ctx.lineWidth = 6;
    ctx.strokeRect(panelX, panelY, panelW, panelH);

    // Viền trong bo nhẹ
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.strokeRect(panelX + 4, panelY + 4, panelW - 8, panelH - 8);

    // 2. Tiêu đề 3D "NHÂN VẬT" với chữ Pixel nhiều màu & Sao lấp lánh
    ctx.font = '900 36px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    
    // Đổ bóng chữ
    ctx.fillStyle = '#3a2050';
    ctx.fillText('NHÂN VẬT', canvas.width / 2 + 3, panelY + 63);

    // Vẽ từng ký tự màu sắc
    const titleText = 'NHÂN VẬT';
    const colors = ['#f8d038', '#f858a8', '#38a8b8', '#9848d0', '#509848', '#f87820', '#38a8b8', '#f858a8'];
    let startX = canvas.width / 2 - 95;
    for (let i = 0; i < titleText.length; i++) {
        ctx.fillStyle = colors[i % colors.length];
        ctx.fillText(titleText[i], startX + i * 24, panelY + 60);
    }

    // Vẽ các ngôi sao vàng trang trí
    drawStar(panelX + 70, panelY + 45, '#f8d038');
    drawStar(panelX + 350, panelY + 50, '#f8d038');
    drawStar(panelX + 40, panelY + 160, '#f8d038');
    drawStar(panelX + 380, panelY + 280, '#f8d038');

    // 3. Vẽ 6 Ô nhân vật (3 Cột x 2 Hàng)
    const startGridX = 55;
    const startGridY = 130;
    const boxW = 110;
    const boxH = 120;
    const gapX = 20;
    const gapY = 25;

    CHARACTERS.forEach((char, i) => {
        let col = i % 3;
        let row = Math.floor(i / 3);
        let bx = startGridX + col * (boxW + gapX);
        let by = startGridY + row * (boxH + gapY);

        let isSelected = (selectedSkin === i);

        // Nền ô nhân vật
        ctx.fillStyle = '#a6e3ed';
        ctx.fillRect(bx, by, boxW, boxH);

        // Viền ô (Nếu chọn thì viền Vàng Kim 3D, không thì viền trắng)
        if (isSelected) {
            ctx.strokeStyle = '#d49b00';
            ctx.lineWidth = 6;
            ctx.strokeRect(bx - 2, by - 2, boxW + 4, boxH + 4);
            
            ctx.strokeStyle = '#fff7b2';
            ctx.lineWidth = 3;
            ctx.strokeRect(bx, by, boxW, boxH);
        } else {
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 3;
            ctx.strokeRect(bx, by, boxW, boxH);
        }

        // Vẽ Sprite Nhân Vật
        drawPixelBird(bx + boxW / 2, by + 38, i, 1.8);

        // Nhãn Tên Nhân Vật (Khung xám xanh)
        ctx.fillStyle = isSelected ? '#d49b00' : '#457a82';
        ctx.fillRect(bx + 10, by + 72, boxW - 20, 18);
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1.5;
        ctx.strokeRect(bx + 10, by + 72, boxW - 20, 18);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 10px "Courier New"';
        ctx.fillText(char.name, bx + boxW / 2, by + 85);

        // Nút "CHỌN" phía dưới ô
        ctx.fillStyle = isSelected ? '#f8b000' : '#e0f8f8';
        ctx.fillRect(bx + 20, by + 94, boxW - 40, 18);
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1.5;
        ctx.strokeRect(bx + 20, by + 94, boxW - 40, 18);

        ctx.fillStyle = isSelected ? '#ffffff' : '#000000';
        ctx.font = 'bold 11px "Courier New"';
        ctx.fillText('CHỌN', bx + boxW / 2, by + 107);
    });

    // 4. Hàng nút chức năng ở đáy Menu
    const bottomBtns = ['CHƠI NGAY', 'CỬA HÀNG', 'BXH', 'CÀI ĐẶT'];
    const btnW = 85;
    const btnH = 32;
    const btnGap = 10;
    let bStartX = 52;
    let bY = 530;

    bottomBtns.forEach((btnText, idx) => {
        let bx = bStartX + idx * (btnW + btnGap);

        ctx.fillStyle = (idx === 0) ? '#e0f8f8' : '#e0f8f8';
        ctx.fillRect(bx, bY, btnW, btnH);
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.strokeRect(bx, bY, btnW, btnH);

        ctx.fillStyle = '#000';
        ctx.font = 'bold 11px "Courier New"';
        ctx.fillText(btnText, bx + btnW / 2, bY + 20);
    });
}

// Hàm vẽ ngôi sao lấp lánh
function drawStar(cx, cy, color) {
    ctx.save();
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(cx, cy, 3, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillRect(cx - 6, cy - 1, 12, 2);
    ctx.fillRect(cx - 1, cy - 6, 2, 12);
    ctx.restore();
}

// --- UI CHÍNH / GAME OVER ---
function drawUI() {
    if (gameState === 'START' || gameState === 'CHARACTERS') {
        drawCharacterMenu();
    } else if (gameState === 'PLAYING') {
        ctx.fillStyle = '#fff'; ctx.strokeStyle = '#000'; ctx.lineWidth = 3;
        ctx.font = '36px Courier New'; ctx.textAlign = 'center';
        ctx.strokeText(score, canvas.width / 2, 60);
        ctx.fillText(score, canvas.width / 2, 60);
    } else if (gameState === 'GAMEOVER') {
        ctx.fillStyle = '#fff'; ctx.strokeStyle = '#000'; ctx.lineWidth = 3;
        ctx.font = '30px Courier New'; ctx.textAlign = 'center';
        ctx.strokeText('GAME OVER', canvas.width / 2, 180);
        ctx.fillText('GAME OVER', canvas.width / 2, 180);

        drawPixelBird(canvas.width / 2, 230, selectedSkin, 2.2);

        ctx.font = '18px Courier New';
        ctx.strokeText(`Điểm: ${score}`, canvas.width / 2, 290);
        ctx.fillText(`Điểm: ${score}`, canvas.width / 2, 290);
        ctx.strokeText(`Cao nhất: ${highScore}`, canvas.width / 2, 320);
        ctx.fillText(`Cao nhất: ${highScore}`, canvas.width / 2, 320);

        ctx.font = '14px Courier New';
        ctx.strokeText('Bấm SPACE hoặc CHẠM để chơi lại', canvas.width / 2, 380);
        ctx.fillText('Bấm SPACE hoặc CHẠM để chơi lại', canvas.width / 2, 380);
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
    if (gameState === 'PLAYING') bird.draw();
    drawUI();
    requestAnimationFrame(loop);
}

// --- TƯƠNG TÁC TẠI MÀN HÌNH CHỌN NHÂN VẬT ---
function handleInteraction(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const clickX = clientX - rect.left;
    const clickY = clientY - rect.top;

    if (gameState === 'START' || gameState === 'CHARACTERS') {
        const startGridX = 55, startGridY = 130, boxW = 110, boxH = 120, gapX = 20, gapY = 25;

        // 1. Kiểm tra click chọn 6 Nhân vật
        CHARACTERS.forEach((char, i) => {
            let col = i % 3; let row = Math.floor(i / 3);
            let bx = startGridX + col * (boxW + gapX);
            let by = startGridY + row * (boxH + gapY);

            if (clickX >= bx && clickX <= bx + boxW && clickY >= by && clickY <= by + boxH) {
                selectedSkin = i;
                playSound('score');
            }
        });

        // 2. Kiểm tra click Nút "CHƠI NGAY"
        const btnW = 85, btnH = 32, btnGap = 10, bStartX = 52, bY = 530;
        let playBtnX = bStartX; // Nút đầu tiên
        if (clickX >= playBtnX && clickX <= playBtnX + btnW && clickY >= bY && clickY <= bY + btnH) {
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
        if (gameState === 'START' || gameState === 'CHARACTERS') {
            bird.reset(); pipes.reset(); score = 0; frames = 0;
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

components.html(game_html, width=500, height=660)
