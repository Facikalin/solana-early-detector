import asyncio
import json
import websockets

SOLANA_WS = "wss://api.mainnet-beta.solana.com/"
RAYDIUM_PROGRAM = "675kPX9MHTjS2zt1qrXMVEJwBLBsmLSPL5pdb5dSks1R"

async def listener():
    print("🚀 ALL stream (Raydium initialize filtreli)\n")

    async with websockets.connect(
        SOLANA_WS,
        ping_interval=20,
        ping_timeout=20,
        max_size=None
    ) as ws:

        subscribe_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "logsSubscribe",
            "params": [
                "all",
                {"commitment": "confirmed"}
            ]
        }

        await ws.send(json.dumps(subscribe_msg))

        sub_response = await ws.recv()
        print("📡 Subscription OK\n")

        while True:
            message = await ws.recv()
            data = json.loads(message)

            if "params" not in data:
                continue

            value = data["params"]["result"]["value"]
            logs = value.get("logs", [])
            signature = value.get("signature")

            if not signature:
                continue

            print("TX geldi:", signature)

            raydium_seen = False
            initialize_seen = False

            for log in logs:
                if RAYDIUM_PROGRAM in log:
                    raydium_seen = True
                if "initialize" in log.lower():
                    initialize_seen = True

            if raydium_seen and initialize_seen:
                print("🔥 YENİ RAYDIUM POOL:", signature)



# 🔥 BU KISIM EKSİKTİ
if __name__ == "__main__":
    asyncio.run(listener())
