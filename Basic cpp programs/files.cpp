#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
	string str;
	cin >> str;
	ofstream fout = fopen(str, "w");
	fout << "olololo";
	fout.close();
}