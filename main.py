from typing import List, Optional
from rich.table import Table
from rich.console import Console

import typer
from typing_extensions import Annotated

from board import Board

console = Console()

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
    
    table = Table(title="\nFinal Cutlist", title_style="bold italic")

    table.add_column("Board #", style="cyan")
    table.add_column("Cuts", style="green")
    table.add_column("Waste (in.)", style="red")

    for idx, board in enumerate(boards, start=1):
        table.add_row(f"Board {str(idx)} ({board.length}\")", f"{board.cuts}", f"{board.remaining}\"")

    console.print(table)

if __name__ == "__main__":
    typer.run(main)