/*
** server.c -- a stream socket server demo
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>

#define PORT "3490"  // the port users will be connecting to

#define BACKLOG 10	 // how many pending connections queue will hold

void sigchld_handler(int s)
{
	(void)s; // quiet unused variable warning

	// waitpid() might overwrite errno, so we save and restore it:
	int saved_errno = errno;

    //busy loop; wait for processes to die(?)
	while(waitpid(-1, NULL, WNOHANG) > 0);

	errno = saved_errno;
}


// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}

	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(void)
{
	int sockfd, new_fd;  // listen on sock_fd, new connection on new_fd
	struct addrinfo hints, *servinfo, *p; // hints is passed into, servinfo is used to return a list of addrinfo structs, p is placeholder used in for loop.
	struct sockaddr_storage their_addr; // connector's address information
	socklen_t sin_size;
	struct sigaction sa;
	int yes=1;
	char s[INET6_ADDRSTRLEN];
	int rv;

	// zero out the addrinfo struct, and set the appropriate flags
    memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC; // address family, current value indicates getaddrinfo should return socket addresses for either family.
	hints.ai_socktype = SOCK_STREAM; // preferred socket type, either stream or datagram; each indicating the usage of either TCP or UDP;
	hints.ai_flags = AI_PASSIVE; // use my IP

    // non-zero return value indicates an error getting information from the addrinfo struct
    // store list of addrinfo structs in servinfo.
	if ((rv = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	// loop through all the results and bind to the first we can, loop through all of the addrinfo structus in return from getaddrinfo until we bind to one.
	for(p = servinfo; p != NULL; p = p->ai_next) {
        //try to create socket, move onto next addrinfo struct if unable to create a socket.
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
				p->ai_protocol)) == -1) {
			perror("server: socket");
			continue;
		}

        //using the fd from the addrinfo struct, try to set the socket options; and terminate execution if setting sock opts throws errors. 
		if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
				sizeof(int)) == -1) {
			perror("setsockopt");
			exit(1);
		}


        //attempt to bind the socket to the address in the addrinfo struct, close socket fd if errors occur
		if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("server: bind");
			continue;
		}

        //if not issues arise while either creating, setting or binding a socket; continue execution.
		break;
	}

	freeaddrinfo(servinfo); // all done with this structure

    // if no such socket was found while looping through servinfo as returned by getaddrinfo, terminate execution
    // this implies that the for loop terminated, and never broke (which implies that the socketfd was created)
	if (p == NULL)  {
		fprintf(stderr, "server: failed to bind\n");
		exit(1);
	}

    // prepare socket for listening for oncoming connections.
    // BACKLOG implies only 10 connections can be pending at a time before the socket refuses to accept messages.
	if (listen(sockfd, BACKLOG) == -1) {
		perror("listen");
		exit(1);
	}

    // deals with signals, requires more research; something to do with waiting for child processes to die.
	sa.sa_handler = sigchld_handler; // reap all dead processes
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_RESTART;
	if (sigaction(SIGCHLD, &sa, NULL) == -1) {
		perror("sigaction");
		exit(1);
	}

	printf("server: waiting for connections...\n");

	while(1) {  // main accept() loop
		sin_size = sizeof their_addr;
        // wait for connections, continue waiting if issues. 
		new_fd = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
		if (new_fd == -1) {
			perror("accept");
			continue;
		}

        // get the internet protocol address in readable format, and print to terminal.
		inet_ntop(their_addr.ss_family,
			get_in_addr((struct sockaddr *)&their_addr),
			s, sizeof s);
		printf("server: got connection from %s\n", s);

		if (!fork()) { // this is the child process
			close(sockfd); // child doesn't need the listener
			if (send(new_fd, "Hello, world!", 13, 0) == -1)
				perror("send");
			close(new_fd);
			exit(0);
		}
		close(new_fd);  // parent doesn't need this
	}

	return 0;
}

/*
    In General
        - Create socket
        - Bind Socket
        - Listen on Socket
            - Do thing
            - Repeat
        - Close Socket
        - Terminate Program
*/