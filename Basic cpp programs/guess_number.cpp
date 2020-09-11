#includePath <iostream>
using namespace std;


int main()
{
    int rightAnswer = 1 + rand() % 10;

    for (int i = 0, i < 3, i++) 
    {
        cout << "Попробуйте угадать чсло от 1 до 10." << '\n' << "Введите ваше число: " << endl;
        int playerAnswer; 
        cin >> playerAnswer;

        if (playerAnswer == rightAnswer)
        {
            cout <<"Вы угадали! Ответ: " << rightAnswer << '\n';
            break;
        } else if (playerAnswer < rightAnswer) 
        {
            cout << "Указанное число меньше. " << endl 

        } else 
        {
            cout << "Указанное число больше. " << endl
        }
        
        cout << "У вас осталось " << 3 - i << " Попыток. Try again!" << endl 

         
    }
    cout << "Правильный ответ: " << rightAnswer;
    return 0
}
 
