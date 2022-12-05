import argparse
from game import Game

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Select simulation mode.')
    parser.add_argument('--reset', action='store_true')
    parser.add_argument('--split', type=str, default="none")
    parser.add_argument('--double', type=str, default="none")
    parser.add_argument('--draw', type=str, default="naive")
    parser.add_argument('--round', type=int, default=10000)
    args = parser.parse_args()
    
    splitStrategy = ["none", "online", "calculate"]
    assert args.split in splitStrategy, "Unknown split strategy: "+args.split
    doubledownStrategy = ["none", "online", "calculate"]
    assert args.double in doubledownStrategy, "Unknown doubledown strategy: "+args.double
    drawingStrategy = ["naive", "online", "calculate"]
    assert args.draw in drawingStrategy, "Unknown doubledown strategy: "+args.draw
    print("Reset: ", args.reset)
    print("Splitting pair strategy: " + args.split)
    print("Doubledown strategy: " + args.double)
    print("Drawing strategy: " + args.draw)
    print("Simulation rounds: " + str(args.round))
    game = Game(1, args.split, args.double, args.draw)
    game.startGame(args.round, args.reset)
