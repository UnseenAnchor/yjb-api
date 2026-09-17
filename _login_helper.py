"""分步登录辅助:step1 发送验证码,step2 用验证码登录"""
import sys, json, uuid
from pathlib import Path
from yjb_tool import YJBClient, save_token, TOKEN_FILE

STATE_FILE = Path("_device_id.tmp")


def step1(phone: str):
    device_id = str(uuid.uuid4()).upper()
    client = YJBClient(token=device_id, api="new")
    print(f"正在向 {phone} 发送验证码...")
    resp = client.post('/send_code', json={"phone": phone})
    STATE_FILE.write_text(json.dumps({"device_id": device_id, "phone": phone}))
    print(f"验证码已发送,device_id 已保存到 {STATE_FILE}")
    print(f"send_code 响应: {resp}")


def step2(code: str):
    state = json.loads(STATE_FILE.read_text())
    client = YJBClient(token=state["device_id"], api="new")
    print("正在登录...")
    data = client.post('/login', json={
        "phone": state["phone"],
        "mode": "phone",
        "verify_code": code,
        "invite_code": "",
        "is_band_wechat": 1,
    })
    token = data.get('token')
    if not token:
        print(f"登录响应无 token: {data}")
        sys.exit(1)
    save_token(token)
    print(f"✅ 登录成功,token 已保存到 {TOKEN_FILE}")
    # 打印除 token 外的响应内容,便于查看用户信息
    show = {k: v for k, v in data.items() if k != 'token'}
    print(f"用户信息: {json.dumps(show, ensure_ascii=False, indent=2)}")


if __name__ == "__main__":
    if sys.argv[1] == "1":
        step1(sys.argv[2])
    else:
        step2(sys.argv[2])
