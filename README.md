# backpackapi
**This is an api template for backpack automation transactions.** <br>
**You can effectively increase the trading volume with low fees through maker orders.**<br>
**backpack 자동화 거래를 위한 api 템플릿입니다.**<br>
**메이커 주문을 통한 저렴한 수수료로 거래볼륨을 효과적으로 늘릴 수 있습니다.**
<br><br><br>

**API Docs (API 문서)**<br>
- https://docs.backpack.exchange/<br>
- pip install bpx-api<br>
<br><br><br>

**How to use it**<br>
 Download all three files in /backpack.<br>
 Enter your api key and secret in trade.py<br>
* The api key and secret can be created at https://backpack.exchange/portfolio/settings/api-keys.
<br><br>
Run trade.py<br>
Enter multiple variables at execution.<br>
1. Purchase amount: Enter the amount to be purchased per order (all sales)<br>
2. Order Timeout: If the timeout is exceeded after the order is submitted, cancel the order.<br>
3. Order number: Find the nth most favorable asking price in the order book.<br>
4. Pair Name: Enter a transaction pair consisting of base and counter.<br>
5. Item Name: Enter the base name for checking the balance.<br>
<br><br>
**사용안내**<br>
/backpack 내 3개의 파일을 모두 다운로드 받습니다.<br>
trade.py 안에 본인의 api key와 secret 을 입력합니다.<br>
* api key와 secret은 https://backpack.exchange/portfolio/settings/api-keys 에서 생성 할 수 있습니다.<br>
<br><br>
trade.py를 실행합니다.<br>
실행 시 여러 변수를 입력합니다.<br>
1. 매수 금액 : 1번의 주문 당 매수 할 금액을 입력 (매도는 전량)<br>
2. 주문 타임아웃 : 주문 제출 후 타임아웃이 초과되면 주문을 취소합니다.<br>
3. 호가 순번 : 오더북 내에서 n번째로 유리한 호가를 찾습니다.<br>
4. 페어명칭 : base 와 counter 로 이루어진 거래쌍을 입력합니다.<br>
5. 종목명칭 : 잔고 확인을 위한 base 명칭을 입력합니다.<br>
