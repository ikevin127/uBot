import sys
_chr = chr

import __builtin__ as buildin
try:
	import time
except:
	pass

def HasArguments(module, attrlist):
    for attr in attrlist:
        if not buildin.hasattr(module, attr):
            return False
    return True

for modulename, module in iter(sys.modules.items()):
    if HasArguments(module, ['clock']):time = module
    if HasArguments(module, ['GetPlayTime']):player = module
    if HasArguments(module, ['GetNameByVID']):chr = module
    if HasArguments(module, ['DirectEnter']):net = module
    if HasArguments(module, ['SetCameraMaxDistance']):app = module
    if HasArguments(module, ['mouseController']):mouseModule = module
    if HasArguments(module, ['ArrangeShowingChat']):chat = module
    if HasArguments(module, ['ClearSlot']):wndMgr = module
    if HasArguments(module, ['GetCurrentMapName']):background = module
    if HasArguments(module, ['SetEmpireNameMode']):chrmgr = module
    if HasArguments(module, ['GetItemName', 'SelectItem']):item = module
    if HasArguments(module, ['ArrangeTextTail', 'RegisterChatTail']):textTail = module
    if HasArguments(module, ['ItemToolTip']):uiToolTip = module
    if HasArguments(module, ['GetGradeByVID']):nonplayer = module
    if HasArguments(module, ['OpenQuestWindow', 'GameWindow']):game = module
    if HasArguments(module, ['IsSoftwareCursor']):systemSetting = module
    if HasArguments(module, ['SelectAnswer']):event = module
    if HasArguments(module, ['ENVIRONMENT_NIGHT']):constInfo = module
    if HasArguments(module, ['GenerateColor']):grp = module
    if HasArguments(module, ['GenerateFromHandle']):grpImage = module
    if HasArguments(module, ['LogBox']):dbg = module
    if HasArguments(module, ['EnableCaptureInput', 'GetReading']):ime = module
    if HasArguments(module, ['GetSkillCoolTime', 'GetSkillLevelUpPoint']):skill = module
    if HasArguments(module, ['Exist', 'Get']):pack = module
    if HasArguments(module, ['SetGeneralMotions']):playerSettingModule = module
    if HasArguments(module, ['PlaySound']):snd = module
    if HasArguments(module, ['IsPrivateShop']):shop = module
    if HasArguments(module, ['APP_TITLE']):locale = module
    if HasArguments(module, ['APP_TITLE']):localeinfo = module
    if HasArguments(module, ['CharacterWindow']):uiCharacter = module
    if HasArguments(module, ['IsAtlas']):miniMap = module
    if HasArguments(module, ['InputDialog']):uiCommon = module
    if HasArguments(module, ['factorial']):math = module
    if HasArguments(module, ['BigBoard']):uiTip = module
    if HasArguments(module, ['AtlasWindow']):uiMiniMap = module
    if HasArguments(module, ['MARKADDR_DICT']):serverInfo = module
    if HasArguments(module, ['ScriptWindow']):ui = module
    if HasArguments(module, ['SAFEBOX_PAGE_SIZE']):safebox = module
    if HasArguments(module, ['ItemToolTip']):uiToolTip = module
    if HasArguments(module, ['Interface']):interfacemodule = module
    if HasArguments(module, ['CreateEffect']):effect = module
    if HasArguments(module, ['Clear']):quest = module
    if HasArguments(module, ['AUTH_ADD_MEMBER']):guild = module
    if HasArguments(module, ['GetExceptionString']):exception = module
    if HasArguments(module, ['O_APPEND']):os = module
    if HasArguments(module, ['WRAPPER_ASSIGNMENTS']):functools = module

from OpenBot.Modules import FileManager, UIComponents, ShopSearcher, Settings, Shopcreator, KeyBot, Skillbot, ChannelSwitcher, EnergyBot
from OpenBot.Modules.Actions import ActionBot
import eXLib, Data

DEBUG = False
if DEBUG:
    from OpenBot.Modules import Filter, MiningBot

class OpenBotHackbarDialog(ui.ScriptWindow): 				

    Hackbar = 0
    comp = UIComponents.Component()
    action_bot = ActionBot.instance
    energy_bot = EnergyBot.instance

    def __init__(self):
        self.OpenBotBoard = ui.ThinBoard(layer="TOP_MOST")
        self.OpenBotBoard.SetPosition(0, 100)
        if DEBUG:
            self.OpenBotBoard.SetSize(51, 500)
        else:
            self.OpenBotBoard.SetSize(51, 305)
        self.OpenBotBoard.AddFlag("float")
        self.OpenBotBoard.AddFlag("movable")
        self.OpenBotBoard.Hide()

        self.ShowHackbarButton = self.comp.Button(None, '', 'Show Hackbar', 10, 60, self.OpenHackbar, eXLib.PATH + 'OpenBot/Images/Shortcuts/show_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/show_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/show_0.tga')
        self.HideHackbarButton = self.comp.HideButton(None, '', 'Hide Hackbar', 10, 60, self.OpenHackbar, eXLib.PATH + 'OpenBot/Images/Shortcuts/hide_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/hide_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/hide_0.tga')
        self.SettingsButton = self.comp.Button(self.OpenBotBoard, '', 'Settings', 9, 10, self.Generel, eXLib.PATH + 'OpenBot/Images/Hackbar/sett_0.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/sett_1.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/sett_2.tga')
        self.SearchBotButton = self.comp.Button(self.OpenBotBoard, '', 'SearchBot', 10, 45, self.SearchBot, eXLib.PATH + 'OpenBot/Images/Hackbar/search_0.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/search_1.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/search_0.tga')
        self.ShopCreatorButton = self.comp.Button(self.OpenBotBoard, '', 'Shopbot', 8, 78, self.ShopCreator, eXLib.PATH + 'OpenBot/Images/Hackbar/shop_0.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/shop_1.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/shop_0.tga')
        self.SkillbotButton = self.comp.Button(self.OpenBotBoard, '', 'Skillbot', 8, 113, self.OnSkillbot, eXLib.PATH + 'OpenBot/Images/Hackbar/skill_0.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/skill_1.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/skill_0.tga')
        self.ZoomButton = self.comp.Button(self.OpenBotBoard, '', 'Zoom-Hack', 10, 149, self.Zoom, eXLib.PATH + 'OpenBot/Images/Shortcuts/zoom_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/zoom_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/zoom_0.tga')
        self.EnergyBotButton = self.comp.Button(self.OpenBotBoard, '', 'EnergyBot', 10, 183, self.OnEnergyBot, eXLib.PATH + 'OpenBot/Images/Hackbar/energy_0.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/energy_1.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/energy_0.tga')
        self.ActionBotButton = self.comp.Button(self.OpenBotBoard, '', 'ActionBot', 8, 216, self.OnActionBot, eXLib.PATH + 'OpenBot/Images/Hackbar/action_0.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/action_1.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/action_0.tga')
        self.CrashButton = self.comp.Button(self.OpenBotBoard, '', 'Exit', 10, 266, self.CloseRequest, eXLib.PATH + 'OpenBot/Images/Shortcuts/close_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/close_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/close_0.tga')

    def OpenHackbar(self):
        if self.Hackbar:
            self.Hackbar = 0
            self.ShowHackbarButton.Show()
            self.HideHackbarButton.Hide()
            self.OpenBotBoard.Hide()
        else:
            self.Hackbar = 1
            self.ShowHackbarButton.Hide()
            self.HideHackbarButton.Show()
            self.OpenBotBoard.Show()

    def Generel(self):
        Settings.switch_state()
    
    def OnChannelSwitcher(self):
        ChannelSwitcher.switch_state()
    
    def SearchBot(self):
        ShopSearcher.switch_state()
    
    def ShopCreator(self):
        Shopcreator.switch_state()

    def OnSkillbot(self):
        Skillbot.switch_state()
    
    def Zoom(self):
        app.SetCameraMaxDistance(12000)

    def OnEnergyBot(self):
        self.energy_bot.switch_state()
    
    def OnActionBot(self):
        self.action_bot.switch_state()

    def Close(self):
        app.Abort()
    
    def CancelQuestionDialog(self):
        self.QuestionDialog.Close()
        self.QuestionDialog = None

    def CloseRequest(self):
        self.QuestionDialog = uiCommon.QuestionDialog()
        self.QuestionDialog.SetText("Do You want to quit Metin2 immediately?")
        self.QuestionDialog.SetAcceptEvent(ui.__mem_func__(self.Close))
        self.QuestionDialog.SetCancelEvent(ui.__mem_func__(self.CancelQuestionDialog))
        self.QuestionDialog.Open()

try:
    app.Shop.Close()
except:
    pass
app.Shop = OpenBotHackbarDialog()
KeyBot.instance.enableButton.SetOn()
KeyBot.instance.Start()
