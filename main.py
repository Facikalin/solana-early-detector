import asyncio
import json
import websockets

SOLANA_WS = "wss://api.mainnet-beta.solana.com/"
RAYDIUM_PROGRAM = "675kPX9MHTjS2zt1qrXMVEJwBLBsmLSPL5pdb5dSks1R"

async def listener():
    print("🚀 ALL stream (Raydium pool detector)\n")

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
        await ws.recv()

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

            raydium_invoke = False
            initialize_event = False

            for log in logs:
                # Raydium invoke yakala
                if log.startswith("Program " + RAYDIUM_PROGRAM) and "invoke" in log:
                    raydium_invoke = True

                # initialize event yakala
                if "initialize" in log.lower():
                    initialize_event = True

            if raydium_invoke:
                print("🟢 Raydium TX:", signature)

            if raydium_invoke and initialize_event:
                print("🔥 YENİ RAYDIUM POOL:", signature)
                print("--------------------------------------------------")


if __name__ == "__main__":
    asyncio.run(listener())
