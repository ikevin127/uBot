
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
	# module = sys.modules[modulename]
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

from OpenBot.Modules.Actions import Action, ActionBot, ActionFunctions, ActionRequirementsCheckers
from OpenBot.Modules.OpenLog import DebugPrint
import UIComponents, FileManager, eXLib
from OpenBot.Modules import OpenLib
from FileManager import boolean
from BotBase import BotBase

ALL_GIVABLE_ITEMS = [
    1040, 1041, 1042, 1043, 1044, # Cat Bite Knife +0 to +4
    12260, 12261, 12262, 12263, 12264, # Fear Mask +0 to +4
    12390, 12391, 12392, 12393, 12394, # Orc Hood +0 to +4
    12530, 12531, 12532, 12533, 12534, # Horned Helmet +0 to +4
    12670, 12671, 12672, 12673, 12674, # Cardinal's Hat +0 to +4
    21530, 21531, 21532, 21533, 21534 # Godsend Helmet +0 to +4
]

class EnergyBot(BotBase):
    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.ItemSlotToBuy = 4
        self.ItemCountToBuy = 5
        self.weaponShopQuest = False
        self.LoadSettings()
        self.BuildWindow()

    def BuildWindow(self):
        comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 190)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('EnergyBot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()

        self.hasWeaponShopQuest = comp.OnOffButton(self.Board, '\t\t\t\t\t\t\t\t\t\t I have Weapon Shop mission', '', 20, 50,funcState=self.WeaponShopQuestOnOff,defaultValue=int(self.weaponShopQuest))

        self.enableEnergyBot = comp.OnOffButton(self.Board, '', '', 100, 110,
                                            OffUpVisual=eXLib.PATH + 'OpenBot/Images/start_0.tga',
                                            OffOverVisual=eXLib.PATH + 'OpenBot/Images/start_1.tga',
                                            OffDownVisual=eXLib.PATH + 'OpenBot/Images/start_2.tga',
                                            OnUpVisual=eXLib.PATH + 'OpenBot/Images/stop_0.tga',
                                            OnOverVisual=eXLib.PATH + 'OpenBot/Images/stop_1.tga',
                                            OnDownVisual=eXLib.PATH + 'OpenBot/Images/stop_2.tga',
                                            funcState=self.SwitchEnableEnergyBot, defaultValue=False)       

    def LoadSettings(self):
        self.weaponShopQuest = boolean(FileManager.ReadConfig("HasWeaponShopQuest"))

    def SaveSettings(self):
		FileManager.WriteConfig("HasWeaponShopQuest", str(self.weaponShopQuest))
		FileManager.Save()

    def WeaponShopQuestOnOff(self,val):
        self.weaponShopQuest = val
        self.SaveSettings()

    def SwitchEnableExchangeEnergyToCrystal(self, val):
        pass
    
    def AddExchangeEnergyToCrystalToStage(self):
        actions_dict = {0: {'function_args': [20001, (62350, 51180), 'metin2_map_a1'],
              'function': ActionFunctions.ChangeEnergyToCrystal,
              'requirements': {},
              'callback': instance.SetIsCurrActionDoneTrue},
              1: {'function_args': [20001, (66150, 73450), 'metin2_map_b1'],
              'function': ActionFunctions.ChangeEnergyToCrystal,
              'requirements': {},
              'callback': instance.SetIsCurrActionDoneTrue},
              2: {'function_args': [20001, (29205, 81577), 'metin2_map_c1'],
              'function': ActionFunctions.ChangeEnergyToCrystal,
              'requirements': {},
              'callback': instance.SetIsCurrActionDoneTrue},
              }
        self.currSchema['stages'][self.currStage]['actions'].append(actions_dict[self.currStage])

    def SwitchEnableEnergyBot(self, val):
        if val:
            self.Start()
            self.currSchema = ENERGY_BOT_SCHEMA
            self.RecognizeStartStage()
        else:
            self.Stop()
        
        DebugPrint(str(self.currSchema))

    def RecognizeStartStage(self):
        if ActionRequirementsCheckers.isInMaps(['metin2_map_a1']):
            self.currStage = 0
        elif ActionRequirementsCheckers.isInMaps(['metin2_map_b1']):
            self.currStage = 1
        elif ActionRequirementsCheckers.isInMaps(['metin2_map_c1']):
            self.currStage = 2
        else:
            self.Stop()
    
    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
            self.SaveSettings()
        else:
            self.Board.Show()

    def Frame(self):
        if self.isCurrActionDone:
            action_dict = self.currSchema['stages'][self.currStage]['actions'][self.currAction]
            self.isCurrActionDone = False
            if ActionFunctions.GoBuyItemsFromNPC.__name__ == self.currSchema['stages'][self.currStage]['actions'][self.currAction]['function'].__name__:
                DebugPrint(str(OpenLib.GetNumberOfFreeSlots()))
                item_slot = self.ItemSlotToBuy
                self.currSchema['stages'][self.currStage]['actions'][self.currAction]['function_args'][0] = [item_slot for x in range(OpenLib.GetNumberOfFreeSlots())]
                weapon_shop_quest_value = int(self.weaponShopQuest)
                if len(action_dict['function_args']) > 3:
                    # Check if index 4 argument exists
                    if len(action_dict['function_args']) > 4:
                        # Replace index 4 argument
                        action_dict['function_args'][4] = weapon_shop_quest_value 
                    else:
                        # Append if index 4 argument does not exist
                        action_dict['function_args'].append(weapon_shop_quest_value)  
            
            ActionBot.instance.AddNewAction(action_dict)
            DebugPrint(str(action_dict))

instance = EnergyBot()

ENERGY_BOT_SCHEMA = {
    'requirements': {
        'maps': ['metin2_map_a1', 'metin2_map_b1', 'metin2_map_c1'],
        'lvl': 35},
    'options': {'SlotToBuy': 4},
    'stages': {
        0: {'options': [ActionBot.STAGE_REPEAT],
            'actions': [{'function_args': [[], 9001, (60100, 56100), instance.SetIsCurrActionDoneTrue],
                        'function': ActionFunctions.GoBuyItemsFromNPC,
                        'requirements': {},
                        'interruptors': [ActionRequirementsCheckers.hasEnoughMoney],
                        'interruptors_args': [25000],
                        'interrupt_function': lambda: Action.NOTHING
                        },
                        {'function_args': [ALL_GIVABLE_ITEMS, 20001, (62200, 51600)],
                        'function': ActionFunctions.GetEnergyFromAlchemist,
                        'requirements': {},
                        'callback': instance.SetIsCurrActionDoneTrue
                        },
                        ]},
        1: {'options': [ActionBot.STAGE_REPEAT],
            'actions': [{'function_args': [[], 9001, (67700, 65600), instance.SetIsCurrActionDoneTrue],
                        'function': ActionFunctions.GoBuyItemsFromNPC,
                        'requirements': {},
                        'interruptors': [ActionRequirementsCheckers.hasEnoughMoney],
                        'interruptors_args': [25000],
                        'interrupt_function': lambda: Action.NOTHING
                        },
                        {'function_args': [ALL_GIVABLE_ITEMS, 20001, (65900, 72800)],
                        'function': ActionFunctions.GetEnergyFromAlchemist,
                        'requirements': {},
                        'callback': instance.SetIsCurrActionDoneTrue
                        },
                        ]},
        2: {'options': [ActionBot.STAGE_REPEAT],
            'actions': [{'function_args': [[], 9001, (42800, 61200), instance.SetIsCurrActionDoneTrue],
                        'function': ActionFunctions.GoBuyItemsFromNPC,
                        'requirements': {},
                        'interruptors': [ActionRequirementsCheckers.hasEnoughMoney],
                        'interruptors_args': [25000],
                        'interrupt_function': lambda: Action.NOTHING
                        },
                        {'function_args': [ALL_GIVABLE_ITEMS, 20001, (29700, 81500)],
                        'function': ActionFunctions.GetEnergyFromAlchemist,
                        'requirements': {},
                        'callback': instance.SetIsCurrActionDoneTrue
                        },
                        ]}
    }
}