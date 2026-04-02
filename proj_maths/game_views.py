from django.shortcuts import render, redirect
from django.contrib import messages
import random

from . import categories_work
from . import terms_work

def pair_game(request):
    category_id = request.GET.get('category_id')
    categories = categories_work.get_list_of_categories()
    if not categories:
        context = {
            'categories': categories,
            'selected_category_info': {},
        }
    
    # Если не определена выбранная категория
    if not (category_id and category_id != ''):
        category_id = "1"

    selected_category_info = categories_work.get_category_info(category_id)

    # Если выбранная категория не существует или не ликвидна
    if not selected_category_info:
        category_id = "1"
        selected_category_info = categories_work.get_category_info(category_id)
    
    context = {
        'categories': categories,
        'selected_category_info': selected_category_info,
    }
    
    pairs_to_use = terms_work.select_terms_for_game(selected_category_info)

    # Инициализируем игровое состояние в сессии
    if 'pair_game_state' not in request.session:
        game_state = initialize_game_state(pairs_to_use, selected_category_info['id'])
        request.session['pair_game_state'] = game_state
    elif request.session['pair_game_state']['category_id'] != selected_category_info['id']:
        game_state = initialize_game_state(pairs_to_use, selected_category_info['id'])
        request.session['pair_game_state'] = game_state
    
    game_state = request.session['pair_game_state']
    
    if request.method == 'POST':
        print(game_state)
        if game_state['current_st'] == 'ERROR' or game_state['current_st'] == 'CORRECT':
            game_state['current_st'] = 'IDLE'
            game_state['left_id'] = ''
            game_state['right_id'] = ''
            game_state['message'] = "Давай! Вперед"

        left_id = request.POST.get('left_id', '')
        right_id = request.POST.get('right_id', '')
        action = request.POST.get('action', '')
        
        if action == 'reset':
            pairs_to_use = terms_work.select_terms_for_game(selected_category_info)
            request.session['pair_game_state'] = initialize_game_state(pairs_to_use, selected_category_info['id'])
            game_state = request.session['pair_game_state']
        
        elif action == 'quit':
            request.session.pop('pair_game_state')
            return redirect("/")
        
        # Это запись и чтение из сессии нажатых кнопок
        if left_id:
            if game_state['left_id']:
                if game_state['left_id'] == left_id:
                    game_state['left_id'] = ''
                else:
                    game_state['left_id'] = left_id
            else:
                game_state['left_id'] = left_id
        else:
            left_id = game_state['left_id']

        if right_id:
            if game_state['right_id']:
                if game_state['right_id'] == right_id:
                    game_state['right_id'] = ''
                else:
                    game_state['right_id'] = right_id
            else:
                game_state['right_id'] = right_id
        else:
            right_id = game_state['right_id']

        # Обработка пары
        if left_id and right_id:
            
            left_word = next((w for w in game_state['left_words'] if w['id'] == left_id), None)
            right_word = next((w for w in game_state['right_words'] if w['id'] == right_id), None)
            
            if left_word and right_word and left_word['status'] == 'active' and right_word['status'] == 'active':
                if left_id == right_id:
                    left_word['status'] = 'removed'
                    right_word['status'] = 'removed'
                                    
                    
                    game_state['message'] = "Верно!"
                    game_state['current_st'] = 'CORRECT'
                    
                    if game_state['active_pairs'] > 1:
                        game_state['active_pairs'] -= 1
                    else:
                        game_state['message'] = "Все верно! Поздравляем"
                else:
                    game_state['message'] = "Не угадал"
                    game_state['current_st'] = 'ERROR'
                    game_state['errors'] += 1
            
        request.session['pair_game_state'] = game_state
        return redirect(f"/pair-game?category_id={selected_category_info['id']}#game-section")
    
    context = context | game_state
    
    return render(request, 'pair_game.html', context)

def initialize_game_state(pairs, category_id):
    """Инициализирует начальное состояние игры"""
    
    left_words = [{'id': pair['id'], 'text': pair['left'], 'status': 'active'} for pair in pairs]
    right_words = [{'id': pair['id'], 'text': pair['right'], 'status': 'active'} for pair in pairs]
    
    random.shuffle(left_words)
    random.shuffle(right_words)
    
    return {
        'active_pairs': len(pairs),
        'errors': 0,
        'left_words': left_words,
        'right_words': right_words,
        'left_id': '',
        'right_id': '',
        'message': "Давай! Вперед",
        'current_st' : 'IDLE',  # варианты 'IDLE', 'CORRECT', 'ERROR',
        'category_id': category_id
    }