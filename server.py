from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# إعدادات الاتصال (اللي أرسلتها سابقاً)
COOKIES = {
    '_ga': 'GA1.1.358772145.1772262859',
    'mobile_device': '1',
    'wp-wpml_current_language': 'ar',
    'HstCfa4923502': '1772262858954',
    'HstCmu4923502': '1772262858954',
    'HstCnv4923502': '1',
    'HstCns4923502': '1',
    '__gads': 'ID=c61ee6cafd1d1104:T=1772262858:RT=1772262858:S=ALNI_Ma3qpSOrj5kKy0XxCPME895SaJP-g',
    '__gpi': 'UID=00001343e7f07bd4:T=1772262858:RT=1772262858:S=ALNI_MaHfjYGruxpqveqcwvTZBYtdt83eQ',
    '__eoi': 'ID=a8c0136ed7bfef2c:T=1772262858:RT=1772262858:S=AA-AfjbshKzHie_SkPd66_wWxAdA',
    'HstCla4923502': '1772262862133',
    'HstPn4923502': '2',
    'HstPt4923502': '2',
    'FCCDCF': '%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%22c20e722a-5c97-4f05-9563-3e7bc8b6cfb7%5C%22%2C%5B1772262863%2C635000000%5D%5D%22%5D%5D%5D',
    'FCNEC': '%5B%5B%22AKsRol8I-as9lYkxD8XB6MccX2AetB6KLhOP41onGQ5kTHSa1226PZwrmIdZTcrO1SoQezX2z37g2ztjWeuUFvpnC1easxwwQDEQKPw7eEp_cMis5blhXsDwQ5pDo519TdJft_kJCqlzm7Mu3vOLoAIaFCdoESV7Tg%3D%3D%22%5D%5D',
    '_ga_V4C5BVLHBE': 'GS2.1.s1772262858$o1$g1$t1772262903$j15$l0$h0',
}

HEADERS = {
    'authority': 'zoominsta.de',
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'cookie': '_ga=GA1.1.358772145.1772262859; mobile_device=1; wp-wpml_current_language=ar; HstCfa4923502=1772262858954; HstCmu4923502=1772262858954; HstCnv4923502=1; HstCns4923502=1; __gads=ID=c61ee6cafd1d1104:T=1772262858:RT=1772262858:S=ALNI_Ma3qpSOrj5kKy0XxCPME895SaJP-g; __gpi=UID=00001343e7f07bd4:T=1772262858:RT=1772262858:S=ALNI_MaHfjYGruxpqveqcwvTZBYtdt83eQ; __eoi=ID=a8c0136ed7bfef2c:T=1772262858:RT=1772262858:S=AA-AfjbshKzHie_SkPd66_wWxAdA; HstCla4923502=1772262862133; HstPn4923502=2; HstPt4923502=2; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%22c20e722a-5c97-4f05-9563-3e7bc8b6cfb7%5C%22%2C%5B1772262863%2C635000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol8I-as9lYkxD8XB6MccX2AetB6KLhOP41onGQ5kTHSa1226PZwrmIdZTcrO1SoQezX2z37g2ztjWeuUFvpnC1easxwwQDEQKPw7eEp_cMis5blhXsDwQ5pDo519TdJft_kJCqlzm7Mu3vOLoAIaFCdoESV7Tg%3D%3D%22%5D%5D; _ga_V4C5BVLHBE=GS2.1.s1772262858$o1$g1$t1772262903$j15$l0$h0',
    'origin': 'https://zoominsta.de',
    'referer': 'https://zoominsta.de/ar/',
    'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-encoded': 'true',
    'x-requested-with': 'XMLHttpRequest',
    'x-signature': '66810f5e5dfe7d14b5362002d397d5d56c2c1b13b20608f9bb3e0ea109c50ac2',
    'x-valy-cache': 'true',
}

DATA_TEMPLATE = {
    'payload': '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',
}

# دالة لفحص الحساب
def check_account(username):
    # ضع هنا الطريقة التي تستخدمها لإنشاء payload حسب username
    DATA_TEMPLATE['payload'] = username  # مثال بسيط
    try:
        response = requests.post('https://zoominsta.de/process', cookies=COOKIES, headers=HEADERS, data=DATA_TEMPLATE, timeout=10)
        response.raise_for_status()
        data = response.json()

        # تحقق إذا الحساب موجود
        if data.get('result') and not data['result'].get('error', True):
            return {"error": False, "profile": data['result']['profile']}
        else:
            return {"error": True}

    except Exception as e:
        return {"error": True}

# المسار الذي يستقبله HTML
@app.route('/check', methods=['POST'])
def check():
    username = request.form.get('username')
    if not username:
        return jsonify({"result": {"error": True}})

    result = check_account(username)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)