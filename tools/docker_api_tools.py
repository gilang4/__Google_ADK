# tools/docker_api_tools.py
"""
Tools that allow the ADK Gemini agent to call the Docker Healthcare AI Pipeline.
Each function is registered as a tool the agent can use.
"""

import requests
import json
from typing import Optional

# ── Configuration ──────────────────────────────────────
DOCKER_API_BASE = "http://localhost:8000"  # Your Docker FastAPI


def fhir_explore_patient(base_url: str = "https://r4.smarthealthit.org") -> dict:
    """
    Fetch a random patient from a FHIR server.
    
    Use this when you need:
    - Patient demographics (name, DOB, ID)
    - Active conditions and medications
    - Lab results and vital signs
    - Encounter history
    
    Args:
        base_url: The FHIR server to query (default: SMART Health IT sandbox)
    
    Returns:
        A dictionary containing complete patient data
    """
    try:
        response = requests.post(f"{DOCKER_API_BASE}/api/fhir/explore", 
                                 params={"base_url": base_url})
        data = response.json()
        
        if data.get("status") == "success":
            # Return just the patient data, not the wrapper
            return {
                "success": True,
                "patient_id": data["patient_id"],
                "patient_name": data["patient_name"],
                "conditions_count": data["conditions_count"],
                "medications_count": data["medications_count"],
                "patient_data": data["data"]
            }
        else:
            return {"success": False, "error": "Failed to fetch patient"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def summarize_with_ollama(patient_data: dict) -> dict:
    """
    Generate a clinical summary using local Llama 3.2 (Ollama).
    
    Use this when you need:
    - A concise, local AI summary (no internet required)
    - Quick analysis without cloud costs
    
    Args:
        patient_data: The patient data dict from fhir_explore_patient()
    
    Returns:
        A dictionary containing the AI-generated clinical summary
    """
    try:
        response = requests.post(
            f"{DOCKER_API_BASE}/api/summarize/ollama",
            json={"patient_data": patient_data}
        )
        data = response.json()
        
        if data.get("status") == "success":
            return {
                "success": True,
                "model": data["model"],
                "summary": data["summary"],
                "full_analysis": data["full_result"]
            }
        else:
            return {"success": False, "error": "Summarization failed"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def summarize_with_azure(patient_data: dict) -> dict:
    """
    Generate a clinical summary using Azure OpenAI GPT.
    
    Use this when you need:
    - Detailed, comprehensive AI analysis
    - Cloud-powered speed and accuracy
    - Complex medical reasoning
    
    Args:
        patient_data: The patient data dict from fhir_explore_patient()
    
    Returns:
        A dictionary containing the AI-generated clinical summary
    """
    try:
        response = requests.post(
            f"{DOCKER_API_BASE}/api/summarize/azure",
            json={"patient_data": patient_data}
        )
        data = response.json()
        
        if data.get("status") == "success":
            return {
                "success": True,
                "model": data["model"],
                "summary": data["summary"],
                "full_analysis": data["full_result"]
            }
        else:
            return {"success": False, "error": "Summarization failed"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def analyze_medical_image(image_path: str) -> dict:
    """
    Analyze a medical image (X-ray, CT, etc.) for findings.
    
    NOTE: Currently returns mock results. Real CheXagent coming in Step 4.
    
    Args:
        image_path: Path to the image file to analyze
    
    Returns:
        A dictionary containing the image analysis report
    """
    try:
        with open(image_path, "rb") as f:
            response = requests.post(
                f"{DOCKER_API_BASE}/analyze-image",
                files={"file": f}
            )
        data = response.json()
        return {
            "success": True,
            "filename": data.get("filename"),
            "report": data.get("report"),
            "status": data.get("status")
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Tool Registration for ADK ──────────────────────────
# This tells the ADK agent about available tools
AVAILABLE_TOOLS = {
    "fhir_explore_patient": {
        "function": fhir_explore_patient,
        "description": "Fetch a random patient's complete medical record from a FHIR server",
        "parameters": ["base_url"]
    },
    "summarize_with_ollama": {
        "function": summarize_with_ollama,
        "description": "Generate a clinical summary using local Llama 3.2 AI",
        "parameters": ["patient_data"]
    },
    "summarize_with_azure": {
        "function": summarize_with_azure,
        "description": "Generate a clinical summary using cloud Azure GPT AI",
        "parameters": ["patient_data"]
    },
    "analyze_medical_image": {
        "function": analyze_medical_image,
        "description": "Analyze a medical image for findings (mock for now)",
        "parameters": ["image_path"]
    }
}