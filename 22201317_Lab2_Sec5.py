#Task1
import random
with open("input_data.txt", "r") as input_file:
    n, t = map(int, input_file.readline().strip().split())
    course_list = []
    for i in range(n):
        course_list.append(input_file.readline().strip())  
def initialize_population(num_courses, num_slots, population_size):
    initial_popu = []
    for i in range(population_size):
        chromosome = []
        for j in range(num_courses * num_slots):
            chromosome.append(random.choice([0, 1]))
        initial_popu.append(chromosome)
    return initial_popu
def evaluate_fitness(chromosomes, num_courses, num_slots):
    fit_scores = []
    for chromosome in chromosomes:
        penal_over = 0
        penal_incons = 0
        for slot in range(num_slots):
            start = slot * num_courses
            end = start + num_courses
            slot_courses = chromosome[start:end]
            courses_in_slot = sum(slot_courses)
            if courses_in_slot > 1:
                penal_over += courses_in_slot - 1
        for course in range(num_courses):
            occurr = sum(chromosome[course::num_courses])
            if occurr != 1:
                penal_incons += abs(occurr - 1)
        fit_scores.append(-(penal_over + penal_incons))     
    return fit_scores
def select_parents(population):
    return random.sample(population, 2)
def perform_crossover(parent1, parent2):
    cross_point = random.randint(1, len(parent1) - 1)
    off_spring1 = parent1[:cross_point] + parent2[cross_point:]
    off_spring2 = parent2[:cross_point] + parent1[cross_point:]
    return off_spring1, off_spring2
def mutate(chromosome):
    idx = random.randint(0, len(chromosome) - 1)
    chromosome[idx] = 1 - chromosome[idx]
    return chromosome
def genetic_algo(num_courses, num_slots, population_size=10, max_generations=50):
    gene_popu = initialize_population(num_courses, num_slots, population_size)
    best_sol = None
    best_fit = float("-inf")
    global parents_twocross1
    global parents_twocross2
    parents_twocross1,parents_twocross2 =select_parents(gene_popu)
    for k in range(max_generations):
        fit_scores = evaluate_fitness(gene_popu, num_courses, num_slots)
        #print(fit_scores)
        #print(gene_popu)
        for i in range(len(gene_popu)):
            if fit_scores[i] > best_fit:
                best_fit = fit_scores[i]
                best_sol = gene_popu[i]
        if best_fit == 0:
            return best_sol, best_fit
        else:
            new_popu = []
            while len(new_popu)/2 < population_size:
                parent1, parent2 = select_parents(gene_popu)
                mut1,mut2=perform_crossover(parent1, parent2)
                offspring1 = mutate(mut1)
                offspring2 = mutate(mut2)
                #print(mut2)
                #offspring1 = mutate(perform_crossover(parent1, parent2)[0])
                #print(perform_crossover(parent1, parent2)[1])
                #offspring2 = mutate(perform_crossover(parent1, parent2)[1])
                #print(perform_crossover(parent1, parent2)[1])
                new_popu.extend([offspring1, offspring2])
                #print(new_popu)
            fit_scores = evaluate_fitness(new_popu, num_courses, num_slots)
            population_fit = []
            for i in range(len(new_popu)):
                population_fit.append((new_popu[i], fit_scores[i]))    
            population_fit.sort(key=lambda x: x[1], reverse=True)
            gene_popu = []
            #print(population_fit)
            for chromosome, _ in population_fit[:population_size]:
                gene_popu.append(chromosome)
            print(gene_popu)    
    return best_sol, best_fit
final_solution, final_fitness = genetic_algo(n, t)
#Task2
def two_point_crossover(parent_one, parent_two):
    cross_point_one = random.randint(1, len(parent_one) - 2)
    cross_point_two = random.randint(cross_point_one + 1, len(parent_one) - 1)
    offspring_one = parent_one[:cross_point_one] + parent_two[cross_point_one:cross_point_two] + parent_one[cross_point_two:]
    offspring_two = parent_two[:cross_point_one] + parent_one[cross_point_one:cross_point_two] + parent_two[cross_point_two:]
    return offspring_one, offspring_two
off_two_one,off_two_two=two_point_crossover(parents_twocross1,parents_twocross2)
with open("output_data.txt", "w") as output_file:
    output_file.write("Task 1:\n")
    output_file.write("".join(map(str, final_solution)) + "\n")
    output_file.write(str(final_fitness) + "\n")
    output_file.write("Task2:\n")
    output_file.write("Parents\n")
    output_file.write("".join(map(str, parents_twocross1)) + "\n")
    output_file.write("".join(map(str, parents_twocross2)) + "\n")
    output_file.write("Offspring\n")
    output_file.write("".join(map(str, off_two_one)) + "\n")
    output_file.write("".join(map(str, off_two_two)) + "\n")