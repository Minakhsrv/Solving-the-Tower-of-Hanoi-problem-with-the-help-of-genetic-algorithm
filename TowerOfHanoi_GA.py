import numpy as np
import matplotlib.pyplot as plt
import random
import copy

def generate_initial_population(n_pop, n_bits, num_towers=3):  #تعریف داده های ورودی اگر داریم به صورت رشته،در اینجا رندوم ایجاد شده
    pop = []
    for i in range(n_pop):
        specimen = []
        min_length = 2 ** n_bits - 1  # طول کروموزوم رو کمترین تعداد جابه جایی در نظر میگیریم

        max_length = min_length + 50   #حداکثر 50 حرکت پس از بهینگی انجام بشه
        specimen_size = random.randint(min_length, max_length)

        while len(specimen) < specimen_size:
            origin_tower = random.randint(1, num_towers)  # به صورت رندوم یک برج رو برای مبدا انتخاب می کنیم
            if len(specimen) == 0:
                origin_tower = 1

            destination_tower = random.randint(1, num_towers)  # به صورت رندوم یک برج رو برای مقصد انتخاب می کنیم
            
            element = (origin_tower, destination_tower)  # هر المنت برجمون یک مبدا و مقصدی داره که حرکت رو نشون میده
            specimen.append(element)

        pop.append(specimen)

    return pop

def fitness(specimen, n_bits, print_state=lambda x: None):  #تابع برازندگی
    #بایذ بازی با حرکات معتبر انجام بشه
    state = [[i + 1 for i in range(n_bits)], [], []]
    print_state(state)
    fitness_value = 1
    for movement in specimen:
        origin_tower = movement[0] - 1
        destination_tower = movement[1] - 1

        # نادیده گرفتن حرکات نامعتبر تا فقط حرکات مجاز انجام بشه
        if len(state[origin_tower]) == 0:
            # نمیتونیم از یک برج خالی حرکت رو شروع کنیم   حرکت نامعتبر
            fitness_value = fitness_value - 5
            continue

        origin_peg = state[origin_tower][0]
        if len(state[destination_tower]) > 0 and state[destination_tower][0] < origin_peg:
            #نمیتونیم دیسک بزرگتر رو روی یک دیسک کوپکتر قرار بدیم   حرکت نامعتبر
            fitness_value = fitness_value - 5
            continue

        state[origin_tower].pop(0)
        state[destination_tower].insert(0, origin_peg)
        print_state(state)

        if len(state[1]) == n_bits or len(state[2]) == n_bits:
        # اگر با یک حرکت کل دیسک ها از برج مبدا به مقصد منتقل بشن (یک حالت نادر یا اگه فقط یک دیسک داشته باشیم) در این صورت یک مقدار زیاد به ارزش فیتنس اضافه میکنیم
            fitness_value = fitness_value + 10000
            break
        fitness_value = fitness_value + 1

    # براساس تعداد دیسک هایی که هنوز در برج شروع مونده از برازش کم میکنیم
    fitness_value = fitness_value - len(state[0]) * 10
    # براساس تعداد حرکاتی که انجام داده از برازش کم میکنیم
    fitness_value = fitness_value - len(specimen)

    fitness_value = fitness_value + len(state[2]) * 5
    fitness_value = fitness_value + sum(state[2]) * 8
    fitness_value = fitness_value - sum(state[0]) * 15
    fitness_value = fitness_value - len(state[1]) * 5

    if len(state[2]) and state[2][-1] == n_bits:
        fitness_value = fitness_value + 400
    return fitness_value

def crossover(parents, population_len, n_bits):  #تابع تولید نسل جدید
    for i in range(population_len - 1):
        specimen = []
        while len(specimen) < 2 ** n_bits - 1:
            # با ترکیب تصادفی والدین فرزندان جدید ایجاد می کنیم
        
            parent_1, parent_2 = random.sample(parents, 2)

            pt1 = len(parent_1) // 2
            pt2 = len(parent_2) // 2

            part_1 = parent_1[:pt1]
            part_2 = parent_2[pt2:]

            random.shuffle(part_2)

            specimen = part_1
            specimen.extend(part_2)

        pop.append(specimen)
    return pop

def mutate(pop, mut_r):  #تابع جهش
    for specimen in pop:
        specimen_len = len(specimen)
        mutable_genes = random.randint(1, specimen_len)
        for gene in range(mutable_genes):
            if random.uniform(0, 1) >= mut_r:
                continue

            index = random.randint(1, specimen_len - 1)

            origin_tower = 0
            destination_tower = 0

            while origin_tower == destination_tower:
                origin_tower = random.randint(1, 3)
                destination_tower = random.randint(1, 3)

            element = (origin_tower, destination_tower)

            specimen[index] = element
    return pop

n_bits = 5  #طول رشته یا تعداد دیسک ها
n_pop = 100 #سایز جمعیت
crossover_parents_len = 10
new_specimens_size = 20  # تعداد کروموزوم های تولیدی در هر تولید نسل
num_generations = 10   #تعداد نسل ها
mut_r = 0.50 + n_bits / 15  #نرخ جهش
pop = generate_initial_population(n_pop, n_bits) #فراخوانی تابع ساخت جمعیت
#populationn_bits
len(pop)
generational_fitness = []

#لوپ اصلی
for generation in range(num_generations):
    population_fitness = [fitness(specimen, n_bits) for specimen in pop]
    population_fitness, pop = zip(*sorted(zip(population_fitness, pop), reverse=True))

    pop = list(pop)

    best_index = np.argmax(population_fitness)
    best_specimen = copy.deepcopy(pop[best_index])
    best_fitness = fitness(best_specimen, n_bits)
    generational_fitness.append(best_fitness)
    print('Generation {} best index: {}. Fitness: {}'.format(generation, best_index, best_fitness))
    print('Generation {} best specimen'.format(generation))
    print(pop[best_index])
    print('Generation {} best specimen final state'.format(generation))
    fitness(best_specimen, n_bits, lambda x: print(x))

    # فقط بهترین والدین برای تولید نسل بعد انتخاب میشوند
    parents = pop[:crossover_parents_len]

    # ساخت جمعیت جدید
    pop = crossover(parents, n_pop - new_specimens_size - 1, n_bits)
    # جهش در جمعیت جدید
    pop = mutate(pop, mut_r)

    # بهترین نمونه از همانگونه که هستند به نسل بعد میرسند برای تضمین عدم کاهش برازندگی
    pop.append(best_specimen)

    # معرفی نمونه های برتر
    new_specimens = generate_initial_population(new_specimens_size, n_bits)
    pop.extend(new_specimens)

plt.plot(generational_fitness)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.show()
