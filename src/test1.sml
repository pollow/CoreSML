val a = 10;
val (a,b,c) = (1,2,3);
val [a,b,c]=[1,2,3];
val a={name="abc", age=20};
val a = let val m = 1 in m * 2 end;
datatype bool = true | false;
datatype card = square | queen | king;
case x of 
    [] => []
    | x::xs => xs;
val a = fn x=>x*2+1;
if a>0 andalso b<0 orelse c>0 then fn x=>x*2+1 else false;
fun f(xs:int)= 
	case xs of 
	1 => 1
	|2 => 2 
