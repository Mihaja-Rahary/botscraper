def parse_int_safe(x):
    if not x: return 0
    s = ''.join(ch for ch in str(x) if ch.isdigit())
    try:
        return int(s)
    except:
        return 0

def compute_score(likes):
    n = parse_int_safe(likes)
    return round(n ** 0.5, 2)
