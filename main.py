import asyncio
import json
import websockets

SOLANA_WS = "wss://api.mainnet-beta.solana.com/"
RAYDIUM_PROGRAM = "675kPX9MHTjS2zt1qrXMVEJwBLBsmLSPL5pdb5dSks1R"

async def listener():
    print("🚀 Raydium initialize listener başlatıldı\n")

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
                {"mentions": [RAYDIUM_PROGRAM]},
                {"commitment": "confirmed"}
            ]
        }

        await ws.send(json.dumps(subscribe_msg))
        await ws.recv()

        while True:
            message = await ws.recv()
            data = json.loads(message)

            if "params" not in data:
                continue

            value = data["params"]["result"]["value"]
            logs = value.get("logs", [])
            signature = value.get("signature")

            for log in logs:
                if "initialize" in log.lower():
                    print("🔥 YENİ POOL:", signature)
                    break


if __name__ == "__main__":
    asyncio.run(listener())
