import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird Game", layout="centered")

st.title("Flappy Bird Game")

# Nhúng toàn bộ mã HTML/CSS/JS vào đây
html_code = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
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
// Chèn toàn bộ đoạn JS của Flappy Bird ở đây...
</script>
</body>
</html>
"""

# Hiển thị game lên giao diện Streamlit
components.html(html_code, height=660)
