//
//  main.cpp
//  ce290l
//
//  Created by Mathilde Badoual on 1/22/18.
//  Copyright © 2018 Mathilde Badoual. All rights reserved.
//

#include <iostream>
#include <vector>

using namespace std;

void printMatrix(vector<vector<int>> mat)
{
    for(int i=0 ; i<mat.size() ; i++)
    {
        for(int j=0 ; j<mat[0].size() ; j++)
        {
        cout<< mat[i][j]<<" ";
        }
        cout<<endl;
    }
}

vector<vector<int>> matrixMult(vector<vector<int>> mat_a, vector<vector<int>> mat_b, int size)
{
    vector<vector<int>> mult(size, vector<int>(size));
    for(int i = 0; i < 2; ++i)
    {
        for(int j = 0; j < 2; ++j)
        {
            for(int k = 0; k < 2; ++k)
            {
                mult[i][j] += mat_a[i][k] * mat_b[k][j];
            }
        }
    }
    return mult;
}

vector<vector<int>> DefMatrix(int matrix[2][2], int size)
{
    vector<vector<int>> vect_vect;
    for(int i=0; i<size; i++)
    {
        vector<int> temp;
        for(int j=0; j<size; j++)
        {
            temp.push_back(matrix[i][j]);
        }
        vect_vect.push_back(temp);
    }
    return vect_vect;
}

int main(int argc, const char * argv[])
{
    int a[2][2] = {
        {2, -2},
        {2, 2}
    };
    int b[2][2] = {
        {0, 0},
        {0, 1}
    };
    int size = 2;
    vector<vector<int>> mat_a = DefMatrix(a, size);
    printMatrix(mat_a);
    cout << endl;
    vector<vector<int>> mat_b = DefMatrix(b, size);
    printMatrix(mat_b);
    cout << endl;
    vector<vector<int>> mult = matrixMult(mat_a, mat_b, size);
    printMatrix(mult);
    cout << endl;
    return 0;
}
