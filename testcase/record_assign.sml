val it : int = 
  let 
    val {x = a : int, y = b : real} : {x : int, y : real}= { x = 0, y = 3.3 }
  in
    a
  end
