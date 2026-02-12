import asyncio
import json
import time
import websockets

SOLANA_WS = "wss://api.mainnet-beta.solana.com"
RAYDIUM_AMM_PROGRAM = "675kPX9MHTjS2zt1qrXMVEJwBLBsmLSPL5pdb5dSks1R"

async def raydium_listener():
    print("🚀 Solana Raydium Listener başlatılıyor...\n")

    try:
        async with websockets.connect(SOLANA_WS, ping_interval=20) as ws:
            subscribe_msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "logsSubscribe",
                "params": [
                    {"mentions": [RAYDIUM_AMM_PROGRAM]},
                    {"commitment": "confirmed"}
                ]
            }

            await ws.send(json.dumps(subscribe_msg))
            print("🔍 Raydium AMM logları dinleniyor...\n")
            
            response = await asyncio.wait_for(ws.recv(), timeout=10)
            sub_response = json.loads(response)
            print(f"📡 Subscription Yanıtı: {json.dumps(sub_response, indent=2)}\n")

            if "error" in sub_response:
                print(f"❌ Hata: {sub_response['error']}")
                return

            last_heartbeat = time.time()
            message_count = 0

            while True:
                try:
                    message = await asyncio.wait_for(ws.recv(), timeout=30)
                    data = json.loads(message)
                    message_count += 1

                    if time.time() - last_heartbeat > 10:
                        print(f"⏱️ Dinleniyor... ({message_count} mesaj alındı)")
                        last_heartbeat = time.time()

                    if "params" not in data:
                        continue

                    value = data["params"]["result"]["value"]
                    signature = value.get("signature")
                    logs = value.get("logs", [])

                    if signature:
                        print(f"🧾 TX: {signature}")
                        for log in logs:
                            if "initialize" in log.lower() or "create" in log.lower():
                                print(f"   🔥 {log}")

                except asyncio.TimeoutError:
                    if time.time() - last_heartbeat > 10:
                        print(f"⏱️ Dinleniyor... ({message_count} mesaj alındı)")
                        last_heartbeat = time.time()

                except Exception as e:
                    print(f"⚠️ Hata: {e}")

    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")

if __name__ == "__main__":
    asyncio.run(raydium_listener())
