
"""
Class that represents a process.
@author Felipe Garcia
@version 1.0
"""
class Process:
  """
  Constructor of the class, initializes all its attributes.
  """
  def __init__(self, name: str, bt: str, at: str, q: str, p: str) -> None:
    self.__name: str = name
    self.__bt: int = int(bt)
    self.__at: int = int(at)
    self.__q: int = int(q)
    self.__p: int = int(p)
    self.__wt: int = 0
    self.__ct: int = 0
    self.__rt: int = None
    self.__tat: int = 0
    self.__status: str = "new"
    self.__time_exe: int = 0

  """
  Method that assigns the value of the response time if it is the first time the process is being executed. Changes the state to 'running' if it was in 'ready'. Increases the time_exe counter, which tracks how much time has been executed. Checks if the process has finished; if so, it changes its state to 'finished' and completes the assignment of the metric values.
  @param t Scheduler time.
  """
  def run(self, t) -> None:
    if self.__status == "ready":
      self.__status = "running"
      if self.__rt == None:
        self.__rt = t - 1
    
    self.__time_exe += 1

    if self.__time_exe == self.__bt:
      self.status = "finished"
      self.__ct = t
      self.__tat = self.__ct - self.__at

  """
  Method used to increment the waiting time of the process while it is in the ready state.
  """
  def wait(self) -> None:
    self.__wt += 1

  @property
  def wt(self) -> int:
    return self.__wt
  
  @property
  def ct(self) -> int:
    return self.__ct
  
  @property
  def rt(self) -> int:
    return self.__rt
  
  @property
  def tat(self) -> int:
    return self.__tat

  @property
  def time_exe(self) -> int:
    return self.__time_exe

  @property
  def q(self) -> int:
    return self.__q

  @property
  def at(self) -> int:
    return self.__at
  
  @property
  def status(self) -> str:
    return self.__status
  
  @status.setter
  def status(self, value) -> None:
    self.__status = value
  
  @at.setter
  def at(self, value) -> None:
    self.__at = value

  """
  Method that allows us to compare by the values of bt (burst time) used in the Shortest Job First (SJF) algorithm; this is used as the key in a sort function.
  """
  @classmethod
  def by_bt(cls, process) -> int:
    return process.__bt
  
  """
  Method that allows us to compare by the values of remaining completion time used in the Shortest Time to Completion First (STCF) algorithm; this is used as the key in a sort function.
  """
  @classmethod
  def by_remaining_completion(cls, process) -> int:
    return process.__bt - process.__time_exe
  
  """
  Method that allows us to compare by priority values to sort them within the implementations.
  """
  @classmethod
  def by_p(cls, process) -> int:
    return process.__p
  
  """
  Method that allows us to compare by arrival time values used in the First-Come First-Served (FCFS) algorithm; this is used as the key in a sort function.
  """
  @classmethod
  def by_at(cls, process) -> int:
    return process.__at

  """
  Method used to obtain all the data and metrics of a process.
  return A string containing all the data of the process.
  """
  def __str__(self) -> str:
    return f"{self.__name}; {self.__bt}; {self.__at}; {self.__q}; {self.__p}; {self.__wt}; {self.__ct}; {self.__rt}; {self.__tat}"