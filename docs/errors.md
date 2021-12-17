# Errors

Error messages returned from the API may be general errors without a specific structure to
the error string or messages that have error codes embedded in the error string. The latter
*usually* indicate that the user/client has sent bad input, while the former indicate a server
error. A message with an error code has the following structure:

```text
Sample service error code <error code> <error type>: <message>
```

There is a 1:1 mapping from error code to error type; error type is simply a more readable
version of the error code. The error type **may change** for an error code, but the error code
for a specific error will not.

The current error codes are:

```text
20000 Unauthorized
30000 Missing input parameter
30001 Illegal input parameter
30010 Metadata validation failed
40000 Concurrency violation
50000 No such user
50010 No such sample
50020 No such sample version
50030 No such sample node
50040 No such workspace data
50050 No such data link
60000 Data link exists for data ID
60010 Too many data links
100000 Unsupported operation
```