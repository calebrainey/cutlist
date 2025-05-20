from rich.table import Table
from rich.console import Console

from fractions import Fraction

import typer
from typing_extensions import Annotated

from board import Board, AVAILABLE_BOARD_LENGTHS

console = Console()

def get_fraction(size):
    try:
        size = size.strip()
        if " " in size:
            whole, fraction = size.split(" ")
            numerator, denominator = fraction.split("/")
            decimal = float(whole) + float(numerator) / float(denominator)
        elif "/" in size:
            numerator, denominator = size.split("/")
            decimal = float(numerator) / float(denominator)
        else:
            decimal = float(size)
        
        return decimal
        
    except:
        raise ValueError(f"Invalid fraction size format: {size}")

def parse_cuts(cuts):
    cut_list = []
    try:
        for cut in cuts:
            size, qty = cut.split(":")
            cut_list.extend([get_fraction(size)] * int(qty))
        cut_list.sort(reverse=True)
        return cut_list
    except Exception as e:
        console.print(f"[bold red]❌ Unable to process cut: {e}[/bold red]")
        console.print(f"[yellow]Hint: Use the format length:quantity, like 24:3 or 18.5:2[/yellow]")
        raise typer.Exit(code=1)

def greedy_algo(cut_list: list, board_list):
    board_to_use = 0
    cuts_to_make = len(cut_list)

    for cut in cut_list:
        cut_made = False

        for board in board_list:
            if board.can_fit(cut):
                board.add_cut(cut)
                cut_made = True
                break
    
    used_boards = [board for board in board_list if board.cuts]
    return used_boards

def main():
    use_custom = typer.confirm('Do you know the board length you want to use?', default=True)
    if use_custom:
        stock_lengths = typer.prompt("Enter stock length (in inches).\nSeparate multiple boards with a comma")
        if "," in stock_lengths:
            stock_lengths = stock_lengths.split(",")
            stock_lengths = sorted([float(length) for length in stock_lengths], reverse=True)
            stock_boards = [Board(length) for length in stock_lengths]
        elif stock_lengths:
            stock_boards = Board(stock_lengths)
    else:
        stock_boards = None
    
    cuts = []    
    
    console.print("\n[bold green]Let's build your cut list.[/bold green]")
    console.print("[dim]Format each entry as length:quantity — e.g., 24.5:2[/dim]")
    
    while True:
        entry = typer.prompt("Enter a cut(s) in the format [length]:[quantity], or press Enter to finish", default="", show_default=False)
        try:
            if entry:
                size, qty = entry.split(":")
                int(qty)
            else:
                break
        except:
            console.print(f"[red]Invalid cut format. Try again (example 24:3)[/red]")
            continue

        cuts.append(entry)
    
    cut_list = parse_cuts(cuts)

    boards = None

    if stock_boards:
        simulated_boards = greedy_algo(cut_list, stock_boards)
    else:
        # best_boards = None
        # best_board_length = None
        # fewest_boards = float('inf')
        # least_waste = None
        
        available_board_lengths = sorted(AVAILABLE_BOARD_LENGTHS, reverse=True)
        boards = [Board(length) for length in available_board_lengths]

        simulated_boards = greedy_algo(cut_list, boards)
        

        # for board in boards:
        #     board = [board]
        #     simulated_boards = greedy_algo(cut_list, board)
            
        #     total_waste = sum(board.waste for board in simulated_boards)

        #     if len(simulated_boards) < fewest_boards:
        #         best_boards = simulated_boards
        #         best_board_length = board
        #         fewest_boards = len(simulated_boards)
        #         least_waste = total_waste
        #     elif len(simulated_boards) == fewest_boards and total_waste < least_waste:
        #         best_boards = simulated_boards
        #         best_board_length = board
        #         fewest_boards = len(simulated_boards)
        #         least_waste = total_waste
        
        # boards = best_boards
        # stock_lengths = best_board_length

    # Start table render
    table = Table(title="\nFinal Cutlist", title_style="bold italic", show_footer=True)

    table.add_column("Board #", style="cyan", footer_style="bold")
    table.add_column("Cuts", style="green", footer_style="bold")
    table.add_column("Unused Board (in.)", style="red", footer_style="bold")

    for idx, board in enumerate(simulated_boards, start=1):
        table.add_row(f"Board {idx} ({board.length}\")", f"{board.cuts}", f"{board.remaining}\"")

    cut_sum = 0
    waste_sum = 0 

    for board in simulated_boards:
        for cut in board.cuts:
            cut_sum += 1
        waste_sum += board.waste

    table.columns[0].footer = f"Total Boards: {len(simulated_boards)}"
    table.columns[1].footer = f"Total Cuts: {cut_sum}"
    table.columns[2].footer = f"Total Unused: {waste_sum}"
    
    console.print(table)

if __name__ == "__main__":
    typer.run(main)