#include <iostream>
#include <vector>

using namespace std;
typedef vector<vector<double>> matrix;

void printMatrix(const matrix mat) {
  const auto rows = mat.size();
  const auto cols = mat[0].size();
  for (auto i = 0; i < rows; ++i) {
    for (auto j = 0; j < cols; ++j) {
      cout << mat[i][j] << " ";
    }
    cout << endl;
  }
  cout << endl;
}

matrix matrixMult(const matrix x, const matrix y) {
  const auto rows_x = x.size();
  const auto cols_x = x[0].size();
  const auto rows_y = y.size();
  const auto cols_y = y[0].size();
  matrix product(rows_x, vector<double>(cols_y));
  for (auto row = 0; row < rows_x; ++row) {
    for (int col = 0; col < cols_y; ++col) {
      auto jai_le_sum = 0.0;
      for (int k = 0; k < cols_x; ++k) {
        jai_le_sum += x[row][k] * y[k][col];
      }
      product[row][col] = jai_le_sum;
    }
  }
  return product;
}

int main(int argc, const char* argv[]) {
  auto a = matrix({{2, -2}, {2, 2}});
  auto b = matrix({{0, 0}, {0, 1}});
  printMatrix(a);
  printMatrix(b);
  matrix product = matrixMult(a, b);
  printMatrix(product);
  return 0;
}
