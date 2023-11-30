import numpy as np

lam = 3                                                                                             # arrival rate
mu = 2                                                                                              # service rate

max_time = float(input("Enter the maximum simulation time: "))                                        #user input for  how much time simulation will run
num_runs = int(input("Enter the number of simulation runs: "))                                        #for how many time the simulation would perform 


class Simulation:                                                           #
    def __init__(self):                                                    
        self.num_in_system = 0                                                                         # intially number of customers are zero
        self.clock = 0.0                                                                               # #intially clock is zero as it will take current time which event is performed
        self.t_depart = float("inf")                                                                   ##intially the departure value stores infinity because there is no departure before arrival
        self.num_arrivals = 0                                                                          #intially total number of arrivals are zero ,gradually it is incremented
        self.num_departs = 0                                                                           #intially total number of departure are zero ,gradually it is incremented
        self.total_service_time = 0.0                                                                  # it will store the total service time
        self.server_busy_time = 0.0                                                                    #it will provide how much time server is busy in processing the jobs ,intially its zero
        self.event_list = []                                                                           #it is a list that keeps track of the events(arrival or departture) scheduled to occur in the simulation
        self.arrival_times = []                                                                        # it is a list that keeps updation of arrival times
        self.departure_times = []                                                                      # it is a list that keeps updation of departure times
        self.waiting_times = []                                                                        # it is a waiting time of a customer in a queue of being served
       # self.turnaround_times = []                                                                     #it will store the complete time each process takes to complete 

    def generate_interarrival(self):                                                                   #define a generate arrival function which will generate randomly inter arrival time
        return np.random.exponential(1 / lam)

    def initialize_event_list(self):                                                                   #define a function for generating a calender of arrival time and departure time
        arrival_time = self.generate_interarrival()                                                    #it will store the first arrival i.e the inter arrival
        self.event_list.append(('arrival', arrival_time))                                              #it will update the event list with arrival time
        self.event_list.append(('departure', float('inf')))                                            #it will update later the departure event but intially it takes infinty value as departure

    def generate_service(self):                                                                         #this function is used to generate the random service time taken by a customer
        return np.random.exponential(1 / mu)

    def handle_arrival_event(self):                                                                     #this function will handle the complete arrival event
        self.num_in_system += 1                                                                         #if there is arrival in the system then it will increment to 1
        last_arrival_time = self.arrival_times[-1] if self.arrival_times else 0.0                       #it will store the last arrival time if its there otherwise 0
        arrival_time = last_arrival_time + self.generate_interarrival()                                 #it will store the value current arrival (last arrival and the interarrival of current arrival)
        self.event_list.append(('arrival', arrival_time))                                               # it will append the arrival time in the event list calender
        self.num_arrivals += 1                                                                          # if there is arrival then it will increment the number of arrivals
        self.arrival_times.append(arrival_time)                                                         # it will append the arrival time

        service_time = self.generate_service()                                                          #it will take the values of random generate service time

        if self.num_in_system == 1:                                                                      #it will check the condition if there is customer in the system then it will perform the rest calculation
            departure = self.clock + service_time                                                        #it will the store the value as per the current clock and service time
            waiting_time = 0.0                                                                           #if the departure happens before the arrival of next event then waiting time is 0
        else:
            departure = max(arrival_time, self.departure_times[-1]) + service_time                       #in this condition we will check which value is greater last departure or arrival of current as per that we add with service time
            waiting_time = max(0, self.departure_times[-1] - arrival_time)                               # first it will check which one is maximum the difference or 0

        self.departure_times.append(departure)                                                           #it will append the departure time
        self.waiting_times.append(waiting_time)                                                          #it will append the waiting time
        self.total_service_time += service_time                                                          #it will store complete service time
        self.clock = arrival_time                                                                        #it will update the self clock
        print(f"Arrival at {arrival_time:.2f}, Inter-arrival Time: {arrival_time - last_arrival_time:.2f}, Service Time: {service_time:.2f}, Departure at: {departure:.2f}, Waiting Time: {waiting_time:.2f}")

    def handle_departure_event(self):                                                                     #this func will handle the departure event
        self.num_in_system -= 1                                                                           #it will decrement the cumstomer from the system
        self.num_departs += 1                                                                             #it will increment the value of departure of the customer

        if self.num_in_system > 0:                                                                        #it will check if the num of customers in the system is greater then 0
            service_time = self.generate_service()                                                        #it will take the service time
            departure = self.clock + service_time                                                         #it will store the departure as per the current clock and service time
            waiting_time = max( 0, self.departure_times[-1] - self.arrival_times[self.num_departs])       #again we are calculating the waiting time just handling the departure counter how many departure happend

            self.departure_times.append(departure)
            self.waiting_times.append(waiting_time)
            self.total_service_time += service_time

            self.t_depart = departure
            self.event_list.append(('departure', departure))
            self.clock = self.t_depart
        else:
            self.t_depart = float("inf")
            self.departure_times.append(self.clock)
            self.waiting_times.append(0)

    def simulate(self, max_time):
        self.initialize_event_list()

        while self.clock < max_time:
            event_type, event_time = min(self.event_list, key=lambda x: x[1])                             #it will take the minumum value from the event list
            self.clock = event_time
            self.event_list.remove((event_type, event_time))

            if event_type == 'arrival':
                self.handle_arrival_event()
            elif event_type == 'departure':
                self.handle_departure_event()

    def simulate_multiple_runs(self, max_time, num_runs):
        simulation_results = []

        for _ in range(num_runs):
            self.__init__()  # Reset simulation state for each run
            self.simulate(max_time)
            simulation_results.append({
                "num_arrivals": self.num_arrivals,
                "num_departs": self.num_departs,
                "mean_num_customers": self.num_in_system / self.clock,
                "mean_response_time": np.mean(self.waiting_times) + np.mean(self.total_service_time),
                "throughput": self.num_arrivals / self.clock,
                "utilization": self.total_service_time / self.clock,
                "arrival_times": self.arrival_times
            })

        return simulation_results


# Created an instance of the Simulation class
simulation = Simulation()

# Simulate the queue system for multiple runs
simulation_results = simulation.simulate_multiple_runs(max_time, num_runs)

# Print the simulation results for each run
for i, result in enumerate(simulation_results):
    print(f"Simulation {i + 1} results:")
    # print(f"Number of arrivals: {result['num_arrivals']}")
    # print(f"Number of departures: {result['num_departs']}")
    print(f"Mean number of customers: {result['mean_num_customers']}")
    print(f"Mean response time: {result['mean_response_time']}")
    print(f"Throughput: {result['throughput']}")
    print(f"Utilization: {result['utilization']}")
    print()

# Calculate confidence level using the standard error of the mean
confidence_level_response_time = 1.96 * np.std([result['mean_response_time']for result in simulation_results]) / np.sqrt(num_runs) #This constant value corresponds to the critical value for a 95 % confidence interval in a standard normal distribution.
confidence_level_throughput = 1.96 *  np.std([result['throughput']for result in simulation_results]) / np.sqrt(num_runs)
confidence_level_utilization = 1.96 * np.std([result['utilization']for result in simulation_results]) / np.sqrt(num_runs)

# Calculate variance
variance_response_time = np.var([result['mean_response_time'] for result in simulation_results])
variance_throughput = np.var([result['throughput']for result in simulation_results])
variance_utilization = np.var([result['utilization']for result in simulation_results])

# Calculate mean time interval
mean_time_interval = np.mean([max(result['arrival_times']) -min(result['arrival_times']) for result in simulation_results])

print(f"Confidence Level (response time): {confidence_level_response_time}")
print(f"Variance (response time): {variance_response_time}")
print()
print(f"Confidence Level (throughput): {confidence_level_throughput}")
print(f"Variance (throughput): {variance_throughput}")
print()
print(f"Confidence Level (utilization): {confidence_level_utilization}")
print(f"Variance (utilization): {variance_utilization}")
print()
print(f"Mean time interval: {mean_time_interval}")
