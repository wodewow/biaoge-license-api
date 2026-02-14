# BiaoGeVIP License API

## 部署步骤

1. 在GitHub创建新仓库，名称：`biaoge-license-api`
2. 上传这个文件夹的所有文件到仓库
3. 访问 https://vercel.com/new
4. 选择刚创建的仓库
5. 点击 Deploy
6. 部署完成后会得到一个URL，比如：`https://your-project.vercel.app`

## API使用

### 验证激活码
```
GET /api/verify?key=BIAOGE-2024-TEST-0001&device=设备ID
```

### 绑定设备
```
POST /api/bind
{
  "key": "BIAOGE-2024-TEST-0001",
  "device_id": "设备ID",
  "secret": "your_admin_secret_key_here"
}
```

## 修改激活码

编辑 `api/verify.py` 中的 `LICENSE_DATA` 字典，添加或修改激活码。

## 安全建议

1. 修改 `ADMIN_SECRET` 为复杂密钥
2. 定期更新激活码列表
3. 监控API调用频率
