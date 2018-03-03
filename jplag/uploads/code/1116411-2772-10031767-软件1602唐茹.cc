#include<stdio.h>
#include<string.h>

char str[1000000],str1[1000000];
int next[1000000];

void getNext()
{
    int i=0,j=-1;
    int len=strlen(str1);
    next[0]=-1;
    while(i<len)
    {
        if(j==-1||str1[i]==str1[j])
        {
            i++;
            j++;
            next[i]=j;
        }
        else j=next[j];
    }
}

int kmp()
{
    int i=0,j=0;
    int str_len=strlen(str),str1_len=strlen(str1);
    getNext();
    while(i<str_len&&j<str1_len)
    {
        if(j==-1||str[i]==str1[j])
        {
            i++;
            j++;
        }
        else j=next[j];
    }
    if(j>=str1_len) return i-j+1;
    else return -1;
}

int main()
{
    while(~scanf("%s%s",str,str1))
    {
        printf("%d\n",kmp());
    }
    return 0;
}
