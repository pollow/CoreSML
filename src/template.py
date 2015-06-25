header = r"""; ModuleID = 'std.c'
target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32-n8:16:32-S128"
target triple = "i386-pc-linux-gnu"

%union.primative = type { i32 }

@.str = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str1 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str2 = private unnamed_addr constant [3 x i8] c"%f\00", align 1
@.str3 = private unnamed_addr constant [19 x i8] c"Runtime Error: %s\0A\00", align 1
@.str4 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@.str5 = private unnamed_addr constant [4 x i8] c"%f\0A\00", align 1
@.str6 = private unnamed_addr constant [10 x i8] c"78123.326\00", align 1
@.str7 = private unnamed_addr constant [7 x i8] c"712312\00", align 1
@.str8 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@.str9 = private unnamed_addr constant [8 x i8] c"ABCDEFG\00", align 1
@.str10 = private unnamed_addr constant [19 x i8] c"Raise A Exception.\00", align 1
@.str11 = private unnamed_addr constant [26 x i8] c"Should never reach here.\0A\00", align 1

; Function Attrs: nounwind
define void @print(i32* %env) #0 {
  %1 = alloca i32*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i8**
  %5 = load i8** %4, align 4
  %6 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([3 x i8]* @.str, i32 0, i32 0), i8* %5)
  ret void
}

declare i32 @printf(i8*, ...) #1

; Function Attrs: nounwind readonly
declare i32 @strlen(i8*) #2

; Function Attrs: nounwind
declare i8* @strcpy(i8*, i8*) #0

; Function Attrs: nounwind
define void @rtError(i8* %s) #0 {
  %1 = alloca i8*, align 4
  store i8* %s, i8** %1, align 4
  %2 = load i8** %1, align 4
  %3 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([19 x i8]* @.str3, i32 0, i32 0), i8* %2)
  call void @exit(i32 0) #6
  unreachable
                                                  ; No predecessors!
  ret void
}

; Function Attrs: nounwind
declare noalias i8* @malloc(i32) #0


; Function Attrs: noreturn nounwind
declare void @exit(i32) #3

; Function Attrs: nounwind
declare void @llvm.memset.p0i8.i32(i8* nocapture, i8, i32, i32, i1) #1

@string1 = private unnamed_addr constant [13 x i8] c"Hello World\0A\00", align 1

"""

# @.str = private unnamed_addr constant [14 x i8] c"Hello world!\0A\00", align 1

main = """ ; Function Attrs: nounwind
define i32 @main() #0 {{
  %scope = alloca i32*, align 4
  %1 = call noalias i8* @malloc(i32 16) nounwind
  %2 = bitcast i8* %1 to i32*
  store i32* %2, i32** %scope, align 4
  %3 = load i32** %scope, align 4
  %4 = bitcast i32* %3 to i8*
  call void @llvm.memset.p0i8.i32(i8* %4, i8 1, i32 16, i32 4, i1 false)
  ; scope = [parent, built-in function env which should be zero]

{}

}}


"""

tail = r"""
attributes #0 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind readonly "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { noreturn nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #4 = { nounwind readonly }
attributes #5 = { nounwind }
attributes #6 = { noreturn nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Ubuntu clang version 3.4-1ubuntu3 (tags/RELEASE_34/final) (based on LLVM 3.4)"}
"""

