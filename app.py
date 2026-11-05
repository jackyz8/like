from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)
INFO_API = "https://ff-info-psi.vercel.app/info"


def get_player_info(uid, region):
    r = requests.get(INFO_API, params={"uid": uid, "region": region}, timeout=10)
    r.raise_for_status()
    data = r.json()

    # Supports the common nested response from the info API.
    basic = data.get("basicInfo") or data.get("basic_info") or {}
    account = data.get("AccountInfo") or data.get("accountInfo") or {}

    name = basic.get("nickname") or basic.get("name") or data.get("name") or "N/A"
    out_uid = account.get("UID") or account.get("uid") or data.get("uid") or uid
    level = basic.get("level") or data.get("level") or 0
    out_region = basic.get("region") or data.get("region") or region
    likes = basic.get("liked") or basic.get("likes") or data.get("likes") or 0

    return {
        "uid": str(out_uid),
        "name": str(name),
        "level": level,
        "region": str(out_region),
        "likes": int(likes) if str(likes).isdigit() else 0,
    }


@app.get("/Storm-Like")
def like_api():
    uid = request.args.get("uid", "").strip()
    region = (request.args.get("region") or request.args.get("server") or "IND").strip().upper()

    if not uid:
        return jsonify({"status": 0, "error": "UID required"}), 400

    try:
        player = get_player_info(uid, region)
    except Exception as e:
        return jsonify({
            "status": 0,
            "error": "Info API unavailable",
            "details": str(e),
        }), 502

    # DEMO ONLY: this number is simulated and does not change any game account.
    likes_sent = random.randint(200, 220)
    likes_before = max(0, player["likes"] - likes_sent)
    likes_after = player["likes"]

    return jsonify({
        "status": 1,
        "PlayerNickname": player["name"],
        "UID": player["uid"],
        "Region": player["region"],
        "Level": player["level"],
        "LikesGivenByAPI": likes_sent,
        "LikesbeforeCommand": likes_before,
        "LikesafterCommand": likes_after,
        "Owner": "@TheStorm07x , @nayakxcheats"
    })


@app.get("/")
def home():
    return jsonify({
        "message": "Running...",
        "owner": "@TheStorm07x",
        "usage": "/Storm-Like?uid=13057940699&region=IND"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
