import asyncio
import hikari
import os
from blacksheep.server import Application
from blacksheep.server.responses import pretty_json
from utilities import RAW_RESP, GUID
from utilities import clean_uid, filter_presence


bot = hikari.GatewayBot(intents=hikari.Intents.ALL, token=os.getenv("TOKEN"))
app = Application()
app.use_cors(
    allow_methods="*",
    allow_origins="*",
    allow_headers="* Authorization",
    max_age=300,
)

@app.route("/")
async def wow(request):
  return pretty_json({
    "running":True
  })
@app.route("/api/:uid")
async def home(request,uid):
    uid=clean_uid(uid)
    try:
        user=bot.cache.get_member(GUID, uid) or await bot.rest.fetch_member(GUID, uid)
    except hikari.errors.NotFoundError:
        user=None
    if user:
        presence=filter_presence(user)
        url=user.make_avatar_url(ext="png", size=128)
        if url:
          url=url.url
        else:
          url=user.default_avatar_url.url
        return pretty_json(
            {
                "username":f"{user.username}#{user.discriminator}",
                "userid":user.id,
                "is_bot":user.is_bot,
                "avatar_url": url,
                "presence":presence
            }
        )
    else:
        return pretty_json(
            RAW_RESP
        )

async def b_task(app: Application) -> None:
    # example background task, running once every second,
    # this example also shows how to activate a service using the CI container
    await bot.start()
    await bot.join()
        


async def configure_background_tasks(app):
    asyncio.get_event_loop().create_task(b_task(app))


app.on_start += configure_background_tasks