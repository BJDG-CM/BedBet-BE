from app.db import user_col, team_col, money_col, coin_col, clean_doc
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


def getUserInfo(userUid: str):
    user = user_col.find_one({"userUid": userUid})
    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    # ObjectId / datetime 직렬화를 위해 clean_doc 또는 jsonable_encoder 사용
    user = clean_doc(user) or {}
    user.pop("password", None)
    return JSONResponse(status_code=200, content={"user": jsonable_encoder(user)})

def deleteUser(userUid: str):
    user_col.delete_one({"userUid": userUid})
    team_col.update_many(
        {"teammates.userUid": userUid},
        {"$pull": {"teammates": {"userUid": userUid}}}
    )
    money_col.delete_one({"userUid": userUid})
    coin_col.delete_one({"userUid": userUid})   
    
    return JSONResponse(status_code=200, content={"message": "User deleted successfully"})