#include "calc.h"
#include <stdio.h>

int calc_add(int a, int b) {
    return a + b;
}

int calc_multiply(int a, int b) {
    return a * b;
}

static char greeting_buffer[256];

const char* calc_greeting(const char* name) {
    snprintf(greeting_buffer, sizeof(greeting_buffer), "Hello, %s!", name ? name : "world");
    return greeting_buffer;
}
