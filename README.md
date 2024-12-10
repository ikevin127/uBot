# [GF] uBot - Energy Fragment Bot

This is an updated version of the [GF] Metin2 - Energy Fragment Bot showcased in this YouTube [video](https://www.youtube.com/watch?v=AYJiVVfTNHE).

**The repo contains 3 files:**
- PyLoader.mix (python loader terminal)
- loader.py (in-game script reload window)
- script.py (uBot)

## Instructions
1. Add all 3 files to your metin2 client folder.
2. Open the game, when client opens a CMD terminal will open as well (this is the .mix (.dll) C++ python injector).
3. Before you login into the metin2 account, load the loader.py (this is the python script loader) in the CMD terminal that opened with the game client.
4. Once you input the command "load loader.py" and hit Enter -> you can now login into the game and the CMD terminal should say that the script was loaded by the time you reach the character select window.
5. Once you are in the game, you will see the 2 script windows: uBot and pyLoader.

## Notes
1. You can also compile the PyLoader.mix (.dll) C++ python injector yourself from [source](https://mega.nz/file/CdUGEAjQ#6wnsaspseurhD0u3h_FkFeoHfKtZMwp5QCN2t-PpM38).
2. Beware that the module names change frequently with weekly GF maintenance, you need to replace them in the uBot script.py file, otherwise the script won't work with outdated module names.
3. The loader.py in-game window with the Reload Script button allows you to modify the script.py while the game is running so you can do real-time changes in the script (I did this to facilitate easier development) so you won't have to close and re-open the game everytime you want to change something in the script.