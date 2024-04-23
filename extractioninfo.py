from typing import Tuple,List,Any,Dict
import json
import pygame

ENNEMIES = Dict[str,List[Any]]

WAVES = List[List[str]]

PICKUPS = List[List[Any]]
POIDS = List[int]

BUFF = List[Any]
LEVELS = List[int]

ARME = Tuple[str, List[Dict[str, Any]]]

ITEMS = List[List[Any]]
STATS_BUFFS = Dict[str, List[Any]]

def extraction_save(name_file:str) -> Tuple[int,float,float,int,list]:
    """
    Renvoie les données de sauvegarde d'une partie contenue dans name_file.
    Renvoie dans l'ordre:
        la configuration d'écran actuelle, un entier,
        le volume du son d'arrière plan, un floatant,
        le volume du son des effets, un floatant,
        les gemmes, un entier,
        les items achetés (donc plus disponibles) au shop global, une liste de string.
    """
    with open(name_file, "r") as f:
        levels_infos = json.load(f)
    return levels_infos["actual_display"], levels_infos["volume_bgm"], levels_infos["volume_se"],\
           levels_infos["gemmes"], levels_infos["items_achetes"]

def extraction_data_level(path:str) -> Tuple[pygame.Surface,str,list,pygame.Surface,str,str]:
    """
    path: nom du chemin où est contenu les infos des niveaux. Format:json.
    Renvoie un tuple avec dans l'ordre:
        1/le fichier contenant l'affichage du player.
        2/le fichier contenant les armes utiliées par le player.
        3/le fichier contenant l'affichage du background.
        4/le fichier contenant les infos des ennemis.
        5/le fichier contenant les infos des vagues.
        6/le fichier contenant l'affichage de l'image lors de level_select, non utilisé
        7/le fichier contenant la musique de fond du niveau associé
    """
    return pygame.image.load(path +"player.png").convert_alpha(),\
           path +"weapon.json",\
           pygame.image.load(path + "background.png").convert_alpha(),\
           path+"ennemies.json",\
           path+"vagues.json",\
           path+"display_choix.png",\
           path+"bgm.mp3"

def extraction_ennemy(name_file:str) -> ENNEMIES:
    """
    name_file: nom du fichier où sont contenus les infos des ennemis. Format:json.
    Renvoie un dictionnaire avec en clé le nom de chaque monstre et en valeur leurs statistiques,
    dans l'ordre du constructeur de Ennemy.
    """
    with open(name_file, "r") as f:
        ennemy_infos = json.load(f)
    ennemies = {}
    for nom, ennemy in ennemy_infos.items():
        ennemy_info =     ([ennemy["PV"],
                            ennemy["SPEED"],
                            ennemy["XP"],
                            ennemy["SIZE"],
                            pygame.image.load(ennemy["DISPLAY"]).convert_alpha()])
        
        if "BULLETS_COOLDOWNS" in ennemy:
            ennemy_info.append(ennemy["BULLETS_COOLDOWNS"])
            ennemy_info.append(ennemy["AMOUNTS_FIRED"])
            ennemy_info.append([pygame.mixer.Sound(file_path) for file_path in ennemy["BULLETS_SOUNDS"]])
            stats_bullets = []
            for i in range(len(ennemy["BULLETS_COOLDOWNS"])):
                stats_bullets.append([ennemy["BULLETS_SPEEDS"][i],
                                    ennemy["BULLETS_DEGATS"][i],
                                    ennemy["DISPERSIONS"][i],
                                    pygame.image.load(ennemy["DISPLAYS_BULLETS"][i]).convert_alpha(),
                                    ennemy["BULLETS_SIZES"][i],
                                    ennemy["BULLETS_CATEGORIES"][i]])
            ennemy_info.append(stats_bullets)
        else:
            ennemy_info.extend([[],[],[],[[]]])

        if "EFFECTS_COOLDOWNS" in ennemy:
            ennemy_info.append(ennemy["EFFECTS_COOLDOWNS"])
            stats_effects = []
            for i in range(len(ennemy["EFFECTS_COOLDOWNS"])):
                stats_effects.append([ennemy["EFFECTS_SIZES"][i],
                                      pygame.image.load(ennemy["EFFECTS_DISPLAYS"][i]).convert_alpha(),
                                      ennemy["EFFECTS_DEGATS"][i],
                                      ennemy["EFFECTS_TIME_FOR_ACTIVATION"][i],
                                      ennemy["EFFECTS_CATEGORIES"][i],
                                      pygame.mixer.Sound(ennemy["EFFECTS_SOUNDS"][i])])
            ennemy_info.append(stats_effects)
        else:
            ennemy_info.extend([[],[[]]])

        if "ENNEMIES_SPAWNS_COOLDOWNS" in ennemy:
            ennemy_info.append(ennemy["ENNEMIES_SPAWNS_COOLDOWNS"])
            ennemy_info.append(ennemy["NAMES_ENNEMIES"])

        ennemies[nom] = ennemy_info
    return ennemies

def extraction_waves(name_file:str) -> WAVES:
    """
    name_file: nom du fichier où sont contenus les infos des vagues. Format:json.
    Renvoie une liste de listes, rangés dans l'ordre de leur apparition.
    Chacune des listes de la liste contient le nom de tous les ennemis à faire apparaitre
    pour une vague.
    """
    with open(name_file, "r") as f:
        levels_info = json.load(f)
    levels_info.sort(key = lambda level_info:level_info["NUMERO"])
    levels = []
    for level_info in levels_info:
        levels.append([])
        for ennemy, number in level_info["ENNEMIES"].items():
            levels[-1].extend([ennemy]*number)
    return levels

def extraction_pickup(name_file:str) -> Tuple[PICKUPS,POIDS]:
    """
    name_file: nom du fichier où sont contenus les infos des pickups. Format:json.
    Renvoie deux listes, une avec les statistiques de chaque monstre,
    dans l'ordre du constructeur de PickUp. L'autre avec le poids de
    chaque pick.
    """
    with open(name_file, "r") as f:
        pickups_infos = json.load(f)

    poids = []
    pickups = []
    for pick_up in pickups_infos:
        poids.append(pick_up["POIDS"])
        pickups.append([pick_up["DUREE_EXISTANCE"],
                        pick_up["STATS_BUFF"],
                        pygame.image.load(pick_up["DISPLAY"]).convert_alpha()])
    return pickups,poids

def extraction_weapon(name_file:str) -> Tuple[Dict[str,ARME],ITEMS,List[str]]:
    """
    Extrait les infos relatives aux armes du fichier nom_fichier et les renvoie sous formes d'un triplet [ARMES,ITEMS,ARMES_DEBLOQUEES].
    Renvoie les armes dans un dicionnaire avec en clé, le nom de l'arme et en valeur les infos de l'arme.
    Voir la description de Weapon pour plus d'infos.
    Renvoie les ITEMS dans une liste d'items, ces items sont générés à partir des infos des weapons.
    Renvoie les armes débloquées dans une liste, ce sont les armes que Player a accès dès le début. 
    """
    with open(name_file, "r") as f:
        armes_infos = json.load(f)
    armes = {}
    items = []
    weapons_unlocked =[]
    for nom, arme_info in armes_infos.items():
        levels = []
        if arme_info["unlocked"] :
            weapons_unlocked.append(nom)
        if arme_info["category"] == "bullet":
            cooldown, sound, amount_fired, speed, degat, dispersion, display, size, type = [0,0,0,0,0,0,"",0,0]
            for level_info in arme_info["levels"]:
                if len(levels) == 0:
                    assert set(level_info.keys()) == set(["cooldown", "sound", "amount_fired", "speed", "degat",\
                                                         "dispersion", "display", "size", "type"]), f"Les clés de level_info pour le premier\
                                                         niveau de l'arme de type bullet devraient être:\
                                                         'cooldown', 'sound', 'amount_fired', 'speed', 'degat',\
                                                         'dispersion', 'display', 'size', 'type'. Ici elles sont {list(level_info.keys())}"
                cooldown = level_info.get("cooldown", cooldown)
                sound = level_info.get("sound", sound)
                amount_fired = level_info.get("amount_fired",amount_fired)
                speed = level_info.get("speed", speed)
                degat = level_info.get("degat", degat)
                dispersion = level_info.get("dispersion", dispersion)
                display = level_info.get("display", display)
                size = level_info.get("size", size)
                type = level_info.get("type", type)
                degat = level_info.get("degat", degat)
                levels.append({"cooldown": cooldown,
                                "sound": pygame.mixer.Sound(sound),
                                "amount_fired": amount_fired,
                                "stats": [speed, degat, dispersion, pygame.image.load(display).convert_alpha(), size, type]})
        elif arme_info["category"] == "effect":
            cooldown, size, display, degat, time_before_activation, type, sound = [0,0,"",0,0,0,0]
            for level_info in arme_info["levels"]:
                if len(levels) == 0:
                    assert set(level_info.keys()) == set(["cooldown", "size", "display", "degat", "time_before_activation",\
                                                         "type", "sound"]), f"Les clés de level_info pour le premier\
                                                         niveau de l'arme de type effect devraient être:\
                                                         'cooldown', 'size', 'display', 'degat', 'time_before_activation',\
                                                         'type', 'sound'. Ici elles sont {list(level_info.keys())}"
                cooldown = level_info.get("cooldown",cooldown)
                size = level_info.get("size",size)
                display = level_info.get("display",display)
                degat = level_info.get("degat",degat)
                time_before_activation = level_info.get("time_before_activation",time_before_activation)
                type = level_info.get("type",type)
                sound = level_info.get("sound",sound)
                levels.append( {"cooldown": cooldown,
                                "stats": [size, pygame.image.load(display).convert_alpha(), degat, time_before_activation, type, pygame.mixer.Sound(sound)]})
        else:
            assert False, f"Le type d'arme renseigné n'est pas valide, il devrait être bullet ou effet, ici il est {arme_info['type']}"
        armes[nom] = (arme_info["category"],levels)
        items.append(("weapon", nom, len(arme_info["levels"]), arme_info["prix"],pygame.image.load(arme_info["choix_display"])))
    return armes,items,weapons_unlocked

def extraction_items(name_file:str) -> Tuple[ITEMS, STATS_BUFFS]:
    """
    Renvoie les informations liées aux items extraites de name_file dans un tuple (items, stats_buffs)
    items: une liste contenant tous les items chacun représenté par une liste
        contenant dans l'ordre des arguments de shop_item, la valeur associé.
        Pour plus d'info, se référer à la documentationn de shop_item.
    stats_buffs: Pour les items de type buff, les stats sont stockées dans un dictionnaire
    avec en clé le nom de l'item et en valeur les stats, dans le même ordre que les arguments
    de buff. Pour plus d'info, se référer à la documentationn de buff.
    """
    with open(name_file, "r") as f:
        items_infos = json.load(f)
    items = []
    stats_buffs = {}
    for item_info in items_infos:
        assert set(["type","nom","availability","image","prix"]).issubset(item_info.keys()), f"item_info devrait au moins contenir les clés: 'type','nom','availability','image','prix', ici contient: {item_info.keys()}"
        assert set(item_info.keys()).issubset(set(["type","nom","availability","image","prix","stats"])), f"item_info devrait contenir en tous les clés: 'type', 'nom', 'availability', 'image', 'prix', 'stats', ici contient: {item_info.keys()}"
        items.append((item_info["type"],item_info["nom"],item_info["availability"],item_info["prix"],pygame.image.load(item_info["image"])))
        if item_info["type"] == "buff":
            assert "stats" in item_info, f"'stats' devrait être dans les clés de item_info, pour l'instant, item_info contient comme clé: {list(item_info.keys())}"
            stats = item_info["stats"]
            stats_buffs[item_info["nom"]] = stats["category"],stats["modifier"],stats["value"],stats["duree"]
    return items,stats_buffs

def extraction_data_choix_levels(environnements_paths:List[str]) -> List[Dict[str,Any]]:
    """
    environnements_paths: liste de chemin menant à la description de niveaux.
    Renvoie pour chaque chemin d'environnements_paths un dictionnaire:
        {"background": image à affiché lors du choix des environnements,
         "path": chemin menant aux données de l'environnement
    """
    datas = []
    for path in environnements_paths:
        datas.append(path)
    return datas

def extraction_data_item_shop_environnements(name_file:str) -> List[List[Any]]:
    """
    Renvoie une liste d'items pour le shop, chaque item étant un environnement.
    Pour plus d'infos, voir la classe de shop.
    """
    with open(name_file, "r") as f:
        environnements_infos = json.load(f)
    environnements = []
    for environnement_info in environnements_infos:
        environnements.append(("environment",environnement_info["nom"],1, environnement_info["prix"], pygame.image.load(environnement_info["image"])))
    return environnements