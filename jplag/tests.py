import os
from shutil import rmtree

from django.test import TestCase

from .models import Checker, Code, Jplag


class JplagModelTests(TestCase):
    def test_make_run_cmd(self):
        jplag = Jplag(0)
        run_cmd = jplag.make_run_cmd(
            language='c/c++',
            percent='80%',
            result_dir='test',
            submit_dir='test'
        )
        self.assertEqual(
            run_cmd, 'java -jar jplag.jar -l c/c++ -m 80% -r test -s test'
        )
        run_cmd = jplag.make_run_cmd(
            language='java17',
        )
        self.assertEqual(
            run_cmd, 'java -jar jplag.jar -l java17 -m 80% -r jplag/jplag/result/0 -s jplag/jplag/codes/0')

    def test_save_code(self):
        jplag = Jplag(0)
        code = '''
#include <iostream>
using namespace std;
int main() {
    cout << "Hello World!" << endl;
}
'''
        jplag.save_code('test1.cpp', code)
        with open('jplag/jplag/codes/0/test1.cpp') as fr:
            self.assertEqual(code, fr.read())

    def test_run_jplag(self):
        jplag = Jplag(0)
        code = '''
#include <bits/stdc++.h>
using namespace std;
int N, M;
int n[100005];
int ans;
void binsearch(int low,int high)
{
    if(low>high)
        return ;
    int mid=(high-low)/2+low;
    int sum=0,count=1;
    for(int i=0;i<N;i++)
    {
        if(sum+n[i]<=mid)
        {
            sum+=n[i];
        }
        else
        {
            count++;
            sum=n[i];
        }
    }
    if(count>M)
    {
        binsearch(mid+1,high);
    }
    else
    {
        ans=mid;
        binsearch(low,mid-1);
    }
}
int main()
{
    int low,high;
    while(~scanf("%d %d",&N,&M))
    {
        low=high=0;
        for(int i=0;i<N;i++)
        {
            scanf("%d",&n[i]);
            low=max(low,n[i]);
            high+=n[i];
        }
        binsearch(low,high);
        printf("%d\n",ans);
    }
    return 0;
}
'''
        jplag.save_code('test1.cpp', code)
        jplag.save_code('test2.cpp', code)
        code2 = '''
#include <cstdio>
using namespace std;

int a[100000], n, m;

int Binary(int low, int high);

int main(int argc, char const *argv[]) {
    while(~ scanf("%d %d", &n, &m)) {
        int low = 0, high = 0;
        for(int i=0; i<n; ++i) {
            scanf("%d", &a[i]);
            low = a[i] > low ? a[i] : low;
            high += a[i];
        }
        printf("%d\n", Binary(low, high));
    }

    return 0;
}

int Binary(int low, int high) {
    int mid, sum, cnt, ans;
    while(low <= high) {
        mid = (low+high)/2;
        sum = 0;
        cnt = 1;
        for(int i=0; i<n; ++i) {
            if(sum+a[i] <= mid)
                sum += a[i];
            else {
                cnt++;
                sum = a[i];
            }
        }
        if(cnt > m) low = mid+1;
        else {
            high = mid-1;
            ans = mid;
        }
    }

    return ans;
}
'''
        jplag.save_code('test3.cpp', code2)
        jplag.make_run_cmd(language='c/c++')
        jplag.run_jplag()

        flag = os.path.exists('jplag/jplag/result/0')
        self.assertEqual(flag, True)
        rmtree('jplag/jplag/result/0')


class CodesModelTests(TestCase):
    def test_check_name(self):
        code = Code()
        code.name = 'HelloWorld'
        rst = code.check_name()
        self.assertEqual(rst, True)

        code.name = 'Hello World'
        rst = code.check_name()
        self.assertEqual(rst, False)

        code.name = '你好世界'
        rst = code.check_name()
        self.assertEqual(rst, True)

        code.name = '你好世界.cpp'
        rst = code.check_name()
        self.assertEqual(rst, True)

        code.name = '../index.php'
        rst = code.check_name()
        self.assertEqual(rst, False)
