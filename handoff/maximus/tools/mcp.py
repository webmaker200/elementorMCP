import json, subprocess, time, os, sys
S=os.path.dirname(os.path.abspath(__file__))
URL='https://medcaredemo.online/medcare/wp-json/elementor/mcp/'
AUTH='Authorization: Basic '+os.environ['WP_BASIC_AUTH']  # base64(user:app_password); never commit
def _post(body, sid=None, hdr=False):
    f=S+'/_req.json'; open(f,'w').write(json.dumps(body))
    cmd=['curl','-sS','-m','240','-X','POST','-H','Content-Type: application/json','-H','Accept: application/json, text/event-stream','-H',AUTH]
    if sid: cmd+=['-H','Mcp-Session-Id: '+sid]
    if hdr: cmd+=['-D',S+'/_h.txt']
    cmd+=['--data','@'+f,URL]
    for i in range(6):
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode==0 and (r.stdout.strip() or body.get('id') is None): return r.stdout
        time.sleep(2*(i+1))
    raise RuntimeError(r.stderr)
def sid():
    p=S+'/sid'
    return open(p).read().strip() if os.path.exists(p) else None
def init():
    _post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"cc","version":"1"}}},hdr=True)
    s=[l.split(':',1)[1].strip() for l in open(S+'/_h.txt') if l.lower().startswith('mcp-session-id')][0]
    open(S+'/sid','w').write(s)
    _post({"jsonrpc":"2.0","method":"notifications/initialized"},sid=s)
    return s
def call(name,args):
    for attempt in range(2):
        out=_post({"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":name,"arguments":args}},sid=sid())
        d=json.loads(out)
        if 'error' in d and attempt==0 and 'session' in json.dumps(d['error']).lower():
            init(); continue
        break
    if 'error' in d: raise RuntimeError(json.dumps(d['error']))
    txt=''.join(c.get('text','') for c in d['result'].get('content',[]))
    if d['result'].get('isError'): raise RuntimeError(txt)
    try: return json.loads(txt)
    except Exception: return txt
if __name__=='__main__':
    r=call(sys.argv[1], json.loads(sys.argv[2]) if len(sys.argv)>2 else {})
    print(r if isinstance(r,str) else json.dumps(r,indent=1))
def get(url, auth=True, raw=False):
    cmd=['curl','-sS','-m','90','-L']+(['-H',AUTH] if auth else [])+[url]
    for i in range(6):
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode==0 and r.stdout.strip():
            return r.stdout if raw else json.loads(r.stdout)
        time.sleep(2*(i+1))
    raise RuntimeError(r.stderr)
def rest(method, path, body=None):
    cmd=['curl','-sS','-m','90','-X',method,'-H',AUTH,'-H','Content-Type: application/json']
    if body is not None: cmd+=['--data',json.dumps(body)]
    cmd+=['https://medcaredemo.online/medcare/wp-json/wp/v2/'+path]
    for i in range(6):
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode==0 and r.stdout.strip(): return json.loads(r.stdout)
        time.sleep(2*(i+1))
    raise RuntimeError(r.stderr)
