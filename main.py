from typing import List, Optional
from rich.table import Table
from rich.console import Console

import typer
from typing_extensions import Annotated

from board import Board, AVAILABLE_BOARD_LENGTHS

console = Console()

def parse_cuts(cuts):
    cut_list = []
    try:
        for cut in cuts:
            size, qty = cut.split(":")
            cut_list.extend([float(size)] * int(qty))
        cut_list.sort(reverse=True)
        return cut_list
    except Exception as e:
        console.print(f"[bold red]❌ Unable to process cut: {e}[/bold red]")
        console.print(f"[yellow]Hint: Use the format length:quantity, like 24:3 or 18.5:2[/yellow]")
        raise typer.Exit(code=1)

def greedy_algo(cut_list: list, stock_length):
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

    return boards

def main():
    use_custom = typer.confirm('Do you know the board length you want to use?', default=True)
    if use_custom:
        stock_length = typer.prompt("Enter stock length (in inches)", type=float)
    else:
        stock_length = None
    
    cuts = []    
    
    console.print("\n[bold green]Let's build your cut list.[/bold green]")
    console.print("[dim]Format each entry as length:quantity — e.g., 24.5:2[/dim]")
    
    while True:
        entry = typer.prompt("Enter a cut(s) in the format [length]:[quantity], or press Enter to finish", default="", show_default=False)
        try:
            if entry:
                size, qty = entry.split(":")
                float(size)
                int(qty)
            else:
                break
        except:
            console.print(f"[red]Invalid cut format. Try again (example 24:3)[/red]")
            continue

        cuts.append(entry)
    
    cut_list = parse_cuts(cuts)

    boards = None

    if stock_length:
        boards = greedy_algo(cut_list, stock_length)
    else:
        best_boards = None
        best_board_length = None
        fewest_boards = float('inf')
        least_waste = None
        
        for size in AVAILABLE_BOARD_LENGTHS:
            simulated_boards = greedy_algo(cut_list, size)
            
            total_waste = sum(board.waste for board in simulated_boards)

            if len(simulated_boards) < fewest_boards:
                best_boards = simulated_boards
                best_board_length = size
                fewest_boards = len(simulated_boards)
                least_waste = total_waste
            elif len(simulated_boards) == fewest_boards and total_waste < least_waste:
                best_boards = simulated_boards
                best_board_length = size
                fewest_boards = len(simulated_boards)
                least_waste = total_waste
        
        boards = best_boards
        stock_length = best_board_length

    # Start table render
    table = Table(title="\nFinal Cutlist", title_style="bold italic", show_footer=True)

    table.add_column("Board #", style="cyan", footer_style="bold")
    table.add_column("Cuts", style="green", footer_style="bold")
    table.add_column("Waste (in.)", style="red", footer_style="bold")

    for idx, board in enumerate(boards, start=1):
        table.add_row(f"Board {idx} ({board.length}\")", f"{board.cuts}", f"{board.remaining}\"")

    cut_sum = 0
    waste_sum = 0 

    for board in boards:
        for cut in board.cuts:
            cut_sum += 1
        waste_sum += board.waste

    table.columns[0].footer = f"Total Boards: {len(boards)}"
    table.columns[1].footer = f"Total Cuts: {cut_sum}"
    table.columns[2].footer = f"Total Waste: {waste_sum}"
    
    console.print(table)

if __name__ == "__main__":
    typer.run(main)