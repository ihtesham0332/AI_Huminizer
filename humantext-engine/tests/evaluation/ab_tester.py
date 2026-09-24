from app.graph.workflow import build_humanization_graph

# Mock Dataset
TEST_DATA = [
    {
        "id": 1,
        "category": "Academic",
        "text": "The p-value was calculated as 0.04 (Smith, 2023), indicating statistical significance.",
        "must_contain": ["0.04", "Smith, 2023"]
    },
    {
        "id": 2,
        "category": "Medical",
        "text": "The patient does not suffer from hypertension.",
        "must_contain": ["does not", "hypertension"]
    }
]

def run_ab_test():
    """
    Evaluates the LangGraph Agentic Pipeline against semantic and factual retention requirements.
    """
    app = build_humanization_graph()
    
    successes = 0
    for sample in TEST_DATA:
        print(f"Testing Sample {sample['id']}...")
        initial_state = {"original_text": sample["text"]}
        final_state = app.invoke(initial_state)
        
        output = final_state.get("final_output", "")
        
        # Verify Factual/Semantic Preservation
        passed = all(token in output for token in sample["must_contain"])
        if passed:
            successes += 1
            print(f"Sample {sample['id']} PASSED.")
        else:
            print(f"Sample {sample['id']} FAILED. Missing protected tokens.")
            print(f"Output was: {output}")
            
    print(f"\nFinal Score: {successes}/{len(TEST_DATA)} ({(successes/len(TEST_DATA))*100}%)")

if __name__ == "__main__":
    run_ab_test()
