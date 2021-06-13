def parser_estimate(time: str) -> int:
    helper = {'m': 0, 'h': 0, 'd': 0, 'w': 0, }
    step = 0
    time = time.replace(' ', '')
    for i, sym in enumerate(time):
        if not sym.isdigit():
            helper[sym] = time[step:i]
            step = i + 1
    return int(helper['w']) * 5 * 8 * 60 + int(helper['d']) * 8 * 60 + int(helper['h']) * 60 + int(helper['m'])
