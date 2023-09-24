#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <conio.h>

int main() {
    int n, k, i;
    char d;
    int a, b, c = 0, q;

    srand(time(NULL)); // 난수 발생기 초기화

    for (i = 1; i <= 10; i++) {
        q = rand() % 4; // 0부터 3까지의 난수 발생
        n = rand() % 90 + 10; // 10부터 99까지의 난수 발생
        k = rand() % 9 + 1; // 1부터 9까지의 난수 발생

        switch (q) {
            case 0:
                printf("%d:%d + %d = ", i, n, k);
                b = n + k;
                break;
            case 1:
                printf("%d:%d - %d = ", i, n, k);
                b = n - k;
                break;
            case 2:
                printf("%d:%d * %d = ", i, n, k);
                b = n * k;
                break;
            case 3:
                printf("%d:%d / %d = ", i, n, k);
                b = n / k;
                break;
        }

        scanf("%d", &a);
        if (a == b) {
            printf("Good\n");
            c++;
        } else {
            while (1) {
                printf("다시 시도하시겠습니까? y/n\n");
                d = getche();

                if (d == 'y') {
                    if (q == 0) {
                        printf("\n%d: %d + %d = \n", i, n, k);
                        scanf("%d", &a);
                    } else if (q == 1) {
                        printf("\n%d: %d - %d = ", i, n, k);
                        scanf("%d", &a);
                    } else if (q == 2) {
                        printf("\n%d: %d * %d = ", i, n, k);
                        scanf("%d", &a);
                    } else {
                        printf("\n%d: %d / %d = ", i, n, k);
                        scanf("%d", &a);
                    }
                    if (a == b) {
                        printf("Good\n");
                        c++;
                        break;
                    }
                } else {
                    printf("정답은 %d\n", b);
                    break;
                }
            }
        }
    }
    printf("%d", c);
    return 0;
}
