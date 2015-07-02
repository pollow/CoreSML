val it : int = 
  let
    val add10 : int -> int = fn 0 : int => addi { 1 = 10, 2 = 10 }
  in
    print (intToStr (add10 0)); 0
  end

