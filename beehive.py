from random import *
import time
import os


class Bee:
    _max_age = 10
    _max_weight = 10.0
    __gender = 'default'

    def __init__(self, bid, weight, age):
        self.weight = weight
        self.age = age
        self.bid = bid

    def eat_honey(self, honey):
        eat_size = self.weight / 5.0
        if honey < eat_size:
            return 'dead', honey
        else:
            if self.weight < self._max_weight:
                self.weight += eat_size
                self.weight = round(self.weight, 1)
                honey -= eat_size
                return self.__gender, honey
            else:
                self.weight = self._max_weight
                return self.__gender, honey

    def lvl_up(self):
        if self.age >= self._max_age:
            return 'dead'
        else:
            self.age += 1
            return 'life'

    def get_info(self):
        return f'    id: {self.bid}   weight:  {self.weight}   age:  {self.age}'


class BeeF(Bee):
    __gender = 'female'

    def __init__(self, bid, weight, age):
        super().__init__(bid, weight, age)

    def new_egg(self):
        pass

    @staticmethod
    def get_eff(honey):
        return round(honey / 2.0)


class BeeM(Bee):
    __gender = 'male'
    __defEggs = 2

    def __init__(self, bid, weight, age):
        super().__init__(bid, weight, age)

    def new_egg(self):
        pass

    def get_eff(self):
        return randint(1, self.__defEggs)


class Baby:
    __bees = ['worker', 'male', 'worker', 'male']
    __future_bee = None

    __weight = 1.0
    __max_weight = 3.0
    __eat_size = 1.0
    __delay = 2

    def __init__(self):
        self.__future_bee = self.__bees[randint(0, 3)]
        pass

    def d_delay(self):
        self.__delay -= 1
        if self.__delay <= 0:
            return 'born'
        else:
            return 'embryo'

    def trans_to_bee(self):
        return self.__future_bee

    def eat_honey(self, honey):
        if honey < self.__eat_size:
            return 'dead', honey

        if self.__weight >= self.__max_weight:
            return self.trans_to_bee(), honey
        else:
            self.__weight += self.__eat_size
            honey -= self.__eat_size
            gender = self.d_delay()
            return gender, honey

    def get_info(self):
        return f'  future bee: {self.__future_bee}    weight: {self.__weight}   delay: {self.__delay}'


class BeeW(Bee):
    __gender = 'worker'

    def __init__(self, bid, weight, age):
        super().__init__(bid, weight, age)

    def get_honey(self):
        return self.weight * randint(1, 4) / 5.5

    def clean_hive(self):
        pass


class Hive:
    __honey = 20.0
    __age = 0
    __state = 'life'

    mother_eggs = 0
    father_eggs = 0
    eggs = 0

    babies = []

    def __init__(self, bee_f, bees_m, bees_w):
        self.bee_f = bee_f
        self.bees_m = bees_m
        self.bees_w = bees_w

    def count_eggs(self):
        self.mother_eggs = BeeF.get_eff(self.__honey)
        fathers_eff = 0
        for bee in self.bees_m:
            fathers_eff += bee.get_eff()
        self.father_eggs = fathers_eff
        self.eggs = abs(self.mother_eggs - self.father_eggs)

    def print_info(self):
        mom_eff = BeeF.get_eff(self.__honey)
        fathers_eff = 0
        for bee in self.bees_m:
            fathers_eff += bee.get_eff()
        print()
        print(f'  Hive age: {self.__age}                Honey: {self.__honey}')
        print(f'  Mother efficiency: {mom_eff}      Father efficiency: {fathers_eff}      Eggs: {self.eggs}')
        print()
        print('  Mother:')
        print(self.bee_f.get_info())
        print()
        print('  Fathers:')
        for bee in self.bees_m:
            print(bee.get_info())
        print()
        print('  Workers:')
        for bee in self.bees_w:
            print(bee.get_info())
        print()
        print('  Babies:')
        if self.babies != []:
            for baby in self.babies:
                print(baby.get_info())

    def i_age(self):
        self.__age += 1

    def gen_honey(self):
        for bee in self.bees_w:
            self.__honey += bee.get_honey()
            self.__honey = round(self.__honey, 1)

    def dead(self):
        self.__state = 'dead'

    def spent_honey(self, ids):
        for bee in self.bees_m:
            gender, honey = bee.eat_honey(self.__honey)
            self.__honey = honey
            if gender == 'dead':
                self.bees_m.remove(bee)
        for bee in self.bees_w:
            gender, honey = bee.eat_honey(self.__honey)
            self.__honey = honey
            if gender == 'dead':
                self.bees_w.remove(bee)

        if self.babies != []:
            for baby in self.babies:
                gender, honey = baby.eat_honey(self.__honey)
                self.__honey = honey
                if gender == 'dead':
                    self.babies.remove(baby)
                if gender != 'dead':
                    if gender == 'male':
                        self.babies.remove(baby)
                        self.bees_m.append(BeeM(ids[randint(20, 80)], randint(1, 3), randint(1, 3)))
                    elif gender == 'worker':
                        self.babies.remove(baby)
                        self.bees_w.append(BeeW(ids[randint(20, 80)], randint(1, 3), randint(1, 3)))

        gender, honey = self.bee_f.eat_honey(self.__honey)

        if gender == 'dead':
            self.dead()
        self.__honey = round(self.__honey, 1)

    def lvl_up(self):
        for bee in self.bees_m:
            bee_state = bee.lvl_up()
            if bee_state == 'dead':
                self.bees_m.remove(bee)
        for bee in self.bees_w:
            bee_state = bee.lvl_up()
            if bee_state == 'dead':
                self.bees_w.remove(bee)

    def get_state(self):
        return self.__state, self.__age

    def spawn_babies(self):
        for i in range(self.eggs):
            self.babies.append(Baby())

    def balance(self):
        self.babies = self.babies[0:10]
        self.bees_w = self.bees_w[0:10]
        self.bees_m = self.bees_m[0:10]


def gen_ids():
    rand_chars = ['a', 'b', 'c', 'd', '1', '2', '3']
    ids = []
    for i in range(100):
        shuffle(rand_chars)
        ids.append(''.join(rand_chars))
    return ids


def dead(age):
    print('DDDDD  EEEEE   AAA   DDDDD')
    print('D   D  E      A   A  D   D')
    print('D   D  EEEEE  AAAAA  D   D')
    print('D   D  E      A   A  D   D')
    print('DDDDD  EEEEE  A   A  DDDDD')
    print()
    print(f'         Hive age: {age}    ')
    print()


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


ids = gen_ids()

hive = Hive(
    BeeF(ids[0], 5, 1),
    [
        BeeM(ids[1], 1, 1),
        BeeM(ids[2], 1, 3),
        BeeM(ids[3], 6, 4)
    ],
    [
        BeeW(ids[6], 1, 1),
        BeeW(ids[7], 2, 1),
        BeeW(ids[8], 3, 3),
        BeeW(ids[9], 1, 1),
        BeeW(ids[10], 2, 2),
        BeeW(ids[11], 3, 1),
        BeeW(ids[12], 2, 1),
        BeeW(ids[13], 4, 5),
        BeeW(ids[14], 5, 1),
        BeeW(ids[15], 1, 4),
        BeeW(ids[16], 2, 2)
    ]
)

next_id = 20

while True:
    clear()
    state = hive.get_state()
    if state[0] == 'dead':
        clear()
        dead(state[1])
        break
    hive.print_info()
    hive.gen_honey()
    hive.spent_honey(ids)
    hive.count_eggs()
    hive.spawn_babies()
    hive.balance()
    hive.lvl_up()
    hive.i_age()
    time.sleep(1)
