"""
Interpreter for the Stack-based esolang
"""
import sys, time
from random import randint


def quiterr(x):
    print(x)
    sys.exit()


def parse(cmd, fmt, varl):
    r = []
    if len(cmd) - 1 != len(fmt):
        quiterr("Syntax error")
    for i, j in enumerate(fmt):
        if j == "r":
            if cmd[i + 1] in varl:
                r.append(varl[cmd[i + 1]])
            else:
                quiterr("Undefined variable")
        elif j == "i":
            if cmd[i + 1].isdigit():
                r.append(int(cmd[i + 1]))
            else:
                quiterr("Syntax error")
        else:
            r.append(cmd[i + 1])
    return r


def stack_based(c, timeout=None):
    c = c.strip()
    try:
        c = [i.split(";")[0].strip() for i in c.split("\n")]
        while "" in c:
            c.remove("")
        c = "\n".join(c)
        if not c:
            return  # to accept empty programs
        cmds = [
            (
                [j.lower() for j in i.split(" ")]
                if i.split()[0].lower() != "p"
                else ["p", i.split('"')[1]]
            )
            for i in c.split("\n")
        ]
    except:
        quiterr("Syntax error")
    stack = []
    varl = {}
    ip = 0

    def _pop():
        if not stack:
            quiterr("Empty error")
        return stack.pop()

    def _top():
        if not stack:
            quiterr("Empty error")
        return stack[-1]

    def var(cmd, ip):
        q = parse(cmd, "w", varl)
        varl[q[0]] = 0
        return ip + 1

    def i(cmd, ip):
        q = parse(cmd, "w", varl)
        if q[0] not in varl:
            quiterr("Undefined variable")
        varl[q[0]] = int(input())
        if varl[q[0]] < 0:
            quiterr("Negative error")
        return ip + 1

    def o(cmd, ip):
        q = parse(cmd, "r", varl)
        print(q[0])
        return ip + 1

    def ic(cmd, ip):
        q = parse(cmd, "w", varl)
        if q[0] not in varl:
            quiterr("Undefined variable")
        c = sys.stdin.read(1)
        varl[q[0]] = ord(c) if c else 0
        return ip + 1

    def oc(cmd, ip):
        q = parse(cmd, "r", varl)
        print(chr(q[0]), end="")
        return ip + 1

    def p(cmd, ip):
        if len(cmd) != 2:
            quiterr("Syntax error")
        print(cmd[1], end="")
        return ip + 1

    def s(cmd, ip):
        q = parse(cmd, "wi", varl)
        if q[0] not in varl:
            quiterr("Undefined variable")
        varl[q[0]] = q[1]
        return ip + 1

    def a(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = q[0] + q[1]
        return ip + 1

    def su(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = q[0] - q[1]
        if varl[q[2]] < 0:
            quiterr("Negative error")
        return ip + 1

    def m(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = q[0] * q[1]
        return ip + 1

    def Q(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        if q[1] == 0:
            quiterr("Division error")
        varl[q[2]] = q[0] // q[1]
        return ip + 1

    def R(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        if q[1] == 0:
            varl[q[2]] = 0
        varl[q[2]] = q[0] % q[1]
        return ip + 1

    def C(cmd, ip):
        q = parse(cmd, "rw", varl)
        if q[1] not in varl:
            quiterr("Undefined variable")
        varl[q[1]] = q[0]
        return ip + 1

    def push(cmd, ip):
        q = parse(cmd, "r", varl)
        stack.append(q[0])
        return ip + 1

    def pop(cmd, ip):
        if len(cmd) == 1:
            _pop()
        else:
            q = parse(cmd, "w", varl)
            if q[0] not in varl:
                quiterr("Undefined variable")
            varl[q[0]] = _pop()
        return ip + 1

    def top(cmd, ip):
        q = parse(cmd, "w", varl)
        if q[0] not in varl:
            quiterr("Undefined variable")
        varl[q[0]] = _top()
        return ip + 1

    def sz(cmd, ip):
        q = parse(cmd, "w", varl)
        if q[0] not in varl:
            quiterr("Undefined variable")
        varl[q[0]] = len(stack)
        return ip + 1

    def lt(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = 1 if q[0] < q[1] else 0
        return ip + 1

    def gt(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = 1 if q[0] > q[1] else 0
        return ip + 1

    def le(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = 1 if q[0] <= q[1] else 0
        return ip + 1

    def ge(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = 1 if q[0] >= q[1] else 0
        return ip + 1

    def eq(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = 1 if q[0] == q[1] else 0
        return ip + 1

    def ne(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = 1 if q[0] != q[1] else 0
        return ip + 1

    def ja(cmd, ip):
        q = parse(cmd, "ri", varl)
        if q[0]:
            return ip + q[1]
        else:
            return ip + 1

    def jb(cmd, ip):
        q = parse(cmd, "ri", varl)
        if q[0]:
            return ip - q[1]
        else:
            return ip + 1

    def nop(cmd, ip):
        return ip + 1

    def halt(cmd, ip):
        sys.exit()

    def rnd(cmd, ip):
        q = parse(cmd, "w", varl)
        if q[0] not in varl:
            quiterr("Undefined variable")
        varl[q[0]] = randint(0, 1)
        return ip + 1

    def And(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = int(bool(q[0]) and bool(q[1]))
        return ip + 1

    def Or(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = int(bool(q[0]) or bool(q[1]))
        return ip + 1

    def Not(cmd, ip):
        q = parse(cmd, "rw", varl)
        if q[1] not in varl:
            quiterr("Undefined variable")
        varl[q[1]] = int(not bool(q[0]))
        return ip + 1

    def bnd(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = q[0] & q[1]
        return ip + 1

    def bor(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = q[0] | q[1]
        return ip + 1

    def xor(cmd, ip):
        q = parse(cmd, "rrw", varl)
        if q[2] not in varl:
            quiterr("Undefined variable")
        varl[q[2]] = q[0] ^ q[1]
        return ip + 1

    cmddict = {
        "var": var,
        "i": i,
        "o": o,
        "ic": ic,
        "oc": oc,
        "p": p,
        "s": s,
        "a": a,
        "su": su,
        "m": m,
        "q": Q,
        "r": R,
        "c": C,
        "push": push,
        "pop": pop,
        "top": top,
        "sz": sz,
        "lt": lt,
        "gt": gt,
        "le": le,
        "ge": ge,
        "eq": eq,
        "ne": ne,
        "ja": ja,
        "jb": jb,
        "nop": nop,
        "halt": halt,
        "rnd": rnd,
        "and": And,
        "or": Or,
        "not": Not,
        "bnd": bnd,
        "bor": bor,
        "xor": xor,
    }
    if timeout:
        starttime = time.time()
    while 0 <= ip < len(cmds):
        if timeout:
            if time.time() - starttime > timeout:
                sys.exit()
        if cmds[ip][0] not in cmddict:
            quiterr("Syntax error")
        ip = cmddict[cmds[ip][0]](cmds[ip], ip)
