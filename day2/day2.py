def parse_input_line(line):
    # returns (id, max red, max green, max blue)
    prefix, game = line.split(':')
    game_id = int(prefix.split()[1])
    red = green = blue = 0
    for info in game.split(';'):
        for amount, color in map(str.split, info.split(',')):
            match color:
                case 'red':
                    red = max(red, int(amount))
                case 'green':
                    green = max(green, int(amount))
                case 'blue':
                    blue = max(blue, int(amount))
                case _:
                    raise ValueError
    return (game_id, red, green, blue)


def part1():
    result = 0
    with open('input') as file:
        for line in file:
            game_id, red, green, blue = parse_input_line(line)
            if red <= 12 and green <= 13 and blue <= 14:
                result += game_id
    return result


def part2():
    result = 0
    with open('input') as file:
        for line in file:
            game_id, red, green, blue = parse_input_line(line)
            result += red*green*blue
    return result
