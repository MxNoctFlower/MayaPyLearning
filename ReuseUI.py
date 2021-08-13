from maya import cmds
from AniTweenerUI import betwixt
from MakeGearClass import Gear

class Window(object):
    """
    A class used to create a basic window on the screen
    """

    name = "Window"

    #Makes a window aappear on the screen
    def appear(self):
        #Allows only one window of this type to appear on the screen
        if cmds.window(self.name, query = True, exists = True):
            cmds.deleteUI(self.name)
        cmds.window(self.name)
        self.makeup()
        cmds.showWindow()

    #The contents inside the window
    def makeup(self):
        pass

    #What happens when "Reset" is clicked
    def reset(self, *args): pass
    #What happens when "Close" is clicked
    def close(self, *args): cmds.deleteUI(self.name)

class BetwixtWindow(Window):
    """
    Window for the in-betweener functions
    """
    #The contents inside the window
    def makeup(self):
        col = cmds.columnLayout()
        cmds.text(label="Choose how much you want to tween your animation")

        row = cmds.rowLayout(numberOfColumns = 2)
        #Creating the slider and connect it to the "betwixt" function
        self.scale = cmds.floatSlider(min = 0, max = 35, value = 10, step = 1, changeCommand = betwixt)
        #Creating the "Reset" function
        cmds.button(label = "Reset", command = self.reset)

        #Setting the Parent to columns so that the "Close" button can go under the slider
        cmds.setParent(col)
        cmds.button(label = "Close", command = self.close)

    def reset(self, *args): cmds.floatSlider(self.scale, edit = True, value = 10)
    def close(self, *args): cmds.deleteUI(self.name)

class GearWindow(Window):
    """"
    Window for the Gear functions
    """

    def __init__(self):
        self.gear = None

    def makeup(self):

        col = cmds.columnLayout()
        cmds.text(label = "Slide to adjust the gear.")

        row = cmds.rowLayout(numberOfColumns = 4)
        cmds.text(label="Teeth:")
        #Creating a box to enter the number of teeth
        self.scale = cmds.intField( changeCommand = self.UpdateGear)
        #Button will create a gear
        cmds.button(label = "Make Gear", command = self.SpawnGear)
        cmds.button(label = "Reset", command = self.reset)

        cmds.setParent(col)
        cmds.button(label = "Close", command = self.close)

    #Connecting to the "ModifyTeeth" function in the Gear class
    def UpdateGear(self, teeth):
        if self.gear:
            self.gear.ModifyTeeth(teeth=teeth)
        #cmds.text(self.tag, edit = True, label = teeth)

    #Connecting to the "makeGear" function in the Gear class
    def SpawnGear(self, *args):
        teeth = cmds.intField(self.scale, query=True, value=True)

        self.gear = Gear()
        self.gear.makeGear(teeth=teeth)

    #Resetting the slider and the text
    def reset(self, *args):
        self.gear = None
        cmds.intField(self.scale, edit = True, value = 0)


