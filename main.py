import asyncio
import hikari
import os
import json
from blacksheep import Application, WebSocket, WebSocketDisconnectError, pretty_json
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


async def make_response(uid):
  # Make a JSON body out of given data
  try:
      user=bot.cache.get_member(GUID, uid)
  except hikari.errors.NotFoundError:
      user=None
  if user:
      presence=filter_presence(user)
      url=user.make_avatar_url(ext="png", size=128)
      if url:
        url=url.url
      else:
        url=user.default_avatar_url.url
      return {
              "username":f"{user.username}#{user.discriminator}",
              "userid":user.id,
              "is_bot":user.is_bot,
              "avatar_url": url,
              "presence":presence
          }
  else:
      return RAW_RESP

    
async def was_rest(bot, GUID, uid):
  print("Rest FETCH")
  return await bot.rest.fetch_member(GUID, uid)
  
@app.route("/")
async def home(request):
  return pretty_json({
    "running":True
  })
  
@app.route("/api/:uid")
async def api_uid(request,uid):
    uid=clean_uid(uid)
    data=await make_response(uid)
    return pretty_json(data)

@app.router.ws("/ws")
async def ws_recv(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            msg = await websocket.receive_text()
            uid=clean_uid(msg)
            data=await make_response(uid)
            await websocket.send_json(data)

    except WebSocketDisconnectError:
        print("out of scope")
        pass

async def b_task(app: Application) -> None:
    # example background task, running once every second,
    # this example also shows how to activate a service using the CI container
    await bot.start()
    await bot.join()
        


async def configure_background_tasks(app):
    asyncio.get_event_loop().create_task(b_task(app))


app.on_start += configure_background_tasks