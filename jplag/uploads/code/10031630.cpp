#include <stdio.h>
#include <stdlib.h>
int a[100000010],b[100000010];
int next[100000010],m,n;
void Next()
{
    int j;
    next[0]=-1;
    for (j=1;j<m;j++)
    {
        int i=next[j-1];
        while (b[j]!=b[i+1]&&i>=0)
        {
            i=next[i];
        }
        if (b[j]==b[i+1])
            next[j]=i+1;
        else
            next[j]=-1;
    }
}
int kmp(int a[],int b[])
{
    Next();
    int p=0,s=0;
    while (p<m&&s<n)
    {
        if (a[s]==b[p])
        {
            s++;
            p++;
        }
        else
        {
            if (p==0)
                s++;
            else
                p=next[p-1]+1;

        }
    }
    if (p<m)
        return -1;
    else
        return s-m+1;
}
int main()
{
    int i,k,t;
    while (~scanf ("%d",&n))
    {
        for (i=0;i<n;i++)
            scanf ("%d",&a[i]);
        scanf ("%d",&m);
        for (i=0;i<m;i++)
            scanf ("%d",&b[i]);
        k=kmp(a,b);
        if (k!=-1)
        {
            t=kmp(a+k,b);
            if (t==-1)
                printf ("%d %d\n",k,k+m-1);
            else
                printf ("-1\n");
        }
        else
                printf ("-1\n");
    }
    return 0;
}
