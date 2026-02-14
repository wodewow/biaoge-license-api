from http.server import BaseHTTPRequestHandler
import json
import hashlib

LICENSE_DATA = {
    "keys": {
        "BIAOGE-2024-TEST-0001": {
            "user": "测试用户",
            "enabled": True,
            "device_id": None
        }
    }
}

ADMIN_SECRET = "your_admin_secret_key_here"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/verify?key='):
            key = self.path.split('key=')[1].split('&')[0]
            device_id = None
            if '&device=' in self.path:
                device_id = self.path.split('device=')[1]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if key in LICENSE_DATA['keys']:
                key_info = LICENSE_DATA['keys'][key]
                
                if not key_info['enabled']:
                    response = {'valid': False, 'message': '激活码已被禁用'}
                elif key_info['device_id'] and key_info['device_id'] != device_id:
                    response = {'valid': False, 'message': '激活码已在其他设备上使用'}
                else:
                    response = {
                        'valid': True,
                        'message': f"激活成功 - {key_info['user']}",
                        'user': key_info['user'],
                        'device_bound': key_info['device_id'] is not None
                    }
            else:
                response = {'valid': False, 'message': '激活码无效'}
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/bind':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            key = data.get('key')
            device_id = data.get('device_id')
            secret = data.get('secret')
            
            if secret != ADMIN_SECRET:
                response = {'success': False, 'message': '权限验证失败'}
            elif key in LICENSE_DATA['keys']:
                LICENSE_DATA['keys'][key]['device_id'] = device_id
                response = {'success': True, 'message': '设备绑定成功'}
            else:
                response = {'success': False, 'message': '激活码不存在'}
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
