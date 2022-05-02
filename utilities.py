import time
from datetime import timezone 
import datetime


def utc_converter(dt):
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp

BUID=921064942289977375
GUID=921064159330832414
RAW_PRES = {
    "exists":False,
    "name":None,
    "status":"OFFLINE",
    "status_enum":"offline",
    "type":"PLAYING",
    "type_enum":0,
    "created_at":time.time(),
    "state":None,
    "details":None,
    "large_image":{
        "exists":False,
        "text":None,
        "image":None
    },
    "small_image":{
        "exists":False,
        "text":None,
        "image":None
    },
}
RAW_RESP = {
    "username":f"Dummy#1234",
    "userid":1234,
    "is_bot":False,
    "avatar_url":"https://example.com",
    "presence":RAW_PRES.copy()
}

def filter_presence(user):
    '''
    
    Convert's Presence Like Objects to a raw JSON format

    '''
    presence=user.get_presence()
    resp_PRES=RAW_PRES.copy()
    resp_PRES["large_image"]=RAW_PRES["large_image"].copy()
    resp_PRES["small_image"]=RAW_PRES["small_image"].copy()
    if presence:
        resp_PRES["status"]=presence.visible_status.name
        resp_PRES["status_enum"]=presence.visible_status.value
        if len(presence.activities) > 0:
            activity=presence.activities[0]
            resp_PRES['exists']=True
            resp_PRES['name']=activity.name
            resp_PRES['type']=activity.type.name
            resp_PRES['type_enum']=activity.type.value
            resp_PRES['created_at']=utc_converter(activity.created_at)
            if resp_PRES['type_enum'] != 4:
                if activity.assets:
                    if activity.assets.large_image:
                        resp_PRES['large_image']["exists"]=True
                        resp_PRES['large_image']["image"]=activity.assets.large_image
                        resp_PRES['large_image']["text"]=activity.assets.large_text or None
                    if activity.assets.small_image:
                        resp_PRES['small_image']["exists"]=True
                        resp_PRES['small_image']["image"]=activity.assets.small_image
                        resp_PRES['small_image']["text"]=activity.assets.small_text or None
            resp_PRES['details']=activity.details or None
            resp_PRES['state']=activity.state or None
    return resp_PRES
def clean_uid(uid):
    # Filters out weird userids
    if not (uid.isdigit() and len(uid) in range(17,19)):
        uid=BUID
    uid=int(uid)
    return uid