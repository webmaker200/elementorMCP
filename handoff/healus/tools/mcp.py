"""Minimal Elementor MCP / WP REST client. Auth comes from the local MCP config (~/.claude.json), never from the repo."""
import json, os, subprocess, time
URL = 'https://medcaredemo.online/medcare/wp-json/elementor/mcp/'
API = 'https://medcaredemo.online/medcare/wp-json/'
def _auth():
    try:
        return json.load(open(os.path.expanduser('~/.claude.json')))['mcpServers']['medcare-mso-elementor']['headers']['Authorization']
    except Exception:  # fall back to the environment secret (base64 user:app-password)
        v = os.environ['WP_BASIC_AUTH']
        v = v.split('=', 1)[1] if v.startswith('WP_BASIC_AUTH=') else v
        return v if v.startswith('Basic ') else 'Basic ' + v


AUTH = 'Authorization: ' + _auth()
_sid = [None]


def _post(body, hdr=False):
    f = '/tmp/claude-0/_healus_req.json'
    os.makedirs('/tmp/claude-0', exist_ok=True)
    open(f, 'w').write(json.dumps(body))
    cmd = ['curl', '-sS', '-m', '300', '-X', 'POST', '-H', 'Content-Type: application/json', '-H', 'Accept: application/json, text/event-stream', '-H', AUTH]
    if _sid[0]:
        cmd += ['-H', 'Mcp-Session-Id: ' + _sid[0]]
    if hdr:
        cmd += ['-D', '/tmp/claude-0/_healus_h.txt']
    cmd += ['--data', '@' + f, URL]
    for i in range(6):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and (r.stdout.strip() or body.get('id') is None):
            return r.stdout
        time.sleep(2 * (i + 1))
    raise RuntimeError(r.stderr)


def init():
    _sid[0] = None
    _post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "healus", "version": "1"}}}, hdr=True)
    _sid[0] = [l.split(':', 1)[1].strip() for l in open('/tmp/claude-0/_healus_h.txt') if l.lower().startswith('mcp-session-id')][0]
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"})


def call(name, args):
    if not _sid[0]:
        init()
    d = json.loads(_post({"jsonrpc": "2.0", "id": 9, "method": "tools/call", "params": {"name": name, "arguments": args}}))
    if 'error' in d:
        raise RuntimeError(json.dumps(d['error'])[:2000])
    txt = ''.join(c.get('text', '') for c in d['result'].get('content', []))
    if d['result'].get('isError'):
        raise RuntimeError(txt[:3000])
    try:
        return json.loads(txt)
    except Exception:
        return txt


def rest(method, path, body=None, auth=True):
    cmd = ['curl', '-sS', '-m', '120', '-X', method] + (['-H', AUTH] if auth else []) + ['-H', 'Content-Type: application/json']
    if body is not None:
        cmd += ['--data', json.dumps(body)]
    cmd += [path if path.startswith('http') else API + path]
    for i in range(6):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
        time.sleep(2 * (i + 1))
    raise RuntimeError(r.stderr)
