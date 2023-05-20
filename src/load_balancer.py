from .worker import Worker

class LoadBalancer:

    def __init__(self, initial_worker_count):
        self.W_arr = [0.0] * 5
        self.worker_count: int = initial_worker_count

        self.number_of_workers_to_remove = 0
        self.number_of_workers_to_add = 0

    def balance_worker_load(self, worker_group_size: int, processing_queue_frame_count: int):
        """
        This is the main function that balances the worker load.
        W is the average number of frames in the processing queue(A) per worker(B).
        W = A / B.
        """
        A = processing_queue_frame_count

        # Number of workers. This does not include idle workers.
        # I am not sure if I am calculating this number correctly. So if B has to include idle workers,
        # then comment line bellow and uncomment the line after.
        B = max(1, (self.worker_count - worker_group_size))
        # B = self.worker_count

        W = A / B
        self.W_arr.append(W)

        # average of last 5 minutes
        average_w = sum(self.W_arr[-5:]) / 5
        if average_w > 12:
            self.number_of_workers_to_add = 5
        elif average_w < 5:
            self.number_of_workers_to_remove = min(4, max(self.worker_count - 20, 0))

    def add_workers(self, current_worker_group):
        """
        This function adds new workers to the current worker group.
        """
        for _ in range(self.number_of_workers_to_add):
            current_worker_group.append(Worker())
            self.worker_count += 1

        self.number_of_workers_to_add = 0

    def remove_workers(self, current_worker_group):
        """
        This function removes workers from the current worker group.
        Given worker group represents workers that are not busy.
        If number of workers to remove is greater than the number of workers in the group,
        then the number_of_workers_to_remove is reduced to remove workers on next iteration.
        """
        for i in range(self.number_of_workers_to_remove):
            try:
                current_worker_group.pop()
                self.worker_count -= 1
            except IndexError:
                self.number_of_workers_to_remove = self.number_of_workers_to_remove - i
                break

            self.number_of_workers_to_remove = 0
