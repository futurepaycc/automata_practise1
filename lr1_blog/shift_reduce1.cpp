/*
来源: https://www.cnblogs.com/FlyerBird/p/9940723.html

文法:

E−>E+E
E−>E∗E
E−>id

TODO:
尝试增加优先级
 */

/* GCC: g++ -g -o shift_reduce1 shift_reduce1.cpp */

#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <stack>
#include <string>
using namespace std;
stack<string> stk, tmp;
string input_string;
bool flag = false;
int main(void) {
	cout << ">";
    cin >> input_string;  //输入串: id*id+id
    input_string += "$";  //加上标识符
    printf("----------|----------|----------\n");
    printf("    栈    |   输入   |    动作  \n");
    printf("----------|----------|----------\n");
    int now = 0;  //当前扫描字符位置
    while (!flag) {
        now = 0;
        if (stk.empty()) {  //如果一开始栈为空，直接移进符号
            stk.push("$");
            cout << "$         |";
            cout.setf(ios::right);  //设置字符对其方式
            cout.width(10);         //设置字符宽度
            cout << input_string;
            cout << "|移进" << endl;
            printf("----------|----------|----------\n");
            string token;
            if (input_string[now] == 'i') {  //移进符号为id
                token = "id";
                now = 2;
            } else {  //移进符号不为id
                token = input_string[now];
                now = 1;
            }
            stk.push(token);                                                     //将符号压入栈
            input_string = input_string.substr(now, input_string.size() - now);  //丢弃已扫描的字符
            continue;
        }
        while (!stk.empty()) {  //用两个栈来回倒，输出字符
            tmp.push(stk.top());
            stk.pop();
        }
        while (!tmp.empty()) {
            cout << tmp.top();
            stk.push(tmp.top());
            tmp.pop();
        }
        if (stk.top() == "id") {  // E-->id归约，优先级最高
            cout.width(10 - stk.size());
            cout << "|";
            cout.setf(ios::right);  //设置字符对其方式
            cout.width(10);         //设置字符宽度
            cout << input_string;
            cout << "|按E-->id进行归约" << endl;
            printf("----------|----------|----------\n");
            stk.pop();
            stk.push("E");
            continue;
        }
        if (input_string[now] == '$' && stk.size() == 2 && stk.top() == "E") {  //接受状态
            flag = true;
            cout << "        |         $|接受" << endl;
            printf("----------|----------|----------\n");
            continue;
        }
        if (input_string[now] != '$') {  //移进字符
            string tp;
            if (input_string[now] == 'i') {
                tp = "id";
                now = 2;
            } else {
                tp = input_string[now];
                now = 1;
            }
            cout.width(11 - stk.size());
            cout << "|";
            cout.setf(ios::right);  //设置字符对其方式
            cout.width(10);         //设置字符宽度
            cout << input_string;
            cout << "|移进" << endl;
            printf("----------|----------|----------\n");
            stk.push(tp);
            input_string = input_string.substr(now, input_string.size() - now);  //丢弃已扫描的字符
            continue;
        }
        if (input_string[now] == '$' && !flag) {  // E-->E+E或者E-->E*E归约
            string tc;
            tc = stk.top();
            if (tc == "E") stk.pop();
            tc += stk.top();
            if (stk.top() != "E") {
                stk.pop();
                tc += stk.top();
                cout.setf(ios::right);       //设置字符对其方式
                cout.width(9 - stk.size());  //设置字符宽度
                cout << "|";
                cout << "         $|";
                cout << "按E-->" << tc << "归约" << endl;
                printf("----------|----------|----------\n");
                stk.pop();
                stk.push("E");
            }
        }
    }
    return 0;
}