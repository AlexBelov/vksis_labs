pol = '110111'

def div(a,b):
    res = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            res += '0'
        else:
            res += '1'
    return res.lstrip('0')

while(True):
    msg = raw_input('').rstrip('\n')

    i = 0
    # msg = msg.lstrip('0') # ????
    a = msg[i:i+len(pol)]
    i += len(pol)
    res = div(a, pol)

    while True:
        if i+len(pol)-len(res) > len(msg):
            res += msg[i:]
            break
        a = res + msg[i:i+len(pol)-len(res)]
        i += len(pol)-len(res)
        res = div(a, pol)

    result = ''
    if len(res) < len(pol)-1:
        for i in range(len(pol) - 1 - len(res)):
            result += '0'
        result += res
    else:
        result += res

    print result
