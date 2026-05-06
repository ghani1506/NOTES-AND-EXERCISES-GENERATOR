
import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="Infographic Lesson Generator", layout="wide")

st.title("🎨 AI Infographic Lesson Generator")
st.write(
    "Generate colourful educational infographic images for notes and exercises "
    "based on a lesson objective."
)

api_key = st.text_input("Enter OpenAI API Key", type="password")

lesson_objective = st.text_area(
    "Lesson Objective",
    placeholder="Example: Students will learn how to transpose simple formulae."
)

subject = st.selectbox(
    "Subject",
    ["Mathematics", "Science", "English", "History", "Geography", "ICT"]
)

grade = st.selectbox(
    "Grade Level",
    ["Primary", "Middle School", "Secondary", "High School"]
)

style = st.selectbox(
    "Infographic Style",
    ["Colourful Classroom Poster", "Modern Minimal", "Comic Style", "Neon Educational"]
)

generate = st.button("Generate Infographics")

if generate:
    if not api_key:
        st.error("Please enter your OpenAI API Key.")
    elif not lesson_objective:
        st.error("Please enter a lesson objective.")
    else:
        client = OpenAI(api_key=api_key)

        notes_prompt = f'''
        Create a colourful educational infographic poster for {subject}.
        Grade level: {grade}.
        Style: {style}.

        Lesson Objective:
        {lesson_objective}

        Requirements:
        - Create detailed lesson notes
        - Use headings and sections
        - Include worked examples
        - Use icons and illustrations
        - Make it visually engaging
        - Use classroom poster layout
        - Include formulas or diagrams where appropriate
        - Make it look like a professional educational infographic
        '''

        exercises_prompt = f'''
        Create a colourful worksheet infographic for {subject}.
        Grade level: {grade}.
        Style: {style}.

        Lesson Objective:
        {lesson_objective}

        Requirements:
        - Generate exercises from easy to challenging
        - Follow Bloom's Taxonomy:
            1. Remembering
            2. Understanding
            3. Applying
            4. Analysing
            5. Evaluating
            6. Creating
        - Include answer spaces
        - Use colourful educational layout
        - Add icons and illustrations
        - Make it suitable for students
        '''

        with st.spinner("Generating Notes Infographic..."):
            notes_image = client.images.generate(
                model="gpt-image-1",
                prompt=notes_prompt,
                size="1536x1024"
            )

        with st.spinner("Generating Exercises Infographic..."):
            exercises_image = client.images.generate(
                model="gpt-image-1",
                prompt=exercises_prompt,
                size="1536x1024"
            )

        notes_url = notes_image.data[0].url
        exercises_url = exercises_image.data[0].url

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📘 Lesson Notes Infographic")
            st.image(notes_url, use_container_width=True)

        with col2:
            st.subheader("📝 Exercises Infographic")
            st.image(exercises_url, use_container_width=True)

        st.success("Infographics generated successfully!")
