"""Minimal WordPress XML-RPC client (application-password auth from the MCP config)."""
import base64, os, subprocess, xmlrpc.client
import mcp

_u, _p = base64.b64decode(mcp.AUTH.split('Basic ')[1]).decode().split(':', 1)
URL = 'https://medcaredemo.online/medcare/xmlrpc.php'


def call(method, *args):
    body = xmlrpc.client.dumps((1, _u, _p) + args, method, allow_none=True)
    f = '/tmp/claude-0/_xrpc.xml'
    open(f, 'w').write(body)
    try:
        for _ in range(4):
            r = subprocess.run(['curl', '-sS', '-m', '180', '-H', 'Content-Type: text/xml; charset=utf-8', '--data-binary', '@' + f, URL],
                               capture_output=True, text=True)
            if r.stdout.lstrip().startswith('<?xml'):
                return xmlrpc.client.loads(r.stdout)[0][0]
        raise RuntimeError(r.stdout[:500] + r.stderr[:300])
    finally:
        os.remove(f)
