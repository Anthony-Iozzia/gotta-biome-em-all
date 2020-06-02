import os
import json
import sys

overworld_biomes_list = ["badlands", "badlands_plateau", "bamboo_jungle",
                         "bamboo_jungle_hills", "beach", "birch_forest",
                         "birch_forest_hills", "cold_ocean", "dark_forest",
                         "deep_cold_ocean", "deep_frozen_ocean",
                         "deep_lukewarm_ocean", "desert", "desert_hills",
                         "forest", "frozen_river", "giant_tree_taiga",
                         "giant_tree_taiga_hills", "jungle", "jungle_edge",
                         "jungle_hills", "lukewarm_ocean", "mountains",
                         "mushroom_field_shore", "mushroom_fields", "plains",
                         "river", "savanna", "savanna_plateau", "snowy_beach",
                         "snowy_mountains", "snowy_taiga", "snowy_taiga_hills",
                         "snowy_tundra", "stone_shore", "swamp", "taiga",
                         "taiga_hills", "warm_ocean", "wooded_badlands_plateau",
                         "wooded_hills", "wooded_mountains"]

nether_biomes_list = ["nether_wastes", "warped_forest", "crimson_forest",
                      "soul_sand_valley", "basalt_deltas"]


def extract_uuid(file_name):
    pieces = file_name.split(".")
    return pieces[0]


def choose_file_or_dir(path):
    dict_elems = {}
    position = 0
    elements_list = os.listdir(path)
    if len(elements_list) == 1:
        return elements_list[0]
    else:
        for element in elements_list:
            position += 1
            dict_elems[str(position)] = element
            if os.path.isfile(path + element):
                element = extract_uuid(element)
            print("[" + str(position) + "] " + element)
        print("> ", end="")
        choice = input()
        if(choice == ""):
            choice = "1"
        choice = choice.strip()
        return dict_elems[choice]


def print_list_indented(lst):
    for elem in lst:
        print("  " + elem)


def display_infos(dimension_name, biomes_list, advancement_name, advancement_title, data):
    if advancement_name in data:
        print()
        print("_________ " + dimension_name + " _________")
        advancement_json = data[advancement_name]
        biomes_found_list = []
        for biome in advancement_json["criteria"]:
            pieces = biome.split(":")
            biome = pieces[1]
            if biome in biomes_list:
                biomes_found_list.append(biome)
            else:
                print("Error: the biome " + biome +
                      " was not found. It could mean that this program is not up to date. Please inform the developer.")

        biomes_missing_list = set(biomes_list) - set(biomes_found_list)

        nb_biomes_found = len(biomes_found_list)
        nb_biomes_missing = len(biomes_missing_list)
        nb_biomes_total = len(biomes_list)

        if nb_biomes_found > 0:
            print("You have already discovered these " +
                  str(nb_biomes_found) + " biomes:")
            print_list_indented(biomes_found_list)

        if(nb_biomes_missing > 0):
            if nb_biomes_found > 0:
                print()
            print("You do not have discovered these " +
                  str(nb_biomes_missing) + " biomes:")
            print_list_indented(biomes_missing_list)

        percentage = (nb_biomes_found / nb_biomes_total) * 100
        percentage = int(round(percentage))
        print()
        print("Biomes discovered: " + str(nb_biomes_found) + "/" +
              str(nb_biomes_total) + " (" + str(percentage) + "%)")

        advancement_done_msg = "The advancement \"" + advancement_title + "\" is "
        if not advancement_json["done"]:
            advancement_done_msg += "not "
        advancement_done_msg += "done."
        print(advancement_done_msg)

        if advancement_json["done"]:
            print("Congratulations!")


# Choose Minecraft installation path
print("Enter the path to your Minecraft installation folder (enter nothing for the default path): ", end="")
path = input()
if path == "nothing":
    print("Are you happy about your joke? Now, go find your biomes, you little clown :~D")
    path = ""
if path == "":
    path = os.path.expanduser('~') + "/AppData/Roaming/.minecraft/"
else:
    path = path.strip(' "/\\')
    path = path + "/"

path += "saves/"

# Choose world
elements_list = os.listdir(path)
if len(elements_list) < 1:
    print("No world found! Please create a world.")
    sys.exit()
print()
if len(elements_list) > 1:
    print("The following worlds were found, please choose one (enter the associated number):")

world_name = choose_file_or_dir(path)
path += world_name + "/"
print("Selected world: " + world_name)

path += "advancements/"

# Choose player
elements_list = os.listdir(path)
if len(elements_list) < 1:
    print("No player found! Please join your world first.")
    sys.exit()
print()
if len(elements_list) > 1:
    print("The following player UUIDs were found, please choose one (you can find your UUID on namemc.com):")

uuid_json = choose_file_or_dir(path)
path += uuid_json
print("Selected player: " + extract_uuid(uuid_json))

# Read json and display informations
with open(path) as json_file:
    data = json.load(json_file)
    display_infos("Overworld", overworld_biomes_list,
                  "minecraft:adventure/adventuring_time", "Adventuring Time", data)

    display_infos("Nether", nether_biomes_list,
                  "minecraft:nether/explore_nether", "Hot Tourist Destinations", data)
