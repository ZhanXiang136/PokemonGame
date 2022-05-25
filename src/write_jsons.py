import requests
import json

def allowed_move(test_move):
    '''
    checks if pokemon move is a registered move in move.json
    :param test_move: move to be checked
    :return: whether or not the move is in move.json
    '''
    with open('modules/move.json', 'r') as file:
        move_object = json.load(file)
        for move in move_object['results']:
            if move == test_move:
                return True
        return False


def write_pokemons():
    '''
    write a json of all pokemon that has more than 4 moves, has at least one type, and not a mega
    :return: None
    '''
    with open('modules/pokemon.json', 'w') as file:
        pokemon_object = {
            'count': 0,
            'next': 'https://pokeapi.co/api/v2/pokemon/',
            'results': {}
        }

        while pokemon_object['next'] is not None:
            response = requests.get(pokemon_object['next']).json()
            for pokemon in response['results']:
                pokemon_response = requests.get(pokemon['url']).json()
                if len(pokemon_response['moves']) >= 4 and len(pokemon_response['types']) != 0 and "-mega" not in pokemon['name']:
                    pokemon_info = {
                        'name': pokemon_response['name'],
                        'id': pokemon_response['id'],
                        'types': [type['type']['name'] for type in pokemon_response['types']],
                        'stats': [stat['base_stat'] for stat in pokemon_response['stats']],# [hp, attack, defense, special-attack, special-defense, speed]
                        'moves': [move['move']['name'] for move in pokemon_response['moves'] if allowed_move(move['move']['name'])],
                        'sprite_front': pokemon_response['sprites']['front_default'],
                        'sprite_back': pokemon_response['sprites']['back_default'],
                    }

                    pokemon_object['results'][pokemon_response['name']] = pokemon_info
                    pokemon_object['count'] += 1
                    print(pokemon_response['name'])
            pokemon_object['next'] = response['next']

        json.dump(pokemon_object, file)


def write_moves():
    '''
    write a json of all move that has a power value, has a accuracy, has a damage class of 'physical', and has a type
    :return:
    '''
    with open('modules/move.json', 'w') as file:
        move_object = {
            'count': 0,
            'next': 'https://pokeapi.co/api/v2/move',
            'results': {}
        }

        while move_object['next'] is not None:
            response = requests.get(move_object['next']).json()
            for move in response['results']:
                move_response = requests.get(move['url']).json()
                if move_response['power'] is not None and move_response['accuracy'] is not None and move_response[
                    'damage_class'] is not None and move_response['type'] is not None:
                    move_info = {
                        'name': move_response['name'],
                        'accuracy': move_response['accuracy'],
                        'power': move_response['power'],
                        'damage_class': move_response['damage_class']['name'],
                        'type': move_response['type']['name'],
                        'pp': move_response['pp']
                    }

                    move_object['results'][move_response['name']] = move_info
                    move_object['count'] += 1
                    print(move_response['name'])
            move_object['next'] = response['next']

        json.dump(move_object, file)

if __name__ == '__main__':
    write_pokemons()
