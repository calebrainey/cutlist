from typing import List, Optional

import typer
from typing_extensions import Annotated

from board import Board

def parse_cuts(cuts):
    cut_list = []
    for cut in cuts:
        size, qty = cut.split(":")
        cut_list.extend([float(size)] * int(qty))
    cut_list.sort(reverse=True)
    return cut_list

def main():
    stock_length = typer.prompt("Enter stock length (in inches)", type=float)
    cuts = []
    
    while True:
        entry = typer.prompt("Enter a cut in the format [length]:[quantity], or press Enter to finish", default="", show_default=False)
        if not entry:
            break

        cuts.append(entry)
    
    cut_list = parse_cuts(cuts)

    boards = []
    for cut in cut_list:
        cut_placed = False
        for board in boards:
            if board.add_cut(cut):
                cut_placed = True
                break
        
        if not cut_placed:
            new_board = Board(stock_length)
            new_board.add_cut(cut)
            boards.append(new_board)
    
    for idx, board in enumerate(boards, start=1):
        print(f"Board {idx}: {board.cuts}")
        print(f"Waste: {board.remaining}")

if __name__ == "__main__":
    typer.run(main)