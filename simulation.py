import simpy

class TargetSystem:
    def __init__(self, env, processing_rate, target_password):
        self.env = env
        self.processing_rate = processing_rate
        self.queue = []
        self.target_password = target_password

        # metric variables and/or other parameters
        self.total_wait_time = 0
        self.measure_queue_length = []
        self.processed_passwords = 0

        # start methods as a separate process within environment
        self.env.process(self.process_password())

    def process_password(self):
        while True:

            if self.queue:
                if self.processed_passwords % 10 == 0:
                    self.measure_queue_length.append(len(self.queue))
                password, arrival_time = self.queue[0]
                self.queue.pop(0)
                self.processed_passwords += 1

                waiting_time = self.env.now - arrival_time
                self.total_wait_time += waiting_time

                if password == self.target_password:
                    print(f"Password found : {password}")
                    print(f"Number password tested: {self.processed_passwords}")
                    print(f"Simulation ended at: {env.now}")
                    print(f"Average wait time: {self.total_wait_time / self.processed_passwords}")
                    print(f"Average queue length: {sum(self.measure_queue_length) / len(self.measure_queue_length)}")
                    end_event.succeed()
                    break

            yield self.env.timeout(1 / self.processing_rate)

class AttackSystem:
    def __init__(self, env, arrival_rate, target_system, filename):
        self.env = env
        self.arrival_rate = arrival_rate
        self.target_system = target_system
        self.filename = filename

        self.env.process(self.attack_event())

    def attack_event(self):
        with open(self.filename, "r") as file:
            for line in file:
                password = line.strip()
                arrival_time = self.env.now
                self.target_system.queue.append((password, arrival_time))
                yield self.env.timeout(1 / self.arrival_rate)
    
if __name__ == "__main__":
    env = simpy.Environment()
    end_event = env.event()

    # variables
    arrival_rate = 1000
    service_rate = 1000
    target_password = "test"

    generatedPass_file = "four_characters.txt"

    # initialization
    target_system = TargetSystem(env, service_rate, target_password)
    attack_system = AttackSystem(env, arrival_rate, target_system, generatedPass_file)
    
    env.run(until=end_event)

    print(f"Server Utilization: {arrival_rate / service_rate}")

