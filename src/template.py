header = r"""; ModuleID = 'std.c'
target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32-n8:16:32-S128"
target triple = "i386-pc-linux-gnu"

%union.primative = type { i32 }

@.str = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str1 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str2 = private unnamed_addr constant [3 x i8] c"%f\00", align 1
@.str3 = private unnamed_addr constant [19 x i8] c"Runtime Error: %s\0A\00", align 1
@.str4 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align  1
@.str5 = private unnamed_addr constant [4 x i8] c"%f\0A\00", align 1
@.str6 = private unnamed_addr constant [10 x i8] c"78123.326\00", align 1
@.str7 = private unnamed_addr constant [7 x i8] c"712312\00", align 1
@.str8 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@.str9 = private unnamed_addr constant [8 x i8] c"ABCDEFG\00", align 1
@.str10 = private unnamed_addr constant [19 x i8] c"Raise A Exception.\00", align 1
@.str11 = private unnamed_addr constant [26 x i8] c"Should never reach here.\0A\00", align 1
@.str12 = private unnamed_addr constant [4 x i8] c"%x\0A\00", align 1

; declare C interface

; Function Attrs: nounwind
declare noalias i8* @malloc(i32) #0

; Function Attrs: nounwind
declare void @llvm.memset.p0i8.i32(i8* nocapture, i8, i32, i32, i1) #1

declare i32 @printf(i8*, ...) #1

; Function Attrs: nounwind readonly
declare double @atof(i8*) #2

; Function Attrs: nounwind readonly
declare i32 @atoi(i8*) #2

; Function Attrs: nounwind
declare i32 @sprintf(i8*, i8*, ...) #0

; Function Attrs: nounwind
declare i32 @snprintf(i8*, i32, i8*, ...) #0

; Function Attrs: nounwind readonly
declare i32 @strlen(i8*) #2

; Function Attrs: nounwind
declare i8* @strcpy(i8*, i8*) #0

; Standard Library

define i32 @addi(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %context = alloca i32*, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i32**
  %5 = load i32** %4, align 4
  store i32* %5, i32** %context, align 4
  %6 = load i32** %context, align 4
  %7 = load i32* %6, align 4
  store i32 %7, i32* %a, align 4
  %8 = load i32** %context, align 4
  %9 = getelementptr inbounds i32* %8, i32 1
  %10 = load i32* %9, align 4
  store i32 %10, i32* %b, align 4
  %11 = load i32* %a, align 4
  %12 = load i32* %b, align 4
  %13 = add nsw i32 %11, %12
  ret i32 %13
}

; Function Attrs: nounwind
define i32 @subi(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %context = alloca i32*, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i32**
  %5 = load i32** %4, align 4
  store i32* %5, i32** %context, align 4
  %6 = load i32** %context, align 4
  %7 = load i32* %6, align 4
  store i32 %7, i32* %a, align 4
  %8 = load i32** %context, align 4
  %9 = getelementptr inbounds i32* %8, i32 1
  %10 = load i32* %9, align 4
  store i32 %10, i32* %b, align 4
  %11 = load i32* %a, align 4
  %12 = load i32* %b, align 4
  %13 = sub nsw i32 %11, %12
  ret i32 %13
}

; Function Attrs: nounwind
define i32 @muli(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %context = alloca i32*, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i32**
  %5 = load i32** %4, align 4
  store i32* %5, i32** %context, align 4
  %6 = load i32** %context, align 4
  %7 = load i32* %6, align 4
  store i32 %7, i32* %a, align 4
  %8 = load i32** %context, align 4
  %9 = getelementptr inbounds i32* %8, i32 1
  %10 = load i32* %9, align 4
  store i32 %10, i32* %b, align 4
  %11 = load i32* %a, align 4
  %12 = load i32* %b, align 4
  %13 = mul nsw i32 %11, %12
  ret i32 %13
}

; Function Attrs: nounwind
define i32 @intToReal(i32* %env) #0 {
  %1 = alloca i32*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = load i32* %3, align 4
  %5 = sitofp i32 %4 to float
  %6 = fptosi float %5 to i32
  ret i32 %6
}

define i8* @intToStr(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %dummy = alloca [1 x i8], align 1
  %n = alloca i32, align 4
  %siz = alloca i32, align 4
  %s = alloca i8*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = load i32* %3, align 4
  store i32 %4, i32* %n, align 4
  %5 = getelementptr inbounds [1 x i8]* %dummy, i32 0, i32 0
  %6 = load i32* %n, align 4
  %7 = call i32 (i8*, i32, i8*, ...)* @snprintf(i8* %5, i32 1, i8* getelementptr inbounds ([3 x i8]* @.str1, i32 0, i32 0), i32 %6) #5
  store i32 %7, i32* %siz, align 4
  %8 = load i32* %siz, align 4
  %9 = mul i32 %8, 1
  %10 = call noalias i8* @malloc(i32 %9) #5
  store i8* %10, i8** %s, align 4
  %11 = load i8** %s, align 4
  %12 = load i32* %n, align 4
  %13 = call i32 (i8*, i8*, ...)* @sprintf(i8* %11, i8* getelementptr inbounds ([3 x i8]* @.str1, i32 0, i32 0), i32 %12) #5
  %14 = load i8** %s, align 4
  ret i8* %14
}

; Function Attrs: nounwind
define i8* @realToStr(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %dummy = alloca [1 x i8], align 1
  %n = alloca float, align 4
  %siz = alloca i32, align 4
  %s = alloca i8*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to float*
  %5 = load float* %4, align 4
  store float %5, float* %n, align 4
  %6 = getelementptr inbounds [1 x i8]* %dummy, i32 0, i32 0
  %7 = load float* %n, align 4
  %8 = fpext float %7 to double
  %9 = call i32 (i8*, i32, i8*, ...)* @snprintf(i8* %6, i32 1, i8* getelementptr inbounds ([3 x i8]* @.str2, i32 0, i32 0), double %8) #5
  store i32 %9, i32* %siz, align 4
  %10 = load i32* %siz, align 4
  %11 = mul i32 %10, 1
  %12 = call noalias i8* @malloc(i32 %11) #5
  store i8* %12, i8** %s, align 4
  %13 = load i8** %s, align 4
  %14 = load float* %n, align 4
  %15 = fpext float %14 to double
  %16 = call i32 (i8*, i8*, ...)* @sprintf(i8* %13, i8* getelementptr inbounds ([3 x i8]* @.str2, i32 0, i32 0), double %15) #5
  %17 = load i8** %s, align 4
  ret i8* %17
}

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
define void @printHex(i32 %x) #0 {
  %1 = alloca i32, align 4
  store i32 %x, i32* %1, align 4
  %2 = load i32* %1, align 4
  %3 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str12, i32 0, i32 0), i32 %2)
  ret void
}

; Function Attrs: noreturn nounwind
declare void @exit(i32) #3

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

