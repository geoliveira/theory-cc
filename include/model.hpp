#ifndef MODEL_H
#define MODEL_H

#include <stdio.h>
#include <iostream>

using namespace std;

class Variable {
    public:
        // It's 0 when default constructor is called.
        // The value is not lower than 0.
        int value{0};
    public:
        // Default constructor
        Variable() {}
        // Initializing a variable with a number
        Variable(int v) { value = (v > 0) ? v : 0; }

        // Operator overloading with a int argument
        Variable operator + (int n) {
            int op = value + n;
            int res = (op > 0) ? op : 0;
            return Variable(res);
        }
        Variable operator - (int n) {
            int op = value - n;
            int res = (op > 0) ? op : 0;
            return Variable(res);
        }
        bool operator < (int n) {
            return value < n;
        }
        bool operator > (int n) {
            return value > n;
        }
        bool operator >= (int n) {
            return value >= n;
        }
        bool operator <= (int n) {
            return value <= n;
        }
        bool operator != (int n) {
            return value != n;
        }
        // Operator overloading with a Variable argument
        Variable operator+(Variable var) {
            int op = value + var.value;
            int res = (op > 0) ? op : 0;
            return Variable(res);
        }
        Variable operator-(Variable var) {
            int op = value - var.value;
            int res = (op > 0) ? op : 0;
            return Variable(res);
        }

        // Debug printing
        void print() {
            cout << "Variable is " << value << endl;
        }
};

// using Instruction = Variable;

// class Label {
//     public:
//         Instruction instruction;

//     public:
//         // Initializing a label with a instruction
//         Label(Instruction i) {
//             instruction = i;
//         }

//         // Debug printing
//         void print() {
//             cout << "Label is " << instruction.value << endl;
//         }
// };

#endif