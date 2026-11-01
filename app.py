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
let gameState = 'START';
let score = 0;
let highScore = localStorage.getItem('fb_highscore') || 0;
let isNewHighScore = false;
let frames = 0;
let selectedSkin = 1;
let currentDifficulty = 'EASY';

const CHARACTERS = [
    { id: 0, name: 'GBI', color: '#e82878', effect: 'Hào quang Hồng' },
    { id: 1, name: 'OHINH', color: '#f8d038', effect: 'Tia chớp Vàng' },
    { id: 2, name: 'HOI BINK', color: '#509848', effect: 'Lá rơi Xanh' },
    { id: 3, name: 'KHON', color: '#8838d0', effect: 'Hỏa diệm Tím' },
    { id: 4, name: 'BINH', color: '#38a8b8', effect: 'Bong bóng Nước' },
    { id: 5, name: 'NARWHAL', color: '#20b2aa', effect: 'Băng giá Tuyết' }
];

const menuPlayBtn = { x: 75, y: 390, w: 145, h: 90 };
const menuCharBtn = { x: 260, y: 390, w: 145, h: 90 };

const diffEasyBtn = { x: 100, y: 220, w: 280, h: 65 };   
const diffNormalBtn = { x: 100, y: 305, w: 280, h: 65 }; 
const diffHardBtn = { x: 100, y: 390, w: 280, h: 65 };   
const diffBackBtn = { x: 100, y: 480, w: 280, h: 50 };

const gameOverOkBtn = { x: 75, y: 470, w: 145, h: 55 };
const gameOverShareBtn = { x: 260, y: 470, w: 145, h: 55 };

// --- HÀM VẼ NHÂN VẬT PIXEL ---
function drawPixelBird(x, y, skinId, scale = 2.6, rotation = 0) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation);
    const p = scale;

    if (skinId === 0) {
        ctx.fillStyle = '#2b221e'; ctx.fillRect(-8*p, -7*p, 16*p, 13*p);
        ctx.fillStyle = '#f8ea38'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#e82878'; ctx.fillRect(-7*p, -7*p, 14*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-4*p, -7*p, 2*p, 3*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -4*p, 7*p, 5*p);
        ctx.fillStyle = '#2b221e'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#e82878'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, 0*p, 4*p, 3*p);
    } 
    else if (skinId === 1) {
        ctx.fillStyle = '#2b221e'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#f8d038'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#f8b000'; ctx.fillRect(-6*p, 2*p, 10*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -6*p, 7*p, 6*p);
        ctx.fillStyle = '#2b221e'; ctx.fillRect(3*p, -4*p, 2*p, 3*p);
        ctx.fillStyle = '#f85820'; ctx.fillRect(2*p, 0*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    } 
    else if (skinId === 2) {
        ctx.fillStyle = '#1e2b1e'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#509848'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#78c038'; ctx.fillRect(-5*p, -10*p, 10*p, 4*p); ctx.fillRect(-7*p, -7*p, 14*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#1e2b1e'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#f87820'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 3) {
        ctx.fillStyle = '#261933'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#8838d0'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#f858a8'; ctx.fillRect(-6*p, -10*p, 11*p, 4*p);
        ctx.fillRect(-7*p, -8*p, 2*p, 2*p); ctx.fillRect(-2*p, -8*p, 2*p, 2*p); ctx.fillRect(3*p, -8*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#261933'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#f89020'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#f878c0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 4) {
        ctx.fillStyle = '#16282b'; ctx.fillRect(-8*p, -6*p, 16*p, 12*p);
        ctx.fillStyle = '#38a8b8'; ctx.fillRect(-7*p, -5*p, 14*p, 10*p);
        ctx.fillStyle = '#c048d0'; ctx.fillRect(3*p, -11*p, 3*p, 5*p);
        ctx.fillStyle = '#f878e8'; ctx.fillRect(4*p, -9*p, 2*p, 2*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(0*p, -5*p, 7*p, 6*p);
        ctx.fillStyle = '#16282b'; ctx.fillRect(3*p, -3*p, 2*p, 3*p);
        ctx.fillStyle = '#306870'; ctx.fillRect(2*p, 1*p, 7*p, 4*p);
        ctx.fillStyle = '#78e0f0'; ctx.fillRect(-7*p, -1*p, 4*p, 3*p);
    }
    else if (skinId === 5) {
        ctx.fillStyle = '#0a1e24'; ctx.fillRect(-10*p, -4*p, 20*p, 10*p);
        ctx.fillStyle = '#20b2aa'; ctx.fillRect(-9*p, -3*p, 18*p, 8*p);
        ctx.fillStyle = '#e0f8f8'; ctx.fillRect(-9*p, 1*p, 18*p, 4*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(7*p, -7*p, 2*p, 6*p); ctx.fillRect(8*p, -9*p, 2*p, 3*p);
        ctx.fillStyle = '#20b2aa'; ctx.fillRect(-13*p, -6*p, 4*p, 6*p); ctx.fillRect(-13*p, 2*p, 4*p, 6*p);
        ctx.fillStyle = '#ffffff'; ctx.fillRect(1*p, -3*p, 5*p, 5*p);
        ctx.fillStyle = '#0a1e24'; ctx.fillRect(3*p, -2*p, 2*p, 3*p);
    }

    ctx.restore();
}

// --- VẼ HIỆU ỨNG ĐỘC QUYỀN CHO TỪNG SKIN ---
function drawSkinEffects(x, y, skinId) {
    ctx.save();
    let time = frames * 0.1;

    if (skinId === 0) {
        ctx.strokeStyle = 'rgba(232, 40, 120, 0.6)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(x, y, 22 + Math.sin(time) * 4, 0, Math.PI * 2);
        ctx.stroke();
    } 
    else if (skinId === 1) {
        if (frames % 15 < 8) {
            ctx.fillStyle = '#ffff00';
            ctx.fillRect(x - 20 + Math.random() * 10, y - 20 + Math.random() * 10, 6, 6);
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(x + 10, y - 15, 4, 4);
        }
    } 
    else if (skinId === 2) {
        for (let i = 0; i < 3; i++) {
            let lx = x - 15 - (i * 12 + (frames * 2) % 30);
            let ly = y + Math.sin(time + i) * 15;
            ctx.fillStyle = '#78c038';
            ctx.fillRect(lx, ly, 6, 4);
        }
    } 
    else if (skinId === 3) {
        ctx.fillStyle = 'rgba(136, 56, 208, 0.7)';
        ctx.beginPath();
        ctx.arc(x - 10, y + 8 + Math.sin(time * 2) * 5, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(248, 88, 168, 0.5)';
        ctx.beginPath();
        ctx.arc(x - 14, y + 4, 5, 0, Math.PI * 2);
        ctx.fill();
    } 
    else if (skinId === 4) {
        let bx = x - 18 - ((frames * 1.5) % 35);
        let by = y + Math.cos(time) * 12;
        ctx.fillStyle = 'rgba(120, 224, 240, 0.7)';
        ctx.beginPath(); ctx.arc(bx, by, 5, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(bx - 1, by - 1, 2, 0, Math.PI * 2); ctx.stroke();
    } 
    else if (skinId === 5) {
        for (let i = 0; i < 3; i++) {
            let tx = x - 10 - (i * 10 + (frames * 1.8) % 25);
            let ty = y - 15 + (i * 12 + frames) % 30;
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(tx, ty, 4, 4);
        }
    }
    ctx.restore();
}

// --- ĐỐI TƯỢNG CHIM ---
const bird = {
    x: 90, y: 250, radius: 14, gravity: 0.28, jumpForce: -5.2, velocity: 0,
    draw() {
        let rotation = Math.min(Math.PI / 2.5, Math.max(-Math.PI / 4, (this.velocity / 12)));
        drawSkinEffects(this.x, this.y, selectedSkin);
        drawPixelBird(this.x, this.y, selectedSkin, 2.2, rotation);
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

// --- QUẢN LÝ ỐNG CỐNG & ĐỘ KHÓ ---
const pipes = {
    items: [], gap: 130, width: 56, speed: 2.2, pipeCounter: 0,
    
    setDifficulty(diff) {
        currentDifficulty = diff;
        if (diff === 'EASY') {
            this.gap = 145;
            this.speed = 1.9;
        } else if (diff === 'NORMAL') {
            this.gap = 130;
            this.speed = 2.3;
        } else if (diff === 'HARD') {
            this.gap = 105;
            this.speed = 2.9;
        }
    },

    draw() {
        this.items.forEach(p => {
            drawPipesByTheme(p.x, 0, this.width, p.top, true, p.isInfinite, currentDifficulty);
            drawPipesByTheme(p.x, p.bottom, this.width, canvas.height - 80 - p.bottom, false, p.isInfinite, currentDifficulty);
        });
    },
    update() {
        if (frames % 95 === 0) {
            let maxTop = canvas.height - 80 - this.gap - 50;
            let minTop = 50;
            let top = Math.floor(Math.random() * (maxTop - minTop + 1)) + minTop;
            
            this.pipeCounter++;
            let isInfinite = (this.pipeCounter % 5 === 0); // Cứ mỗi 5 cột sẽ xuất hiện cột vô hạn

            this.items.push({ 
                x: canvas.width, 
                top: top, 
                bottom: top + this.gap, 
                passed: false,
                isInfinite: isInfinite 
            });
        }
        this.items.forEach((p, index) => {
            p.x -= this.speed;

            let rimExtra = 6;
            if (bird.x + bird.radius > p.x - rimExtra && bird.x - bird.radius < p.x + this.width + rimExtra &&
               (bird.y - bird.radius < p.top || bird.y + bird.radius > p.bottom)) {
                triggerGameOver();
            }
            if (p.x + this.width < bird.x && !p.passed) {
                p.passed = true; score++; 
                playSound('score');

                if (score > highScore) { 
                    highScore = score; 
                    isNewHighScore = true;
                    localStorage.setItem('fb_highscore', highScore); 
                }
            }
            if (p.x + this.width < 0) this.items.splice(index, 1);
        });
    },
    reset() { 
        this.items = []; 
        this.pipeCounter = 0;
    }
};

// --- HÀM VẼ GĂNG TAY TÍM CHO MAP TRUNG BÌNH ---
function drawPurpleFistGlove(x, y, width, isTop) {
    ctx.save();
    const colBorder = '#281038';
    const colMain   = '#9a50c8';
    const colLight  = '#c088f0';
    const colDark   = '#682898';
    const colWhite  = '#ffffff';

    if (!isTop) {
        let gx = x - 6;
        let gy = y;

        ctx.fillStyle = colMain; ctx.fillRect(gx, gy + 32, width + 12, 12);
        ctx.fillStyle = colLight; ctx.fillRect(gx + 4, gy + 32, 8, 12);
        ctx.fillStyle = colDark; ctx.fillRect(gx + width, gy + 32, 8, 12);
        ctx.strokeStyle = colBorder; ctx.lineWidth = 3; ctx.strokeRect(gx, gy + 32, width + 12, 12);

        ctx.fillStyle = colMain;
        ctx.fillRect(gx - 4, gy + 4, width + 20, 28);
        ctx.fillRect(gx, gy, width + 12, 34);

        ctx.fillStyle = colLight;
        ctx.fillRect(gx - 2, gy + 4, 10, 24);
        ctx.fillStyle = colWhite;
        ctx.fillRect(gx + 8, gy + 6, 4, 20);

        ctx.fillStyle = colDark;
        ctx.fillRect(gx + width + 4, gy + 6, 8, 22);

        ctx.fillStyle = colBorder;
        ctx.fillRect(gx + 6, gy + 8, width, 3);
        ctx.fillRect(gx + 6, gy + 18, width, 3);
        
        ctx.fillStyle = colMain; ctx.fillRect(gx - 10, gy + 12, 10, 16);
        ctx.fillStyle = colLight; ctx.fillRect(gx - 8, gy + 14, 4, 12);
        ctx.strokeStyle = colBorder; ctx.lineWidth = 3; ctx.strokeRect(gx - 10, gy + 12, 10, 16);

        ctx.strokeStyle = colBorder; ctx.lineWidth = 3.5;
        ctx.strokeRect(gx - 4, gy, width + 20, 32);

    } else {
        let gx = x - 6;
        let gy = y - 44;

        ctx.fillStyle = colMain; ctx.fillRect(gx, gy, width + 12, 12);
        ctx.fillStyle = colLight; ctx.fillRect(gx + 4, gy, 8, 12);
        ctx.fillStyle = colDark; ctx.fillRect(gx + width, gy, 8, 12);
        ctx.strokeStyle = colBorder; ctx.lineWidth = 3; ctx.strokeRect(gx, gy, width + 12, 12);

        ctx.fillStyle = colMain;
        ctx.fillRect(gx - 4, gy + 12, width + 20, 28);
        ctx.fillRect(gx, gy + 10, width + 12, 34);

        ctx.fillStyle = colLight;
        ctx.fillRect(gx - 2, gy + 14, 10, 24);
        ctx.fillStyle = colWhite;
        ctx.fillRect(gx + 8, gy + 16, 4, 20);

        ctx.fillStyle = colDark;
        ctx.fillRect(gx + width + 4, gy + 14, 8, 22);

        ctx.fillStyle = colBorder;
        ctx.fillRect(gx + 6, gy + 20, width, 3);
        ctx.fillRect(gx + 6, gy + 30, width, 3);

        ctx.fillStyle = colMain; ctx.fillRect(gx - 10, gy + 16, 10, 16);
        ctx.fillStyle = colLight; ctx.fillRect(gx - 8, gy + 18, 4, 12);
        ctx.strokeStyle = colBorder; ctx.lineWidth = 3; ctx.strokeRect(gx - 10, gy + 16, 10, 16);

        ctx.strokeStyle = colBorder; ctx.lineWidth = 3.5;
        ctx.strokeRect(gx - 4, gy + 12, width + 20, 32);
    }
    ctx.restore();
}

// --- HÀM VẼ ĐÔI MẮT RỰC LỬA TRÊN NẮP CỐNG (MAP KHÓ) ---
function drawHardPipeEyes(x, rimY, rW, isTop) {
    ctx.save();
    let eyeCenterX1 = x + rW * 0.3;
    let eyeCenterX2 = x + rW * 0.7;
    let eyeY = isTop ? (rimY + 14) : (rimY + 14);

    ctx.fillStyle = 'rgba(255, 50, 0, 0.4)';
    ctx.beginPath(); ctx.arc(eyeCenterX1, eyeY, 7, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(eyeCenterX2, eyeY, 7, 0, Math.PI * 2); ctx.fill();

    ctx.fillStyle = '#ff1100';
    ctx.fillRect(eyeCenterX1 - 4, eyeY - 3, 8, 6);
    ctx.fillRect(eyeCenterX2 - 4, eyeY - 3, 8, 6);

    ctx.fillStyle = '#ffff00';
    ctx.fillRect(eyeCenterX1 - 2, eyeY - 2, 4, 4);
    ctx.fillRect(eyeCenterX2 - 2, eyeY - 2, 4, 4);
    ctx.restore();
}

// --- HỆ THỐNG VẼ CỐNG (THAY CỘT CARO BẰNG CỘT VÔ HẠN KÉO DÀI XUYÊN SUỐT) ---
function drawPipesByTheme(x, y, width, height, isTop, isInfinite, difficulty) {
    ctx.save();

    if (isInfinite) {
        // Cột Vô Hạn: Kiểu dáng năng lượng không giới hạn với viền sáng rực rỡ và hiệu ứng chạy dọc
        const infColorMain = '#112233';
        const infColorGlow = '#00ffff';
        const infColorCore = '#ffffff';

        if (isTop) {
            let bodyH = Math.max(0, height);
            ctx.fillStyle = infColorMain; ctx.fillRect(x, 0, width, bodyH);
            ctx.strokeStyle = infColorGlow; ctx.lineWidth = 3; ctx.strokeRect(x, 0, width, bodyH);

            // Các đường sọc năng lượng chạy vô hạn
            ctx.fillStyle = infColorCore;
            let offset = (frames * 3) % 20;
            for (let sy = -20 + offset; sy < bodyH; sy += 20) {
                ctx.fillRect(x + width / 2 - 4, sy, 8, 10);
            }
        } else {
            let bodyY = y;
            let bodyH = Math.max(0, canvas.height - 80 - bodyY);
            ctx.fillStyle = infColorMain; ctx.fillRect(x, bodyY, width, bodyH);
            ctx.strokeStyle = infColorGlow; ctx.lineWidth = 3; ctx.strokeRect(x, bodyY, width, bodyH);

            ctx.fillStyle = infColorCore;
            let offset = (frames * 3) % 20;
            for (let sy = bodyY - 20 + offset; sy < canvas.height - 80; sy += 20) {
                ctx.fillRect(x + width / 2 - 4, sy, 8, 10);
            }
        }
    } else {
        if (difficulty === 'EASY') {
            const colDarkBorder = '#232b1a';
            const colMainGreen  = '#75cb27';
            const colLightGreen = '#b8e637';
            const colWhiteLine  = '#ffffff';
            const colDarkGreen  = '#549c1b';

            if (isTop) {
                let bodyH = Math.max(0, height - 28);
                ctx.fillStyle = colMainGreen; ctx.fillRect(x, 0, width, bodyH);
                ctx.fillStyle = colLightGreen; ctx.fillRect(x + 4, 0, 10, bodyH);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, 0, 4, bodyH);
                ctx.fillStyle = colDarkGreen; ctx.fillRect(x + width - 12, 0, 12, bodyH);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, 0, width, bodyH);

                let rimY = bodyH;
                let rX = x - 3, rW = width + 6;
                ctx.fillStyle = colMainGreen; ctx.fillRect(rX, rimY, rW, 28);
                ctx.fillStyle = colLightGreen; ctx.fillRect(rX + 5, rimY, 12, 28);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(rX + 17, rimY, 4, 28);
                ctx.fillStyle = colDarkGreen; ctx.fillRect(rX + rW - 14, rimY, 14, 28);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(rX, rimY, rW, 28);
            } else {
                let rimY = y;
                let bodyY = y + 28;
                let bodyH = Math.max(0, canvas.height - bodyY);
                let rX = x - 3, rW = width + 6;
                ctx.fillStyle = colMainGreen; ctx.fillRect(x, bodyY, width, bodyH);
                ctx.fillStyle = colLightGreen; ctx.fillRect(x + 4, bodyY, 10, bodyH);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, bodyY, 4, bodyH);
                ctx.fillStyle = colDarkGreen; ctx.fillRect(x + width - 12, bodyY, 12, bodyH);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, bodyY, width, bodyH);

                ctx.fillStyle = colMainGreen; ctx.fillRect(rX, rimY, rW, 28);
                ctx.fillStyle = colLightGreen; ctx.fillRect(rX + 5, rimY, 12, 28);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(rX + 17, rimY, 4, 28);
                ctx.fillStyle = colDarkGreen; ctx.fillRect(rX + rW - 14, rimY, 14, 28);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(rX, rimY, rW, 28);
            }
        }
        else if (difficulty === 'NORMAL') {
            const colDarkBorder = '#281038';
            const colMainPurple = '#9a50c8';
            const colLightPurple= '#c088f0';
            const colWhiteLine  = '#ffffff';
            const colDarkPurple = '#682898';

            if (isTop) {
                let bodyH = Math.max(0, height - 44);
                ctx.fillStyle = colMainPurple; ctx.fillRect(x, 0, width, bodyH);
                ctx.fillStyle = colLightPurple; ctx.fillRect(x + 4, 0, 10, bodyH);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, 0, 4, bodyH);
                ctx.fillStyle = colDarkPurple; ctx.fillRect(x + width - 12, 0, 12, bodyH);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, 0, width, bodyH);

                drawPurpleFistGlove(x, bodyH + 44, width, true);
            } else {
                let bodyY = y + 44;
                let bodyH = Math.max(0, canvas.height - bodyY);
                ctx.fillStyle = colMainPurple; ctx.fillRect(x, bodyY, width, bodyH);
                ctx.fillStyle = colLightPurple; ctx.fillRect(x + 4, bodyY, 10, bodyH);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, bodyY, 4, bodyH);
                ctx.fillStyle = colDarkPurple; ctx.fillRect(x + width - 12, 0, 12, bodyH);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, bodyY, width, bodyH);

                drawPurpleFistGlove(x, y, width, false);
            }
        }
        else if (difficulty === 'HARD') {
            const colDarkBorder = '#3a0808';
            const colMainRed    = '#d83838';
            const colLightRed   = '#f87878';
            const colWhiteLine  = '#ffffff';
            const colDarkRed    = '#981818';

            if (isTop) {
                let bodyH = Math.max(0, height - 28);
                ctx.fillStyle = colMainRed; ctx.fillRect(x, 0, width, bodyH);
                ctx.fillStyle = colLightRed; ctx.fillRect(x + 4, 0, 10, bodyH);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, 0, 4, bodyH);
                ctx.fillStyle = colDarkRed; ctx.fillRect(x + width - 12, 0, 12, bodyH);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, 0, width, bodyH);

                let rimY = bodyH;
                let rX = x - 3, rW = width + 6;
                ctx.fillStyle = colMainRed; ctx.fillRect(rX, rimY, rW, 28);
                ctx.fillStyle = colLightRed; ctx.fillRect(rX + 5, rimY, 12, 28);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(rX + 17, rimY, 4, 28);
                ctx.fillStyle = colDarkRed; ctx.fillRect(rX + rW - 14, rimY, 14, 28);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(rX, rimY, rW, 28);

                ctx.fillStyle = '#ffffff';
                for (let i = 0; i < width; i += 8) {
                    ctx.beginPath();
                    ctx.moveTo(x + i, rimY + 28);
                    ctx.lineTo(x + i + 4, rimY + 34);
                    ctx.lineTo(x + i + 8, rimY + 28);
                    ctx.fill();
                }

                drawHardPipeEyes(rX, rimY, rW, true);
            } else {
                let rimY = y;
                let bodyY = y + 28;
                let bodyH = Math.max(0, canvas.height - bodyY);
                let rX = x - 3, rW = width + 6;
                ctx.fillStyle = colMainRed; ctx.fillRect(x, bodyY, width, bodyH);
                ctx.fillStyle = colLightRed; ctx.fillRect(x + 4, bodyY, 10, bodyH);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, bodyY, 4, bodyH);
                ctx.fillStyle = colDarkRed; ctx.fillRect(x + width - 12, bodyY, 12, bodyH);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, bodyY, width, bodyH);

                ctx.fillStyle = colMainRed; ctx.fillRect(rX, rimY, rW, 28);
                ctx.fillStyle = colLightRed; ctx.fillRect(rX + 5, rimY, 12, 28);
                ctx.fillStyle = colWhiteLine; ctx.fillRect(rX + 17, rimY, 4, 28);
                ctx.fillStyle = colDarkRed; ctx.fillRect(rX + rW - 14, rimY, 14, 28);
                ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(rX, rimY, rW, 28);

                ctx.fillStyle = '#ffffff';
                for (let i = 0; i < width; i += 8) {
                    ctx.beginPath();
                    ctx.moveTo(x + i, rimY);
                    ctx.lineTo(x + i + 4, rimY - 6);
                    ctx.lineTo(x + i + 8, rimY);
                    ctx.fill();
                }

                drawHardPipeEyes(rX, rimY, rW, false);
            }
        }
    }
    ctx.restore();
}

function drawBackgroundCity() {
    if (currentDifficulty === 'EASY') {
        ctx.fillStyle = '#70c5ce'; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#a1e4c3';
        ctx.beginPath();
        ctx.arc(60, 520, 70, 0, Math.PI * 2);
        ctx.arc(180, 530, 80, 0, Math.PI * 2);
        ctx.arc(320, 520, 90, 0, Math.PI * 2);
        ctx.arc(440, 530, 75, 0, Math.PI * 2);
        ctx.fill();
    } 
    else if (currentDifficulty === 'NORMAL') {
        ctx.fillStyle = '#e8b0d8'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    } 
    else if (currentDifficulty === 'HARD') {
        ctx.fillStyle = '#e87878'; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#c85050';
        ctx.fillRect(50, 460, 60, 100);
        ctx.fillRect(170, 430, 70, 130);
        ctx.fillRect(320, 450, 80, 110);
    }
}

function drawGround() {
    let groundCol = '#ded895';
    let grassCol = '#75cb27';
    let grassTop = '#9bd843';

    if (currentDifficulty === 'NORMAL') {
        groundCol = '#c098d8'; grassCol = '#9a50c8'; grassTop = '#b878e8';
    } else if (currentDifficulty === 'HARD') {
        groundCol = '#d8b095'; grassCol = '#d83838'; grassTop = '#f87878';
    }

    ctx.fillStyle = groundCol; ctx.fillRect(0, canvas.height - 80, canvas.width, 80);
    ctx.strokeStyle = '#232b1a'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(0, canvas.height - 80); ctx.lineTo(canvas.width, canvas.height - 80); ctx.stroke();
    
    ctx.fillStyle = grassCol; ctx.fillRect(0, canvas.height - 80, canvas.width, 16);
    ctx.fillStyle = grassTop;
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
        drawPixelBird(btn.x + btn.w / 2, btn.y + btn.h / 2, selectedSkin, 2.4);
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
    drawPixelBird(canvas.width / 2, floatY, selectedSkin, 3.0);

    drawMenuButton(menuPlayBtn, true);
    drawMenuButton(menuCharBtn, false);
}

function drawDifficultyMenu() {
    let titleX = canvas.width / 2;
    let titleY = 130;

    ctx.save();
    ctx.font = '900 38px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#000000'; ctx.fillText('CHỌN ĐỘ KHÓ', titleX + 3, titleY + 3);
    ctx.fillStyle = '#f8d038'; ctx.fillText('CHỌN ĐỘ KHÓ', titleX, titleY);
    ctx.restore();

    drawDiffButton(diffEasyBtn, 'DỄ', '#54cb37');
    drawDiffButton(diffNormalBtn, 'TRUNG BÌNH', '#9a50c8');
    drawDiffButton(diffHardBtn, 'KHÓ', '#d83838');
    drawDiffButton(diffBackBtn, 'QUAY LẠI', '#555555');
}

function drawDiffButton(btn, label, color) {
    ctx.save();
    ctx.fillStyle = '#3a2000';
    ctx.fillRect(btn.x - 3, btn.y - 3, btn.w + 6, btn.h + 6);

    ctx.fillStyle = color;
    ctx.fillRect(btn.x, btn.y, btn.w, btn.h);

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(btn.x, btn.y, btn.w, 4);
    ctx.fillRect(btn.x, btn.y, 4, btn.h);

    ctx.font = '900 20px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(label, btn.x + btn.w / 2, btn.y + 40);
    ctx.restore();
}

function drawCharacterMenu() {
    let panelX = 30, panelY = 30, panelW = 420, panelH = 580;
    ctx.fillStyle = '#bdebf2'; ctx.fillRect(panelX, panelY, panelW, panelH);
    ctx.strokeStyle = '#2b484f'; ctx.lineWidth = 6; ctx.strokeRect(panelX, panelY, panelW, panelH);

    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3; ctx.strokeRect(panelX + 4, panelY + 4, panelW - 8, panelH - 8);

    ctx.font = '900 32px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#3a2050'; ctx.fillText('HIỆU ỨNG NHÂN VẬT', canvas.width / 2 + 2, panelY + 45);

    const startGridX = 55, startGridY = 85, boxW = 110, boxH = 135, gapX = 20, gapY = 15;
    CHARACTERS.forEach((char, i) => {
        let col = i % 3;
        let row = Math.floor(i / 3);
        let bx = startGridX + col * (boxW + gapX);
        let by = startGridY + row * (boxH + gapY);
        let isSelected = (selectedSkin === i);

        ctx.fillStyle = '#a6e3ed'; ctx.fillRect(bx, by, boxW, boxH);
        if (isSelected) {
            ctx.strokeStyle = '#d49b00'; ctx.lineWidth = 5; ctx.strokeRect(bx - 2, by - 2, boxW + 4, boxH + 4);
            ctx.strokeStyle = '#fff7b2'; ctx.lineWidth = 2; ctx.strokeRect(bx, by, boxW, boxH);
        } else {
            ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.strokeRect(bx, by, boxW, boxH);
        }

        drawPixelBird(bx + boxW / 2, by + 32, i, 2.0);

        ctx.fillStyle = isSelected ? '#d49b00' : '#457a82';
        ctx.fillRect(bx + 8, by + 65, boxW - 16, 16);
        ctx.strokeStyle = '#000'; ctx.lineWidth = 1; ctx.strokeRect(bx + 8, by + 65, boxW - 16, 16);

        ctx.fillStyle = '#ffffff'; ctx.font = 'bold 10px "Courier New"';
        ctx.fillText(char.name, bx + boxW / 2, by + 77);

        ctx.fillStyle = '#222222'; ctx.font = 'bold 8px "Courier New"';
        ctx.fillText(char.effect, bx + boxW / 2, by + 95);

        ctx.fillStyle = isSelected ? '#f8b000' : '#e0f8f8';
        ctx.fillRect(bx + 15, by + 104, boxW - 30, 20);
        ctx.strokeStyle = '#000'; ctx.lineWidth = 1.5; ctx.strokeRect(bx + 15, by + 104, boxW - 30, 20);

        ctx.fillStyle = isSelected ? '#ffffff' : '#000000';
        ctx.font = 'bold 10px "Courier New"';
        ctx.fillText('CHỌN', bx + boxW / 2, by + 118);
    });

    ctx.fillStyle = '#75cb27'; ctx.fillRect(140, 550, 200, 38);
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.strokeRect(140, 550, 200, 38);
    ctx.fillStyle = '#fff'; ctx.font = 'bold 16px "Courier New"';
    ctx.fillText('QUAY LẠI', canvas.width / 2, 574);
}

function drawPixelMedal(cx, cy, currentScore) {
    ctx.save();
    ctx.translate(cx, cy);
    const p = 2;

    let colBorder = '#8a5014';
    let colMain   = '#f8b000';
    let colLight  = '#ffe066';
    let colDark   = '#d48800';

    if (currentScore >= 30) { 
        colBorder = '#1c4a52'; colMain = '#40e0d0'; colLight = '#a6f7f0'; colDark = '#20b2aa';
    } else if (currentScore >= 20) { 
        colBorder = '#8a5014'; colMain = '#f8d038'; colLight = '#fff4a3'; colDark = '#d49b00';
    } else if (currentScore >= 10) { 
        colBorder = '#3a3a3a'; colMain = '#d0d0d0'; colLight = '#ffffff'; colDark = '#a0a0a0';
    } else if (currentScore >= 5) { 
        colBorder = '#4a250a'; colMain = '#cc7722'; colLight = '#f8a866'; colDark = '#994411';
    }

    ctx.fillStyle = colBorder;
    ctx.fillRect(-11*p, -15*p, 22*p, 30*p);
    ctx.fillRect(-15*p, -11*p, 30*p, 22*p);
    ctx.fillRect(-13*p, -13*p, 26*p, 26*p);

    ctx.fillStyle = colMain;
    ctx.fillRect(-10*p, -13*p, 20*p, 26*p);
    ctx.fillRect(-13*p, -10*p, 26*p, 20*p);
    ctx.fillRect(-11*p, -11*p, 22*p, 22*p);

    ctx.fillStyle = colLight;
    ctx.fillRect(-9*p, -11*p, 14*p, 4*p);
    ctx.fillRect(-11*p, -9*p, 4*p, 14*p);

    ctx.fillStyle = colDark;
    ctx.fillRect(-5*p, 9*p, 14*p, 3*p);
    ctx.fillRect(9*p, -5*p, 3*p, 14*p);

    ctx.restore();
}

function drawGameOverScreen() {
    let titleX = canvas.width / 2;
    let titleY = 140;

    ctx.save();
    ctx.font = '900 44px "Courier New", sans-serif';
    ctx.textAlign = 'center';

    ctx.fillStyle = '#3a2000';
    ctx.fillText('game over', titleX + 4, titleY + 4);
    ctx.fillStyle = '#f89020';
    ctx.fillText('game over', titleX, titleY);
    ctx.restore();

    let pbX = 50, pbY = 180, pbW = 380, pbH = 240;

    ctx.fillStyle = '#e8dcac';
    ctx.fillRect(pbX, pbY, pbW, pbH);
    ctx.strokeStyle = '#c4b078';
    ctx.lineWidth = 6;
    ctx.strokeRect(pbX, pbY, pbW, pbH);

    ctx.strokeStyle = '#5c4820';
    ctx.lineWidth = 3;
    ctx.strokeRect(pbX - 3, pbY - 3, pbW + 6, pbH + 6);

    ctx.fillStyle = '#d49040';
    ctx.font = 'bold 18px "Courier New"';
    ctx.textAlign = 'left';
    ctx.fillText('MEDAL', pbX + 40, pbY + 45);

    drawPixelMedal(pbX + 80, pbY + 125, score);

    ctx.textAlign = 'right';
    ctx.fillStyle = '#d49040';
    ctx.font = 'bold 18px "Courier New"';
    ctx.fillText('SCORE', pbX + pbW - 40, pbY + 45);

    drawPixelNumber(score, pbX + pbW - 40, pbY + 70);

    ctx.fillStyle = '#d49040';
    ctx.font = 'bold 18px "Courier New"';
    ctx.fillText('BEST', pbX + pbW - 40, pbY + 135);

    drawPixelNumber(highScore, pbX + pbW - 40, pbY + 160);

    drawOkShareBtn(gameOverOkBtn, 'OK');
    drawOkShareBtn(gameOverShareBtn, 'MENU');
}

function drawPixelNumber(num, rightX, topY) {
    ctx.save();
    ctx.font = '900 34px "Courier New", monospace';
    ctx.textAlign = 'right';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(num, rightX + 2, topY + 26);
    ctx.fillText(num, rightX - 2, topY + 26);
    ctx.fillText(num, rightX, topY + 28);
    ctx.fillText(num, rightX, topY + 24);

    ctx.fillStyle = '#000000';
    ctx.fillText(num, rightX, topY + 26);
    ctx.restore();
}

function drawOkShareBtn(btn, label) {
    ctx.save();
    ctx.fillStyle = '#4a1500';
    ctx.fillRect(btn.x - 3, btn.y - 3, btn.w + 6, btn.h + 6);

    ctx.fillStyle = '#e85800';
    ctx.fillRect(btn.x, btn.y, btn.w, btn.h);

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(btn.x, btn.y, btn.w, 4);
    ctx.fillRect(btn.x, btn.y, 4, btn.h);

    ctx.font = '900 22px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(label, btn.x + btn.w / 2, btn.y + 35);
    ctx.restore();
}

function drawUI() {
    if (gameState === 'START') {
        drawMainMenu();
    } else if (gameState === 'DIFFICULTY') {
        drawDifficultyMenu();
    } else if (gameState === 'CHARACTERS') {
        drawCharacterMenu();
    } else if (gameState === 'PLAYING') {
        ctx.fillStyle = '#fff'; ctx.strokeStyle = '#000'; ctx.lineWidth = 3;
        ctx.font = '36px Courier New'; ctx.textAlign = 'center';
        ctx.strokeText(score, canvas.width / 2, 60);
        ctx.fillText(score, canvas.width / 2, 60);
    } else if (gameState === 'GAMEOVER') {
        drawGameOverScreen();
    }
}

function triggerGameOver() {
    if (gameState !== 'GAMEOVER') { 
        playSound('hit'); 
        gameState = 'GAMEOVER'; 
    }
}

function loop() {
    if (gameState === 'PLAYING') {
        bird.update();
        pipes.update();
    }
    
    frames++;

    drawBackgroundCity();
    pipes.draw(); 
    drawGround();

    if (gameState === 'PLAYING') {
        bird.draw();
    }
    drawUI();

    requestAnimationFrame(loop);
}

// --- TƯƠNG TÁC ĐIỀU KHIỂN ---
function handleInteraction(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const clickX = clientX - rect.left;
    const clickY = clientY - rect.top;

    if (gameState === 'START') {
        if (clickX >= menuPlayBtn.x && clickX <= menuPlayBtn.x + menuPlayBtn.w &&
            clickY >= menuPlayBtn.y && clickY <= menuPlayBtn.y + menuPlayBtn.h) {
            gameState = 'DIFFICULTY'; 
            playSound('score');
            return;
        }
        if (clickX >= menuCharBtn.x && clickX <= menuCharBtn.x + menuCharBtn.w &&
            clickY >= menuCharBtn.y && clickY <= menuCharBtn.y + menuCharBtn.h) {
            gameState = 'CHARACTERS';
            playSound('score');
            return;
        }
    } 
    else if (gameState === 'DIFFICULTY') {
        if (clickX >= diffEasyBtn.x && clickX <= diffEasyBtn.x + diffEasyBtn.w &&
            clickY >= diffEasyBtn.y && clickY <= diffEasyBtn.y + diffEasyBtn.h) {
            pipes.setDifficulty('EASY');
            startGame();
            return;
        }
        if (clickX >= diffNormalBtn.x && clickX <= diffNormalBtn.x + diffNormalBtn.w &&
            clickY >= diffNormalBtn.y && clickY <= diffNormalBtn.y + diffNormalBtn.h) {
            pipes.setDifficulty('NORMAL');
            startGame();
            return;
        }
        if (clickX >= diffHardBtn.x && clickX <= diffHardBtn.x + diffHardBtn.w &&
            clickY >= diffHardBtn.y && clickY <= diffHardBtn.y + diffHardBtn.h) {
            pipes.setDifficulty('HARD');
            startGame();
            return;
        }
        if (clickX >= diffBackBtn.x && clickX <= diffBackBtn.x + diffBackBtn.w &&
            clickY >= diffBackBtn.y && clickY <= diffBackBtn.y + diffBackBtn.h) {
            gameState = 'START';
            playSound('score');
            return;
        }
    }
    else if (gameState === 'CHARACTERS') {
        const startGridX = 55, startGridY = 85, boxW = 110, boxH = 135, gapX = 20, gapY = 15;
        CHARACTERS.forEach((char, i) => {
            let col = i % 3; let row = Math.floor(i / 3);
            let bx = startGridX + col * (boxW + gapX);
            let by = startGridY + row * (boxH + gapY);

            if (clickX >= bx && clickX <= bx + boxW && clickY >= by && clickY <= by + boxH) {
                selectedSkin = i;
                playSound('score');
            }
        });

        if (clickX >= 140 && clickX <= 340 && clickY >= 550 && clickY <= 588) {
            gameState = 'START';
            playSound('score');
        }
    } 
    else if (gameState === 'PLAYING') {
        bird.jump();
    } 
    else if (gameState === 'GAMEOVER') {
        if (clickX >= gameOverOkBtn.x && clickX <= gameOverOkBtn.x + gameOverOkBtn.w &&
            clickY >= gameOverOkBtn.y && clickY <= gameOverOkBtn.y + gameOverOkBtn.h) {
            startGame();
            return;
        }
        if (clickX >= gameOverShareBtn.x && clickX <= gameOverShareBtn.x + gameOverShareBtn.w &&
            clickY >= gameOverShareBtn.y && clickY <= gameOverShareBtn.y + gameOverShareBtn.h) {
            gameState = 'START';
            return;
        }
    }
}

function startGame() {
    bird.reset(); 
    pipes.reset(); 
    score = 0; 
    frames = 0; 
    isNewHighScore = false;
    gameState = 'PLAYING'; 
    bird.jump();
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        e.preventDefault();
        if (gameState === 'START') {
            gameState = 'DIFFICULTY';
        } else if (gameState === 'DIFFICULTY') {
            pipes.setDifficulty('EASY');
            startGame();
        } else if (gameState === 'CHARACTERS') {
            gameState = 'START';
        } else if (gameState === 'PLAYING') {
            bird.jump();
        } else if (gameState === 'GAMEOVER') {
            startGame();
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
