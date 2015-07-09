val it = 
  let 
    val s = "Goodbye World!\n"
  in
    let
      val s = "Hello World!\n"
    in
      print s
    end;
    print s; 0
  end
