import os

import crescent, hikari

bot = hikari.GatewayBot(os.environ["TOKEN"], intents=hikari.Intents.MESSAGE_CONTENT)
client = crescent.Client(bot)
client.plugins.load_folder("Botty.plugins")

@client.include
@crescent.command(description="Pong!")
async def ping(ctx:crescent.Context) -> None:
    await ctx.respond("Pong!")



if __name__ == "__main__":
    if os.name != "nt":
        import asyncio

        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    bot.run()

