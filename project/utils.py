def parser_estimate(time: str) -> int:
    helper = {'m': 0, 'h': 0, 'd': 0, 'w': 0, }
    step = 0
    time = time.replace(' ', '')
    for i, sym in enumerate(time):
        if not sym.isdigit():
            helper[sym] = time[step:i]
            step = i + 1
    return int(helper['w']) * 5 * 8 * 60 + int(helper['d']) * 8 * 60 + int(helper['h']) * 60 + int(helper['m'])


def parser_to_str(time: int) -> str:
    helper = {'w': 0, 'd': 0, 'h': 0, 'm': 0}
    helper['w'] = time // (5 * 8 * 60)
    time -= int(helper['w']) * 5 * 8 * 60
    helper['d'] = time // (8 * 60)
    time -= int(helper['d']) * 8 * 60
    helper['h'] = time // 60
    time -= int(helper['h']) * 60
    helper['m'] = time
    dir = {k: v for k, v in helper.items() if helper[k] != 0}
    res_str = ''
    for k, v in dir.items():
        res_str += str(dir[k]) + k + ' '
    return res_str
