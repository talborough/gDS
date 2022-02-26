# gDS

(Python) Global Data Store (gDS) - A lightweight data store (for building test platforms in Python among other things)

gDS may not be for you:

* If you need the ACID qualities of a DBMS gDS is not for you.
    
* If you need more space than a memory-resident data store can handle gDS is not for you.

* If you need SQL or don't want to use the notation required to access the data, gDS is not for you.
    
* If you would rather not be concerned about data-locking issues (there are discussions on how to manage them below) gDS is not for you.
    
(For anyone left..) If you need a core, controlling data store so you can multi-process in Python and consume multiple host CPUs to 
get a "large" job done gDS may be for you. gDS was developed to help manage an end-to-end test tool that featured hundreds of 
independent activities (processes and threads) running against a VMware installation with hundreds of bare-metal hosts and thousands 
of VMs. gDS was used to keep all the run-time activities heading in the same direction.

gDS uses Python shared-memory "list" and "dict" objects (created by the Python "multiprocessing" library) to synthesize global 
run-time tables. An easy-to-use naming convention and notation (once you get used to it) makes it very plain what data is being 
manipulated and the notation remains consistent whether multi-processing, multi-threading or both. Any change in the data by one 
process/thread is instantly reflected in all cooperating processes/threads. The tables are defined by a data-definition file which 
is processed by the "gDSCodeGen" program into a Python file, and then consumed by the code using the data store.

Note that even though the manipulation of the data is done with ordinary Python code, the data store itself can still be organized in a
relational way. Indeed, if the data store is relationally organized it is often easier to work with and, the reverse is sometimes true: if
the data is hard to work with it may well be because it is not relationally organized.

Example files
=============

* animalFarm_01 - This example is brutally simple. It does *NO* multi-processing or multi-threading. It sets up a few counties / 
        farms / animals and dumps them out with the generated debug/dump routines.

* animalFarm_02 - This example is currently under construction. Its goal is to be descriptive and non-trivial (multi-processing 
        and multi-threading). One large goal is to expose strategies for handling concurrent access.

Example animalFarm_01
=====================

To run the example executable file "animalFarm_01":

* The data-definition file "animalFarm_01.dd" must be processed (once) into "animalFarm_01.py" by the included processor:

    * Edit the first line of the "gDSCodeGen" file to cite the installed version of python3

    * Execute the code generator on the "animalFarm_01.dd" file:
        
            ./gDSCodeGen animalFarm_01
        
* After the above operatione, the example program can be run:

    * Edit the first line of the example file ("animalFarm_01") to cite the installed version of python 3 to run

    * Execute the example file (see the file - it performs some very simple operations):
        
            ./animalFarm_01
