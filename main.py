import asyncio
import json
import time
import websockets

# Solana Mainnet WebSocket
SOLANA_WS = "wss://api.mainnet-beta.solana.com"

# Raydium AMM Program ID (MAINNET)
RAYDIUM_AMM_PROGRAM = "675kPX9MHTjS2zt1qrXMVEJwBLBsmLSPL5pdb5dSks1R"

async def raydium_listener():
    print("🚀 Solana Raydium Listener başlatılıyor...\n")

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
        
        # Subscription yanıtını kontrol et
        response = await asyncio.wait_for(ws.recv(), timeout=10)
        sub_response = json.loads(response)
        print(f"📡 Subscription Yanıtı: {json.dumps(sub_response, indent=2)}\n")

        last_heartbeat = time.time()
        message_count = 0

        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=30)
                data = json.loads(message)
                message_count += 1

                # heartbeat – çalıştığını anlamak için
                if time.time() - last_heartbeat > 10:
                    print(f"⏱️ Dinleniyor... (heartbeat) - {message_count} mesaj alındı")
                    last_heartbeat = time.time()

                if "params" not in data:
                    continue

                params = data.get("params", {})
                result = params.get("result", {})
                value = result.get("value", {})
                
                signature = value.get("signature")
                logs = value.get("logs", [])
                
                if not signature:
                    continue
                
                print(f"🧾 TX Yakalandı: {signature}")
                
                # Log'larda Raydium event'ler var mı diye kontrol et
                for log in logs:
                    if "initialize" in log.lower() or "create" in log.lower():
                        print(f"   🔥 {log}")

            except websockets.exceptions.ConnectionClosed:
                print("❌ WebSocket bağlantısı koptu. Yeniden bağlanılıyor...")
                await asyncio.sleep(3)
                return await raydium_listener()

            except asyncio.TimeoutError:
                print("⏱️ Dinleniyor... - hiç mesaj yok (timeout)")
                last_heartbeat = time.time()

            except Exception as e:
                print("⚠️ Hata:", e)
                await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(raydium_listener())
