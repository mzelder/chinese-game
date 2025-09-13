def roll_dice(lobby_id):
    if lobby_id not in games:
        return {"error": "Lobby not found."}
    
    dice_value = r.randint(1, 6)
    
    lobby = games[lobby_id]
    lobby.last_dice_roll = dice_value

    response = {
        "lobby_id": lobby_id,
        "dice_value": dice_value
    }
    return response