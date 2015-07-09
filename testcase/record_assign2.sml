val it : int = 
  let 
    val {1 = x : int, 2 = y : int, 3 = {1 = a : int, 2 = b : int} : {1 : int, 2 : int} } : {1:int, 2:int, 3: {1:int, 2:int}} = {1 = 3, 2 = 6, 3 = {1 = 10, 2 = 9} } 
  in 
    print (intToStr y); 0
  end 
