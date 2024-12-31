import ui, sys, os
import eXLib
import chr,app
exec ('import sys')
_chr = chr

b = sys.modules.keys()
for i in range (len(b)):
	h=b[i]
	r=0
	for g in range(len(h)):
		if h[g] != '.':
			r=r+1
			if r==len(h):
				a=dir(__import__(b[i]))
				for y in range(len(a)):
					if a[y]=='GetMainCharacterIndex' or 'MAX_HP' or 'SetSingleDIKKeyState' or 'INVENTORY_PAGE_SIZE' or 'INVENTORY_SLOT_COUNT':
						playerm=b[i]
					if a[y]=='GetVIDInfo':
						chrmgrm=b[i]
					if a[y]=='SendShopEndPacket':
						netm=b[i]
					if a[y]=='AppendChat':
						chatm=b[i]
imp='import '

try:
	exec (imp+chatm+' as _chat')
except:
	pass
try:
	exec (imp+netm+' as _net')
except:
	pass
try:
	exec (imp+playerm+' as _player')
except:
	pass
try:
	exec (imp+chrmgrm+' as _chrmgr')
except:
	pass


sys.modules['player'] = _player
sys.modules['net'] = _net
sys.modules['chat'] = _chat
sys.modules['chrmgr'] = _chrmgr

def SetSingleDIKKeyState(key,state):
    if state == 1:
        _player.OnKeyDown(key)
    else:
        _player.OnKeyUp(key)

def SetAttackKeyState(state):
    if state == 1:
        _player.OnKeyDown(app.DIK_SPACE)
    else:
        _player.OnKeyUp(app.DIK_SPACE)

setattr(chr, 'GetPixelPosition', eXLib.GetPixelPosition)
setattr(chr, 'MoveToDestPosition', eXLib.MoveToDestPosition)
setattr(_player, 'SetSingleDIKKeyState', SetSingleDIKKeyState)
setattr(_player, 'SetAttackKeyState', SetAttackKeyState)

#Set Path
folder = eXLib.PATH+"OpenBot"
command = 'mklink /d OpenBot "' + folder +'"'

sys.path.append(os.path.join(eXLib.PATH))
sys.path.append(os.path.join(eXLib.PATH, 'OpenBot'))
sys.path.append(os.path.join(eXLib.PATH, 'OpenBot', 'lib'))
sys.path.append(os.path.join(eXLib.PATH, 'OpenBot', 'Modules'))
