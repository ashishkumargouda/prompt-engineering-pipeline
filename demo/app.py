"""
Prompt Engineering Pipeline - Live Demo
A simple Streamlit app to test all 10 prompts interactively.
"""

import streamlit as st
import os

# Page config
st.set_page_config(
    page_title="Prompt Engineering Pipeline Demo",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Prompt Engineering Pipeline — Live Demo")
st.markdown("Select a prompt below, paste your input, and see how it works. *Note: Add your API key to connect to an LLM.*")

# Define all 10 prompts with their descriptions
PROMPTS = {
    "1 - Customer Chat Log Parser": {
        "category": "Structured Output",
        "description": "Converts raw customer chat logs into clean, PostgreSQL-ready JSON.",
        "input_label": "Paste raw chat log:",
        "placeholder": "Customer: Hi, my order #45523 hasn't arrived. It's been 8 days...\nAgent: I understand your frustration. Let me check...\n...",
        "prompt_file": "prompts/structured-output/structured-output_customer-chat-log-parser.md"
    },
    "2 - Financial Report KPI Extractor": {
        "category": "Structured Output",
        "description": "Extracts KPIs from unstructured financial reports.",
        "input_label": "Paste financial report text:",
        "placeholder": "Acme Corp reported Q3 revenue of $12.4M, up 18% YoY. Gross margin was 62%...",
        "prompt_file": "prompts/structured-output/structured-output_financial-report-kpi-extractor.md"
    },
    "3 - Incident Post-Mortem Generator": {
        "category": "Dynamic Template",
        "description": "Generates blameless post-mortem reports from incident data.",
        "input_label": "Paste incident details:",
        "placeholder": "Service: payment-api | Severity: P1 | Downtime: 47 minutes | Root cause notes: Database connection pool exhausted...",
        "prompt_file": "prompts/dynamic-templates/dynamic-template_incident-postmortem-generator.md"
    },
    "4 - Ad Copy Generator": {
        "category": "Dynamic Template",
        "description": "Generates platform-specific ad copy from a campaign brief.",
        "input_label": "Paste campaign brief:",
        "placeholder": "Brand: FitMeal | Product: Meal prep subscription | Audience: Busy professionals 25-40 | Pain point: No time to cook healthy...",
        "prompt_file": "prompts/dynamic-templates/dynamic-template_ad-copy-generator.md"
    },
    "5 - SOC Security Log Analyzer": {
        "category": "Few-Shot + Routing",
        "description": "Triage raw system logs like a Tier-1 security analyst.",
        "input_label": "Paste system log entry:",
        "placeholder": "2024-11-03T02:14:33Z FAILED_LOGIN user=admin src_ip=185.220.101.45 dst=10.0.0.5 attempts=47 protocol=SSH",
        "prompt_file": "prompts/few-shot-routing/few-shot_soc-security-log-analyzer.md"
    },
    "6 - Support Routing Classifier": {
        "category": "Few-Shot + Routing",
        "description": "Routes customer messages to the correct support queue.",
        "input_label": "Paste customer message:",
        "placeholder": "I've been waiting for my refund for 3 weeks now. This is the fourth time I'm contacting you. This is absolutely unacceptable.",
        "prompt_file": "prompts/few-shot-routing/few-shot_support-routing-classifier.md"
    },
    "7 - Backend Error Debugger": {
        "category": "Chain-of-Thought",
        "description": "Debugs production errors with systematic 7-step reasoning.",
        "input_label": "Paste error details:",
        "placeholder": "Service: user-api | Error: NullPointerException at line 142 | Stack trace: ...",
        "prompt_file": "prompts/chain-of-thought/chain-of-thought_backend-error-debugger.md"
    },
    "8 - ML Model Discrepancy Analyzer": {
        "category": "Chain-of-Thought",
        "description": "Diagnoses why models perform differently in production vs testing.",
        "input_label": "Paste model performance details:",
        "placeholder": "Test accuracy: 94% | Production accuracy: 71% | Model: XGBoost | Training data: Jan-Mar 2024...",
        "prompt_file": "prompts/chain-of-thought/chain-of-thought_ml-model-discrepancy-analyzer.md"
    },
    "9 - Legal Contract Risk Extractor": {
        "category": "Few-Shot + Structured Output",
        "description": "Extracts obligations and risks from legal contracts.",
        "input_label": "Paste contract excerpt:",
        "placeholder": "The Service Provider shall deliver the completed software module no later than 45 days from the Effective Date...",
        "prompt_file": "prompts/few-shot-routing/few-shot_legal-contract-risk-extractor.md"
    },
    "10 - Build-vs-Buy Decision Analyzer": {
        "category": "Chain-of-Thought + Template",
        "description": "Strategic analysis framework for build-vs-buy decisions.",
        "input_label": "Paste decision context:",
        "placeholder": "Company: TechStart (Series A) | Team: 12 engineers | Capability: Internal analytics dashboard | Budget: $50K...",
        "prompt_file": "prompts/chain-of-thought/chain-of-thought_build-vs-buy-analysis.md"
    }
}

# Create two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Select a Prompt")
    selected_prompt = st.selectbox(
        "Choose a prompt to test:",
        list(PROMPTS.keys())
    )
    
    prompt_info = PROMPTS[selected_prompt]
    st.markdown(f"**Category:** {prompt_info['category']}")
    st.markdown(f"**Description:** {prompt_info['description']}")

with col2:
    st.subheader("2. Enter Input")
    user_input = st.text_area(
        prompt_info['input_label'],
        placeholder=prompt_info['placeholder'],
        height=200
    )
    
    st.subheader("3. Generate Output")
    
    api_key = st.text_input("OpenAI API Key (optional — required for live generation):", type="password")
    
    if st.button("Generate Output", type="primary"):
        if not user_input:
            st.warning("Please enter some input text first.")
        elif not api_key:
            # Show the prompt that would be sent
            st.info("No API key provided. Showing the prompt template instead:")
            try:
                with open(prompt_info['prompt_file'], 'r') as f:
                    prompt_content = f.read()
                st.code(prompt_content.replace("{{RAW_CHAT_LOG}}", user_input)
                                   .replace("{{FINANCIAL_REPORT_TEXT}}", user_input)
                                   .replace("{{RAW_SYSTEM_LOG}}", user_input)
                                   .replace("{{CUSTOMER_MESSAGE}}", user_input)
                                   .replace("{{RAW_CONTRACT_TEXT}}", user_input)
                                   .replace("{{SERVICE_NAME}}", "your-service")
                                   .replace("{{ERROR_MESSAGE}}", user_input[:100])
                                   .replace("{{RAW_TIMELINE_LOGS}}", user_input)
                                   .replace("{{INCIDENT_COMMANDER_NAME}}", "On-call Engineer")
                                   [:2000] + "...", language="markdown")
            except FileNotFoundError:
                st.code("Prompt file not found. Please organize files as described in README.", language="text")
        else:
            # Real API call
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                with open(prompt_info['prompt_file'], 'r') as f:
                    prompt_content = f.read()
                
                # Basic variable replacement
                final_prompt = prompt_content.replace("{{RAW_CHAT_LOG}}", user_input)\
                                            .replace("{{FINANCIAL_REPORT_TEXT}}", user_input)\
                                            .replace("{{RAW_SYSTEM_LOG}}", user_input)\
                                            .replace("{{CUSTOMER_MESSAGE}}", user_input)\
                                            .replace("{{RAW_CONTRACT_TEXT}}", user_input)
                
                with st.spinner("Generating..."):
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": final_prompt}],
                        temperature=0.1
                    )
                    st.markdown("### Output:")
                    st.code(response.choices[0].message.content, language="json")
            except Exception as e:
                st.error(f"Error: {e}. Make sure your API key is valid and you have credits.")

st.divider()
st.caption("Prompt Engineering Pipeline — [Your Name] | [GitHub Link] | [LinkedIn Link]")
