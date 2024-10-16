from os import listdir
from ProcessScheduler import ProcessScheduler

def main():
  ProcessScheduler.clean_file()
  for program in listdir('programs'):
    scheduler: ProcessScheduler = ProcessScheduler()
    scheduler.load_program(program)
    scheduler.mlq()
    scheduler.write_results()
  # scheduler = ProcessScheduler()
  # scheduler.load_program('mlq025.txt')
  # scheduler.mlq()
  # scheduler.write_results()
  
main()