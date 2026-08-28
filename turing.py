from typing import NamedTuple

class StateRule(NamedTuple):
    name: str
    read: str
    write: str
    direction: str
    new_state: str

def parse_states(states):
    states += ','
    parsed_states = []
    new_rule = []

    for char in states:
        if char == ' ':
            continue
        if char == ',':
            #add new rule to parsed states
            parsed_states.append(StateRule(new_rule[0], new_rule[1], new_rule[2], new_rule[3], new_rule[4]))
            new_rule = []
            continue

        new_rule.append(char)

    return parsed_states

def find_state(state_name, state_table, read_val):
    for state in state_table:
        if state.name == state_name and state.read == read_val:
            return state
    raise ValueError(f'No state of name {state_name} with read value of {read_val}')

def write_to_string(index, char, string):
    return string[:index] + char + string[index+1:]

def execute(state_table, tape, max_iters, initial_pos = 0):
    head_pos = initial_pos
    read_val = tape[head_pos]
    current_state = find_state(state_table[0].name, state_table, read_val)

    print('state | head | tape | counter')

    counter = 0
    while counter < max_iters:
        
        print(f'{current_state.name}{current_state.read} | {head_pos} | {tape} | step: {counter}')
        
        #write value
        tape = write_to_string(head_pos, current_state.write, tape)

        #move the head pos
        if current_state.direction.upper() == 'R':
            head_pos += 1
            if head_pos >= len(tape):
                tape += '0'
        elif current_state.direction.upper() == 'L':
            head_pos -= 1
            if head_pos < 0:
                tape = '0' + tape
                head_pos = 0

        #go to new state
        read_val = tape[head_pos]
        if current_state.new_state.upper() == 'H':
            break #halt
        current_state = find_state(current_state.new_state, state_table, read_val)

        counter += 1
    return tape

def main():
    print('Input the state machine as a series of states in the form of [state][read][write][direction][newState], separated by commas:')
    print('EX: A10RB, A00RA, B01LA, B11RH')
    raw_states = input('$ ')
    tape = input('Input an initial tape (input default for an empty tape): \n')
    if tape == 'default' or tape == '':
        tape = '0'
        initial_pos = 0
    
    else:
        #check for invalid characters
        for char in tape:
            if char != '0' and char != '1':
                raise ValueError(f'Invalid character input in tape: {char}')

        try:
            initial_pos = int(input('Input initial head position: '))
        except ValueError:
            print('Invalid character. Please input an integer')        
    
    parsed_states = parse_states(raw_states)
    print('')
    print(execute(parsed_states, tape, 1000, initial_pos))
main()