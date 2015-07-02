val it = 
  let 
    val f : int -> int = fn x : int => addi { 1 = x, 2 = 10 } 
  in 
    print (intToStr (f 25)); 0 
  end
