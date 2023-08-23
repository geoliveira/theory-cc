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
        void operator = (int n) {
            int res = (n > 0) ? n : 0;
            value = res;
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
            return Variable(value + var.value);
        }
        Variable operator-(Variable var) {
            int op = value - var.value;
            int res = (op > 0) ? op : 0;
            return Variable(res);
        }
        Variable operator * (Variable var) {
            return Variable(value * var.value);
        }

        // Debug printing
        void print() {
            cout << "Variable is " << value << endl;
        }
};

int main(void) {
    Variable x1, x2, x3, x4;
    x1.print(); // implementação para prósitos de debug

    // Macros
    // – GOTO L
    // tomando vantagem da linguagem C++, podemos utilizar label e o comando "goto <label>". Ex:
    // – V ← 0
built_in_label:
    x1 = 1; // implementação na linha 30
    x1.print();
    if (x1 != 1) { // implementação na linha 46
        goto built_in_label;
    }
    // – V ← V’
    // vantagem da própria linguagem
    // – V ← V’+V”
    x2 = x1;
    x3 = x2 + x1; // implementação na linha 50
    x3.print();
    // – V ← V’∗V”
    x2 = x2 + 1; // implementação na linha 18
    x4 = x3 * x2; // implementação na linha 58
    x4.print();

    return 0;
}
