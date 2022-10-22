So the documentation is really lacking because I have spent plenty of time streamlining and optimizing lempel-ziv encoding code. 
It works but is still really slow with bigger files and that should not be an issue! That is because I use a 8 kilo byte sliding window during the encoding process. So it should achieve nearly same kind of encoding speed results with smaller (tens of kilo bytes) and bigger (few mega bytes) files.
With 80 kilo byte file the speed is 60000 kilo bytes / second. With 2.8 mega byte file the speed drops down to 14000 kilo bytes / second.

Solution:
I will try to learn line execution time profiling tool and try and resolve this issue.

If I do not manage withing the following 3 days I will polish up the rest of project and ship the product.