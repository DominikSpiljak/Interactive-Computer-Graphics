#include "irg_math.h"
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

void print_result(vector<vector<float>> result) {
	cout << "[x y z] = [" << result[0][0] << " " << result[1][0] << " " << result[2][0] << "]" << endl;
}


int main() {
	vector<vector<float>> M1(3, vector<float>(3)), v1(3, vector<float>(1));
	vector<float> inputVector;
	string input_str;

	cout << "Parametri = ";

	getline(cin, input_str);
	stringstream ss(input_str);

	while (ss.good()){
		string substr;
		getline(ss, substr, ',');
		int x;
		x = stoi(substr);
		inputVector.push_back(x);
	}

	int j = 0;
	for (int i = 0; i < 12; i++) {
		if (i == 3 || i == 7 || i == 11) {
			v1[j][0] = inputVector[i];
			j++;
		}
		else {
			M1[i / 4][i % 4] = inputVector[i];
		}
	}
	
	vector<vector<float>> inverse_M1 = inverse_matrix3x3(M1);
	vector<vector<float>> result = multiply_matrices(inverse_M1, v1);
	print_result(result);


	return 0;
}