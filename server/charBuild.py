from faketime import time

from flask import request

from constants import USER_JSON_PATH
from utils import read_json, write_json


def charBuildBatchSetCharVoiceLan():

    data = request.data
    data = {
        "result": {},
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }
    return data


def charBuildaddonStoryUnlock():
    
    data = request.data
    request_data = request.get_json()

    ts = {"fts": int(time()), "rts": int(time())} # TODO

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "troop": {
                    "addon": {
                    }
                }
            }
        }
    }

    storyId = {"story": {request_data["storyId"]: ts}}
    charId = {request_data["charId"]: storyId}

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["troop"]["addon"].update(charId)

    data["playerDataDelta"]["modified"]["troop"]["addon"].update(charId)

    write_json(saved_data, USER_JSON_PATH)

    return data


def charBuildSetCharVoiceLan():

    data = request.data
    request_data = request.get_json()

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "troop": {
                    "chars": {
                    }
                }
            }
        }
    }

    saved_data = read_json(USER_JSON_PATH)
    for character in request_data["charList"]:

        saved_data["user"]["troop"]["chars"][str(character)]["voiceLan"] = request_data["voiceLan"]
        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(character): {
                "voiceLan": request_data["voiceLan"]
            }
        })

    write_json(saved_data, USER_JSON_PATH)

    return data


def charBuildSetDefaultSkill():

    data = request.data
    request_data = request.get_json()

    charInstId = request_data["charInstId"]
    defaultSkillIndex = request_data["defaultSkillIndex"]
    
    data = {
        "playerDataDelta": {
            "modified": {
                "troop": {
                    "chars": {}
                }
            },
            "deleted": {}
        }
    }

    saved_data = read_json(USER_JSON_PATH)

    char_data = saved_data["user"]["troop"]["chars"].get(str(charInstId))

    if char_data:

        char_data["defaultSkillIndex"] = defaultSkillIndex


        current_template = char_data.get("currentTmpl")

        if current_template:
            # Update the 'defaultSkillIndex' in the 'tmpl' section for the current template
            if current_template in char_data["tmpl"]:
                char_data["tmpl"][current_template]["defaultSkillIndex"] = defaultSkillIndex


        data["playerDataDelta"]["modified"]["troop"]["chars"][str(charInstId)] = {
            "defaultSkillIndex": defaultSkillIndex,
            "tmpl": {
                current_template: {
                    "defaultSkillIndex": defaultSkillIndex
                }
            }
        }


        write_json(saved_data, USER_JSON_PATH)

    return data


def charBuildChangeCharSkin():
    
    data = request.data
    request_data = request.get_json()

    charInstId = request_data["charInstId"]
    skinId = request_data["skinId"]

    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "chars":{}
                }
            },
            "deleted":{}
        }
    }

    saved_data = read_json(USER_JSON_PATH)
    
    char_data = saved_data["user"]["troop"]["chars"].get(str(charInstId))

    if char_data:

        char_data["skinId"] = skinId

        current_template = char_data.get("currentTmpl")

        if current_template:
            # Update the 'skinId' in the 'tmpl' section for the current template
            if current_template in char_data["tmpl"]:
                char_data["tmpl"][current_template]["skinId"] = skinId


        data["playerDataDelta"]["modified"]["troop"]["chars"].update({
            str(charInstId): {
                "skin": skinId,
                "tmpl": {
                    current_template: {
                        "skinId": skinId
                    }
                }
            }
        })

    saved_data["user"]["troop"]["chars"][str(charInstId)]["skin"] = skinId
    write_json(saved_data, USER_JSON_PATH)

    return data

def charBuildSetEquipment():

    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    equipId = request_data["equipId"]
    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "chars":{}
                }
            },
            "deleted":{}
        }
    }

    saved_data = read_json(USER_JSON_PATH)
    data["playerDataDelta"]["modified"].update({
        "troop": {
            "chars": {
                str(charInstId): {
                    "currentEquip": equipId
                }
            }
        }
    })

    saved_data["user"]["troop"]["chars"][str(charInstId)]["currentEquip"] = equipId
    write_json(saved_data, USER_JSON_PATH)

    return data


def charBuildChangeCharTemplate():

    data = request.data
    request_data = request.get_json()

    data = {
        "playerDataDelta":{
            "modified":{
                "troop":{
                    "chars":{
                        str(request_data["charInstId"]): {
                            "currentTmpl": request_data["templateId"]
                        }
                    }
                }
            },
            "deleted":{}
        }
    }

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["troop"]["chars"][str(request_data["charInstId"])]["currentTmpl"] = request_data["templateId"]
    write_json(saved_data, USER_JSON_PATH)

    return data