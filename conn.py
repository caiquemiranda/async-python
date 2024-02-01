import asyncio
import MetaTrader5 as mt5
import random

def enviar_ordem():
    if not mt5.initialize():
        print("Erro na inicialização")
        mt5.shutdown()
        return

    symbol = "USDJPY"
    lot = 0.01
    point = mt5.symbol_info(symbol).point
    price = mt5.symbol_info_tick(symbol).ask
    desvio = 10

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": price - 100 * point,
        "tp": price + 100 * point,
        "deviation": desvio,
        "magic": random.randint(0, 100000),
        "comment": "teste",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Erro ao enviar ordem:", result.retcode)
    else:
        print("Ordem enviada com sucesso")

    mt5.shutdown()


async def enviar_ordem_async():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, enviar_ordem)


async def main():
    tasks = [enviar_ordem_async() for _ in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
