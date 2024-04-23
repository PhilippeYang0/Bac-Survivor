import json

def update(save_file:str,actual_display:int = -1,volume_bgm:float = -1,volume_se:float = -1,gemmes:int = -1,items_achetes: list = []) -> None:
    """
    Insère les valeurs actual_display, volume_bgm, volume_se, gemmes, items_achete
    """
    with open(save_file, "r+") as f:        
        save_json = json.load(f)
        # On crée un nouveau dictionnaire avec la valeur de gemmes remplacés
        if not (actual_display == -1):
            save_json["actual_display"] = actual_display
        if not (volume_bgm == -1):
            save_json["volume_bgm"] = volume_bgm
        if not (volume_se == -1):
            save_json["volume_se"] = volume_se
        if not (gemmes == -1):
            save_json["gemmes"] = gemmes
        if not (items_achetes == []):
            save_json['items_achetes'] = items_achetes
        
        f.seek(0) #le curseur de lecture revient au début
        json.dump(save_json,f) #la réécriture écrase les jsons existants pour écrire le nouveau
        f.truncate() #gère le cas où le nouveau dictionnaire est plus petit que le précédent

    