#!/bin/bash
# full rebuild: composition -> fetch built data -> add slider script / keyframes -> write + publish
set -e
cd "$(dirname "$0")"
python3 run_build.py | head -c 300; echo
python3 - <<'PY'
import json,sys
sys.path.insert(0,'../../healus/tools'); import mcp
d=json.loads(mcp.rest('GET','wp/v2/pages/411494?context=edit&_fields=meta')['meta']['_elementor_data'])
json.dump(d,open('../build/built.json','w'),ensure_ascii=False,indent=1); print('fetched',len(d))
PY
python3 postprocess.py | tail -1
python3 deploy_coder.py | tail -2
