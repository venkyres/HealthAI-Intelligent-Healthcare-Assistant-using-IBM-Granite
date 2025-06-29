
!pip install transformers gradio

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_name = "ibm-granite/granite-3.3-2b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Create a text generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)

def patient_chat_assistant(user_query):
    prompt = f"You are a helpful and safe AI healthcare assistant. Do not provide diagnoses or prescriptions. Patient says: '{user_query}'. Respond clearly and responsibly."
    result = generator(prompt)[0]['generated_text']
    return result[len(prompt):].strip()
def disease_prediction(symptoms):
    prompt = f"Patient presents with the following symptoms: {symptoms}. What possible non-diagnostic conditions could be considered? Provide general insights only."
    result = generator(prompt)[0]['generated_text']
    return result[len(prompt):].strip()
def treatment_plan(age, gender, history, condition):
    prompt = (f"Patient profile: Age: {age}, Gender: {gender}, Medical History: {history}. "
              f"Condition: {condition}. Suggest general home remedies, over-the-counter guidance, and wellness tips. "
              f"Do not prescribe medication.")
    result = generator(prompt)[0]['generated_text']
    return result[len(prompt):].strip()

import gradio as gr

with gr.Blocks(title="HealthAI: Intelligent Healthcare Assistant") as app:
    gr.Markdown("## 🧠 HealthAI: Intelligent Healthcare Assistant")

    with gr.Tab("🩺 Patient Chat Assistant"):
        user_input = gr.Textbox(label="Ask a health-related question (non-diagnostic)")
        chat_output = gr.Textbox(label="Response")
        chat_btn = gr.Button("Get Response")
        chat_btn.click(fn=patient_chat_assistant, inputs=user_input, outputs=chat_output)

    with gr.Tab("🧬 Disease Prediction"):
        symptoms_input = gr.Textbox(label="Enter symptoms (comma-separated)")
        prediction_output = gr.Textbox(label="Possible Conditions")
        pred_btn = gr.Button("Predict")
        pred_btn.click(fn=disease_prediction, inputs=symptoms_input, outputs=prediction_output)

    with gr.Tab("🧾 Personalized Treatment Plan"):
        age = gr.Number(label="Age")
        gender = gr.Dropdown(["Male", "Female", "Other"], label="Gender")
        history = gr.Textbox(label="Medical History")
        condition = gr.Textbox(label="Current Condition")
        plan_output = gr.Textbox(label="Suggested Plan")
        plan_btn = gr.Button("Generate Plan")
        plan_btn.click(fn=treatment_plan, inputs=[age, gender, history, condition], outputs=plan_output)

app.launch()
