from random import randint

def roll(number_of_dice, number_of_sides):
    dice_pool = []
    i = 0
    while i <= number_of_dice:
        dieroll = randint(1, number_of_sides)
        dice_pool.append(dieroll)
        i += 1
    return sum(dice_pool)
