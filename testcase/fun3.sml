val it = 
  let 
    val f : int -> unit = fn x => (print (intToStr x); f (addi {1 = 1, 2 = x})) | 100 => (print (intToStr x))
  in 
    print (intToStr (f {1 = 2, 2 = 0})); 0 
  end


