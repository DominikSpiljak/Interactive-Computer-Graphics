#pragma once
#include <iostream>
#include <vector> 
#include <math.h>
#include <string>

using namespace std;

void print_vector(vector<float> v, string name) {
	cout << endl;
	cout << name << " = " << v[0] << "i + " << v[1] << "j + " << v[2] << "k" << endl;
}

vector<float> sum_vectors(vector<float> v1, vector<float> v2) {
	vector<float> v;

	for (int i = 0; i < v1.size(); i++) {
		v.push_back(v1[i] + v2[i]);
	}
	return v;
}

float dot_multiply_vectors(vector<float> v1, vector<float> v2) {
	float s = 0;

	for (int i = 0; i < v1.size(); i++) {
		s += v1[i] * v2[i];
	}
	return s;
}

vector<float> cross_multiply_vectors_3d(vector<float> v1, vector<float> v2) {
	vector<float> v;

	v.push_back(v1[1] * v2[2] - v1[2] * v2[1]);
	v.push_back(-1 * v1[0] * v2[2] + v1[2] * v2[0]);
	v.push_back(v1[0] * v2[1] - v1[1] * v2[0]);
	return v;
}

float vector_length(vector<float> v) {
	float s = 0;

	for (int i = 0; i < v.size(); i++) {
		s += pow(v[i], 2);
	}
	s = sqrt(s);
	return s;
}

vector<float> multiply_vector_with_scalar(vector<float> v1, float s) {
	vector<float> v;

	for (int i = 0; i < v1.size(); i++) {
		v.push_back(v1[i] * s);
	}
	return v;
}

void print_matrix(vector<vector<float>> m, string name) {
	cout << endl;
	for (int i = 0; i < m.size(); i++) {
		if (i == m.size() / 2) {
			cout << name << " = ";
		}
		else {
			cout << "     ";
		}
		for (int j = 0; j < m[0].size(); j++) {
			cout << m[i][j] << " ";
		}
		cout << endl;
	}
}

vector<vector<float>> sum_matrices(vector<vector<float>> m1, vector<vector<float>> m2) {
	vector<vector<float>> m(3, vector<float>(3));

	for (int i = 0; i < m.size(); i++) {
		m[i] = sum_vectors(m1[i], m2[i]);
	}
	return m;
}

vector<vector<float>> transponse_matrix(vector<vector<float>> m) {
	vector<vector<float>> transponse_m(3, vector<float>(3));

	for (int i = 0; i < transponse_m.size(); i++) {
		for (int j = 0; j < transponse_m[0].size(); j++) {
			transponse_m[j][i] = m[i][j];
		}
	}
	return transponse_m;
}

vector<vector<float >> multiply_matrices(vector<vector<float >> m1, vector<vector<float >> m2) {
	vector<vector<float >> m(m1.size(), vector<float>(m2[0].size()));

	for (int i = 0; i < m.size(); i++) {
		for (int j = 0; j < m[0].size(); j++) {
			vector<float> v1 = m1[i];
			vector<float> v2;
			for (int k = 0; k < m.size(); k++) {
				v2.push_back(m2[k][j]);
			}
			m[i][j] = dot_multiply_vectors(v1, v2);
		}
	}
	return m;
}

float calculate_determinant3x3(vector<vector<float>> m) {
	float d = m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
	return d;
}

vector<vector<float>> calculate_adjugate_matrix(vector<vector<float>> m) {
	vector<vector<float>> adj_m(3, vector<float>(3));
	for (int i = 0; i < m.size(); i++) {
		for (int j = 0; j < m.size(); j++) {
			vector<float> small_matrix;
			for (int k = 0; k < m.size(); k++) {
				for (int l = 0; l < m.size(); l++) {
					if (k != i && l != j) {
						small_matrix.push_back(m[k][l]);
					}
				}
			}
			float small_matrix_det = small_matrix[0] * small_matrix[3] - small_matrix[1] * small_matrix[2];
			if ((i + j) % 2 != 0) {
				adj_m[i][j] = -1 * small_matrix_det;
			}
			else {
				adj_m[i][j] = small_matrix_det;
			}
		}
	}

	return adj_m;
}

vector<vector<float>> inverse_matrix3x3(vector<vector<float>> m) {
	float d = calculate_determinant3x3(m);
	vector<vector<float>> transponse_m = transponse_matrix(m);
	vector<vector<float>> adj_m = calculate_adjugate_matrix(transponse_m);
	vector<vector<float >> inv_m(3, vector<float>(3));
	for (int i = 0; i < inv_m.size(); i++) {
		for (int j = 0; j < inv_m.size(); j++) {
			inv_m[i][j] = (float)adj_m[i][j] / (float)d;
		}
	}
	return inv_m;
}
