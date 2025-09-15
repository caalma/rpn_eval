import asyncio
from lib.converters import async_print
from lib.abb_logic import AbbLogicManager

async def repl_abb():
    """Función que controla la lógica principal del ciclo para el REPL."""

    config = {
        'interface': 'repl',
        'txtout': print,
        'txtoutAsync': async_print
    }

    loop = AbbLogicManager()
    await loop.config(config)
    await loop.initialize()
    await loop.run()


def interface_repl_abb():
    asyncio.run(repl_abb())
