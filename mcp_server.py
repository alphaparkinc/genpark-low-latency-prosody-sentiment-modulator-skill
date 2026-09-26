import sys, json
from client import LowLatencyProsodySentimentModulator

def main():
    mod = LowLatencyProsodySentimentModulator()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(mod.run_benchmark_prosody_modulation(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "modulate_stream_chunk", "description": "Dynamically adjust speech rate, pitch, and cadence based on sentiment."},
                        {"name": "inject_natural_breathing_pauses", "description": "Insert micro-pause break tags into raw text at clause boundaries."},
                        {"name": "generate_ssml_payload", "description": "Construct valid SSML document incorporating modulated prosody settings."},
                        {"name": "run_benchmark_prosody_modulation", "description": "Test prosody modulation across diverse dialogues."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "modulate_stream_chunk":
                    out = mod.modulate_stream_chunk(args.get("raw_text", ""), args.get("override_sentiment"), args.get("urgency_level", 1.0))
                elif tname == "inject_natural_breathing_pauses":
                    out = {"annotated_text": mod.inject_natural_breathing_pauses(args.get("text", ""))}
                elif tname == "generate_ssml_payload":
                    out = mod.generate_ssml_payload(args.get("text", ""), args.get("voice_name", "en-US-JennyMultilingualNeural"), args.get("override_sentiment"))
                elif tname == "run_benchmark_prosody_modulation":
                    out = mod.run_benchmark_prosody_modulation()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
