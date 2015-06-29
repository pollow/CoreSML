#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

union primative {
    int i;
    float r;
    const char *s;
    char c;
};

int addi(uint32_t *env) {
    // add up two integer and return the sum.
    uint32_t *context = (uint32_t *)*(uint32_t **)(env+1);
    int a = (int)*(int *)(context);
    int b = (int)*(int *)(context+1);

    return a + b;
}

int subi(uint32_t *env) {
    // sub up two integer and return the sum.
    uint32_t *context = (uint32_t *)*(uint32_t **)(env+1);
    int a = (int)*(int *)(context);
    int b = (int)*(int *)(context+1);

    return a - b;
}

int muli(uint32_t *env) {
    // mul up two integer and return the sum.
    uint32_t *context = (uint32_t *)*(uint32_t **)(env+1);
    int a = (int)*(int *)(context);
    int b = (int)*(int *)(context+1);

    return a * b;
}

int divi(uint32_t *env) {
    // div up two integer and return the sum.
    uint32_t *context = (uint32_t *)*(uint32_t **)(env+1);
    int a = (int)*(int *)(context);
    int b = (int)*(int *)(context+1);

    return a / b;
}

int eqi(uint32_t *env) {
    // div up two integer and return the sum.
    uint32_t *context = (uint32_t *)*(uint32_t **)(env+1);
    int a = (int)*(int *)(context);
    int b = (int)*(int *)(context+1);

    return a == b;
}

float addr(uint32_t *env) {
    // add up two integer and return the sum.
    float *context = (float *)*(float **)(env+1);
    float a = (float)*(float *)(context);
    float b = (float)*(float *)(context+1);

    return a + b;
}

float subr(uint32_t *env) {
    // sub up two integer and return the sum.
    float *context = (float *)*(float **)(env+1);
    float a = (float)*(float *)(context);
    float b = (float)*(float *)(context+1);

    return a - b;
}

float mulr(uint32_t *env) {
    // mul up two integer and return the sum.
    float *context = (float *)*(float **)(env+1);
    float a = (float)*(float *)(context);
    float b = (float)*(float *)(context+1);


    return a * b;
}

float divr(uint32_t *env) {
    // div up two integer and return the sum.
    float *context = (float *)*(float **)(env+1);
    float a = (float)*(float *)(context);
    float b = (float)*(float *)(context+1);

    return a / b;
}

void print(uint32_t *env) {
    printf("%s", *(char **)(env+1));
    return;
}

int strToInt(uint32_t *env) {
    return atoi(*(char **)(env+1));
}

float strToReal(uint32_t *env) {
    return atof(*(char **)(env+1));
}

int realToInt(uint32_t *env) {
    return (int)(float)*(env+1);
}

int intToReal(uint32_t *env) {
    return (float)(int)*(env+1);
}

char *intToStr(uint32_t *env) {
    char dummy[1];
    int n = (int)*(int *)(env+1);
    int siz = snprintf(dummy, sizeof dummy, "%d", n);
    char *s = (char *)malloc(siz*sizeof(char));
    sprintf(s, "%d", n);
    return s;
}

char *realToStr(uint32_t *env) {
    char dummy[1];
    float n = (float)*(float *)(env+1);
    int siz = snprintf(dummy, sizeof dummy, "%f", n);
    char *s = (char *)malloc(siz*sizeof(char));
    sprintf(s, "%f", n);
    return s;
}

char *concat(uint32_t *env) {
    uint32_t *context = (uint32_t *)*(uint32_t **)(env+1);
    char *s1 = *(char **)(context);
    char *s2 = *(char **)(context + 1);
    int len = (strlen(s1)+strlen(s2)+1);
    char *s = (char *)malloc(len*sizeof(char));
    strcpy(s, s1);
    strcpy(s+strlen(s1), s2);
    s[len-1] = 0;
    return s;
}

void rtError(const char *s) {
    printf("Runtime Error: %s\n", s);
    exit(0);
}

int main() {
    union primative *env = (union primative *)malloc(3 * sizeof(union primative));
    env[0].i = 0; env[1].i = 100; env[2].i = 3;
    printf("%d\n", addi((uint32_t *)env));
    printf("%d\n", subi((uint32_t *)env));
    printf("%d\n", muli((uint32_t *)env));
    printf("%d\n", divi((uint32_t *)env));

    env[0].i = 0; env[1].r = 7.326; env[2].r = 3.33;
    printf("%f\n", addr((uint32_t *)env));
    printf("%f\n", subr((uint32_t *)env));
    printf("%f\n", mulr((uint32_t *)env));
    printf("%f\n", divr((uint32_t *)env));

    env[0].i = 0; env[1].s = "78123.326";
    printf("%f\n", strToReal((uint32_t *)env));
    env[0].i = 0; env[1].s = "712312";
    printf("%d\n", strToInt((uint32_t *)env));

    env[0].i = 0; env[1].r = 78123.326;
    printf("%s\n", realToStr((uint32_t *)env));
    env[0].i = 0; env[1].i = 712312;
    printf("%s\n", intToStr((uint32_t *)env));
    env[0].i = 0; env[1].i = -1;
    printf("%s\n", intToStr((uint32_t *)env));

    env[0].i = 0; env[1].s = "78123.326"; env[2].s = "ABCDEFG";
    print((uint32_t *)env);
    printf("%s\n", concat((uint32_t *)env));

    rtError("Raise A Exception.");

    printf("Should never reach here.\n");
    return 0;
}

