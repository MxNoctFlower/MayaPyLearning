from maya import cmds

SUFFIX = {
    "mesh":"geo",
    "joint":"jnt",
    "directionalLight":"dlgt",
    "camera": None
}
DEFAULT = "grp"
def RenameObj(selection=False):
    """
    This function is used to rename objects in a project.

    Args:
        selection - input if the current selection should be used or not
    Returns:
        A list of objects that were changed 
    """
    #Get selected item. If there is no selected item, then show all items
    items = cmds.ls(selection = selection, dag = True, long = True)

    if selection and not items:
        raise RuntimeError("There are no items selected!")
    items.sort(key = len)

    #Go through each item in selection list
    for item in items:
        shortName = item.split("|")[-1]

        #Get item and their children. If there is no item, get "|"
        children = cmds.listRelatives(item, children = True, fullPath = True) or []
        #If there is one item, get object type of that item. Else, get object type of item
        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(item)

        #Depending on objType, create a specified suffix
        suffix = SUFFIX.get(objType, DEFAULT)

        if not suffix:
            continue
        if item.endswith(suffix):
            continue

        #Create new name and replace object name with new name
        newName = "%s_%s" % (shortName, suffix)
        cmds.rename(item, newName)

        i = items.index(item)
        items[i] = item.replace(shortName, newName)

    return items
