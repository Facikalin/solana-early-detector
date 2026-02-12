import json
import websocket

SOLANA_WS = "wss://mainnet.helius-rpc.com/?api-key=e9013956-6b23-4c03-bc40-afc0e0454a8f"

def on_open(ws):
    print("🚀 Bağlantı açıldı")

    subscribe_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "logsSubscribe",
        "params": [
            "all",
            {"commitment": "confirmed"}
        ]
    }

    ws.send(json.dumps(subscribe_msg))
    print("📡 Subscribe gönderildi")

def on_message(ws, message):
    data = json.loads(message)

    if "result" in data and "id" in data:
        print("📡 Subscription yanıtı:", data)
        return

    if "params" in data:
        value = data["params"]["result"]["value"]
        signature = value.get("signature")

        if signature:
            print("🧾 TX:", signature)

def on_error(ws, error):
    print("❌ Hata:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔌 Bağlantı kapandı")

if __name__ == "__main__":
    websocket.enableTrace(False)

    ws = websocket.WebSocketApp(
        SOLANA_WS,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()
