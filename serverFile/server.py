from fastapi import FastAPI, HTTPException
import requests
from paymentwall import Paymentwall, Widget

app = FastAPI()

project_key = ""
secret_key = ""

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/issue_billing_key")
async def issue_billing_key(customer_uid: str, card_number: str, expiry: str, birth: str, pwd_2digit: str):
    payload = {
        "customer_uid": customer_uid,
        "card_number": card_number,
        "expiry": expiry,
        "birth": birth,
        "pwd_2digit": pwd_2digit,
        "pg": "paymentwall",
        "amount": 0,
        "name": "빌링키 발급",
        "buyer_name": "구매자",
        "buyer_email": "buyer@example.com",
        "buyer_tel": "010-1234-5678"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    try:
        response = requests.post("https://api.iamport.kr/subscribe/customers", json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        if result['code'] == 0:
            return {"message": "빌링키 발급 성공", "customer_uid": customer_uid}
        else:
            raise HTTPException(status_code=400, detail=result['message'])
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pay/")
async def create_payment_widget():
    Paymentwall.set_api_type(Paymentwall.API_GOODS)
    Paymentwall.set_app_key(project_key)
    Paymentwall.set_secret_key(secret_key)

    widget = Widget(
        'user4522',
        'fp',
        [],
        {
            'email': 'user@hostname.com',
            'history[registration_date]': 'registered_date_of_user',
            'ps': 'all',
            'additional_param_name': 'additional_param_value'
        }
    )
    
    html_code = widget.get_html_code()
    return {"widget_html": html_code}