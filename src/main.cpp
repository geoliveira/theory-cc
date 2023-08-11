#include <stdio.h>
#include <iostream>

#include "model.hpp"

using namespace std;

int main(void) {
    Variable x;
    x.print();

first_instruction:
    x = x + 1;
    x.print();

second_instruction:
    x = x - 1;
    x.print();

third_instruction:
    x = x - 2;
    x.print();

    if (x >= 1) {
        x.print();
        goto first_instruction;
    }

    x.print();

    return 0;
}
