import pygame as pg

#set up a button class
class Button:
    # set up the constructor for the button class
    def __init__(self,surface,pos,size,colour = (155,155,155,255),textColour = (255,255,255,255)):
        self.surface = surface
        self.position = pos
        self.size = size
        self.colour = colour
        self.borderColour = (0,0,0,255,255)
        self.text = ""
        self.textColour = textColour
        self.textSize = 20
        self.image = pg.Surface((self.size[0],self.size[1]),pg.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (self.position[0],self.position[1]))
        
    # set up the render function for the button class
    def render(self):
        

        self.renderGraphics()

        
        
        if self.text != "":
            font = pg.font.SysFont("Arial",self.textSize)
            text = font.render(self.text,1,self.textColour)
            self.image.blit(text,(self.size[0]/2 - text.get_width()/2,self.size[1]/2 - text.get_height()/2))

        self.surface.blit(self.image,(self.position[0],self.position[1]))

    def renderGraphics(self):
        pg.draw.rect(self.image,self.colour,(0,0,self.size[0],self.size[1]))
        pg.draw.rect(self.image,self.borderColour,(0,0,self.size[0],self.size[1]),3)
        
        
    
    def eventHandler(self):
        pass
    def onClick(self):
        pass

    def onHover(self):
        pass

    def onLeave(self):
        pass

   
    def onTrigger(self):
        pass

    def onTriggerExit(self):
        pass

  
    def onEnable(self):
        pass

    def onDisable(self):
        pass

   





class MenuButton(Button):
    # set up the constructor for the button class for menu buttons
    def __init__(self,surface,pos,size,text,redirect):
        super().__init__(surface,pos,size,(51,102,0,255),(255,255,255,255))
        self.text = text
        self.colour = (51,102,0,255)
        self.borderColour = (76,153,0,255)
        self.redirect = redirect

        
    def eventHandler(self,info):
        # if the mouse is in the button, then run the onHover function
        if self.rect.collidepoint((info["mouse"])):
            self.onHover()
            for event in info["events"]:
                # if the mouse is clicked and the mouse is in the button, then run the onClick function
                
                match event.type:
                    case pg.MOUSEBUTTONDOWN:
                        return self.onClick()
        else:
            self.onLeave()
     
        
    def onClick(self):
        
        return self.redirect
    
    
    
    def onHover(self):
        self.borderColour = (255,255,255,255)
    
    def onLeave(self):
        self.borderColour = (76,153,0,255)





    

class InputButton(Button):
    def __init__(self,surface,pos,size):
        super().__init__(surface,pos,size,(0,0,0,150))
        self.borderColour = (0,0,0,150)
        self.trigger = False
        
    def eventHandler(self,info):
            for event in info["events"]:
                match event.type:
                    case pg.MOUSEBUTTONDOWN:
                        # if the mouse is clicked and the mouse is in the button, then run the onClick function
                        #if mouse click and mouseposition in rect
                        self.onClick(info)

                    case pg.KEYDOWN:
                        if self.trigger:
                            # if the key is backspace, then remove the last character from the text
                            if event.key == pg.K_RETURN:
                                # if the key is enter, then run the onTriggerExit function
                                self.trigger = False
                                self.onTriggerExit()
                            elif event.key == pg.K_BACKSPACE:
                                self.text = self.text[:-1]
                            else:
                                self.text += event.unicode

    def onClick(self,info):
        # if the mouse is in the button, then run the onHover function
        if self.rect.collidepoint(info["mouse"]):
             if self.trigger == False:
                self.trigger = True
                self.onTrigger()
        else:
            if self.trigger:
                self.trigger = False
                self.onTriggerExit()


    def onTrigger(self):
        self.borderColour = (255,255,255,255)
        self.textColour = (255,255,255,255)
    
    def onTriggerExit(self):
        self.borderColour = (0,0,0,150)
        self.textColour = (128,128,128,255)

  



#make a drop down button, which is a button that when clicked, opens a dropdown menu, where option from a list are displayed. If the user clicks on one of the options, the button text is changed to the option that was clicked
class DropdownButton(Button):
    def __init__(self,surface,pos,size,optionList):
        super().__init__(surface,pos,size,(128,128,128,255))
        self.borderColour = (0,0,0,150)
        self.alternateColour = (180,180,180,255)
        self.trigger = False
        
        self.selectedOption = self.optionList[0]
        self.textColour = (128,128,128,255)
        self.textSize = 20
        self.optionButtons = {}
        for i in optionList:
            self.optionButtons[i] = MenuButton(self.surface,(self.position[0],self.position[1]+self.get),(self.size[0],self.size[1]),i,str(i))
    
    def eventHandler(self,info):

        if self.rect.collidepoint((info["mouse"])):
            self.onHover()
            for event in info["events"]:
                
                match event.type:
                    case pg.MOUSEBUTTONDOWN:
                        if self.trigger:
                            for i in self.optionButtons:
                                option = self.optionButtons[i].eventHandler(info)
                                if option != None:
                                    #swap places of selected option and option
                                    
                                    self.onClick()
        else:
            self.onLeave()
        
    def onClick(self):
        if self.trigger == False:
            self.trigger = True
            self.onTrigger()
        else:
            self.trigger = False
            self.onTriggerExit()
    

  






class ListButton(Button):
    # set up the constructor for the button class for list buttons
    def __init__(self,surface,pos,size,list):
        super().__init__(surface,pos,size,(150,150,150,255))
        self.borderColour = (0,0,0,150)
        self.list = {}
        self.itemSelected = "None"
        for i in list:
            self.list[i] = ListItemButton(self.surface,(self.position[0],self.position[1]+(list.index(i)*25)),(self.size[0],25),i)
        

        
        # list buttons contain a list of buttons, which are the items in the list, typically the names of players


        self.textColour = (255,255,255,255)
        self.textSize = 9
    
    def eventHandler(self,info,lists):
        try:
            for i in self.list:
                checker = self.list[i].eventHandler(info,lists)
                
                
                
                if checker != None:
                    self.itemSelected = checker
        except:
            pass
            
            
            
            

        
    def render(self):
        self.image.fill((128,128,128,128))
        #draw the text in the list
        self.surface.blit(self.image,(self.position[0],self.position[1]))
        for i in self.list:
            self.list[i].render()
        
        

    def updateItems(self,newList):
        # if the list of items has changed, then update the list of buttons
        
        if list(newList.keys()) != list(self.list.keys()):
            
            self.list = {}
            
            
            
            for player in newList:
                self.list[player] = ListItemButton(self.surface,(self.position[0],self.position[1]+(list(newList.keys()).index(player)*25)),(self.size[0],25),player)
        
        for index, item in enumerate(self.list):
            self.list[item].position = (self.position[0],self.position[1]+(index*self.list[item].size[1]))
            self.list[item].rect = self.list[item].image.get_rect(topleft = (self.list[item].position[0],self.list[item].position[1]))
    def removeItem(self,item):
        # if the item is in the list, then remove it
        if item in self.list:
            self.list.pop(item)
    
    def addItem(self,item):
        # if the item is not in the list, then add it
        if item not in self.list:
            self.list[item] = ListItemButton(self.surface,(self.position[0],self.position[1]+(len(self.list)*25)),(self.size[0],25),item)
    
    def transferItem(self,item,destinationList):
        # if the item is in the list, then remove it and add it to the destination list
        if item in self.list:
            self.removeItem(item)
            destinationList.addItem(item)
    
    def clearList(self):
        self.list = []

#when an item in the list is clicked, the trigger is on, and the item can move to another list that is clicked on


class ListItemButton(Button):
    # set up the constructor for the button class for list buttons
    def __init__(self,surface,pos,size,text):
        super().__init__(surface,pos,size,(180,180,180,255))
        self.text = text
        self.trigger = False

    def eventHandler(self,info,lists):
        # if the trigger is on, then the item can be moved to another list
        if self.trigger == False:
            if self.rect.collidepoint((info["mouse"])):
                
                self.onHover()
            else:
                self.onLeave()

        for event in info["events"]:
            match event.type:
                case pg.MOUSEBUTTONDOWN:
                        
                    if self.rect.collidepoint(info["mouse"]):
                        return self.onClick(info,lists)
                            
                    else:
                         #if the trigger is on, and the mouse is not on the current list and also not in blank space, then the item is transferred from its list and moved to the list that the mouse is on
                        if self.trigger:
                            for i in lists:
                                if self.text in lists[i].list:
                                    parentList = lists[i]
                            for i in lists:
                                if lists[i].rect.collidepoint(info["mouse"]):
                                    if lists[i] != parentList:
                                        parentList.transferItem(self.text,lists[i])
                                        self.trigger = False
                                        self.onTriggerExit()
                                        return "None"
                                    else:
                                        self.trigger = False
                                        self.onTriggerExit()
                                        return "None"
                                        
                                        
        

                    

    def onClick(self,info,lists):
        #lists is a dictionary with references to all the lists
        if self.rect.collidepoint(info["mouse"]):
             if self.trigger == False:
                self.trigger = True
                return self.onTrigger()
                
        
        else:
            if self.trigger:
                self.trigger = False
                return self.onTriggerExit()
        


    def onTrigger(self):
        self.colour = (200,200,200,255)
        return self.text

       
    
    def onTriggerExit(self):
        self.colour = (180,180,180,255)
        return "None"

    def render(self):
        self.image.fill(self.colour)
        #draw the text in the list
        font = pg.font.SysFont("Arial",self.textSize)
        text = font.render(self.text,1,self.textColour)
        self.image.blit(text,(0,0))
        
        self.surface.blit(self.image,(self.position[0],self.position[1]))
        
    
    def onHover(self):
        self.colour = (255,150,200,255)
        

    def onLeave(self):
        self.colour = (180,180,180,255)
       

        
    

class InfoButton(Button):
    # this  button can display information given to it
    def __init__(self,surface,pos,size,info):
        super().__init__(surface,pos,size,(100,100,100,255))
        self.info = info
        self.textColour = (255,255,255,255)
        self.textSize = int(size[1])
        self.size = size
        self.position = pos

    def render(self):
        self.image.fill(self.colour)
        #draw the info text
        if self.info != "":
            font = pg.font.SysFont("Arial",self.textSize)
            text = font.render(str(self.info),1,self.textColour)
            pg.transform.scale(self.image,(int(text.get_width())+5,int(text.get_height())+5))
            self.image.blit(text,(0,0))
            
    
        self.surface.blit(self.image,(self.position[0],self.position[1]))




