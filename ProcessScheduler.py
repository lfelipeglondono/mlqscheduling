from Process import Process

"""
Class that represents a process scheduler.
@author Felipe Garcia
@version 1.0
"""
class ProcessScheduler:
  """
  Constructor of the class, initializes all its attributes.
  """
  def __init__(self) -> None:
    self.__processes: list = []
    self.__currentq: int = 0
    self.__time: int = 0
    self.__flag: bool = False
    self.__program: str = ""

    self.__wt_avg: int = 0
    self.__ct_avg: int = 0
    self.__rt_avg: int = 0
    self.__tat_avg: int = 0

  """
  Method that retrieves the process data from the program, creates a Process object for each process, and adds them to the process list.
  @params program File name with its extension.
  """
  def load_program(self, program: str) -> None:
    self.__program = program

    try:
      with open(f'programs/{program}', 'r') as f:
        data_processes = [line.strip() for line in f.readlines() if not line.startswith('#')]

        for data in data_processes:
          self.__processes.append(Process(*[process.rstrip(';') for process in data.split()]))
    except FileNotFoundError:
      print(f'Error: El archivo {program} no se encontró.')
    except Exception as e:
        print(f'Error al procesar {program}: {e}')

  """
  Method that adds the results obtained into a plain text file (.txt).
  """
  def write_results(self) -> None:
    result: str = f"# archivo: {self.__program}\n#Politica: RR(3), RR(5), FCFS\n"
    result += "# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n"

    for process in self.__processes:
      result += str(process) + "\n"
    
    result += f"\nWT={self.__wt_avg}; CT={self.__ct_avg}; RT={self.__rt_avg}; TAT={self.__tat_avg}\n\n###########################################\n\n"

    with open('results.txt', 'a') as file:
      file.write(result)

  """
  """
  def mlq(self) -> None:
    min_at = min(process.at for process in self.__processes)
    if min_at != 0:
      for process in self.__processes:
        process.at = process.at - min_at

    while not self.__finished_processes(self.__processes):
      self.__check()

      self.__flag = False

      if self.__currentq == 1:
        self.__rr(3, 1)

      elif self.__currentq == 2:
        self.__rr(5, 2)
      
      elif self.__currentq == 3:
        self.__fcfs(3)

    self.__wt_avg = round(sum(process.wt for process in self.__processes) / len(self.__processes), 1)
    self.__ct_avg = round(sum(process.ct for process in self.__processes) / len(self.__processes), 1)
    self.__rt_avg = round(sum(process.rt for process in self.__processes) / len(self.__processes), 1)
    self.__tat_avg = round(sum(process.tat for process in self.__processes) / len(self.__processes), 1)

  """
  Method that checks if a process has arrived to assign it the state of 'ready'; if so, it activates a flag so that when an algorithm is executing, it can exit (depending on whether it is preemptive or non-preemptive). It also assigns the attribute 'currentq' to the smallest active queue, to take it into account for the MLQ (Multi-Level Queue).
  """
  def __check(self) -> None:
    if not self.__finished_processes(self.__processes):
      for process in self.__processes:
        if process.at == self.__time:
          process.status = "ready"
          self.__flag = True

      self.__currentq = min(process.q for process in self.__processes if process.status != "finished" and process.status != 'new')

  """
  Method that implements the Round Robin algorithm, in which only the processes from the specified queue are assigned, which is passed as a parameter.
  @param quantum Determines how often a running process will be preempted to give way to the next one in the queue.
  @param queue Determines which queue this algorithm belongs to.
  """
  def __rr(self, quantum, queue) -> None:
    quantum_count: int = 0
    index: int = 0

    process_rr: list = [process for process in self.__processes if process.q == queue and process.status == "ready"]
    process_rr.sort(key= Process.by_p, reverse=True)

    while not self.__finished_processes(process_rr):
      self.__time += 1
      quantum_count += 1

      process_rr[index].run(self.__time)

      for process in self.__processes:
        if process.status == "ready":
          process.wait()

      self.__check()
      
      if process_rr[index].status == 'finished':
        process_rr.pop(index)
        quantum_count = quantum + 1

      if self.__flag and process_rr and self.__currentq < process_rr[0].q:
        process_rr[index].status = "ready"
        break

      if index >= len(process_rr) or (process_rr and quantum_count % quantum == 0):
        if self.__flag and process_rr and self.__currentq == process_rr[0].q:
          process_rr[index].status = "ready"
          process_rr = [process for process in self.__processes if process.q == queue and process.status == "ready"]
          self.__flag = False
        if index < len(process_rr):
          process_rr[index].status = "ready"
        if index >= len(process_rr) - 1:
          index = 0
        else:
          index += 1

  """
  Method that implements the SJF algorithm, in which only the processes from the specified queue are assigned, which is passed as a parameter.
  @param queue Determines which queue this algorithm belongs to.
  """
  def __sjf(self, queue: int) -> None:
    process_run: Process = None

    processes_sjf: list = [process for process in self.__processes if process.q == queue and process.status == "ready"]
    processes_sjf.sort(key= Process.by_p, reverse=True)

    while not self.__finished_processes(processes_sjf) or process_run:
      processes_sjf.sort(key = Process.by_bt)

      if not process_run:
        process_run = processes_sjf.pop(0)

      self.__time += 1

      process_run.run(self.__time)

      if process_run.status == "finished":
        process_run = None

      for process in self.__processes:
        if process.status == "ready":
          process.wait()

      self.__check()
      
      if self.__flag and not process_run:
        break

  """
  Method that implements the STCF algorithm, in which only the processes from the specified queue are assigned, which is passed as a parameter.
  @param queue Determines which queue this algorithm belongs to.
  """
  def __stcf(self, queue: int) -> None:
    processes_stcf: list = [process for process in self.__processes if process.q == queue and process.status == "ready"]
    processes_stcf.sort(key= Process.by_p, reverse=True)

    while not self.__finished_processes(processes_stcf):
      processes_stcf.sort(key = Process.by_remaining_completion)

      self.__time += 1

      processes_stcf[0].run(self.__time)

      if processes_stcf[0].status == 'finished':
        processes_stcf.pop(0)

      for process in self.__processes:
        if process.status == "ready":
          process.wait()

      self.__check()

      if self.__flag and processes_stcf and self.__currentq < processes_stcf[0].q:
        processes_stcf[0].status = "ready"
        break

  """
  Method that implements the FCFS algorithm, in which only the processes from the specified queue are assigned, which is passed as a parameter.
  @param queue Determines which queue this algorithm belongs to.
  """
  def __fcfs(self, queue) -> None:
    process_run: Process = None

    processes_fcfs: list = [process for process in self.__processes if process.q == queue and process.status == "ready"]
    processes_fcfs.sort(key= Process.by_p, reverse=True)
    processes_fcfs.sort(key= Process.by_at, reverse=True)

    while not self.__finished_processes(processes_fcfs) or process_run:
      if not process_run:
        process_run = processes_fcfs.pop(0)

      self.__time += 1

      process_run.run(self.__time)

      if process_run.status == "finished":
        process_run = None

      for process in self.__processes:
        if process.status == "ready":
          process.wait()

      self.__check()

      if self.__flag and not process_run:
        break

  """
  Method that checks if all the processes in the list passed as a parameter have finished.
  @param process Process that is intended to be verified.
  @return A boolean that determines if all processes have finished.
  """
  def __finished_processes(self, processes: list) -> bool:
    for process in processes:
      if process.status != "finished":
        return False
      
    return True
  
  """
  Method that clears the results file.
  """
  @classmethod
  def clean_file(self) -> None:
    with open('results.txt', 'w', encoding='utf-8') as file:
        pass