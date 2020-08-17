#include "irg_math.h"
#include <iostream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;

void print_result(vector<vector<float>> result) {
	cout << "[x y z] = [" << result[0][0] << " " << result[1][0] << " " << result[2][0] << "]" << endl;
}

int main() {
    vector<vector<float>> M(3, vector<float>(3));
    vector<vector<float>> T(3, vector<float>(1));
    string dots = "ABCT";
    for (int i = 0; i < 4; i++) {
        cout << dots[i] << " = ";
        string input_str;

        getline(cin, input_str);
        stringstream ss(input_str);

        int j = 0;
        while (ss.good()) {
            string substr;
            getline(ss, substr, ',');
            int x;
            x = stoi(substr);
            if (i != 3) {
                M[i][j] = x;
            }
            else {
                T[j][0] = x;
            }
            j++;
        }
    }
    vector<vector<float>> transponse_M = transponse_matrix(M);
    vector<vector<float>> inverse_M = inverse_matrix3x3(transponse_M);
    vector<vector<float>> t = multiply_matrices(inverse_M, T);
    print_result(t);
}