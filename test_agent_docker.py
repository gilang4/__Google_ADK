# test_agent_docker.py
"""
Simple test: Agent calls Docker Healthcare API.
Run this script to see the full chain in action!
"""

import requests
import json

# ── Configuration ──────────────────────────────────────
DOCKER_API = "http://localhost:8000"

print("=" * 60)
print("🤖 AGENT → DOCKER TEST")
print("=" * 60)

# ── Step 1: Agent decides "I need patient data" ────────
print("\n📞 Agent: 'I need a random patient. Calling fhir_explore...'")
print(f"   → POST {DOCKER_API}/api/fhir/explore")

response = requests.post(f"{DOCKER_API}/api/fhir/explore")
patient_result = response.json()

print(f"   ✅ Got patient: {patient_result['patient_name']}")
print(f"      ID: {patient_result['patient_id']}")
print(f"      Conditions: {patient_result['conditions_count']}")
print(f"      Medications: {patient_result['medications_count']}")

# ── Step 2: Agent decides "I need a summary" ────────────
print(f"\n📞 Agent: 'Now summarize with Azure GPT...'")
print(f"   → POST {DOCKER_API}/api/summarize/azure")

patient_data = patient_result["data"]
summary_response = requests.post(
    f"{DOCKER_API}/api/summarize/azure",
    json={"patient_data": patient_data}
)
summary_result = summary_response.json()

print(f"   ✅ Summary received!")
print(f"      Model: {summary_result['model']}")

# ── Step 3: Agent presents the result ──────────────────
print(f"\n{'=' * 60}")
print("📋 AGENT'S FINAL OUTPUT TO USER:")
print(f"{'=' * 60}")
print(f"\nPatient ID: {summary_result['full_result'].get('patient_id', 'Unknown')}")
print(f"\n🏥 Conditions:")
for c in summary_result['full_result'].get('conditions', [])[:3]:
    print(f"   - {c}")
print(f"\n💊 Medications:")
for m in summary_result['full_result'].get('medications', [])[:3]:
    print(f"   - {m}")
print(f"\n📄 Clinical Summary:")
print(summary_result['summary'][:300] + "...")
print(f"\n{'=' * 60}")
print("✅ AGENT → DOCKER TEST COMPLETE!")
print(f"{'=' * 60}")