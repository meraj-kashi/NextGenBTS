#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>

#define STACK_SIZE (1024 * 1024)

static int child_function(void* arg) {
    // Execute a command within the new PID namespace
    char* const cmd[] = { "/bin/bash", NULL };
    execvp(cmd[0], cmd);

    perror("execvp");
    return -1;
}

int main() {
    // Create a new PID namespace
    int flags = CLONE_NEWPID;
    char* stack = malloc(STACK_SIZE);
    if (stack == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }

    if (unshare(flags) == -1) {
        perror("unshare");
        exit(EXIT_FAILURE);
    }

    int fd = open("/proc/self/ns/pid", O_RDONLY);
    if (fd == -1) {
        perror("open");
        exit(EXIT_FAILURE);
    }

    if (setns(fd, 0) == -1) {
        perror("setns");
        exit(EXIT_FAILURE);
    }

    close(fd);

    pid_t child_pid = clone(child_function, stack + STACK_SIZE, SIGCHLD, NULL);
    if (child_pid == -1) {
        perror("clone");
        exit(EXIT_FAILURE);
    }

    // Wait for the child process to exit
    if (waitpid(child_pid, NULL, 0) == -1) {
        perror("waitpid");
        exit(EXIT_FAILURE);
    }

    printf("Child process exited.\n");

    return 0;
}
