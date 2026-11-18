# -*- coding: utf-8 -*-
"""Robit, la mascota del proyecto, en pixel art de 20 x 30."""
from pixel import put, norm

HEAD = [
    "........KKKK........",
    ".......KRHRRK.......",
    ".......KRRRrK.......",
    "........KKKK........",
    ".........KK.........",
    ".........KK.........",
    "...KKKKKKKKKKKKKK...",
    "..KHHYYYYYYYYYYYyK..",
    "..KHYYYYYYYYYYYYyK..",
    "..KYYWWWYYYYWWWYyK..",
    "..KYYWKWYYYYWKWYyK..",
    "..KYYWWWYYYYWWWYyK..",
    "..KYPYYYYYYYYYYPyK..",
    "..KYYYKYYYYYYKYYyK..",
    "..KYYYYKKKKKKYYYyK..",
    "..KyyyyyyyyyyyyyyK..",
    "..KKKKKKKKKKKKKKKK..",
    ".......KssssK.......",
]
BODY = [
    "...KKKKKKKKKKKKKK...",
    "...KLLBBBBBBBBBbK...",
    "...KLBBBBBBBBBBbK...",
    "...KLBBKKKKKKBBbK...",
    "...KLBBKGgRrKBBbK...",
    "...KLBBKKKKKKBBbK...",
    "...KLBBBBBBBBBBbK...",
    "...KbbbbbbbbbbbbK...",
    "...KKKKKKKKKKKKKK...",
]
LEGS_STAND = [
    ".....KsSK..KsSK.....",
    ".....KsSK..KsSK.....",
    "....KKKKK..KKKKK....",
]
LEGS_STEP = [
    ".....KsSK..KsSK.....",
    "....KKKKK..KsSK.....",
    "...........KKKKK....",
]
ARM_DOWN_L = ["KK.", "KSK", "KSK", "KSK", "KsK", "KKK"]
ARM_DOWN_R = [".KK", "KSK", "KSK", "KSK", "KsK", "KKK"]
ARM_UP_R = [
    ".KKKK",
    ".KSSK",
    ".KSSK",
    ".KKKK",
    "..KSK",
    "..KSK",
    "..KSK",
    "..KSK",
    "..KSK",
    "..KSK",
    "KKKSK",
    "KKKKK",
]

def compose(arm_l='down', arm_r='down', legs='stand', eyes='open'):
    g = HEAD + BODY + (LEGS_STAND if legs == 'stand' else LEGS_STEP)
    g = ['..' + r + '..' for r in norm(g)]
    top = len(HEAD)                 # fila donde empieza el cuerpo
    if arm_l == 'down': g = put(g, 2, top + 1, ARM_DOWN_L)
    if arm_r == 'down': g = put(g, 19, top + 1, ARM_DOWN_R)
    if arm_r == 'up':   g = put(g, 18, top - 9, ARM_UP_R)
    if arm_l == 'up':   g = put(g, 1, top - 9, [r[::-1] for r in ARM_UP_R])
    if eyes == 'happy':
        g = put(g, 7, 9, ["YKYYYYYYKY", "KYKYYYYKYK", "YYYYYYYYYY"])
    return g

ROBIT1 = compose()                                  # de pie
ROBIT2 = compose(arm_r='up', legs='step')           # saluda y da un paso
ROBIT3 = compose(arm_l='up', arm_r='up', eyes='happy')  # celebra

# Llavero: anilla de 7 x 7 con agujero de 3 x 3 sobre la antena (sustituye la bola)
RING = [
    "..KKKKKKK..",
    "..KKKKKKK..",
    "..KK...KK..",
    "..KK...KK..",
    "..KK...KK..",
    "..KKKKKKK..",
    "..KKKKKKK..",
]
def keychain_grid():
    body = norm(ROBIT1[4:])                     # sin la bola de la antena
    ring = [("......." + r + "......")[:24] for r in RING]
    return norm(ring + body)
