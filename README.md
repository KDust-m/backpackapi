# backpackapi
This is an api template for backpack automation transactions.

backpack 자동화 거래를 위한 api 템플릿입니다.



API Docs (API 문서)

https://docs.backpack.exchange/

pip install bpx-api


How to use it

Download all three files in /backpack.

Enter your api key and secret in trade.py .

* The api key and secret can be created at https://backpack.exchange/portfolio/settings/api-keys.



Run trade.py .

Enter multiple variables at execution.

1. Purchase amount: Enter the amount to be purchased per order (all sales)

2. Order Timeout: If the timeout is exceeded after the order is submitted, cancel the order.

3. Order number: Find the nth most favorable asking price in the order book.

4. Pair Name: Enter a transaction pair consisting of base and counter.

5. Item Name: Enter the base name for checking the balance.

사용안내

/backpack 내 3개의 파일을 모두 다운로드 받습니다.

trade.py 안에 본인의 api key와 secret 을 입력합니다.

* api key와 secret은 https://backpack.exchange/portfolio/settings/api-keys 에서 생성 할 수 있습니다.



trade.py를 실행합니다.

실행 시 여러 변수를 입력합니다.

1. 매수 금액 : 1번의 주문 당 매수 할 금액을 입력 (매도는 전량)

2. 주문 타임아웃 : 주문 제출 후 타임아웃이 초과되면 주문을 취소합니다.

3. 호가 순번 : 오더북 내에서 n번째로 유리한 호가를 찾습니다.

4. 페어명칭 : base 와 counter 로 이루어진 거래쌍을 입력합니다.

5. 종목명칭 : 잔고 확인을 위한 base 명칭을 입력합니다.

