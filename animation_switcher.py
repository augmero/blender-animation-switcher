import bpy

bl_info = {
    "name": "augmero - animation switcher",
    "description": "switches actions and alembics",
    "author": "augmero",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "tracker_url": "https://twitter.com/augmero_nsfw",
    "support": "TESTING",
    "category": "Import-Export",
}

# NOTES, READ BEFORE RUNNING THIS
# I use this for my workflow to switch between multiple animations (actions and alembic caches) in the same blender file
# It works based off of naming conventions and isn't super user friendly

# Possible causes for errors:
#   typos, actions or alembics not made before hand

# Important things to enter in:
# suffix for the action

# Naming convention:
# All alembic files and actions should be based exactly off of their corresponding object name, and include the suffix you set

# Example action to change:
# Script suffix: _002
# Object name: "m blink driver"
# Action name: "m blink driverAction_001"
# Action name after script: "m blink driverAction_002"

# Example alembic to change:
# Script suffix: _002
# Object name: "mercy_torso bind"
# Note: all of my alembic cache objects have " bind" at the end of their name, which the script does take into account
# Current filepath: "//zva caches/mercy_torso_001.abc"
# New filepath: "//zva caches/mercy_torso_002.abc"

# This takes some set up before the script will work
# Need to make the actions and alembics before hand with proper naming convention, script doesn't handle that part yet

# Code assumes that the action name will be "{{object name}}"+"{{suffix}}"
# This is the number of the animation to switch to.
suffix = "_002"
cacheFilePath = "//zva caches/"

# Include these collections to make changes, exclude when done
# The animation_switcher collection has the action_switch and alembic_switch collections inside it
# These aren't the main collections for any objects but I link specific objects I want to be able to switch inside them
involved_collections = [
    "animation_switcher",
    "action_switch",
    "alembic_switch",
]


vl_collections = bpy.context.scene.view_layers["View Layer"].layer_collection


def exclude_collection_view_layer(pCollection, name, exclude):
    for collection in pCollection.children:
        if collection.name.lower() == name.lower():
            print("COLLECTION | " + name + " | FOUND, setting exclude to " + str(exclude))
            collection.exclude = exclude
        elif collection.children:
            exclude_collection_view_layer(collection, name, exclude)


def retrieve_collection(pCollection, collectionName):
    print("Searching for collection " + collectionName)
    for collection in pCollection.children:
        if collection.name.lower() == collectionName.lower():
            print("COLLECTION | " + collectionName + " | FOUND, returning ")
            return collection
        elif collection.children:
            return retrieve_collection(collection, collectionName)


def switch_actions(collectionName, suffix):
    print("SWITCHING ACTIONS TO " + suffix)
    action_collection = retrieve_collection(vl_collections, collectionName).collection
    for obj in action_collection.objects:
        print(obj.name)
        actionName = obj.name+"Action"+suffix
        action = bpy.data.actions[actionName]
        obj.animation_data.action = action


def switch_alembics(collectionName, suffix):
    print("SWITCHING ALEMBICS TO " + suffix)
    alembic_collection = retrieve_collection(vl_collections, collectionName).collection
    for obj in alembic_collection.objects:
        print(obj.name)
        for mod in obj.modifiers:
            print(mod.type)
            if mod.type == "MESH_SEQUENCE_CACHE":
                print("Current filepath: " + mod.cache_file.filepath)
                mod.cache_file.filepath = cacheFilePath + obj.name.split(' ')[0] + suffix + ".abc"
                print("New filepath: " + mod.cache_file.filepath)


# Make sure the involved collections are all included
for collection in involved_collections:
    exclude_collection_view_layer(vl_collections, collection, False)

switch_actions("action_switch", suffix)

switch_alembics("alembic_switch", suffix)

# Can now exclude the involved collections
for collection in involved_collections:
    exclude_collection_view_layer(vl_collections, collection, True)
