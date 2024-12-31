def find_string(string_to_search, substring):
	string_to_search_no_spaces = string_to_search.replace(" ", "").lower()
	substring_no_spaces = substring.replace(" ", "").lower()
	return string_to_search_no_spaces.find(substring_no_spaces) != -1

def HasArguments(module, attrlist):
	for attr in attrlist:
		if hasattr(module, attr):
			return attr
		prefixed_attr = 'myth01734' + attr
		if hasattr(module, prefixed_attr):
			return prefixed_attr
	return None
import sys, time
for modulename, module in iter(sys.modules.items()):
	if HasArguments(module, ['clock']):time = module
	if HasArguments(module, ['MBF_ATTACK']):player = module

	if HasArguments(module, ['GetNameByVID']):chr = module

	if HasArguments(module, ['DirectEnter']):net = module

	if HasArguments(module, ['DIK_X']):app = module

	if HasArguments(module, ['mouseController']):mouseModule = module
	if HasArguments(module, ['ArrangeShowingChat']):chat = module

	if HasArguments(module, ['AppendRequirementSignImage']):wndMgr = module

	if HasArguments(module, ['GetCurrentMapName']):background = module
	if HasArguments(module, ['SetEmoticon']):chrmgr = module

	if HasArguments(module, ['ITEM_TYPE_POLYMORPH']):item = module
	if HasArguments(module, ['ArrangeTextTail']):textTail = module
	if HasArguments(module, ['SkillToolTip']):uiToolTip = module
	if HasArguments(module, ['GetGradeByVID']):nonplayer = module
	if HasArguments(module, ['GameWindow']):game = module
	if HasArguments(module, ['IsSoftwareCursor']):systemSetting = module
	if HasArguments(module, ['SelectAnswer']):event = module
	if HasArguments(module, ['ENVIRONMENT_NIGHT']):constInfo = module
	if HasArguments(module, ['SaveScreenShot']):grp = module
	if HasArguments(module, ['GenerateFromHandle']):grpImage = module
	if HasArguments(module, ['LogBox']):dbg = module
	if HasArguments(module, ['DisableCaptureInput']):ime = module
	if HasArguments(module, ['GetSkillName']):skill = module
	if HasArguments(module, ['Exist']):pack = module
	if HasArguments(module, ['SetGeneralMotions']):playerSettingModule = module
	if HasArguments(module, ['PlaySound']):snd = module

	if HasArguments(module, ['SHOP_SLOT_COUNT']):shop = module

	if HasArguments(module, ['APP_TITLE']):locale = module
	if HasArguments(module, ['APP_TITLE']):localeinfo = module
	if HasArguments(module, ['CharacterWindow']):uiCharacter = module
	if HasArguments(module, ['IsAtlas']):miniMap = module
	if HasArguments(module, ['InputDialog']):uiCommon = module
	if HasArguments(module, ['factorial']):math = module
	if HasArguments(module, ['BigBoard']):uiTip = module
	if HasArguments(module, ['AtlasWindow']):uiMiniMap = module
	if HasArguments(module, ['MARKADDR_DICT']):serverInfo = module

	if HasArguments(module, ['AniImageBox']):ui = module
	if HasArguments(module, ['SAFEBOX_PAGE_SIZE']):safebox = module
	if HasArguments(module, ['CreateEffect']):effect = module
	if HasArguments(module, ['GetQuestCount']):quest = module
	if HasArguments(module, ['AUTH_ADD_MEMBER']):guild = module
	if HasArguments(module, ['GetExceptionString']):exception = module
	if HasArguments(module, ['O_APPEND']):os = module
	if HasArguments(module, ['WRAPPER_ASSIGNMENTS']):functools = module
	if HasArguments(module, ['CaptchaDialog']):captcha = module
	if HasArguments(module, ['ChatLine']):uichat = module
	if HasArguments(module, ['InventoryWindow']):uiinventory = module
	if HasArguments(module, ['StopFishMovement']):fishing = module
	if HasArguments(module, ['SelectCharacterWindow']):introSelect = module
	if HasArguments(module, ['LoadingWindow']):introLoading = module
	if HasArguments(module, ['MainStream']):networkModule = module
	if HasArguments(module, ['CreateCharacterWindow']):introCreate = module
	if HasArguments(module, ['LoginWindow']):introLogin = module
	if HasArguments(module, ['SelectEmpireWindow']):introEmpire = module
	if HasArguments(module, ['uniform']):random = module
	if HasArguments(module, ['ArrangeTextTail']):textTail = module
	if HasArguments(module, ['format_exception']):traceback = module
	if HasArguments(module, ['GetElkFromSelf']):exchange = module
	if HasArguments(module, ['InstancesList']):eXLib = module


import functools,OpenLog,game,sys


# The current phase.
CURRENT_PHASE = 5
phaseCallbacks = {}
GAME_WINDOW = 0

class Hook():
    """
    Hook class that allows to replace functions in modules.
    """
    def __init__(self, toHookFunc, replaceFunc, moduleName=None):
        self.originalFunc = toHookFunc
        self.replaceFunc = replaceFunc
        self.functionName = str(toHookFunc.__name__)
        self.functionOwner = self.GetFunctionOwner(toHookFunc, moduleName)
        self.isHooked = False

    def GetFunctionOwner(self, func, moduleName=None):
        """
        Return the object owner of the function 

        Args:
            func ([function]): a function.
            moduleName (str, optional): The module name to use if func.__module__ is None.

        Returns:
            [object]: Return the object owner of the function.
        """
        try:
            owner = func.im_class  # In case of a class function
        except AttributeError:
            if func.__module__ is None and moduleName is not None:
                owner = sys.modules.get(moduleName)
            else:
                owner = sys.modules.get(func.__module__)
            if owner is None:
                print("Debug: Module", func.__module__, "not found in sys.modules.")
                raise ValueError("Module " + str(func.__module__) + " not found in sys.modules.")
        
        return owner

    def CallOriginalFunction(self, *args, **kwargs):
        """
        Call the original function before the hook.
        Returns:
            [args]: the arguments of the function.
        """
        @functools.wraps(self.originalFunc)
        def run(*args, **kwargs):
            return self.originalFunc(*args, **kwargs)
        return run(*args, **kwargs)
        
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
        if not self.isHooked:
            return
        self.isHooked = False
        setattr(self.functionOwner, self.functionName, self.originalFunc)

def phaseIntercept(*args, **kwargs):
    global CURRENT_PHASE
    if len(args) > 1 and args[1] != 0:
        CURRENT_PHASE = args[0]
    OpenLog.DebugPrint("PHASE: " + str(CURRENT_PHASE))
    for callback_id in phaseCallbacks:
        callback = phaseCallbacks[callback_id]
        if callable(callback):
            callback(CURRENT_PHASE, args[1])
    phaseHook.CallOriginalFunction(*args, **kwargs)

# Pass the module name explicitly if __module__ attribute is None
phaseHook = Hook(net.SetPhaseWindow, phaseIntercept, moduleName='net')

def skipFunc(*args):
    """
    Function that does nothing.
    """
    pass 

def registerPhaseCallback(id, func):
    phaseCallbacks[id] = func

def deletePhaseCallback(id):
    if id in phaseCallbacks:
        del phaseCallbacks[id]

class SkipHook(Hook):
    def __init__(self, toHookFunc):
        Hook.__init__(self, toHookFunc, skipFunc)

def GameWindowIntercept(*args, **kwargs):
    import Hooks, Data
    if args[0] == 0:
        return
    Data.GameWindow = args[0]
    Data.obj = Data.uiShortcut()
    Hooks.GAME_WINDOW = args[0]
    player.SetGameWindow(*args, **kwargs)

def CheckAffectIntercept(*args, **kwargs):
    import Hooks
    if args[0] == chr.AFFECT_AUTO_USE:
        return True
    else:
        Hooks.checkAffectHook.CallOriginalFunction(*args, **kwargs)

debugFunc = 0
questHook = SkipHook(game.GameWindow.OpenQuestWindow)
phaseHook = Hook(net.SetPhaseWindow, phaseIntercept, moduleName='net')
gameWindowHook = Hook(player.SetGameWindow, GameWindowIntercept, moduleName='player')
# checkAffectHook = Hook(item.CheckAffect, CheckAffectIntercept, moduleName='item')

def GetQuestHookObject():
    return questHook

def GetCurrentPhase():
    global CURRENT_PHASE
    return CURRENT_PHASE

def GetGameWindow():
    global GAME_WINDOW
    return GAME_WINDOW

def printFunc(*args, **kwargs):
    """
    Print the arguments of a function to a debug.txt file.(In the game folder)
    """
    with open("debug.txt", "a") as f:
        f.write("[DebugHook] Function called arguments:\n")
        for i, arg in enumerate(args):
            f.write("[DebugHook] Arg " + str(i) + ": " + str(arg) + "\n")
        f.write("\n")
    debugFunc.CallOriginalFunction(*args, **kwargs)

def printFuncNC(*args, **kwargs):
    """
    Print the arguments of a function to a debug.txt file.(In the game folder)
    This happens without Calling the Original.
    """
    with open("debug.txt", "a") as f:
        f.write("[DebugHook] Function called arguments:\n")
        for i, arg in enumerate(args):
            f.write("[DebugHook] Arg " + str(i) + ": " + str(arg) + "\n")
        f.write("\n")

# Print arguments of a function
def _debugHookFunctionArgs(func):
    global debugFunc
    debugFunc = Hook(func, printFunc)
    debugFunc.HookFunction()

def _debugUnhookFunctionArgs():
    debugFunc.UnhookFunction()

phaseHook.HookFunction()
gameWindowHook.HookFunction()
# checkAffectHook.HookFunction()
