import argparse
import json

parser = argparse.ArgumentParser(description="Harborworks fixture CLI")
parser.add_argument("--skill", required=True)
parser.add_argument("--knowledge", required=True)
args = parser.parse_args()

print(json.dumps({
    "context": "org.harborworks.context.core",
    "revision": "core-r1",
    "skill": args.skill,
    "knowledge": args.knowledge,
    "message": "hello from the Harborworks Python fixture"
}, sort_keys=True))
