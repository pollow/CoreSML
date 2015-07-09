val it : int = 
  let 
    val {1 = x, 2 = y, 3 = {1 = a, 2 = b}} = {1 = 3, 2 = 6, 3 = {1 = 10, 2 = 9} } 
  in 
    print (intToStr a); 0
  end 
