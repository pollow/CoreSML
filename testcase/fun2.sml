val it = 
  let 
    val f : {1 : int, 2 : int } -> int = fn {1 = 0, 2 = 0} => (print "HaHa"; 10) | {...} => (print "WoW!"; 20) 
  in 
    print (intToStr (f {1 = 2, 2 = 0})); 0 
  end

