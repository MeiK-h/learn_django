#include <iostream>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
using namespace std;
int s1[1000100],s2[10000100];
int Next[10000100];
int len1,len2;
void getnext()
{
    int i,j;
    i=0;
    Next[0]=j=-1;
    while(i<len2)
    {
        if(j==-1||s2[i]==s2[j])
        {
            Next[++i]=++j;
        }
        else j=Next[j];
    }
}
void kmp()
{
    int i,j,ji=0,flag;
    i=0;j=-1;
    while(i<len1)
    {
        if(j==-1||s1[i]==s2[j])
        {
            i++;j++;
        }
        else j=Next[j];
        if(j>=len2)
        {
            ji++;
            flag=i;
        }
    }
    if(ji==1) printf("%d %d\n",flag-len2+1,flag);
    else printf("-1\n");
}
int main()
{
    int n,m,t,i,j;
    scanf("%d",&len1);
    for(i=0;i<len1;i++)
    {
        scanf("%d",&s1[i]);
    }
    scanf("%d",&len2);
    for(i=0;i<len2;i++)
    {
        scanf("%d",&s2[i]);
    }
    getnext();
//    for(i=0;i<len2;i++)
//    {
//        printf("%d ",Next[i]);
//    }
    kmp();
}
