
/* Program to convert lowercase alphabets to UPPERCASE */

#include<stdio.h>

int main()
{
    char s[101],r[101];
    int i;

    while(scanf("%s",s) != EOF)
    {        
        for(i = 0; s[i] != '\0'; i++)
        {
            if(s[i] >= 'a' && s[i] <= 'z')
                r[i] = s[i] - 'a' + 'A';
            else
                r[i] = s[i];
        }

        r[i] = '\0';

        printf("%s\n",r);
    }

    return 0;
}