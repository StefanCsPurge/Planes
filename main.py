from UserInterface.ConsoleUI import Console
from UserInterface.GUI import GUI
from controllers.gameSrv import GameService

if __name__ == '__main__':
    service = GameService()
    UI = None
    while UI is None:
        try:
            print("""Choose your user interface, enter: [1] for graphical 
                                   [2] for console based""")
            choice = input('->').strip()
            if choice == '1':
                UI = GUI(service)
            elif choice == '2':
                UI = Console(service)
            else:
                raise Exception("Non-existent choice!")
        except Exception as ex:
            print(ex)
    UI.run()
