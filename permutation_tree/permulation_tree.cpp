//
// Created by 梁艺馨 on 2018/8/1.
//
#include <iostream>
using  namespace std;

#define MX 50

int x[MX];
int n;

void permutation(int t)
{
    if(t > n) {
        for(int i = 1; i <= n; i++) {
            cout << x[i] << "  ";
        }
        cout << endl;
        return ;
    }

    for(int i = t; i <= n; i++) {
        swap(x[t], x[i]);
        permutation(t+1);
        swap(x[t], x[i]);
    }
}

int main()
{
    cout << "输入待排列的元素个数n(求1...n的排列)："<<endl;
    cin >> n;
    for(int i = 1; i <= n; i++) {
        x[i] = i;
    }
    permutation(1);

    return 0;
}
