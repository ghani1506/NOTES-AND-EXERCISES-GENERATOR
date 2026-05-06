# app.py
# Streamlit Infographic Image Generator
# Creates 2 colorful educational PNGs from a lesson objective:
# 1) Notes infographic
# 2) Individual exercises from easy to challenging using Bloom's Taxonomy
# No AI/API required. Uses local Python image generation with Pillow.

import io
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import streamlit as st

st.set_page_config(page_title="Lesson Infographic Generator", page_icon="🎨", layout="wide")

def load_font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

FONT_TITLE = load_font(56, True)
FONT_SUBTITLE = load_font(30, True)
FONT_HEADING = load_font(28, True)
FONT_BODY = load_font(22)
FONT_BODY_BOLD = load_font(22, True)
FONT_SMALL = load_font(18)

def wrap_text(text, width=42):
    return textwrap.wrap(text, width=width)

def draw_wrapped_text(draw, text, xy, font, fill, max_width_chars=44, line_gap=8):
    x, y = xy
    for line in wrap_text(text, max_width_chars):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y

def sanitize_topic(lesson_objective):
    text = lesson_objective.strip()
    low = text.lower()
    for s in ["students will be able to", "learners will be able to", "i can", "we are learning to", "to"]:
        if low.startswith(s):
            text = text[len(s):].strip(" :.-")
            break
    return text[:120] if text else "the lesson objective"

def generate_notes_content(objective, grade_level, subject):
    topic = sanitize_topic(objective)
    return [
        ("1. KEY IDEA", f"Today we are learning to {topic}. Focus on the meaning, the method, and how to check your answer."),
        ("2. IMPORTANT VOCABULARY", "Subject • Formula • Substitute • Rearrange • Inverse operation • Check"),
        ("3. STEPS TO FOLLOW", "Read the question carefully. Identify what is given. Choose the correct rule or formula. Work step by step. Check if the answer makes sense."),
        ("4. WORKED EXAMPLE", f"Example task: Use the lesson objective to solve a simple question about {topic}. Write each step clearly and keep your working neat."),
        ("5. COMMON MISTAKES", "Do not skip steps. Do not mix up units. Do not change only one side of an equation. Always check your final answer."),
        ("6. REMEMBER", f"For {grade_level}, a good answer explains the method, shows working, and gives a clear final answer."),
    ]

def generate_exercise_content(objective):
    topic = sanitize_topic(objective)
    return [
        ("1. REMEMBERING", "List two important facts or rules connected to this lesson objective."),
        ("2. UNDERSTANDING", f"Explain in your own words what it means to {topic}."),
        ("3. APPLYING", f"Complete a simple example that uses the skill: {topic}. Show your working."),
        ("4. ANALYSING", "Compare two different methods or examples. What is the same and what is different?"),
        ("5. EVALUATING", "Check a given answer. Decide whether it is correct and explain why."),
        ("6. CREATING", f"Create your own question about {topic}, then solve it fully."),
        ("7. WORD PROBLEM", f"Write and solve a real-life problem where someone needs to {topic}."),
        ("8. CHALLENGE", "Make a harder version of your question. Add one extra step and solve it."),
    ]

def rounded_panel(draw, xy, radius, fill, outline, width=3):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_badge(draw, number, xy, color):
    x, y = xy
    draw.rounded_rectangle((x, y, x + 48, y + 48), radius=12, fill=color)
    draw.text((x + 15, y + 8), str(number), font=FONT_HEADING, fill="white")

def draw_header(draw, title, objective, w):
    draw.text((70, 28), title.upper(), font=FONT_TITLE, fill="#0B1E53")
    draw.text((75, 96), "Generated from lesson objective", font=FONT_SUBTITLE, fill="#16803A")
    draw.rounded_rectangle((70, 145, w - 70, 210), radius=18, fill="#EEF7FF", outline="#2E86DE", width=3)
    draw.text((95, 162), "Objective:", font=FONT_BODY_BOLD, fill="#0B1E53")
    draw_wrapped_text(draw, objective, (220, 162), FONT_BODY, "#111827", max_width_chars=78, line_gap=6)

def draw_footer(draw, w, h):
    draw.rounded_rectangle((150, h - 55, w - 150, h - 15), radius=12, fill="#FFF4C2", outline="#E5B800", width=2)
    draw.text((175, h - 47), "⭐ Remember: Read carefully • Show working • Use key vocabulary • Check your answer", font=FONT_SMALL, fill="#111827")

def create_notes_image(objective, grade_level, subject):
    w, h = 1240, 1754
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    draw_header(draw, f"Lesson Notes: {subject}", objective, w)

    colors = ["#1E88E5", "#43A047", "#8E24AA", "#FB8C00", "#EC407A", "#00ACC1"]
    fills = ["#F2F8FF", "#F3FFF5", "#FBF5FF", "#FFF7EF", "#FFF3F8", "#F0FDFF"]

    y = 245
    for i, (heading, body) in enumerate(generate_notes_content(objective, grade_level, subject), start=1):
        color = colors[(i - 1) % len(colors)]
        fill = fills[(i - 1) % len(fills)]
        rounded_panel(draw, (55, y, w - 55, y + 205), 20, fill, color, 3)
        draw_badge(draw, i, (80, y + 22), color)
        draw.text((145, y + 28), heading, font=FONT_HEADING, fill=color)
        draw_wrapped_text(draw, body, (95, y + 88), FONT_BODY, "#111827", max_width_chars=86)
        y += 227

    draw_footer(draw, w, h)
    return img

def create_exercises_image(objective, grade_level, subject):
    w, h = 1240, 1754
    img = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(img)
    draw_header(draw, f"Practice: {subject}", objective, w)

    colors = ["#1565C0", "#2E7D32", "#6A1B9A", "#EF6C00", "#D81B60", "#00838F", "#F9A825", "#0D47A1"]
    fills = ["#F2F8FF", "#F3FFF5", "#FBF5FF", "#FFF7EF", "#FFF3F8", "#F0FDFF", "#FFFBEA", "#F1F5FF"]

    y = 245
    box_h = 165
    for i, (heading, question) in enumerate(generate_exercise_content(objective), start=1):
        color = colors[(i - 1) % len(colors)]
        fill = fills[(i - 1) % len(fills)]
        rounded_panel(draw, (55, y, w - 55, y + box_h), 20, fill, color, 3)
        draw_badge(draw, i, (80, y + 22), color)
        draw.text((145, y + 28), heading, font=FONT_HEADING, fill=color)
        draw_wrapped_text(draw, question, (95, y + 82), FONT_BODY, "#111827", max_width_chars=62)
        draw.rounded_rectangle((760, y + 35, w - 90, y + box_h - 25), radius=14, fill="white", outline=color, width=2)
        draw.text((780, y + 48), "Answer / working:", font=FONT_SMALL, fill="#374151")
        y += box_h + 18

    draw_footer(draw, w, h)
    return img

def image_to_bytes(img):
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

st.title("🎨 Lesson Infographic Image Generator")
st.write("Generate two colorful educational images from one lesson objective: **notes** and **Bloom's Taxonomy exercises**. No API needed.")

with st.sidebar:
    st.header("Lesson Details")
    subject = st.text_input("Subject", "Mathematics")
    grade_level = st.text_input("Grade / Year Level", "Year 7")
    objective = st.text_area("Lesson Objective", "Students will be able to transpose simple formulae to change the subject.", height=140)
    generate = st.button("Generate Infographics", type="primary")

if generate or objective:
    notes_img = create_notes_image(objective, grade_level, subject)
    exercises_img = create_exercises_image(objective, grade_level, subject)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Notes Infographic")
        st.image(notes_img, use_container_width=True)
        st.download_button("Download Notes PNG", image_to_bytes(notes_img), "lesson_notes_infographic.png", "image/png")

    with col2:
        st.subheader("2. Exercises Infographic")
        st.image(exercises_img, use_container_width=True)
        st.download_button("Download Exercises PNG", image_to_bytes(exercises_img), "lesson_exercises_infographic.png", "image/png")
