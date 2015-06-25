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
define i32 @addi(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = load i32* %3, align 4
  store i32 %4, i32* %a, align 4
  %5 = load i32** %1, align 4
  %6 = getelementptr inbounds i32* %5, i32 2
  %7 = load i32* %6, align 4
  store i32 %7, i32* %b, align 4
  %8 = load i32* %a, align 4
  %9 = load i32* %b, align 4
  %10 = add nsw i32 %8, %9
  ret i32 %10
}

; Function Attrs: nounwind
define float @addr(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca float, align 4
  %b = alloca float, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to float*
  %5 = load float* %4, align 4
  store float %5, float* %a, align 4
  %6 = load i32** %1, align 4
  %7 = getelementptr inbounds i32* %6, i32 2
  %8 = bitcast i32* %7 to float*
  %9 = load float* %8, align 4
  store float %9, float* %b, align 4
  %10 = load float* %a, align 4
  %11 = load float* %b, align 4
  %12 = fadd float %10, %11
  ret float %12
}

; Function Attrs: nounwind
define i32 @subi(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = load i32* %3, align 4
  store i32 %4, i32* %a, align 4
  %5 = load i32** %1, align 4
  %6 = getelementptr inbounds i32* %5, i32 2
  %7 = load i32* %6, align 4
  store i32 %7, i32* %b, align 4
  %8 = load i32* %a, align 4
  %9 = load i32* %b, align 4
  %10 = sub nsw i32 %8, %9
  ret i32 %10
}

; Function Attrs: nounwind
define float @subr(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca float, align 4
  %b = alloca float, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to float*
  %5 = load float* %4, align 4
  store float %5, float* %a, align 4
  %6 = load i32** %1, align 4
  %7 = getelementptr inbounds i32* %6, i32 2
  %8 = bitcast i32* %7 to float*
  %9 = load float* %8, align 4
  store float %9, float* %b, align 4
  %10 = load float* %a, align 4
  %11 = load float* %b, align 4
  %12 = fsub float %10, %11
  ret float %12
}

; Function Attrs: nounwind
define i32 @muli(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = load i32* %3, align 4
  store i32 %4, i32* %a, align 4
  %5 = load i32** %1, align 4
  %6 = getelementptr inbounds i32* %5, i32 2
  %7 = load i32* %6, align 4
  store i32 %7, i32* %b, align 4
  %8 = load i32* %a, align 4
  %9 = load i32* %b, align 4
  %10 = mul nsw i32 %8, %9
  ret i32 %10
}

; Function Attrs: nounwind
define float @mulr(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca float, align 4
  %b = alloca float, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to float*
  %5 = load float* %4, align 4
  store float %5, float* %a, align 4
  %6 = load i32** %1, align 4
  %7 = getelementptr inbounds i32* %6, i32 2
  %8 = bitcast i32* %7 to float*
  %9 = load float* %8, align 4
  store float %9, float* %b, align 4
  %10 = load float* %a, align 4
  %11 = load float* %b, align 4
  %12 = fmul float %10, %11
  ret float %12
}

; Function Attrs: nounwind
define i32 @divi(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca i32, align 4
  %b = alloca i32, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = load i32* %3, align 4
  store i32 %4, i32* %a, align 4
  %5 = load i32** %1, align 4
  %6 = getelementptr inbounds i32* %5, i32 2
  %7 = load i32* %6, align 4
  store i32 %7, i32* %b, align 4
  %8 = load i32* %a, align 4
  %9 = load i32* %b, align 4
  %10 = sdiv i32 %8, %9
  ret i32 %10
}

; Function Attrs: nounwind
define float @divr(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca float, align 4
  %b = alloca float, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to float*
  %5 = load float* %4, align 4
  store float %5, float* %a, align 4
  %6 = load i32** %1, align 4
  %7 = getelementptr inbounds i32* %6, i32 2
  %8 = bitcast i32* %7 to float*
  %9 = load float* %8, align 4
  store float %9, float* %b, align 4
  %10 = load float* %a, align 4
  %11 = load float* %b, align 4
  %12 = fdiv float %10, %11
  ret float %12
}

; Function Attrs: nounwind
define float @eqi(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %a = alloca float, align 4
  %b = alloca float, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to float*
  %5 = load float* %4, align 4
  store float %5, float* %a, align 4
  %6 = load i32** %1, align 4
  %7 = getelementptr inbounds i32* %6, i32 2
  %8 = bitcast i32* %7 to float*
  %9 = load float* %8, align 4
  store float %9, float* %b, align 4
  %10 = load float* %a, align 4
  %11 = load float* %b, align 4
  %12 = fcmp oeq float %10, %11
  %13 = zext i1 %12 to i32
  %14 = sitofp i32 %13 to float
  ret float %14
}

; Function Attrs: nounwind
define void @print(i32* %env) #0 {
  %1 = alloca i32*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i8*
  %5 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([3 x i8]* @.str, i32 0, i32 0), i8* %4)
  ret void
}

declare i32 @printf(i8*, ...) #1

; Function Attrs: nounwind
define i32 @strToInt(i32* %env) #0 {
  %1 = alloca i32*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i8**
  %5 = load i8** %4, align 4
  %6 = call i32 @atoi(i8* %5) #4
  ret i32 %6
}

; Function Attrs: nounwind readonly
declare i32 @atoi(i8*) #2

; Function Attrs: nounwind
define float @strToReal(i32* %env) #0 {
  %1 = alloca i32*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i8**
  %5 = load i8** %4, align 4
  %6 = call double @atof(i8* %5) #4
  %7 = fptrunc double %6 to float
  ret float %7
}

; Function Attrs: nounwind readonly
declare double @atof(i8*) #2

; Function Attrs: nounwind
define i32 @realToInt(i32* %env) #0 {
  %1 = alloca i32*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = load i32* %3, align 4
  %5 = uitofp i32 %4 to float
  %6 = fptosi float %5 to i32
  ret i32 %6
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

; Function Attrs: nounwind
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
declare i32 @snprintf(i8*, i32, i8*, ...) #0

; Function Attrs: nounwind
declare noalias i8* @malloc(i32) #0

; Function Attrs: nounwind
declare i32 @sprintf(i8*, i8*, ...) #0

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
define i8* @concat(i32* %env) #0 {
  %1 = alloca i32*, align 4
  %s1 = alloca i8*, align 4
  %s2 = alloca i8*, align 4
  %len = alloca i32, align 4
  %s = alloca i8*, align 4
  store i32* %env, i32** %1, align 4
  %2 = load i32** %1, align 4
  %3 = getelementptr inbounds i32* %2, i32 1
  %4 = bitcast i32* %3 to i8**
  %5 = load i8** %4, align 4
  store i8* %5, i8** %s1, align 4
  %6 = load i32** %1, align 4
  %7 = getelementptr inbounds i32* %6, i32 2
  %8 = bitcast i32* %7 to i8**
  %9 = load i8** %8, align 4
  store i8* %9, i8** %s2, align 4
  %10 = load i8** %s1, align 4
  %11 = call i32 @strlen(i8* %10) #4
  %12 = load i8** %s2, align 4
  %13 = call i32 @strlen(i8* %12) #4
  %14 = add i32 %11, %13
  %15 = add i32 %14, 1
  store i32 %15, i32* %len, align 4
  %16 = load i32* %len, align 4
  %17 = mul i32 %16, 1
  %18 = call noalias i8* @malloc(i32 %17) #5
  store i8* %18, i8** %s, align 4
  %19 = load i8** %s, align 4
  %20 = load i8** %s1, align 4
  %21 = call i8* @strcpy(i8* %19, i8* %20) #5
  %22 = load i8** %s, align 4
  %23 = load i8** %s1, align 4
  %24 = call i32 @strlen(i8* %23) #4
  %25 = getelementptr inbounds i8* %22, i32 %24
  %26 = load i8** %s2, align 4
  %27 = call i8* @strcpy(i8* %25, i8* %26) #5
  %28 = load i32* %len, align 4
  %29 = sub nsw i32 %28, 1
  %30 = load i8** %s, align 4
  %31 = getelementptr inbounds i8* %30, i32 %29
  store i8 0, i8* %31, align 1
  %32 = load i8** %s, align 4
  ret i8* %32
}

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

; Function Attrs: noreturn nounwind
declare void @exit(i32) #3

"""

# @.str = private unnamed_addr constant [14 x i8] c"Hello world!\0A\00", align 1

main = """ ; Function Attrs: nounwind
define i32 @main() #0 {{

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

