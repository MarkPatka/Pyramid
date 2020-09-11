#include <iostream>


using namespace std;

bool check_if_polindrom(string text)
{
	int len = text.length();
	for (int i = 0; i < len/2; i++)
	{
		if (text[i] != text[len-i-1])
		{
			return false;
		}
	}
	return true;
}

int main()
{
	string str;
	cout << "Введите текст: ";
	cin >> str;
	if (check_if_polindrom(str))
	{
		cout << "Введенный текст - полиндром. ";
	}
	else
	{
		cout << "Введенный текст полиндромом не является. ";
	}
	return 0
}