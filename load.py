import ui, sys, imp, os

class PythonScriptLoader(ui.ScriptWindow):
    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.script_load = None
        self.isShow = 1

        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)

        try:
            import script
            self.script_load = script
        except ImportError as e:
            self.script_load = None
            print("script.py could not be found in root directory")

        self.Board = ui.BoardWithTitleBar()
        self.Board.SetTitleName('pyLoader')
        self.Board.SetSize(190, 80)
        self.Board.SetPosition(3, 320)
        self.Board.AddFlag('movable')
        self.Board.SetCloseEvent(self.OnClose)
        self.Board.Show()

        self.components = Components()
        self.runOnceButton = self.components.Button(self.Board, 'Reload Script', None, 50, 42, self.RunOnce)

    def OnClose(self):
        if self.isShow == 1:
            self.isShow = 0
            self.runOnceButton.Hide()
            self.Board.SetSize(190, 0)
        else:
            self.isShow = 1
            self.runOnceButton.Show()
            self.Board.SetSize(190, 80)

    def RunOnce(self):
        imp.reload(self.script_load)

class Components:
    def Button(self, parent, buttonName, tooltipText, x, y, func, UpVisual='d:\\ymir work\\ui\\public\\large_button_01.sub', OverVisual='d:\\ymir work\\ui\\public\\large_button_02.sub', DownVisual='d:\\ymir work\\ui\\public\\large_button_03.sub'):
        button = ui.Button()
        if parent != None:
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


scriptLoader = PythonScriptLoader()
scriptLoader.Show()