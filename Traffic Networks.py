import random
import numpy as np

class Car:
    def __init__(self, initial_position, initial_velocity):
        self.position = initial_position
        self.v = initial_velocity
        self.distance_to_next = 1
    
    def __repr__(self):
        return 'V:'+str(self.v)+' P:'+str(self.position)
    
    def accelerate(self, v_max):
        if self.distance_to_next > self.v + 1 and v_max > self.v:
            self.v += 1
        
    def decelerate(self):
        if self.v >= self.distance_to_next:
            self.v = self.distance_to_next - 1
        
    def randomise(self, p):
        if self.v > 0 and random.random() < p:
            self.v -= 1  
            
    def change_speed(self, v_max, p):
        self.accelerate(v_max)
        self.decelerate()
        self.randomise(p)
    
    
    def move(self):
        self.position += self.v
        
        
class Road:
    def __init__(self, length, density, p, v_max):
        self.length = length
        self.p = p
        self.density = density
        self.v_max = v_max
        self.cars = []
        self.build_road()
        
    def __repr__(self):
        return str(self.cars)
        
    def build_road(self):
        for position in range(self.length):
            if random.random() < self.density:
                self.cars.append(Car(initial_position = position, initial_velocity = int(np.round(self.v_max*random.random()))))
            else:
                self.cars.append(' ')
    
    def timestep(self):
        # assigning car distances
        for position, car in enumerate(self.cars):
            if car != ' ':
                car.distance_to_next = 1
                for i in range(1, self.length - position):
                    if self.cars[position + i] == ' ':
                        car.distance_to_next += 1
                    else:
                        break
                car.distance_to_next = car.distance_to_next
        
        # making copy for new road
        next_road = [' '] * self.length
        
        # move cars
        for position, car in enumerate(self.cars):
            # if not an empty slot
            if car != ' ':
                car.change_speed(self.v_max, self.p)
                car.move()
                # think I need to add 1 here
                if position + 1 + car.v < self.length:
                    next_road[position + car.v] = car
                else:
                    next_road[position] = ' '
           
        # new car entering
        if next_road[0] == ' ' and random.random() < 0.5:
            next_road[0] = Car(initial_position = 0, initial_velocity = int(np.round(self.v_max*random.random())))
        
        self.cars = next_road
            
            
