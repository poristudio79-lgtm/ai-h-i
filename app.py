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
let selectedSkin = 1;

const CHARACTERS = [
    { id: 0, name: 'GBI', color: '#e82878' },
    { id: 1, name: 'OHINH', color: '#f8d038' },
    { id: 2, name: 'HOI BINK', color: '#509848' },
    { id: 3, name: 'KHON', color: '#8838d0' },
    { id: 4, name: 'BINH', color: '#38a8b8' },
    { id: 5, name: 'NARWHAL', color: '#20b2aa' }
];

const menuPlayBtn = { x: 75, y: 390, w: 145, h: 90 };
const menuCharBtn = { x: 260, y: 390, w: 145, h: 90 };

// --- HÀM VẼ NHÂN VẬT PIXEL ---
function drawPixelBird(x, y, skinId, scale = 2, rotation = 0) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation); // Xoay góc theo hiệu ứng bay lên/rơi xuống
    const p = scale;

    if (skinId === 0) {
        ctx.fillStyle = '#4a403a'; ctx.fillRect(-8*p, -7*p, 16*p, 13*p);
        ctx.fillStyle = '#f8ea38'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#e82878'; ctx.fillRect(-7*p, -7*p, 14*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-4*p, -7*p, 2*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -4*p, 7*p, 5*p);
        ctx.fillStyle = '#4a403a'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#e82878'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, 0*p, 4*p, 3*p);
    } 
    else if (skinId === 1) {
        ctx.fillStyle = '#4a403a'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#f8d038'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#f8b000'; ctx.fillRect(-6*p, 2*p, 10*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -6*p, 7*p, 6*p);
        ctx.fillStyle = '#4a403a'; ctx.fillRect(3*p, -4*p, 2*p, 3*p);
        ctx.fillStyle = '#f85820'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    } 
    else if (skinId === 2) {
        ctx.fillStyle = '#303030'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#509848'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#78c038'; ctx.fillRect(-5*p, -10*p, 10*p, 4*p); ctx.fillRect(-7*p, -7*p, 14*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#303030'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#f87820'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 3) {
        ctx.fillStyle = '#302040'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#8838d0'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#f858a8'; ctx.fillRect(-6*p, -10*p, 11*p, 4*p);
        ctx.fillRect(-7*p, -8*p, 2*p, 2*p); ctx.fillRect(-2*p, -8*p, 2*p, 2*p); ctx.fillRect(3*p, -8*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#302040'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#f89020'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#f878c0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 4) {
        ctx.fillStyle = '#203840'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#38a8b8'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#c048d0'; ctx.fillRect(3*p, -11*p, 3*p, 5*p);
        ctx.fillStyle = '#f878e8'; ctx.fillRect(4*p, -9*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#203840'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#306870'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#78e0f0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 5) {
        ctx.fillStyle = '#103038'; ctx.fillRect(-10*p, -4*p, 20*p, 10*p);
        ctx.fillStyle = '#20b2aa'; ctx.fillRect(-9*p, -3*p, 18*p, 8*p);
        ctx.fillStyle = '#e0f8f8'; ctx.fillRect(-9*p, 1*p, 18*p, 4*p);
        ctx.fillStyle = '#e0e0e0'; ctx.fillRect(7*p, -7*p, 2*p, 6*p); ctx.fillRect(8*p, -9*p, 2*p, 3*p);
        ctx.fillStyle = '#20b2aa'; ctx.fillRect(-13*p, -6*p, 4*p, 6*p); ctx.fillRect(-13*p, 2*p, 4*p, 6*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(1*p, -3*p, 5*p, 5*p);
        ctx.fillStyle = '#103038'; ctx.fillRect(3*p, -2*p, 2*p, 3*p);
    }

    ctx.restore();
}

// --- ĐỐI TƯỢNG CHIM VỚI HIỆU ỨNG RƠI / BAY ---
const bird = {
    x: 90, y: 250, radius: 12, gravity: 0.28, jumpForce: -5.2, velocity: 0,
    
    draw() {
        // Tính góc xoay đầu chim dựa trên vận tốc (Bay lên ngẩng đầu, Rơi xuống cắm đầu)
        let rotation = Math.min(Math.PI / 2.5, Math.max(-Math.PI / 4, (this.velocity / 12)));
        drawPixelBird(this.x, this.y, selectedSkin, 1.8, rotation);
    },

    update() {
        // Hiệu ứng rơi xuống: Tăng dần vận tốc theo trọng lực
        this.velocity += this.gravity;
        this.y += this.velocity;

        // Giới hạn trần màn hình
        if (this.y - this.radius <= 0) {
            this.y = this.radius;
            this.velocity = 0;
        }

        // Chạm đất -> Game Over
        if (this.y + this.radius >= canvas.height - 80) {
            this.y = canvas.height - 80 - this.radius;
            triggerGameOver();
        }
    },

    jump() {
        // Hiệu ứng bay lên: Gán lực âm để đẩy chim vọt lên cao lập tức
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
    items: [], gap: 130, width: 56, speed: 2.2,
    draw() {
        this.items.forEach(p => {
            drawSinglePipe(p.x, 0, this.width, p.top, true);
            drawSinglePipe(p.x, p.bottom, this.width, canvas.height - 80 - p.bottom, false);
        });
    },
    update() {
        if (frames % 95 === 0) {
            let maxTop = canvas.height - 80 - this.gap - 50;
            let minTop = 50;
            let top = Math.floor(Math.random() * (maxTop - minTop + 1)) + minTop;
            this.items.push({ x: canvas.width, top: top, bottom: top + this.gap, passed: false });
        }
        this.items.forEach((p, index) => {
            p.x -= this.speed;

            let rimExtra = 3;
            if (bird.x + bird.radius > p.x - rimExtra && bird.x - bird.radius < p.x + this.width + rimExtra &&
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

function drawSinglePipe(x, y, width, height, isTop) {
    const rimHeight = 28;
    const rimExtraWidth = 6;
    const rimX = x - rimExtraWidth / 2;
    const rimW = width + rimExtraWidth;

    const colDarkBorder = '#232b1a';
    const colMainGreen  = '#75cb27';
    const colLightGreen = '#b8e637';
    const colWhiteLine  = '#ffffff';
    const colDarkGreen  = '#549c1b';

    ctx.save();

    if (isTop) {
        let bodyH = Math.max(0, height - rimHeight);
        ctx.fillStyle = colMainGreen; ctx.fillRect(x, 0, width, bodyH);
        ctx.fillStyle = colLightGreen; ctx.fillRect(x + 4, 0, 10, bodyH);
        ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, 0, 4, bodyH);
        ctx.fillStyle = colDarkGreen; ctx.fillRect(x + width - 12, 0, 12, bodyH);
        ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, 0, width, bodyH);

        let rimY = bodyH;
        ctx.fillStyle = colMainGreen; ctx.fillRect(rimX, rimY, rimW, rimHeight);
        ctx.fillStyle = colLightGreen; ctx.fillRect(rimX + 5, rimY, 12, rimHeight);
        ctx.fillStyle = colWhiteLine; ctx.fillRect(rimX + 17, rimY, 4, rimHeight);
        ctx.fillStyle = colDarkGreen; ctx.fillRect(rimX + rimW - 14, rimY, 14, rimHeight);
        ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(rimX, rimY, rimW, rimHeight);
        ctx.fillStyle = 'rgba(0,0,0,0.25)'; ctx.fillRect(x, rimY + rimHeight, width, 4);
    } else {
        let rimY = y;
        let bodyY = y + rimHeight;
        let bodyH = Math.max(0, canvas.height - bodyY);
        ctx.fillStyle = colMainGreen; ctx.fillRect(x, bodyY, width, bodyH);
        ctx.fillStyle = colLightGreen; ctx.fillRect(x + 4, bodyY, 10, bodyH);
        ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, bodyY, 4, bodyH);
        ctx.fillStyle = colDarkGreen; ctx.fillRect(x + width - 12, bodyY, 12, bodyH);
        ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, bodyY, width, bodyH);

        ctx.fillStyle = colMainGreen; ctx.fillRect(rimX, rimY, rimW, rimHeight);
        ctx.fillStyle = colLightGreen; ctx.fillRect(rimX + 5, rimY, 12, rimHeight);
        ctx.fillStyle = colWhiteLine; ctx.fillRect(rimX + 17, rimY, 4, rimHeight);
        ctx.fillStyle = colDarkGreen; ctx.fillRect(rimX + rimW - 14, rimY, 14, rimHeight);
        ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(rimX, rimY, rimW, rimHeight);
        ctx.fillStyle = 'rgba(0,0,0,0.25)'; ctx.fillRect(x, bodyY, width, 4);
    }
    ctx.restore();
}

function drawBackgroundCity() {
    ctx.fillStyle = '#a1e4c3';
    ctx.beginPath();
    ctx.arc(60, 520, 70, 0, Math.PI * 2);
    ctx.arc(180, 530, 80, 0, Math.PI * 2);
    ctx.arc(320, 520, 90, 0, Math.PI * 2);
    ctx.arc(440, 530, 75, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#83d8b4';
    ctx.fillRect(20, 480, 40, 80);
    ctx.fillRect(80, 450, 50, 110);
    ctx.fillRect(150, 490, 35, 70);
    ctx.fillRect(220, 460, 60, 100);
    ctx.fillRect(300, 440, 45, 120);
    ctx.fillRect(370, 470, 55, 90);
}

function drawGround() {
    ctx.fillStyle = '#ded895'; ctx.fillRect(0, canvas.height - 80, canvas.width, 80);
    ctx.strokeStyle = '#232b1a'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(0, canvas.height - 80); ctx.lineTo(canvas.width, canvas.height - 80); ctx.stroke();
    
    ctx.fillStyle = '#75cb27'; ctx.fillRect(0, canvas.height - 80, canvas.width, 16);
    ctx.fillStyle = '#9bd843';
    for (let i = 0; i < canvas.width; i += 24) {
        ctx.beginPath();
        ctx.moveTo(i, canvas.height - 80);
        ctx.lineTo(i + 12, canvas.height - 80);
        ctx.lineTo(i - 4, canvas.height - 64);
        ctx.lineTo(i - 16, canvas.height - 64);
        ctx.fill();
    }
}

function drawMenuButton(btn, isPlayBtn) {
    ctx.fillStyle = '#f8f8f8'; ctx.strokeStyle = '#2b2b2b'; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.roundRect(btn.x, btn.y, btn.w, btn.h, 16); ctx.fill(); ctx.stroke();

    if (isPlayBtn) {
        let cx = btn.x + btn.w / 2 - 4;
        let cy = btn.y + btn.h / 2;
        ctx.fillStyle = '#00a844';
        ctx.beginPath(); ctx.moveTo(cx - 16, cy - 22); ctx.lineTo(cx + 22, cy); ctx.lineTo(cx - 16, cy + 22); ctx.closePath(); ctx.fill();
        ctx.fillStyle = '#54cb37';
        ctx.beginPath(); ctx.moveTo(cx - 16, cy - 22); ctx.lineTo(cx + 12, cy); ctx.lineTo(cx - 16, cy); ctx.closePath(); ctx.fill();
    } else {
        drawPixelBird(btn.x + btn.w / 2, btn.y + btn.h / 2, selectedSkin, 2.2);
    }
}

function drawMainMenu() {
    let titleX = canvas.width / 2;
    let titleY = 130;

    ctx.save();
    ctx.font = '900 48px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#000000'; ctx.fillText('FlappyBird', titleX + 4, titleY + 4);
    ctx.fillStyle = '#ffffff'; ctx.fillText('FlappyBird', titleX, titleY);
    ctx.restore();

    let floatY = 230 + Math.sin(frames * 0.08) * 8;
    drawPixelBird(canvas.width / 2, floatY, selectedSkin, 2.5);

    drawMenuButton(menuPlayBtn, true);
    drawMenuButton(menuCharBtn, false);
}

function drawCharacterMenu() {
    let panelX = 30, panelY = 40, panelW = 420, panelH = 550;
    ctx.fillStyle = '#bdebf2'; ctx.fillRect(panelX, panelY, panelW, panelH);
    ctx.strokeStyle = '#2b484f'; ctx.lineWidth = 6; ctx.strokeRect(panelX, panelY, panelW, panelH);

    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3; ctx.strokeRect(panelX + 4, panelY + 4, panelW - 8, panelH - 8);

    ctx.font = '900 36px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#3a2050'; ctx.fillText('NHÂN VẬT', canvas.width / 2 + 3, panelY + 63);

    const titleText = 'NHÂN VẬT';
    const colors = ['#f8d038', '#f858a8', '#38a8b8', '#9848d0', '#509848', '#f87820', '#38a8b8', '#f858a8'];
    let startX = canvas.width / 2 - 95;
    for (let i = 0; i < titleText.length; i++) {
        ctx.fillStyle = colors[i % colors.length];
        ctx.fillText(titleText[i], startX + i * 24, panelY + 60);
    }

    const startGridX = 55, startGridY = 130, boxW = 110, boxH = 120, gapX = 20, gapY = 25;
    CHARACTERS.forEach((char, i) => {
        let col = i % 3;
        let row = Math.floor(i / 3);
        let bx = startGridX + col * (boxW + gapX);
        let by = startGridY + row * (boxH + gapY);
        let isSelected = (selectedSkin === i);

        ctx.fillStyle = '#a6e3ed'; ctx.fillRect(bx, by, boxW, boxH);
        if (isSelected) {
            ctx.strokeStyle = '#d49b00'; ctx.lineWidth = 6; ctx.strokeRect(bx - 2, by - 2, boxW + 4, boxH + 4);
            ctx.strokeStyle = '#fff7b2'; ctx.lineWidth = 3; ctx.strokeRect(bx, by, boxW, boxH);
        } else {
            ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3; ctx.strokeRect(bx, by, boxW, boxH);
        }

        drawPixelBird(bx + boxW / 2, by + 38, i, 1.8);

        ctx.fillStyle = isSelected ? '#d49b00' : '#457a82';
        ctx.fillRect(bx + 10, by + 72, boxW - 20, 18);
        ctx.strokeStyle = '#000'; ctx.lineWidth = 1.5; ctx.strokeRect(bx + 10, by + 72, boxW - 20, 18);

        ctx.fillStyle = '#ffffff'; ctx.font = 'bold 10px "Courier New"';
        ctx.fillText(char.name, bx + boxW / 2, by + 85);

        ctx.fillStyle = isSelected ? '#f8b000' : '#e0f8f8';
        ctx.fillRect(bx + 20, by + 94, boxW - 40, 18);
        ctx.strokeStyle = '#000'; ctx.lineWidth = 1.5; ctx.strokeRect(bx + 20, by + 94, boxW - 40, 18);

        ctx.fillStyle = isSelected ? '#ffffff' : '#000000';
        ctx.font = 'bold 11px "Courier New"';
        ctx.fillText('CHỌN', bx + boxW / 2, by + 107);
    });

    ctx.fillStyle = '#75cb27'; ctx.fillRect(140, 530, 200, 45);
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.strokeRect(140, 530, 200, 45);
    ctx.fillStyle = '#fff'; ctx.font = 'bold 18px "Courier New"';
    ctx.fillText('BẮT ĐẦU CHƠI', canvas.width / 2, 558);
}

function drawUI() {
    if (gameState === 'START') {
        drawMainMenu();
    } else if (gameState === 'CHARACTERS') {
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

        drawPixelBird(canvas.width / 2, 230, selectedSkin, 2.2, 0.5);

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
    drawBackgroundCity();

    if (gameState === 'PLAYING') {
        bird.update();
        pipes.update();
    }
    frames++;

    pipes.draw(); 
    drawGround();

    if (gameState === 'PLAYING') {
        bird.draw();
    }
    drawUI();

    requestAnimationFrame(loop);
}

function handleInteraction(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const clickX = clientX - rect.left;
    const clickY = clientY - rect.top;

    if (gameState === 'START') {
        if (clickX >= menuPlayBtn.x && clickX <= menuPlayBtn.x + menuPlayBtn.w &&
            clickY >= menuPlayBtn.y && clickY <= menuPlayBtn.y + menuPlayBtn.h) {
            bird.reset(); pipes.reset(); score = 0; frames = 0;
            gameState = 'PLAYING'; bird.jump();
            return;
        }
        if (clickX >= menuCharBtn.x && clickX <= menuCharBtn.x + menuCharBtn.w &&
            clickY >= menuCharBtn.y && clickY <= menuCharBtn.y + menuCharBtn.h) {
            gameState = 'CHARACTERS';
            playSound('score');
            return;
        }
    } 
    else if (gameState === 'CHARACTERS') {
        const startGridX = 55, startGridY = 130, boxW = 110, boxH = 120, gapX = 20, gapY = 25;
        CHARACTERS.forEach((char, i) => {
            let col = i % 3; let row = Math.floor(i / 3);
            let bx = startGridX + col * (boxW + gapX);
            let by = startGridY + row * (boxH + gapY);

            if (clickX >= bx && clickX <= bx + boxW && clickY >= by && clickY <= by + boxH) {
                selectedSkin = i;
                playSound('score');
            }
        });

        if (clickX >= 140 && clickX <= 340 && clickY >= 530 && clickY <= 575) {
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
        if (gameState === 'START') {
            bird.reset(); pipes.reset(); score = 0; frames = 0;
            gameState = 'PLAYING'; bird.jump();
        } else if (gameState === 'CHARACTERS') {
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
