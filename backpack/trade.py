import math
import time
import logging
from backpack.bpx import BpxClient
from backpack.bpx_pub import Depth

# 설정: API 키 및 시크릿 (반드시 본인의 API 키를 입력해야 함)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"

# 거래 설정
ORDER_CHECK_INTERVAL = 2  # 오픈 오더 확인 주기 (초)


def get_order_book(pair):
    """depth 메서드를 이용하여 호가 정보를 가져옴"""
    order_book = Depth(pair)
    if "asks" not in order_book or "bids" not in order_book:
        return None
    return order_book


def get_nth_price(order_book, side, n):
    """n번째 유리한 호가의 가격을 가져옴"""
    try:
        if side == "Bid" and len(order_book["bids"]) >= n:
            return float(order_book["bids"][n-1][0]) if len(order_book["bids"]) > 4 else float(order_book["bids"][0][0])
        elif side == "Ask" and len(order_book["asks"]) >= n:
            return float(order_book["asks"][n-1][0]) if len(order_book["asks"]) > 4 else float(order_book["asks"][-1][0])
    except (IndexError, TypeError, KeyError):
        return None


def place_limit_order(client, pair, side, price, amount):
    """지정가 주문을 실행"""
    if amount <= 0:
        logging.warning("유효하지 않은 주문 수량: 0 또는 음수 값")
        return None

    order_response = client.ExeOrder(pair, side, "Limit", "GTC", amount, price)

    if not order_response or "id" not in order_response:
        logging.error(f"주문 실패 - 응답: {order_response}")
        return None

    logging.info(f"주문 성공 - 응답: {order_response}")
    return order_response


def cancel_order(client, pair, order_id):
    """주문 취소"""
    return client.orderCancel(pair, order_id)


def get_open_orders(client, pair):
    """현재 오픈된 오더를 가져옴"""
    return client.ordersQuery(pair)


def get_balance(client, asset):
    """bpx.py의 balances 메서드를 이용하여 특정 자산의 잔고 조회"""
    balances = client.balances()
    return float(balances.get(asset, {}).get("available", 0))


def main():
    logging.basicConfig(level=logging.INFO)
    client = BpxClient()
    client.init(API_KEY, API_SECRET)

    # 최초 매수 금액 입력
    usdc_amount = float(input("매수 금액을 입력하세요 (USDC): "))
    ORDER_TIMEOUT = float(input("주문 타임아웃 시간을 입력하세요 (초): "))
    sell_n = int(input("매도 주문 시 사용할 호가 순번을 입력하세요: "))
    buy_n = -int(input("매수 주문 시 사용할 호가 순번을 입력하세요: "))
    TRADING_PAIR = input("페어명칭을 입력하세요 ex) TRUMP_USDC  : ")
    CURRENCY = input("종목명칭을 입력하세요 ex) TRUMP  : ")
    while True:
        try:
            # 잔고 확인
            balance = get_balance(client, CURRENCY)
            if balance >= 0.1:
                logging.info(f"{CURRENCY} 잔액이 존재: {balance}, 매도 주문 진행")
                sell_order_book = get_order_book(TRADING_PAIR)
                if not sell_order_book:
                    logging.warning("매도 호가 정보를 가져오지 못했습니다. 다시 시도합니다.")
                    continue

                sell_price = get_nth_price(sell_order_book, "Ask", sell_n)
                if not sell_price:
                    logging.warning("매도 가격을 가져오지 못했습니다. 다시 시도합니다.")
                    continue

                sell_order = place_limit_order(client, TRADING_PAIR, "Ask", sell_price,  math.floor(balance * 100) / 100)
                if not sell_order:
                    logging.error(f"매도 주문 실패: 가격={sell_price}, 수량={math.floor(balance * 100) / 100}")
                    continue
                logging.info(f"매도 주문 실행: 가격={sell_price}, 수량={math.floor(balance * 100) / 100}")

                # 주문 체결 확인 (최대 30초 대기)
                start_time = time.time()
                while time.time() - start_time < ORDER_TIMEOUT:
                    open_orders = get_open_orders(client, TRADING_PAIR)
                    if not any(order["id"] == sell_order["id"] for order in open_orders):
                        break  # 주문 체결됨
                    time.sleep(ORDER_CHECK_INTERVAL)
                else:
                    cancel_order(client, TRADING_PAIR, sell_order["id"])
                    logging.info("매도 주문 미체결 - 주문 취소 후 재시도")
                    continue

            # 매도 완료 후 매수 수행
            order_book = get_order_book(TRADING_PAIR)
            if not order_book:
                logging.warning("호가 정보를 가져오지 못했습니다. 다시 시도합니다.")
                time.sleep(ORDER_CHECK_INTERVAL)
                continue

            buy_price = get_nth_price(order_book, "Bid", buy_n)
            if not buy_price:
                logging.warning("매수 가격을 가져오지 못했습니다. 다시 시도합니다.")
                continue

            buy_amount = round(usdc_amount / buy_price, 1)  # 소수점 1자리 반올림
            buy_order = place_limit_order(client, TRADING_PAIR, "Bid", buy_price, buy_amount)
            if not buy_order:
                logging.error(f"매수 주문 실패: 가격={buy_price}, 수량={buy_amount}")
                continue
            logging.info(f"매수 주문 실행: 가격={buy_price}, 수량={buy_amount}")

            # 주문 체결 확인 (최대 30초 대기)
            start_time = time.time()
            while time.time() - start_time < ORDER_TIMEOUT:
                open_orders = get_open_orders(client, TRADING_PAIR)
                if not any(order["id"] == buy_order["id"] for order in open_orders):
                    break  # 주문 체결됨
                time.sleep(ORDER_CHECK_INTERVAL)
            else:
                cancel_order(client, TRADING_PAIR, buy_order["id"])
                logging.info("매수 주문 미체결 - 주문 취소 후 재시도")
                continue

        except Exception as e:
            logging.error(f"에러 발생: {e}, 처음부터 다시 실행")
            time.sleep(5)  # 재시도 전 잠시 대기
            continue


if __name__ == "__main__":
    main()
