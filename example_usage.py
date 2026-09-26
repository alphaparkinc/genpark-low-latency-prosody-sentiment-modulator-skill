import sys, json
from client import LowLatencyProsodySentimentModulator

def main():
    print("Testing LowLatencyProsodySentimentModulator...")
    mod = LowLatencyProsodySentimentModulator()
    res = mod.run_benchmark_prosody_modulation()
    print(json.dumps(res, indent=2))
    assert res["urgent_detection"] == "urgent"
    assert res["empathetic_detection"] == "empathetic"
    assert res["ssml_generation_verified"] is True
    print("All Low Latency Prosody Modulator tests passed successfully!")

if __name__ == "__main__":
    main()
