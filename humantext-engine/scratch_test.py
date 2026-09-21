import sys
import traceback
from app.schemas.request import HumanizeRequest
from app.services.humanize import run_humanize_workflow

req = HumanizeRequest(
    text="The system utilizes artificial intelligence to optimize operational efficiency. It can be seen that it is highly effective.",
    document_type="business",
    target_mode="natural_professional",
    target_tone="conversational",
    target_audience="business professionals"
)

try:
    response = run_humanize_workflow(req)
    print(response)
except Exception as e:
    print("Error occurred:")
    traceback.print_exc()
