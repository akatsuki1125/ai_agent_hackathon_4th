#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(void){
    const char *HOST = "127.0.0.1";
    const int PORT = 8008;

    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    inet_pton(AF_INET, HOST, &addr.sin_addr);

    bind(listen_fd, (struct sockaddr *)&addr, sizeof(addr));
    listen(listen_fd, 4);

    printf("listening on %s:%d\n", HOST, PORT);

    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    int conn_fd = accept(listen_fd, (struct sockaddr *)&client_addr, &client_len);

    char buf[1024];
    int n = recv(conn_fd, buf, sizeof(buf), 0);
    if (n>0){
        printf("received bytes %d\n", n);
        printf("received data %s\n", buf);
    }

    close(conn_fd);
    close(listen_fd);
    return 0;
}