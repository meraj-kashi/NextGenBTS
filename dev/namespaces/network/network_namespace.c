#define _GNU_SOURCE
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define STACK_SIZE (1024 * 1024)

static int child_function(void* arg) {
    // Execute a command within the new network namespace
    char* const cmd[] = { "/bin/bash", NULL };
    execvp(cmd[0], cmd);

    perror("execvp");
    return -1;
}

int main() {
    // Create a new network namespace
    int flags = CLONE_NEWNET;
    char* stack = malloc(STACK_SIZE);
    if (stack == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }

    pid_t child_pid = clone(child_function, stack + STACK_SIZE, flags | SIGCHLD, NULL);
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
