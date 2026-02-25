import random
import string
import numpy as np

def parol(pass_length):
    """
    Генератор паролей
    """
    elements = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for i in range(pass_length):
        password += np.random.choice(elements)
    return password

def flip_coin():
    """
    Подбрасывание монетки
    """
    flip = random.randint(0, 2)
    if flip == 0:
        return "ОРЕЛ"
    else:
        return "РЕШКА"

def knb_game():
   
    return {
        'player_score': 0,
        'comp_score': 0,
        'round': 0,
        'active': True,
        'game_log': []
    }

def play_knb_round(game_state, player_choice):
    """
    Камень ножницы бумага
    """
    
    # Проверяем валидность выбора
    valid_choices = ['камень', 'ножницы', 'бумага']
    if player_choice.lower() not in valid_choices:
        return game_state, "Ошибка: выберите 'камень', 'ножницы' или 'бумага'"
    
    player = player_choice.lower()
    
    # Выбор компьютера
    comp = random.choice(valid_choices)
    
    # Определение победителя раунда
    if player == comp:
        result = "🤝 Ничья!"
        winner = None
    elif (player == "камень" and comp == "ножницы") or \
         (player == "ножницы" and comp == "бумага") or \
         (player == "бумага" and comp == "камень"):
        result = "🎉 Вы победили в этом раунде!"
        winner = "player"
        game_state['player_score'] += 1
    else:
        result = "😢 Компьютер победил в этом раунде!"
        winner = "computer"
        game_state['comp_score'] += 1
    
    # Обновляем счетчик раундов
    game_state['round'] += 1
    
    # Результат раунда
    game_state['game_log'].append({
        'round': game_state['round'],
        'player': player,
        'computer': comp,
        'winner': winner
    })
    
    # Cообщение о результате раунда
    round_message = f"Раунд {game_state['round']}:\n"
    round_message += f"🤖 Компьютер: {comp}\n"
    round_message += f"👤 Вы: {player}\n"
    round_message += f"{result}\n"
    round_message += f"Счет: Вы {game_state['player_score']} - {game_state['comp_score']} Компьютер\n"
    
    # Проверяем закончена ли игра
    if game_state['round'] >= 3:
        game_state['active'] = False
        final_message = "\n" + "="*30 + "\n"
        
        if game_state['player_score'] > game_state['comp_score']:
            final_message += "🏆 ПОБЕДА! Вы выиграли игру! 🏆\n"
        elif game_state['player_score'] < game_state['comp_score']:
            final_message += "💀 Поражение! Компьютер выиграл игру 💀\n"
        else:
            final_message += "🤝 Игра окончена вничью! 🤝\n"
        
        final_message += f"\nИтоговый счет: {game_state['player_score']}:{game_state['comp_score']}"
        
        # Добавляем историю игры
        final_message += "\n\nИстория игры:"
        for log in game_state['game_log']:
            winner_symbol = "🎉" if log['winner'] == "player" else "😢" if log['winner'] == "computer" else "🤝"
            final_message += f"\nРаунд {log['round']}: {log['player']} vs {log['computer']} = {winner_symbol}"
        
        return game_state, round_message + final_message
    
    return game_state, round_message + f"\nСледующий раунд! Выберите: камень, ножницы или бумага"

def get_game_result(game_state):
    
    if not game_state['active']:
        return "Игра завершена. Начните новую игру."
    
    status = f"Игра активна\n"
    status += f"Раунд: {game_state['round']}/3\n"
    status += f"Счет: Вы {game_state['player_score']} - {game_state['comp_score']} Компьютер"
    return status
