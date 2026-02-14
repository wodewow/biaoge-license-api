from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

LICENSE_KEYS_JSON = os.environ.get('LICENSE_KEYS_JSON', '{}')

def get_license_data():
    try:
        data = json.loads(LICENSE_KEYS_JSON)
        if 'keys' not in data:
            data = {'keys': data}
        return data
    except:
        return {
            "keys": {
                "BIAOGE-2024-TEST-0001": {
                    "user": "测试用户",
                    "enabled": True,
                    "device_id": None
                }
            }
        }

@app.route('/api/verify', methods=['GET'])
def verify():
    key = request.args.get('key')
    device_id = request.args.get('device')
    
    if not key:
        return jsonify({'valid': False, 'message': '缺少激活码参数'})
    
    LICENSE_DATA = get_license_data()
    
    if key in LICENSE_DATA['keys']:
        key_info = LICENSE_DATA['keys'][key]
        
        if not key_info.get('enabled', True):
            return jsonify({'valid': False, 'message': '激活码已被禁用'})
        elif key_info.get('device_id') and key_info['device_id'] != device_id:
            return jsonify({'valid': False, 'message': '激活码已在其他设备上使用'})
        else:
            return jsonify({
                'valid': True,
                'message': f"激活成功 - {key_info.get('user', '用户')}",
                'user': key_info.get('user', '用户'),
                'device_bound': key_info.get('device_id') is not None
            })
    else:
        return jsonify({'valid': False, 'message': '激活码无效'})

@app.route('/')
def home():
    return 'BiaoGe License API - Running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
