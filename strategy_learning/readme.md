1. "mql5 and communicatie" communicate each other with "frozendll."

  frozendll.dll is to provide shared memory.
  mql5 is run in Metaquete5. Metaquete5 uses its original langauge mql5. It is based on old stype c++.
  mql5 receives prices data from the broker's server and send them to communicate with frozendll.dll.
  communicate receives data from mql5 and saves them on disk. It makes totally 6 files, *.dat.
  
  
