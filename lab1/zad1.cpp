#include <iostream>
#include <vector>
#include "irg_math.h"

using namespace std;

int main() {

	vector<float> v1_1, v1_2;
	float v1_1_items[3] = { 2, 3, -4 };
	v1_1.assign(v1_1_items, v1_1_items + 3);
	float v1_2_items[3] = { -1, 4, -1 };
	v1_2.assign(v1_2_items, v1_2_items + 3);

	vector<float> v1 = sum_vectors(v1_1, v1_2);
	print_vector(v1, "v1");

	float  s = dot_multiply_vectors(v1, v1_2);
	cout << endl << "s = " << s << endl;

	vector<float> v2_2;
	float v2_2_items[3] = { 2, 2, 4 };
	v2_2.assign(v2_2_items, v2_2_items + 3);

	vector<float> v2 = cross_multiply_vectors_3d(v1, v2_2);
	print_vector(v2, "v2");
	
	float  v3 = vector_length(v2);
	cout << endl << "v3 = " << v3 << endl;

	vector<float> v4 = multiply_vector_with_scalar(v2, -1);
	print_vector(v4, "v4");

	float  M1_1_items[3][3] = {{1, 2, 3},
							{2, 1, 3},
							{4, 5, 1}};
	float  M1_2_items[3][3] = {{-1, 2, -3},
							{5, -2, 7},
							{-4, -1, 3}};
	vector<vector<float>> M1_1(3, vector<float>(3)), M1_2(3, vector<float>(3));
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			M1_1[i][j] = M1_1_items[i][j];
			M1_2[i][j] = M1_2_items[i][j];
		}
	}

	vector<vector<float>> M1 = sum_matrices(M1_1, M1_2);
	print_matrix(M1, "M1");

	vector<vector<float>> M2 = multiply_matrices(M1_1, transponse_matrix(M1_2));
	print_matrix(M2, "M2");

	vector<vector<float>> M3 = multiply_matrices(M1_1, inverse_matrix3x3(M1_2));
	print_matrix(M3, "M3");

	return 0;
}