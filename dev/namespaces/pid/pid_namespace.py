import os
import ptrace.debugger
import ptrace.syscall

def create_pid_namespace():
    # Fork a child process
    child_pid = os.fork()
    
    if child_pid == 0:
        # In the child process
        
        # Create a new PID namespace
        os.unshare(os.CLONE_NEWPID)
        
        # Execute a new process in the new namespace
        os.execvp("bash", ["bash"])
    else:
        # In the parent process
        
        # Attach to the child process
        debugger = ptrace.debugger.PtraceDebugger()
        child = debugger.addProcess(child_pid, False)
        
        # Wait for the child process to stop
        child.wait()
        
        # Set the child process's PID namespace
        child.syscall("setns", os.CLONE_NEWPID, 0)
        
        # Detach from the child process
        child.detach()

# Call the function to create the PID namespace
create_pid_namespace()

