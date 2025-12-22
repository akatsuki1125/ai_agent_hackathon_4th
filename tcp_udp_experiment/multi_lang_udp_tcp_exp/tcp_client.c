
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(void){
    const char *HOST = "127.0.0.1";
    const int PORT = 8008;

    int sock = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    inet_pton(AF_INET, HOST, &addr.sin_addr);

    connect(sock, (struct sockaddr *)&addr, sizeof(addr));

    char data[100];
    memset(data, 0, sizeof(data));
    snprintf(data, sizeof(data), "hello world");
    send(sock, data, sizeof(data), 0);

    close(sock);
    return 0;
}
