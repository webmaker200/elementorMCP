"""Upload ../assets/* to the Media Library once (registry: ../media.json). Alt text from ALT; decorative = ''."""
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'healus', 'tools'))
import mcp  # noqa: E402
A = os.path.join(HERE, '..', 'assets'); REG = os.path.join(HERE, '..', 'media.json')
ALT = {'sophus-coder-dashboard': 'Sophus coder view: claim queue with suggested codes and the evidence behind each one',
       'sophus-manager-dashboard': 'Sophus manager view: team output, review queue and AI coder performance',
       'sophus-claim-card-panel': 'Claim CLM-66412 coded by Sophus: I10, E11.9 and 99213 with confidence scores and payer edits passed',
       'sophus-seat-coders': 'Suggested codes for claim CLM-66412 with accepted and review states',
       'sophus-seat-managers': 'Team weekly output chart: claims completed per coder per day against a target of 40',
       'sophus-seat-billing': 'Client volume chart: busiest clients this month by claims',
       'sophus-manager-dashboard-v2': 'Sophus coder dashboard: next claim, daily progress, quality scores and prioritized worklist',
       'sophus-testimonial-401937': 'Dr. Jose Correa',
       'sophus-testimonial-401412': 'Shaunna Mock',
       'sophus-testimonial-399532': 'Max Owens',
       'sophus-testimonial-397918': 'Kelly Ballou',
       'sophus-testimonial-396539': 'Bret',
       'sophus-card-phone': 'Claim CLM-66412: 3 codes suggested with evidence linked and edits passed'}
TYPES = {'.webp': 'image/webp', '.svg': 'image/svg+xml'}
reg = json.load(open(REG)) if os.path.exists(REG) else {}
for f in sorted(os.listdir(A)):
    name, ext = os.path.splitext(f)
    if name in reg or ext not in TYPES:
        continue
    for attempt in range(4):
        r = subprocess.run(['curl', '-sS', '-m', '120', '-X', 'POST', '-H', mcp.AUTH, '-H', f'Content-Type: {TYPES[ext]}',
                            '-H', f'Content-Disposition: attachment; filename="{f}"', '--data-binary', '@' + os.path.join(A, f),
                            mcp.API + 'wp/v2/media?_fields=id,source_url'], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout); break
        except ValueError:
            time.sleep(4)
            hit = [m for m in mcp.rest('GET', 'wp/v2/media?per_page=10&_fields=id,source_url&search=' + name) if m['source_url'].endswith('/' + f)]
            if hit: d = hit[0]; break
    mcp.rest('POST', f'wp/v2/media/{d["id"]}?_fields=id', {'alt_text': ALT.get(name, ''), 'title': name})
    reg[name] = {'id': d['id'], 'url': d['source_url']}
    json.dump(reg, open(REG, 'w'), indent=1)
    print(name, d['id'])
print(len(reg), 'assets in registry')
