import streamlit as st
import ollama

# Page configuration
st.set_page_config(
    page_title="Code Completion with AI",
    page_icon="✨",
    layout="wide"
)

# Title and description
st.title("💻 Code Completion with AI")
st.markdown("Complete your incomplete code using AI models through Ollama")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox(
        "Select Model",
        ["tinyllama:latest", "qwen2.5:0.5b"],
        index=0
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random, lower values more deterministic"
    )
    
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100
    )
    
    st.divider()
    st.markdown("### About")
    st.markdown("This app uses AI models via Ollama to complete your incomplete code snippets.")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input")
    
    # Programming language selection
    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "TypeScript", "Ruby", "PHP"],
        index=0
    )
    
    # Incomplete code input
    incomplete_code = st.text_area(
        "Paste Your Incomplete Code",
        height=250,
        placeholder="Example:\ndef calculate_sum(numbers):\n    # TODO: complete this function\n    ",
        help="Paste the code you want to complete. Use comments like # TODO or // TODO to indicate where completion is needed."
    )
    
    # Additional instructions
    completion_instructions = st.text_area(
        "Completion Instructions (Optional)",
        height=80,
        placeholder="E.g., Add error handling, use list comprehension, optimize for performance"
    )
    
    generate_btn = st.button("✨ Complete Code", type="primary", use_container_width=True)

with col2:
    st.subheader("✅ Completed Code")
    
    # Container for the completed code
    output_container = st.container()

# Complete code when button is clicked
if generate_btn:
    if not incomplete_code.strip():
        st.error("Please provide the incomplete code you want to complete!")
    else:
        with output_container:
            with st.spinner(f"Completing {language} code with {model}..."):
                try:
                    # Construct the prompt
                    prompt = f"""You are an expert {language} programmer. Complete the following incomplete code:

```{language.lower()}
{incomplete_code}
```
"""
                    if completion_instructions.strip():
                        prompt += f"\nInstructions: {completion_instructions}\n"
                    
                    prompt += f"""
Requirements:
- Complete the missing parts of the code
- Follow {language} best practices and conventions
- Add appropriate comments where needed
- Ensure the code is functional and complete
- Keep the existing code structure intact

Provide ONLY the complete code, nothing else."""

                    # Call Ollama API
                    response = ollama.chat(
                        model=model,
                        messages=[
                            {
                                'role': 'user',
                                'content': prompt
                            }
                        ],
                        options={
                            'temperature': temperature,
                            'num_predict': max_tokens
                        }
                    )
                    
                    completed_code = response['message']['content']
                    
                    # Display the completed code
                    st.code(completed_code, language=language.lower())
                    
                    # Success message
                    st.success("✅ Code completed successfully!")
                    
                    # Download button
                    file_extensions = {
                        "Python": "py",
                        "JavaScript": "js",
                        "Java": "java",
                        "C++": "cpp",
                        "C#": "cs",
                        "Go": "go",
                        "Rust": "rs",
                        "TypeScript": "ts",
                        "Ruby": "rb",
                        "PHP": "php"
                    }
                    
                    st.download_button(
                        label="📥 Download Code",
                        data=completed_code,
                        file_name=f"completed_code.{file_extensions.get(language, 'txt')}",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error completing code: {str(e)}")
                    st.info("Make sure Ollama is running and the selected model is installed. Run: `ollama pull " + model + "`")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Powered by AI Models and Ollama | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Instructions in an expander
with st.expander("📖 How to Use"):
    st.markdown("""
    1. **Select a Model**: Choose from available models in the sidebar
    2. **Configure Settings**: Adjust temperature and max tokens as needed
    3. **Choose Language**: Select your programming language
    4. **Paste Incomplete Code**: Paste the code you want to complete
    5. **Add Instructions** (Optional): Specify how you want the code completed
    6. **Complete**: Click the complete button and wait for the AI to finish your code
    7. **Download**: Use the download button to save the completed code
    
    **Tips:**
    - Use TODO comments to mark where completion is needed
    - Lower temperature (0.3-0.5) for more predictable completions
    - Provide clear context in your incomplete code
    - Include function/class signatures for better results
    """)
