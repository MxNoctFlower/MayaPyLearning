from maya import cmds

def betwixt(percent, item=None, attrs=None, selection=True):
    """
    Used to create in-betweeners for an animation by a weighted percentage(controlling ease-ins and ease-outs)
    Args:
        percent: The percentage the user wants to weight the in-betweener
        item: object that is being animated
        attrs: attributes of the object
        selection: Sees if an object is selected or not
    """

    #Checking for errors and filling in parameters
    if not item and not selection:
        raise ValueError('There is nothing to tween!')
    if not item:
        item = cmds.ls(selection = True)[0]
    if not attrs:
        attrs = cmds.listAttr(item, keyable = True)

    #Getting current time on frame timeline
    ctime = cmds.currentTime(query = True)

    #We need a for loop so that each attribute can move along with the item
    for attr in attrs:
        #Creating attribute names
        attrName = '%s.%s' % (item, attr)
        #Getting keyframes for each attribute
        kfs = cmds.keyframe(attrName, query = True)
        #Skip attribute if it has no keyframes
        if not kfs:
            continue
        #Get previous keyframes set before current time
        pkfs = [key for key in kfs if key < ctime]
        #Get later keyframes set after current time
        lkfs = [key for key in kfs if key > ctime]
        if not pkfs and not lkfs:
            continue

        #Get the nearest previous frame and the nearest new frame from the lists
        if pkfs:
            pf = max(pkfs)
        else:
            pf = None

        if lkfs:
            nf = min(lkfs)
        else:
            nf = None

        if not pf or not nf: continue

        #Get values at previous value and new value
        pvalue = cmds.getAttr(attrName, time = pf)
        nvalue = cmds.getAttr(attrName, time = nf)

        #Calculating the current value using the percentage given
        gap = nvalue - pvalue
        weightedgap = (gap * percent)/100.0
        cvalue = weightedgap + pvalue

        #Setting new in-betweener on each attribute that has keyframes in item
        cmds.setKeyframe(attrName, time = ctime, value = cvalue)
