; ModuleID = 'std.c'
target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32-n8:16:32-S128"
target triple = "i386-pc-linux-gnu"

%union.primative = type { i32 }

@.str = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str1 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str2 = private unnamed_addr constant [3 x i8] c"%f\00", align 1
@.str3 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@.str4 = private unnamed_addr constant [4 x i8] c"%f\0A\00", align 1
@.str5 = private unnamed_addr constant [10 x i8] c"78123.326\00", align 1
@.str6 = private unnamed_addr constant [7 x i8] c"712312\00", align 1
@.str7 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@.str8 = private unnamed_addr constant [8 x i8] c"ABCDEFG\00", align 1

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
  %6 = call i32 @atoi(i8* %5) #3
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
  %6 = call double @atof(i8* %5) #3
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
  %7 = call i32 (i8*, i32, i8*, ...)* @snprintf(i8* %5, i32 1, i8* getelementptr inbounds ([3 x i8]* @.str1, i32 0, i32 0), i32 %6) #4
  store i32 %7, i32* %siz, align 4
  %8 = load i32* %siz, align 4
  %9 = mul i32 %8, 1
  %10 = call noalias i8* @malloc(i32 %9) #4
  store i8* %10, i8** %s, align 4
  %11 = load i8** %s, align 4
  %12 = load i32* %n, align 4
  %13 = call i32 (i8*, i8*, ...)* @sprintf(i8* %11, i8* getelementptr inbounds ([3 x i8]* @.str1, i32 0, i32 0), i32 %12) #4
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
  %9 = call i32 (i8*, i32, i8*, ...)* @snprintf(i8* %6, i32 1, i8* getelementptr inbounds ([3 x i8]* @.str2, i32 0, i32 0), double %8) #4
  store i32 %9, i32* %siz, align 4
  %10 = load i32* %siz, align 4
  %11 = mul i32 %10, 1
  %12 = call noalias i8* @malloc(i32 %11) #4
  store i8* %12, i8** %s, align 4
  %13 = load i8** %s, align 4
  %14 = load float* %n, align 4
  %15 = fpext float %14 to double
  %16 = call i32 (i8*, i8*, ...)* @sprintf(i8* %13, i8* getelementptr inbounds ([3 x i8]* @.str2, i32 0, i32 0), double %15) #4
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
  %11 = call i32 @strlen(i8* %10) #3
  %12 = load i8** %s2, align 4
  %13 = call i32 @strlen(i8* %12) #3
  %14 = add i32 %11, %13
  %15 = add i32 %14, 1
  store i32 %15, i32* %len, align 4
  %16 = load i32* %len, align 4
  %17 = mul i32 %16, 1
  %18 = call noalias i8* @malloc(i32 %17) #4
  store i8* %18, i8** %s, align 4
  %19 = load i8** %s, align 4
  %20 = load i8** %s1, align 4
  %21 = call i8* @strcpy(i8* %19, i8* %20) #4
  %22 = load i8** %s, align 4
  %23 = load i8** %s1, align 4
  %24 = call i32 @strlen(i8* %23) #3
  %25 = getelementptr inbounds i8* %22, i32 %24
  %26 = load i8** %s2, align 4
  %27 = call i8* @strcpy(i8* %25, i8* %26) #4
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
define i32 @main() #0 {
  %1 = alloca i32, align 4
  %env = alloca %union.primative*, align 4
  store i32 0, i32* %1
  %2 = call noalias i8* @malloc(i32 12) #4
  %3 = bitcast i8* %2 to %union.primative*
  store %union.primative* %3, %union.primative** %env, align 4
  %4 = load %union.primative** %env, align 4
  %5 = getelementptr inbounds %union.primative* %4, i32 0
  %6 = bitcast %union.primative* %5 to i32*
  store i32 0, i32* %6, align 4
  %7 = load %union.primative** %env, align 4
  %8 = getelementptr inbounds %union.primative* %7, i32 1
  %9 = bitcast %union.primative* %8 to i32*
  store i32 100, i32* %9, align 4
  %10 = load %union.primative** %env, align 4
  %11 = getelementptr inbounds %union.primative* %10, i32 2
  %12 = bitcast %union.primative* %11 to i32*
  store i32 3, i32* %12, align 4
  %13 = load %union.primative** %env, align 4
  %14 = bitcast %union.primative* %13 to i32*
  %15 = call i32 @addi(i32* %14)
  %16 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str3, i32 0, i32 0), i32 %15)
  %17 = load %union.primative** %env, align 4
  %18 = bitcast %union.primative* %17 to i32*
  %19 = call i32 @subi(i32* %18)
  %20 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str3, i32 0, i32 0), i32 %19)
  %21 = load %union.primative** %env, align 4
  %22 = bitcast %union.primative* %21 to i32*
  %23 = call i32 @muli(i32* %22)
  %24 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str3, i32 0, i32 0), i32 %23)
  %25 = load %union.primative** %env, align 4
  %26 = bitcast %union.primative* %25 to i32*
  %27 = call i32 @divi(i32* %26)
  %28 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str3, i32 0, i32 0), i32 %27)
  %29 = load %union.primative** %env, align 4
  %30 = getelementptr inbounds %union.primative* %29, i32 0
  %31 = bitcast %union.primative* %30 to i32*
  store i32 0, i32* %31, align 4
  %32 = load %union.primative** %env, align 4
  %33 = getelementptr inbounds %union.primative* %32, i32 1
  %34 = bitcast %union.primative* %33 to float*
  store float 0x401D4DD300000000, float* %34, align 4
  %35 = load %union.primative** %env, align 4
  %36 = getelementptr inbounds %union.primative* %35, i32 2
  %37 = bitcast %union.primative* %36 to float*
  store float 0x400AA3D700000000, float* %37, align 4
  %38 = load %union.primative** %env, align 4
  %39 = bitcast %union.primative* %38 to i32*
  %40 = call float @addr(i32* %39)
  %41 = fpext float %40 to double
  %42 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str4, i32 0, i32 0), double %41)
  %43 = load %union.primative** %env, align 4
  %44 = bitcast %union.primative* %43 to i32*
  %45 = call float @subr(i32* %44)
  %46 = fpext float %45 to double
  %47 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str4, i32 0, i32 0), double %46)
  %48 = load %union.primative** %env, align 4
  %49 = bitcast %union.primative* %48 to i32*
  %50 = call float @mulr(i32* %49)
  %51 = fpext float %50 to double
  %52 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str4, i32 0, i32 0), double %51)
  %53 = load %union.primative** %env, align 4
  %54 = bitcast %union.primative* %53 to i32*
  %55 = call float @divr(i32* %54)
  %56 = fpext float %55 to double
  %57 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str4, i32 0, i32 0), double %56)
  %58 = load %union.primative** %env, align 4
  %59 = getelementptr inbounds %union.primative* %58, i32 0
  %60 = bitcast %union.primative* %59 to i32*
  store i32 0, i32* %60, align 4
  %61 = load %union.primative** %env, align 4
  %62 = getelementptr inbounds %union.primative* %61, i32 1
  %63 = bitcast %union.primative* %62 to i8**
  store i8* getelementptr inbounds ([10 x i8]* @.str5, i32 0, i32 0), i8** %63, align 4
  %64 = load %union.primative** %env, align 4
  %65 = bitcast %union.primative* %64 to i32*
  %66 = call float @strToReal(i32* %65)
  %67 = fpext float %66 to double
  %68 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str4, i32 0, i32 0), double %67)
  %69 = load %union.primative** %env, align 4
  %70 = getelementptr inbounds %union.primative* %69, i32 0
  %71 = bitcast %union.primative* %70 to i32*
  store i32 0, i32* %71, align 4
  %72 = load %union.primative** %env, align 4
  %73 = getelementptr inbounds %union.primative* %72, i32 1
  %74 = bitcast %union.primative* %73 to i8**
  store i8* getelementptr inbounds ([7 x i8]* @.str6, i32 0, i32 0), i8** %74, align 4
  %75 = load %union.primative** %env, align 4
  %76 = bitcast %union.primative* %75 to i32*
  %77 = call i32 @strToInt(i32* %76)
  %78 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str3, i32 0, i32 0), i32 %77)
  %79 = load %union.primative** %env, align 4
  %80 = getelementptr inbounds %union.primative* %79, i32 0
  %81 = bitcast %union.primative* %80 to i32*
  store i32 0, i32* %81, align 4
  %82 = load %union.primative** %env, align 4
  %83 = getelementptr inbounds %union.primative* %82, i32 1
  %84 = bitcast %union.primative* %83 to float*
  store float 0x40F312B540000000, float* %84, align 4
  %85 = load %union.primative** %env, align 4
  %86 = bitcast %union.primative* %85 to i32*
  %87 = call i8* @realToStr(i32* %86)
  %88 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str7, i32 0, i32 0), i8* %87)
  %89 = load %union.primative** %env, align 4
  %90 = getelementptr inbounds %union.primative* %89, i32 0
  %91 = bitcast %union.primative* %90 to i32*
  store i32 0, i32* %91, align 4
  %92 = load %union.primative** %env, align 4
  %93 = getelementptr inbounds %union.primative* %92, i32 1
  %94 = bitcast %union.primative* %93 to i32*
  store i32 712312, i32* %94, align 4
  %95 = load %union.primative** %env, align 4
  %96 = bitcast %union.primative* %95 to i32*
  %97 = call i8* @intToStr(i32* %96)
  %98 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str7, i32 0, i32 0), i8* %97)
  %99 = load %union.primative** %env, align 4
  %100 = getelementptr inbounds %union.primative* %99, i32 0
  %101 = bitcast %union.primative* %100 to i32*
  store i32 0, i32* %101, align 4
  %102 = load %union.primative** %env, align 4
  %103 = getelementptr inbounds %union.primative* %102, i32 1
  %104 = bitcast %union.primative* %103 to i32*
  store i32 -1, i32* %104, align 4
  %105 = load %union.primative** %env, align 4
  %106 = bitcast %union.primative* %105 to i32*
  %107 = call i8* @intToStr(i32* %106)
  %108 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str7, i32 0, i32 0), i8* %107)
  %109 = load %union.primative** %env, align 4
  %110 = getelementptr inbounds %union.primative* %109, i32 0
  %111 = bitcast %union.primative* %110 to i32*
  store i32 0, i32* %111, align 4
  %112 = load %union.primative** %env, align 4
  %113 = getelementptr inbounds %union.primative* %112, i32 1
  %114 = bitcast %union.primative* %113 to i8**
  store i8* getelementptr inbounds ([10 x i8]* @.str5, i32 0, i32 0), i8** %114, align 4
  %115 = load %union.primative** %env, align 4
  %116 = getelementptr inbounds %union.primative* %115, i32 2
  %117 = bitcast %union.primative* %116 to i8**
  store i8* getelementptr inbounds ([8 x i8]* @.str8, i32 0, i32 0), i8** %117, align 4
  %118 = load %union.primative** %env, align 4
  %119 = bitcast %union.primative* %118 to i32*
  %120 = call i8* @concat(i32* %119)
  %121 = call i32 (i8*, ...)* @printf(i8* getelementptr inbounds ([4 x i8]* @.str7, i32 0, i32 0), i8* %120)
  ret i32 0
}

attributes #0 = { nounwind "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #2 = { nounwind readonly "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "stack-protector-buffer-size"="8" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #3 = { nounwind readonly }
attributes #4 = { nounwind }

!llvm.ident = !{!0}

!0 = metadata !{metadata !"Ubuntu clang version 3.4-1ubuntu3 (tags/RELEASE_34/final) (based on LLVM 3.4)"}
