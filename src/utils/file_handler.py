from datetime import datetime

def save_game(fen, filename=None) -> tuple[bool, str]:
    try:
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"saved_game_{timestamp}.fen"

        with open(filename, 'w') as file:
                file.write(fen)
        return True, ""
    
    except Exception as e:
        return False, str(e)

def load_game(filename) -> tuple[bool, str]:
    try:
        with open(filename, 'r') as file:
            fen = file.read().strip()
        return True, fen
    except Exception as e:
        return False, str(e)