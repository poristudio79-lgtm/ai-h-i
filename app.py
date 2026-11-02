import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird - Clean Normal Map", layout="centered")

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
    { id: 0, name: 'GBI', color: '#e82878', effect: 'Hào quang Đôi' },
    { id: 1, name: 'OHINH', color: '#f8d038', effect: 'Tia chớp Sét' },
    { id: 2, name: 'HOI BINK', color: '#509848', effect: 'Lá mầm Xanh' },
    { id: 3, name: 'KHON', color: '#8838d0', effect: 'Hỏa diệm Bùng' },
    { id: 4, name: 'BINH', color: '#38a8b8', effect: 'Bong bóng Nước' },
    { id: 5, name: 'NARWHAL', color: '#20b2aa', effect: 'Băng giá Tuyết' },
    { id: 6, name: 'BASKETBALL', color: '#f86820', effect: 'Đuôi Lửa Cháy' }
];

const menuPlayBtn = { x: 75, y: 410, w: 145, h: 90 };
const menuCharBtn = { x: 260, y: 410, w: 145, h: 90 };

const diffEasyBtn = { x: 100, y: 220, w: 280, h: 65 };   
const diffNormalBtn = { x: 100, y: 305, w: 280, h: 65 }; 
const diffHardBtn = { x: 100, y: 390, w: 280, h: 65 };   
const diffBackBtn = { x: 100, y: 480, w: 280, h: 50 };

const gameOverOkBtn = { x: 75, y: 470, w: 145, h: 55 };
const gameOverShareBtn = { x: 260, y: 470, w: 145, h: 55 };

// --- HÀM VẼ NHÂN VẬT ---
function drawClassicPixelBird(x, y, skinId, scale = 2.3, rotation = 0) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rotation);
    const p = scale;

    if (skinId === 6) {
        ctx.fillStyle = '#2b1008';
        ctx.fillRect(-5*p, -6*p, 8*p, 1*p);
        ctx.fillRect(-8*p, -5*p, 12*p, 1*p);
        ctx.fillRect(-9*p, -4*p, 15*p, 1*p);
        ctx.fillRect(-10*p, -3*p, 18*p, 5*p);
        ctx.fillRect(-9*p, 2*p, 17*p, 2*p);
        ctx.fillRect(-8*p, 4*p, 15*p, 2*p);
        ctx.fillRect(-5*p, 6*p, 9*p, 1*p);

        ctx.fillStyle = '#f87820';
        ctx.fillRect(-4*p, -5*p, 6*p, 1*p);
        ctx.fillRect(-7*p, -4*p, 9*p, 1*p);
        ctx.fillRect(-8*p, -3*p, 12*p, 5*p);
        ctx.fillRect(-7*p, 2*p, 11*p, 2*p);
        ctx.fillRect(-6*p, 4*p, 9*p, 2*p);

        ctx.fillStyle = '#2b1008';
        ctx.fillRect(-2*p, -3*p, 1*p, 8*p);
        ctx.fillRect(-8*p, -1*p, 13*p, 1*p);

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(1*p, -5*p, 6*p, 6*p);
        ctx.fillRect(0*p, -4*p, 8*p, 4*p);
        ctx.fillStyle = '#2b1008';
        ctx.fillRect(1*p, -5*p, 6*p, 1*p);
        ctx.fillRect(7*p, -4*p, 1*p, 4*p);
        ctx.fillRect(1*p, 1*p, 6*p, 1*p);
        ctx.fillRect(0*p, -4*p, 1*p, 4*p);
        ctx.fillStyle = '#000000';
        ctx.fillRect(4*p, -3*p, 2*p, 4*p);
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(5*p, -2*p, 1*p, 1*p);

        ctx.fillStyle = '#2b1008';
        ctx.fillRect(2*p, 0*p, 8*p, 5*p);
        ctx.fillStyle = '#d84810';
        ctx.fillRect(3*p, 1*p, 6*p, 3*p);
        ctx.fillStyle = '#f8a020';
        ctx.fillRect(3*p, 1*p, 6*p, 1*p);
        ctx.fillStyle = '#2b1008';
        ctx.fillRect(2*p, 2*p, 7*p, 1*p);

        ctx.restore();
        return;
    }

    const skinThemes = [
        { body: '#e82878', belly: '#f8a0c8', wing: '#ffffff', beak: '#f85820', outline: '#2b1018' },
        { body: '#f8d038', belly: '#f8ea88', wing: '#ffffff', beak: '#f85820', outline: '#2b221e' },
        { body: '#509848', belly: '#98e888', wing: '#ffffff', beak: '#f87820', outline: '#122b12' },
        { body: '#8838d0', belly: '#c888f8', wing: '#f878c0', beak: '#f89020', outline: '#1b0a2b' },
        { body: '#38a8b8', belly: '#88e0f0', wing: '#ffffff', beak: '#306870', outline: '#0a1d20' },
        { body: '#20b2aa', belly: '#e0f8f8', wing: '#ffffff', beak: '#f85820', outline: '#081a18' }
    ];

    let t = skinThemes[skinId] || skinThemes[1];

    ctx.fillStyle = t.outline;
    ctx.fillRect(-5*p, -6*p, 8*p, 1*p);
    ctx.fillRect(-8*p, -5*p, 12*p, 1*p);
    ctx.fillRect(-9*p, -4*p, 15*p, 1*p);
    ctx.fillRect(-10*p, -3*p, 18*p, 5*p);
    ctx.fillRect(-9*p, 2*p, 17*p, 2*p);
    ctx.fillRect(-8*p, 4*p, 15*p, 2*p);
    ctx.fillRect(-5*p, 6*p, 9*p, 1*p);

    ctx.fillStyle = t.body;
    ctx.fillRect(-4*p, -5*p, 6*p, 1*p);
    ctx.fillRect(-7*p, -4*p, 9*p, 1*p);
    ctx.fillRect(-8*p, -3*p, 12*p, 5*p);
    ctx.fillRect(-7*p, 2*p, 11*p, 2*p);
    ctx.fillRect(-6*p, 4*p, 9*p, 2*p);

    ctx.fillStyle = t.belly;
    ctx.fillRect(-5*p, 3*p, 7*p, 2*p);
    ctx.fillRect(-3*p, 5*p, 4*p, 1*p);

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(1*p, -5*p, 6*p, 6*p);
    ctx.fillRect(0*p, -4*p, 8*p, 4*p);
    
    ctx.fillStyle = t.outline;
    ctx.fillRect(1*p, -5*p, 6*p, 1*p);
    ctx.fillRect(7*p, -4*p, 1*p, 4*p);
    ctx.fillRect(1*p, 1*p, 6*p, 1*p);
    ctx.fillRect(0*p, -4*p, 1*p, 4*p);

    ctx.fillStyle = '#000000';
    ctx.fillRect(4*p, -3*p, 2*p, 4*p);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(5*p, -2*p, 1*p, 1*p);

    ctx.fillStyle = t.outline;
    ctx.fillRect(-8*p, -1*p, 5*p, 4*p);
    ctx.fillStyle = t.wing;
    ctx.fillRect(-7*p, 0*p, 4*p, 3*p);
    ctx.fillStyle = '#f8ea88';
    ctx.fillRect(-6*p, 1*p, 3*p, 2*p);

    ctx.fillStyle = t.outline;
    ctx.fillRect(2*p, 0*p, 8*p, 5*p);

    ctx.fillStyle = t.beak;
    ctx.fillRect(3*p, 1*p, 6*p, 3*p);
    ctx.fillStyle = '#f8a020';
    ctx.fillRect(3*p, 1*p, 6*p, 1*p);

    ctx.fillStyle = t.outline;
    ctx.fillRect(2*p, 2*p, 7*p, 1*p);

    if (skinId === 5) {
        ctx.fillStyle = '#ffffff'; ctx.strokeStyle = t.outline; ctx.lineWidth = 1.5;
        ctx.fillRect(2*p, -9*p, 2*p, 4*p);
        ctx.strokeRect(2*p, -9*p, 2*p, 4*p);
    }

    ctx.restore();
}

// --- HIỆU ỨNG ĐẶC BIỆT NHÂN VẬT ---
function drawSkinEffects(x, y, skinId) {
    ctx.save();
    let time = frames * 0.12;

    if (skinId === 6) {
        let flameW = 28 + Math.sin(frames * 0.4) * 8;
        let flameH = 16 + Math.cos(frames * 0.3) * 5;

        ctx.fillStyle = 'rgba(248, 56, 16, 0.85)';
        ctx.beginPath();
        ctx.moveTo(x - 12, y);
        ctx.lineTo(x - 35 - flameW, y - flameH);
        ctx.lineTo(x - 28, y);
        ctx.lineTo(x - 35 - flameW, y + flameH);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = 'rgba(255, 200, 0, 0.95)';
        ctx.beginPath();
        ctx.moveTo(x - 10, y);
        ctx.lineTo(x - 22 - flameW * 0.7, y - flameH * 0.5);
        ctx.lineTo(x - 18, y);
        ctx.lineTo(x - 22 - flameW * 0.7, y + flameH * 0.5);
        ctx.closePath();
        ctx.fill();

        let sparkX = x - 25 - ((frames * 3) % 45);
        let sparkY = y + Math.sin(time * 2) * 12;
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(sparkX, sparkY, 4, 4);
        ctx.fillStyle = '#ff4500';
        ctx.fillRect(sparkX + 2, sparkY + 2, 3, 3);
        
        ctx.restore();
        return;
    }

    if (skinId === 0) {
        ctx.strokeStyle = 'rgba(255, 60, 150, 0.8)';
        ctx.lineWidth = 3.5;
        ctx.beginPath();
        ctx.arc(x, y, 20 + Math.sin(time) * 4, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = 'rgba(255, 200, 230, 0.5)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(x, y, 25 + Math.cos(time) * 3, 0, Math.PI * 2);
        ctx.stroke();
    } 
    else if (skinId === 1) {
        if (frames % 12 < 7) {
            ctx.strokeStyle = '#ffff00';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(x - 22, y - 8);
            ctx.lineTo(x - 6, y + 10);
            ctx.lineTo(x + 10, y - 4);
            ctx.lineTo(x + 20, y + 12);
            ctx.stroke();

            ctx.fillStyle = '#ffffff';
            ctx.fillRect(x + 8, y - 12, 4, 4);
        }
    } 
    else if (skinId === 2) {
        for (let i = 0; i < 4; i++) {
            let angle = time + i * (Math.PI / 2);
            let lx = x - 16 + Math.cos(angle) * 14;
            let ly = y + Math.sin(angle) * 12;
            ctx.fillStyle = (i % 2 === 0) ? '#78c038' : '#b8e637';
            ctx.fillRect(lx, ly, 6, 4);
        }
    } 
    else if (skinId === 3) {
        let flamePulse = Math.sin(time * 3) * 3;
        ctx.fillStyle = 'rgba(248, 88, 168, 0.9)';
        ctx.beginPath();
        ctx.arc(x - 12, y + 5, 8 + flamePulse, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = 'rgba(136, 56, 208, 0.8)';
        ctx.beginPath();
        ctx.arc(x - 17, y + 2, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffffff';
        ctx.fillRect(x - 14, y + 3, 3, 3);
    } 
    else if (skinId === 4) {
        let bx = x - 18 - ((frames * 1.8) % 35);
        let by = y + Math.sin(time * 1.5) * 12;
        
        ctx.strokeStyle = 'rgba(120, 224, 240, 0.9)';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(bx, by, 6, 0, Math.PI * 2); ctx.stroke();

        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.fillRect(bx - 2, by - 2, 3, 3);

        let bx2 = x - 10 - ((frames * 1.2) % 22);
        let by2 = y - 8 + Math.cos(time) * 8;
        ctx.strokeStyle = 'rgba(120, 224, 240, 0.7)';
        ctx.beginPath(); ctx.arc(bx2, by2, 3.5, 0, Math.PI * 2); ctx.stroke();
    } 
    else if (skinId === 5) {
        for (let i = 0; i < 4; i++) {
            let tx = x - 10 - (i * 10 + (frames * 2) % 25);
            let ty = y - 15 + (i * 8 + frames * 1.5) % 30;
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(tx, ty, 4, 4);
            ctx.fillStyle = '#20b2aa';
            ctx.fillRect(tx + 1, ty + 1, 2, 2);
        }
    }
    ctx.restore();
}

// --- ĐỐI TƯỢNG CHIM ---
const bird = {
    x: 90, y: 250, radius: 13, gravity: 0.28, jumpForce: -5.2, velocity: 0,
    draw() {
        let rotation = Math.min(Math.PI / 2.5, Math.max(-Math.PI / 4, (this.velocity / 12)));
        drawSkinEffects(this.x, this.y, selectedSkin);
        drawClassicPixelBird(this.x, this.y, selectedSkin, 2.2, rotation);
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
    items: [], gap: 130, width: 56, speed: 2.2,
    
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
            drawPipesByTheme(p.x, 0, this.width, p.top, true, currentDifficulty);
            drawPipesByTheme(p.x, p.bottom, this.width, canvas.height - 80 - p.bottom, false, currentDifficulty);
        });
    },
    update() {
        if (frames % 95 === 0) {
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
    }
};

// --- HÀM VẼ HÀNG RĂNG NHỌN TẠI MIỆNG ỐNG CỐNG ---
function drawPipeTeeth(x, rimY, width, isTop) {
    ctx.save();
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#280808';
    ctx.lineWidth = 2;

    const toothWidth = 8;
    const toothHeight = 9;

    if (isTop) {
        let bottomEdgeY = rimY + 28;
        for (let i = 2; i < width + 6 - toothWidth; i += toothWidth + 2) {
            let tx = x - 3 + i;
            ctx.beginPath();
            ctx.moveTo(tx, bottomEdgeY);
            ctx.lineTo(tx + toothWidth / 2, bottomEdgeY + toothHeight);
            ctx.lineTo(tx + toothWidth, bottomEdgeY);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
        }
    } else {
        let topEdgeY = rimY;
        for (let i = 2; i < width + 6 - toothWidth; i += toothWidth + 2) {
            let tx = x - 3 + i;
            ctx.beginPath();
            ctx.moveTo(tx, topEdgeY);
            ctx.lineTo(tx + toothWidth / 2, topEdgeY - toothHeight);
            ctx.lineTo(tx + toothWidth, topEdgeY);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
        }
    }
    ctx.restore();
}

// --- HÀM VẼ GĂNG TAY TÍM ---
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
        ctx.strokeStyle = colBorder; ctx.lineWidth = 3; ctx.strokeRect(gx - 10, gy + 18, 4, 12);

        ctx.strokeStyle = colBorder; ctx.lineWidth = 3.5;
        ctx.strokeRect(gx - 4, gy + 12, width + 20, 32);
    }
    ctx.restore();
}

// --- HÀM VẼ ĐÔI MẮT QUỶ TRÊN NẮP CỐNG KHÓ ---
function drawHardPipeEyes(x, rimY, rW, isTop) {
    ctx.save();
    let eyeCenterX1 = x + rW * 0.3;
    let eyeCenterX2 = x + rW * 0.7;
    let eyeY = rimY + 14;

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

// --- HỆ THỐNG VẼ CỐNG ---
function drawPipesByTheme(x, y, width, height, isTop, difficulty) {
    ctx.save();

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

            drawPipeTeeth(x, rimY, width, true);
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

            drawPipeTeeth(x, rimY, width, false);
        }
    }
    else if (difficulty === 'NORMAL') {
        const colDarkBorder = '#281038';
        const colMainPurple = '#9a50c8';
        const colDarkPurple = '#682898';

        if (isTop) {
            let bodyH = Math.max(0, height - 44);
            // Thân cống màu tím liền mạch, không còn sọc dọc
            ctx.fillStyle = colMainPurple; ctx.fillRect(x, 0, width, bodyH);
            ctx.fillStyle = colDarkPurple; ctx.fillRect(x + width - 12, 0, 12, bodyH);
            ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, 0, width, bodyH);

            drawPurpleFistGlove(x, bodyH + 44, width, true);
            drawPipeTeeth(x, bodyH + 16, width, true);
        } else {
            let bodyY = y + 44;
            let bodyH = Math.max(0, canvas.height - bodyY);
            ctx.fillStyle = colMainPurple; ctx.fillRect(x, bodyY, width, bodyH);
            ctx.fillStyle = colDarkPurple; ctx.fillRect(x + width - 12, 0, 12, bodyH);
            ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, bodyY, width, bodyH);

            drawPurpleFistGlove(x, y, width, false);
            drawPipeTeeth(x, y, width, false);
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

            drawHardPipeEyes(rX, rimY, rW, true);
            drawPipeTeeth(x, rimY, width, true);
        } else {
            let rimY = y;
            let bodyY = y + 28;
            let bodyH = Math.max(0, canvas.height - bodyY);
            let rX = x - 3, rW = width + 6;
            ctx.fillStyle = colMainRed; ctx.fillRect(x, bodyY, width, bodyH);
            ctx.fillStyle = colLightRed; ctx.fillRect(x + 4, bodyY, 10, bodyH);
            ctx.fillStyle = colWhiteLine; ctx.fillRect(x + 14, bodyY, 4, bodyH);
            ctx.fillStyle = colDarkRed; ctx.fillRect(rX + rW - 14, rimY, 14, 28);
            ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(x, bodyY, width, bodyH);

            ctx.fillStyle = colMainRed; ctx.fillRect(rX, rimY, rW, 28);
            ctx.fillStyle = colLightRed; ctx.fillRect(rX + 5, rimY, 12, 28);
            ctx.fillStyle = colWhiteLine; ctx.fillRect(rX + 17, rimY, 4, 28);
            ctx.fillStyle = colDarkRed; ctx.fillRect(rX + rW - 14, rimY, 14, 28);
            ctx.strokeStyle = colDarkBorder; ctx.lineWidth = 3; ctx.strokeRect(rX, rimY, rW, 28);

            drawHardPipeEyes(rX, rimY, rW, false);
            drawPipeTeeth(x, rimY, width, false);
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
        drawClassicPixelBird(btn.x + btn.w / 2, btn.y + btn.h / 2, selectedSkin, 2.4);
    }
}

// --- HÀM VẼ TIÊU ĐỀ 3D PIXEL RỰC RỠ ---
function drawRetroPixelTitle(cx, topY) {
    ctx.save();
    const p = 5;

    const LETTER_PIXELS = {
        'F': [[1,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,0],[1,0,0,0]],
        'L': [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,1,1,1]],
        'A': [[0,1,1,0],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]],
        'P': [[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,0],[1,0,0,0]],
        'Y': [[1,0,0,1],[1,0,0,1],[0,1,1,0],[0,1,0,0],[0,1,0,0]],
        'B': [[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,1],[1,1,1,0]],
        'I': [[1,1,1],[0,1,0],[0,1,0],[0,1,0],[1,1,1]],
        'R': [[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,1,0],[1,0,0,1]],
        'D': [[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,0]]
    };

    const word1Colors = ['#f8d038', '#f85820', '#e82878', '#a038d0', '#38a8b8', '#509848'];
    const word2Colors = ['#a038d0', '#f8d038', '#f85820', '#38a8b8'];

    let word1 = ['F','L','A','P','P','Y'];
    let startX1 = cx - 135;
    let currX1 = startX1;

    word1.forEach((char, idx) => {
        let grid = LETTER_PIXELS[char];
        let color = word1Colors[idx % word1Colors.length];

        for (let r = 0; r < grid.length; r++) {
            for (let c = 0; c < grid[r].length; c++) {
                if (grid[r][c] === 1) {
                    let bx = currX1 + c * p;
                    let by = topY + r * p;

                    ctx.fillStyle = '#000000';
                    ctx.fillRect(bx + 4, by + 4, p, p);

                    ctx.fillStyle = color;
                    ctx.fillRect(bx, by, p, p);

                    ctx.strokeStyle = '#2b221e';
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(bx, by, p, p);
                }
            }
        }
        currX1 += (grid[0].length + 1) * p;
    });

    let word2 = ['B','I','R','D'];
    let startX2 = cx - 80;
    let currX2 = startX2;
    let topY2 = topY + 38;

    word2.forEach((char, idx) => {
        let grid = LETTER_PIXELS[char];
        let color = word2Colors[idx % word2Colors.length];

        for (let r = 0; r < grid.length; r++) {
            for (let c = 0; c < grid[r].length; c++) {
                if (grid[r][c] === 1) {
                    let bx = currX2 + c * p;
                    let by = topY2 + r * p;

                    ctx.fillStyle = '#000000';
                    ctx.fillRect(bx + 4, by + 4, p, p);

                    ctx.fillStyle = color;
                    ctx.fillRect(bx, by, p, p);

                    ctx.strokeStyle = '#2b221e';
                    ctx.lineWidth = 1.5;
                    ctx.strokeRect(bx, by, p, p);
                }
            }
        }
        currX2 += (grid[0].length + 1) * p;
    });

    ctx.restore();
}

function drawMainMenu() {
    let titleX = canvas.width / 2;
    drawRetroPixelTitle(titleX, 90);

    let floatY = 250 + Math.sin(frames * 0.08) * 8;
    drawClassicPixelBird(canvas.width / 2, floatY, selectedSkin, 3.0);

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
    let panelX = 20, panelY = 20, panelW = 440, panelH = 600;
    ctx.fillStyle = '#bdebf2'; ctx.fillRect(panelX, panelY, panelW, panelH);
    ctx.strokeStyle = '#2b484f'; ctx.lineWidth = 6; ctx.strokeRect(panelX, panelY, panelW, panelH);

    ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3; ctx.strokeRect(panelX + 4, panelY + 4, panelW - 8, panelH - 8);

    ctx.font = '900 28px "Courier New", sans-serif';
    ctx.textAlign = 'center';
    ctx.fillStyle = '#3a2050'; ctx.fillText('HIỆU ỨNG NHÂN VẬT', canvas.width / 2 + 1, panelY + 38);

    const startGridX = 40, startGridY = 70, boxW = 120, boxH = 115, gapX = 20, gapY = 12;
    CHARACTERS.forEach((char, i) => {
        let col = i % 3;
        let row = Math.floor(i / 3);
        let bx = startGridX + col * (boxW + gapX);
        let by = startGridY + row * (boxH + gapY);
        let isSelected = (selectedSkin === i);

        ctx.fillStyle = '#a6e3ed'; ctx.fillRect(bx, by, boxW, boxH);
        if (isSelected) {
            ctx.strokeStyle = '#d49b00'; ctx.lineWidth = 4; ctx.strokeRect(bx - 2, by - 2, boxW + 4, boxH + 4);
            ctx.strokeStyle = '#fff7b2'; ctx.lineWidth = 2; ctx.strokeRect(bx, by, boxW, boxH);
        } else {
            ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.strokeRect(bx, by, boxW, boxH);
        }

        drawClassicPixelBird(bx + boxW / 2, by + 26, i, 1.7);

        ctx.fillStyle = isSelected ? '#d49b00' : '#457a82';
        ctx.fillRect(bx + 6, by + 54, boxW - 12, 14);
        ctx.strokeStyle = '#000'; ctx.lineWidth = 1; ctx.strokeRect(bx + 6, by + 54, boxW - 12, 14);

        ctx.fillStyle = '#ffffff'; ctx.font = 'bold 9px "Courier New"';
        ctx.fillText(char.name, bx + boxW / 2, by + 64);

        ctx.fillStyle = '#222222'; ctx.font = 'bold 8px "Courier New"';
        ctx.fillText(char.effect, bx + boxW / 2, by + 78);

        ctx.fillStyle = isSelected ? '#f8b000' : '#e0f8f8';
        ctx.fillRect(bx + 12, by + 86, boxW - 24, 18);
        ctx.strokeStyle = '#000'; ctx.lineWidth = 1.5; ctx.strokeRect(bx + 12, by + 86, boxW - 24, 18);

        ctx.fillStyle = isSelected ? '#ffffff' : '#000000';
        ctx.font = 'bold 9px "Courier New"';
        ctx.fillText('CHỌN', bx + boxW / 2, by + 98);
    });

    ctx.fillStyle = '#75cb27'; ctx.fillRect(140, 560, 200, 32);
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; ctx.strokeRect(140, 560, 200, 32);
    ctx.fillStyle = '#fff'; ctx.font = 'bold 15px "Courier New"';
    ctx.fillText('QUAY LẠI', canvas.width / 2, 581);
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
        const startGridX = 40, startGridY = 70, boxW = 120, boxH = 115, gapX = 20, gapY = 12;
        CHARACTERS.forEach((char, i) => {
            let col = i % 3; let row = Math.floor(i / 3);
            let bx = startGridX + col * (boxW + gapX);
            let by = startGridY + row * (boxH + gapY);

            if (clickX >= bx && clickX <= bx + boxW && clickY >= by && clickY <= by + boxH) {
                selectedSkin = i;
                playSound('score');
            }
        });

        if (clickX >= 140 && clickX <= 340 && clickY >= 560 && clickY <= 592) {
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
