"""HealUs page (411263): replace the 5 placeholder FAQ items (V4 accordion 1ebd8d4a, FAQ schema on) with the owner's 8.

Middle item 521ed9fb is cloned three times (fresh element + style ids) and inserted before the last item, which keeps its
own no-divider style. Brand written "HealUs" throughout (the supplied copy mixed "HealUS").
Backs up the live _elementor_data first; writes via WP REST; touch + publish.
"""
import copy, json, os, random, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mcp  # noqa: E402

POST, ACC, TEMPLATE = 411263, '1ebd8d4a', '521ed9fb'
FAQ = [
    ('What is HealUs EHR?',
     'HealUs EHR is a cloud-based Electronic Health Record platform designed to help healthcare providers manage patient records, clinical documentation, e-prescribing, scheduling, patient communication, and care coordination from a single system. It streamlines clinical workflows while improving efficiency, compliance, and patient outcomes.'),
    ('How is HealUs EHR different from traditional EHR systems?',
     'Unlike traditional EHRs that often require extensive manual data entry, HealUs EHR combines intelligent workflows, integrated patient management, interoperability, and AI-powered documentation tools to reduce administrative burden and improve provider productivity. Modern EHR users increasingly seek better usability, automation, and clinician-friendly workflows.'),
    ('Does HealUs EHR support AI-powered clinical documentation?',
     'Yes. HealUs EHR integrates with AI-powered clinical documentation solutions, including AI Medical Scribe capabilities, to automatically generate structured clinical notes, SOAP notes, encounter summaries, and documentation directly from patient-provider conversations.'),
    ('Can HealUs EHR integrate with Medical Billing and Revenue Cycle Management (RCM)?',
     'Yes. HealUs EHR is designed to work seamlessly with MedCare PMS, Medical Billing Software, Revenue Cycle Management services, AI Medical Coding, and AI-powered billing automation to create a connected clinical and financial workflow.'),
    ('Does HealUs EHR support e-Prescribing?',
     'Yes. Providers can electronically prescribe medications, manage refills, review medication histories, and improve patient safety through integrated prescribing workflows. Certified EHR platforms commonly support electronic prescribing and secure health information exchange.'),
    ('Is HealUs EHR HIPAA compliant?',
     'Yes. HealUs EHR is built with security and compliance in mind, including encryption, access controls, audit logs, and HIPAA-compliant safeguards to help protect sensitive patient health information. Certified EHR technologies also support advanced security controls and authentication standards.'),
    ('Can HealUs EHR be accessed remotely?',
     'Yes. As a cloud-based platform, HealUs EHR enables authorized users to securely access patient records, schedules, clinical documentation, and reports from any location with internet connectivity.'),
    ('Does HealUs EHR offer a patient portal?',
     'Yes. Patients can securely access health records, communicate with providers, request appointments, review visit summaries, and complete forms through the HealUs Patient Portal.'),
]

meta = mcp.rest('GET', f'wp/v2/pages/{POST}?context=edit&_fields=meta')['meta']
json.dump(meta, open(os.path.join(HERE, '..', 'backup', f'hu_{POST}_{time.strftime("%Y%m%d-%H%M%S")}.json'), 'w'), ensure_ascii=False)
data = json.loads(meta['_elementor_data'])

ids = set()
def collect(e):
    ids.add(e['id']); [collect(c) for c in e.get('elements', [])]
[collect(e) for e in data]
def nid():
    while True:
        i = '%08x' % random.getrandbits(32)
        if i not in ids:
            ids.add(i); return i
def regen(e):
    new = nid(); e['id'] = new
    st = e.get('styles') if isinstance(e.get('styles'), dict) else {}
    remap = {}
    for sid in list(st):
        nsid = f'e-{new}-{nid()[:4]}'
        body = st.pop(sid); body['id'] = nsid; st[nsid] = body; remap[sid] = nsid
    cl = e.get('settings', {}).get('classes')
    if isinstance(cl, dict):
        cl['value'] = [remap.get(c, c) for c in cl['value']]
    for c in e.get('elements', []):
        regen(c)

acc = []
def find(e):
    if e['id'] == ACC: acc.append(e)
    [find(c) for c in e.get('elements', [])]
[find(e) for e in data]
acc = acc[0]
items = acc['elements']
assert len(items) == 5, f'expected the 5 original items, found {len(items)}'
tpl = [i for i in items if i['id'] == TEMPLATE][0]
clones = []
for _ in range(len(FAQ) - len(items)):
    c = copy.deepcopy(tpl); regen(c); clones.append(c)
acc['elements'] = items[:-1] + clones + items[-1:]

def first(e, wt):
    if e.get('widgetType') == wt: return e
    for c in e.get('elements', []):
        r = first(c, wt)
        if r: return r
for item, (q, a) in zip(acc['elements'], FAQ):
    first(item, 'e-heading')['settings']['title']['value'] = q
    first(item, 'e-paragraph')['settings']['paragraph']['value'] = a
assert len(acc['elements']) == len(FAQ)

body = '/tmp/claude-0/_hu_body.json'
json.dump({'meta': {'_elementor_data': json.dumps(data, ensure_ascii=False)}}, open(body, 'w'), ensure_ascii=False)
r = subprocess.run(['curl', '-sS', '-m', '300', '-X', 'POST', '-H', mcp.AUTH, '-H', 'Content-Type: application/json; charset=utf-8',
                    '--data-binary', '@' + body, mcp.API + f'wp/v2/pages/{POST}?_fields=id'], capture_output=True, text=True)
os.remove(body)
assert json.loads(r.stdout).get('id') == POST, r.stdout[:300]
print('written', len(acc['elements']), 'items')

for attempt in range(4):
    try:
        mcp.init()
        mcp.call('elementor-manage-elements', {'post_id': POST, 'operations': [
            {'action': 'update', 'element_id': '7bf06193', 'style': 'width: 100%;'}]})
        print(mcp.call('elementor-publish-document', {'post_id': POST}).get('status'))
        break
    except Exception as e:
        print('retry', str(e)[:120]); time.sleep(10)
