import app, chr, event, game, item, ui, sys
import LHXqEMnOOK as player, FIxdSoEL as net, teIqUKj as chat, QNZB as shop

# If set to `True` in-game chat logs will show-up
IS_DEBUG_MODE = False

# Cat Bite Knife +0
DAGGER_VID = 1040
# We assume the player has the maximum inventory slots unlocked (GF -> 4 * 45), for good measure
MAX_INVENTORY_SIZE = 180

"""
Hooking module.
"""
CURRENT_PHASE = 5
phaseCallbacks = {}
GAME_WINDOW = 0

class Hook():
	"""
	Hook class that allows to replace functions in modules.
	"""
	def __init__(self,toHookFunc,replaceFunc):
		self.originalFunc = toHookFunc
		self.replaceFunc = replaceFunc
		self.functionName = str(toHookFunc.__name__)
		self.functionOwner = self.GetFunctionOwner(toHookFunc)
		self.isHooked = False

	def GetFunctionOwner(self,func):
		"""
		Return the object owner of the function 

		Args:
			func ([function]): a function.

		Returns:
			[object]: Return the object owner of the function.
		"""
		try:
			# In case of a class function
			owner = func.im_class		
		except AttributeError:
			owner = sys.modules[func.__module__]
		
		return owner


	def CallOriginalFunction(self,*args,**kwargs):
		"""
		Call the original function before the hook.
		Returns:
			[args]: the arguments of the function.
		"""
		def run(*args, **kwargs):
			return self.originalFunc(*args, **kwargs)
		return run(*args,**kwargs)
		
	def HookFunction(self):
		"""
		Hook the function.
		"""
		if self.isHooked:
			return
		self.isHooked = True
		setattr(self.functionOwner, self.functionName, self.replaceFunc)

	def UnhookFunction(self):
		"""
		Remove the hook and put the original function.
		"""
		if self.isHooked == False:
			return
		self.isHooked = False
		setattr(self.functionOwner, self.functionName, self.originalFunc)

def skipFunc(*args):
	"""
	Function that doesn nothing.
	"""
	pass 

def phaseIntercept(*args,**kwargs):
	#printFuncNC(*args,**kwargs)
	global CURRENT_PHASE
	if len(args)>1 and args[1] != 0:
		CURRENT_PHASE = args[0]
	for callback_id in phaseCallbacks:
		callback = phaseCallbacks[callback_id]
		if callable(callback):
			callback(CURRENT_PHASE,args[1])
	phaseHook.CallOriginalFunction(*args,**kwargs)

def registerPhaseCallback(id,func):
	phaseCallbacks[id] = func

def deletePhaseCallback(id):
	if id in phaseCallbacks:
		del phaseCallbacks[id]

class SkipHook(Hook):
	def __init__(self,toHookFunc):
		Hook.__init__(self,toHookFunc,skipFunc)

def CheckAffectIntercept(*args,**kwargs):
    checkAffectHook.CallOriginalFunction(*args, **kwargs)

debugFunc = 0
questHook = SkipHook(game.GameWindow.OpenQuestWindow)
phaseHook = Hook(net.SetPhaseWindow,phaseIntercept)
checkAffectHook = Hook(item.CheckAffect, CheckAffectIntercept)

def GetQuestHookObject():
	return questHook

def GetCurrentPhase():
	global CURRENT_PHASE
	return CURRENT_PHASE

def GetGameWindow():
	global GAME_WINDOW
	return GAME_WINDOW

def printFunc(*args,**kwargs):
	"""
	Print the arguments of a function to a debug.txt file.(In the game folder)
	"""
	with open("debug.txt","a") as f:
		f.write("[DebugHook] Function called arguments:\n")
		for i,arg in enumerate(args):
			f.write("[DebugHook] Arg "+ str(i) + ": "+ str(arg)+"\n")
		f.write("\n")
	debugFunc.CallOriginalFunction(*args,**kwargs)

def printFuncNC(*args,**kwargs):
	"""
	Print the arguments of a function to a debug.txt file.(In the game folder)
	This happens without Calling the Original.
	"""
	with open("debug.txt","a") as f:
		f.write("[DebugHook] Function called arguments:\n")
		for i,arg in enumerate(args):
			f.write("[DebugHook] Arg "+ str(i) + ": "+ str(arg)+"\n")
		f.write("\n")

#Print arguments of a function
def _debugHookFunctionArgs(func):
	global debugFunc
	debugFunc = Hook(func,printFunc)
	debugFunc.HookFunction()

def _debugUnhookFunctionArgs():
	debugFunc.UnhookFunction()

phaseHook.HookFunction()
checkAffectHook.HookFunction()

# Log messages in the game chat
def log_message(message):
    chat.AppendChat(chat.CHAT_TYPE_INFO, message)

# Returns the inventory slot index of first item found that matches the specified `itemVID`.
def GetItemByID(itemVID):
	for i in range(0, MAX_INVENTORY_SIZE):
		if player.GetItemIndex(i) == itemVID:
			return i
	return -1

"""
Selects NPC dialog answers. If hook=True will avoid quest answers from showing on screen, the caller is then resposible for removing the hook afterwards by calling UnhookFunction.

Args:
event_answers ([list]): A list containing the answers index.
hook ([boolean]): If `true` will hook quest answers in order to not show it on screen.
"""
def skipAnswers(event_answers, hook=False):
	if hook:
		questHook.HookFunction()
	for index,answer in enumerate(event_answers,start=1):
		event.SelectAnswer(index,answer)

class ScriptManager(ui.ScriptWindow):
    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.function_sleep_time = None
        self.hook_unhook_time = None
        self.running = False
        self.prev_count = None
        self.targetVID = None
        self.isShowing = 1

        # New variables for toggle buttons
        self.is_giving_on = False   # Indicates if the giving items bot is running
        self.is_buying_on = False   # Indicates if the buying items bot is running

        # Create a window for the bot menu
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetTitleName('uBot')
        self.Board.SetSize(100, 130)
        self.Board.SetPosition(3, 120)
        self.Board.AddFlag('movable')
        self.Board.SetCloseEvent(self.OnClose)
        self.Board.Show()

        # Create a component helper for UI elements
        self.comp = Components()

        self.openBotButton = self.comp.Button(self.Board, 'Open', None, 28, 37, self.OnToggle)
        self.openBotButton.Hide()

        # # Toggle button for giving items to the Alchemist
        self.givingToggleButton = self.comp.ToggleButton(self.Board, 'Give', 'Give Items to Alchemist', 28, 37, self.StopGiving, self.StartGiving)

        # Toggle button for buying items
        self.buyingToggleButton = self.comp.ToggleButton(self.Board, 'Buy', 'Buy Items from Weapons Store', 28, 67, self.StopBuying, self.StartBuying)

        # Button for "Guild" functionality
        self.guildButton = self.comp.Button(self.Board, 'Guild', 'Coming Soon', 28, 97, self.GuildFunction)

    def OnClose(self):
        if self.is_giving_on:
            self.StopGiving()
        elif self.is_buying_on:
            self.StopBuying()
        self.Board.Hide()

    def OnToggle(self):
        if self.isShowing == 1:
            if self.is_giving_on:
                self.StopGiving()
            elif self.is_buying_on:
                self.StopBuying()
            self.isShowing = 0
            self.openBotButton.Show()
            self.givingToggleButton.Hide()
            self.buyingToggleButton.Hide()
            self.guildButton.Hide()
            self.Board.SetSize(100, 72)
        else:
            self.isShowing = 1
            self.openBotButton.Hide()
            self.givingToggleButton.Show()
            self.buyingToggleButton.Show()
            self.guildButton.Show()
            self.Board.SetSize(100, 130)

    def __del__(self):
        ui.ScriptWindow.__del__(self)

    # --- New Methods for Giving Items Bot ---

    def StartGiving(self):
        self.is_giving_on = True
        if IS_DEBUG_MODE:
            log_message("Started giving items.")
        self.targetVID = player.GetTargetVID()  # Get the Alchemist VID
        if self.targetVID == 0:
            log_message("Please select the Alchemist NPC.")
            self.StopGiving()
            return
        if IS_DEBUG_MODE:
            log_message("Alchemist VID: %s." % self.targetVID)
        self.prev_count = None
        self.running = True  # Start the OnUpdate loop
        self.RunScript()

    def StopGiving(self):
        self.is_giving_on = False
        self.givingToggleButton.SetUp()
        if IS_DEBUG_MODE:
            log_message("Stopped giving items.")
        # If neither bot is running, stop the OnUpdate loop
        if not self.is_buying_on:
            self.running = False

    # --- New Methods for Buying Items Bot ---

    def StartBuying(self):
        self.is_buying_on = True
        if IS_DEBUG_MODE:
            log_message("Started buying items.")
        self.running = True  # Start the OnUpdate loop
        self.RunScript()

    def StopBuying(self):
        self.is_buying_on = False
        self.buyingToggleButton.SetUp()
        if IS_DEBUG_MODE:
            log_message("Stopped buying items.")
        # If neither bot is running, stop the OnUpdate loop
        if not self.is_giving_on:
            self.running = False

    # --- Method for Guild Button ---

    def GuildFunction(self):
        log_message("Guild Attendence and Donation coming soon.")

    # --- Modified RunScript Method ---

    def RunScript(self):
        current_time = app.GetGlobalTimeStamp()
        playerLevel = player.GetStatus(player.LEVEL)

        if self.is_giving_on:
            # --- Giving Items Logic ---
            if self.prev_count is not None:
                # Check if item count decreased
                current_count = player.GetItemCountByVnum(DAGGER_VID)
                if IS_DEBUG_MODE:
                    log_message("%s items left after run delay." % current_count)

                if (playerLevel < 35):
                    log_message("Cannot give items if your level is under 35. Your level is: %s." % playerLevel)
                    return # Exit early if level under 35

                if current_count == self.prev_count:
                    # Count did not decrease, need to unblock NPC
                    if IS_DEBUG_MODE:
                        log_message("Item was not accepted, talking to NPC to sort things out.")

                    net.SendOnClickPacket(self.targetVID)
                    # Talking to NPC about Energy Fragment production
                    skipAnswers([4, 254, 254, 0], True)
                    self.hook_unhook_time = current_time + 1  # Schedule unhooking after 1 second
                    self.function_sleep_time = current_time + 1.5  # Set delay before re-running script
                    return  # Exit to wait for next OnUpdate
                else:
                    # Count decreased, item was accepted
                    if IS_DEBUG_MODE:
                        log_message("Item accepted by NPC.")
                    self.prev_count = None  # Reset prev_count

            count = player.GetItemCountByVnum(DAGGER_VID)
            if IS_DEBUG_MODE:
                log_message("%s items left." % count)

            if count <= 0:
                log_message("No more items in inventory.")
                self.StopGiving()
                return

            firstItemSlot = GetItemByID(DAGGER_VID)
            if firstItemSlot == -1:
                log_message("Item not found in inventory.")
                self.StopGiving()
                return

            if IS_DEBUG_MODE:
                log_message("Found item at slot %s." % (firstItemSlot + 1))

            # Give the item to the Alchemist
            net.SendGiveItemPacket(self.targetVID, player.SLOT_TYPE_INVENTORY, firstItemSlot, 1)
            if IS_DEBUG_MODE:
                log_message("Item from slot %s was given to Alchemist." % (firstItemSlot + 1))

            skipAnswers([0, 254], True)
            self.hook_unhook_time = current_time + 1  # Schedule unhooking after 1 second

            self.prev_count = count
            self.function_sleep_time = current_time + 1  # Set delay to check after 1 second
            return  # Exit after setting delay

        elif self.is_buying_on:
            # --- Buying Items Logic ---
            empty_slots = player.CountEmptyInventory()
            if empty_slots <= 0:
                log_message("Inventory is full.")
                self.StopBuying()
                return
            elif player.GetMoney() < 20000:
                log_message("Not enough money to buy.")
                self.StopBuying()
                return
            else:
                if not shop.IsOpen():
                    shopVID = player.GetTargetVID()  # Ensure the Shop NPC is selected
                    if shopVID == 0:
                        log_message("Please select the Weapon Shop NPC.")
                        self.StopBuying()
                        return
                    net.SendOnClickPacket(shopVID)
                    # Talking to Weapon Shop NPC to open the shop
                    skipAnswers([1], True)
                    self.hook_unhook_time = current_time + 1  # Schedule unhooking after 1 second
                    if IS_DEBUG_MODE:
                        log_message("Opening shop...")
                    self.function_sleep_time = current_time + 1  # Wait 1 second for the shop to open
                    return
                else:
                    # Shop is open, buy item
                    net.SendShopBuyPacket(4)
                    if IS_DEBUG_MODE:
                        log_message("Bought item from shop slot 4. Empty slots left: %d" % (empty_slots - 1))
                    self.function_sleep_time = current_time + 1  # Delay before buying next item
                    return  # Exit after setting delay

        else:
            # Neither bot is running
            self.running = False
            return

    # --- Modified OnUpdate Method ---

    def OnUpdate(self):
        if not self.running:
            return

        current_time = app.GetGlobalTimeStamp()

        if self.hook_unhook_time and current_time >= self.hook_unhook_time:
            questHook.UnhookFunction()
            self.hook_unhook_time = None
            if IS_DEBUG_MODE:
                log_message("Quest was unhooked.")

        if self.function_sleep_time:
            if current_time >= self.function_sleep_time:
                # Delay has expired
                self.function_sleep_time = None
            else:
                # Still waiting; do nothing
                return  # Wait until function_sleep_time expires

        # At this point, function_sleep_time is None, ready to perform next action
        if self.is_giving_on or self.is_buying_on:
            self.RunScript()
        else:
            self.running = False

class Components:
    def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual='d:\\ymir work\\ui\\public\\small_button_01.sub', OverVisual='d:\\ymir work\\ui\\public\\small_button_02.sub', DownVisual='d:\\ymir work\\ui\\public\\small_button_03.sub'):
        button = ui.Button()
        if parent is not None:
            button.SetParent(parent)
        button.SetPosition(x, y)
        button.SetUpVisual(UpVisual)
        button.SetOverVisual(OverVisual)
        button.SetDownVisual(DownVisual)
        button.SetText(buttonName)
        if tooltipText is not None:
            button.SetToolTipText(tooltipText)
        button.Show()
        button.SetEvent(func)
        return button

    def ToggleButton(self, parent, buttonName, tooltipText, x, y, funcUp, funcDown, UpVisual='d:\\ymir work\\ui\\public\\small_button_01.sub', OverVisual='d:\\ymir work\\ui\\public\\small_button_02.sub', DownVisual='d:\\ymir work\\ui\\public\\small_button_03.sub'):
        toggleButton = ui.ToggleButton()
        if parent is not None:
            toggleButton.SetParent(parent)
        toggleButton.SetPosition(x, y)
        toggleButton.SetUpVisual(UpVisual)
        toggleButton.SetOverVisual(OverVisual)
        toggleButton.SetDownVisual(DownVisual)
        toggleButton.SetText(buttonName)
        if tooltipText is not None:
            toggleButton.SetToolTipText(tooltipText, 24, -19)
        toggleButton.Show()
        toggleButton.SetToggleUpEvent(funcUp)
        toggleButton.SetToggleDownEvent(funcDown)
        return toggleButton

script_manager = ScriptManager()
script_manager.Show()