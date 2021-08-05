from maya import cmds

class Gear:
    """
    This class is used to create and modify a model machine gear
    """
    def __init__(self):
        #Setting default values
        self.transform = None
        self.constructor = None
        self.extrude = None

    def makeGear(self,teeth=10, length=0.3):
        """
        This function is used to make a gear with user-defined parameters
        Args:
            teeth: The amount of teeth on the gear
            length: The length of each tooth on the gear
        """
        #Since teeth are every other face, we need to multiple the number of teeth by 2.
        spread = teeth * 2

        #Create polyPipe with "spread" subdivisions.
        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis = spread)

        #Finding the indexes of the faces we want to extrude.
        sides = range(spread*2, spread*3, 2)

        cmds.select(clear = True)
        #Selecting the faces we want to extrude
        for side in sides:
            cmds.select('%s.f[%s]' % (self.transform,side), add = True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ = length)[0]

    def ModifyTeeth(self, teeth=10, length=0.3):
        """
        This function modifies the number and length of teeth
        Args:
            teeth: The new amount of teeth on the gear
            length: The new length for each tooth
        """
        spread = teeth * 2

        #Selecting gear, giving permission to edit, and adding the new number of faces
        cmds.polyPipe(self.constructor, edit = True, subdivisionsAxis = spread)

        sides = range(spread*2, spread*3, 2)
        #Creating a list of names of sides we want to extrude
        sideNames = []

        #Getting and creating names
        for side in sides:
            sideName = 'f[%s]' % side
            sideNames.append(sideName)

        #Changing number of teeth
        cmds.setAttr('%s.inputComponents' % (self.extrude), len(sideNames), *sideNames, type='componentList')
        #Changing length of teeth
        cmds.polyExtrudeFacet(self.extrude, edit = True, localTranslateZ = length)

