#include <iostream>

using namespace std;
#include<bits/stdc++.h>
int str1[1000100],str2[1000100];
int Next[1000100];
int len1,len2,flag,cnt;
void getNext()
{
    int i=0,j=-1;
    Next[0]=-1;
    while(i<=len2)
    {
        if(j==-1||str2[i]==str2[j])
        {
            i++;
            j++;
            Next[i]=j;
        }
        else j=Next[j];
    }
}
void kmp()
{
    int i=0,j=0,cnt=0;
    getNext();
    while(i<len1)
    {
        if(j==-1||str1[i]==str2[j])
        {
            i++,j++;
        }
        else j=Next[j];

    if(j==len2)
    {
        cnt++;
        flag=i;
    }

    }
    if(cnt==1)
        printf("%d %d\n",flag-len2+1,flag);
    else printf("-1\n");
}
int main()
{
    int i;
    cin>>len1;
        for(i=0;i<len1;i++)
        {
            cin>>str1[i];
        }
    cin>>len2;

        for(i=0;i<len2;i++)
        {
            cin>>str2[i];
        }
    kmp();
}

