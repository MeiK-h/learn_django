#include<stdio.h>
#include<stdlib.h>
#include<string.h>
typedef struct
{
    int *a;
    int length;
    int listsize;
}list;

void main()
{
    list L;
    int n;
    int i;
    int q=0,sum=0;
    scanf("%d",&n);
    L.a=(int *)malloc((n+1)*sizeof(int ));
    for(i=0;i<n;i++)
    {
        scanf("%d",&L.a[i]);
    }
    for(i=0;i<n;i++)
    {
          if(q+L.a[i]>0)q=q+L.a[i];
          else q=0;
          if(q>sum)sum=q;
    }
    printf("%d %d\n",sum,n*2-1);
}
