#!/usr/bin/python
# accepts both stdout and cmd line args
import sys

if __name__ == "__main__":
    if not sys.stdin.isatty(): # Not an interactive device.
        # ... read from stdin
        print "reading from stdin.."
        for line in sys.stdin:
            #sys.stderr.write("DEBUG: got line: " + line)
            args = line.split(' ')
            #sys.stdout.write(line)
            print ("\n".join(args))
    else:
        # get args from the command line
        argc = len(sys.argv)
        print ("got " + str(argc) + " args")
        print ("\n".join(sys.argv[1:]))
        sys.exit(1)

