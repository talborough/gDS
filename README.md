# gDS (V2)

Global Data Store (gDS) - A lightweight data store (for building test platforms in Python among other things)

* See **repo.version** for version information.

* See the associated LinkedIn article: https://www.linkedin.com/pulse/testing-complex-systems-thomas-alborough

* Comments welcome by Tom.Alborough@Gmail.com

gDS may not be for you:

* If you need the "ACID" qualities of a DBMS gDS is not for you.
    
* If you need more space than a memory-resident data store can handle gDS is not for you.

* If you need SQL or don't want to use the notation required to access the data, gDS is not for you.
    
* If you would rather not be concerned about data-locking issues (there are discussions on how to manage them below and in the cited article) gDS is not for you.
    
(For anyone left..) If you need a core, controlling data store so you can multi-process in Python and consume multiple host cores to 
get a "large" job done gDS may be for you.

gDS uses Python shared-memory "list" and "dict" objects (created by the Python "multiprocessing" library) to synthesize global 
run-time tables. An easy-to-use naming convention and notation (once you get used to it) makes it very plain what data is being 
manipulated and the notation remains consistent whether multi-processing, multi-threading or both. Any change in the data by one 
process/thread is instantly reflected in all cooperating processes/threads. The tables are defined by a data-definition file which 
is processed by the "gDSCodeGen" program into a Python file, and then consumed by the code using the data store.

Note that even though the manipulation of the data is done with ordinary Python code, the data store itself can still be organized in a
relational way. Indeed, if the data store is relationally organized it is often easier to work with and, the reverse is sometimes true:
if the data is hard to work with it may well be because it is not relationally organized.

## Example files

* animalFarm_01 - This example is brutally simple. It sets up a few counties and farms and then randomly adds some animals from some
        spawned processes. All the tables are then dumped out and then a subset of the animal collection is printed out.

* animalFarm_02 - "V2" of this has been released. Follow the same rules to prepare, start and run it as for animalFarm_01 (below). The goals of animalFarm_02 are:

    * Be able to demo some of the "test platform" functionality described in the Testing Complex Systems LinkedIn article.

    * Be a descriptive and non-trivial (multi-processing and multi-threading) example of using gDS - one large goal is to expose strategies for handling concurrent access.

    * animalFarm_02 help documentation is available at the end of the "animalFarm_02" file and at "./animalFarm_02 -h".

## Example animalFarm_01 (and animalFarm_02)

To run the example executable file "animalFarm_01":

* The data-definition file "animalFarm_01.dd" must be processed (once) into "animalFarm_01.py" by the included processor:

    * Edit the first line of the "gDSCodeGen" file to cite the installed version of python 3

    * Execute the code generator on the "animalFarm_01.dd" file:
        
            ./gDSCodeGen animalFarm_01
        
* After the above operation, the example program can be run:

    * Edit the first line of the example file ("animalFarm_01") to cite the installed version of python 3 to run

    * Execute the example file (see the file - it performs some very simple operations):
        
            ./animalFarm_01

## .dd File Specifications and Operation

Here's how the the various citations in the "define data" (.dd) files are handled. First, the major keywords:

* **defineTable** - The start of a table definition. One manditory argument - table name. One optional argument - Python lock function name (see example files for usage).

* **defineColumn** - Define a table column. One manditory argument - column name. One optional argument - initial value.

* **defineIndex** - Define an index for the table using the Name column value as the key. One manditory argument - index name.

* **defineUnary** - Define a (list) with one element to use as a flag/counter. One manditory argument - element name. One optional argument - initial value.

* **defineList / defineDict** - Define a global shared list / dictionary with no other semantics. One manditory argument - list/dict name. A way to create completely ad-hoc global shared variables.

The reserved names in use here are:

* **Name** - A column that identifies a row. May need to be a unique value (see below).

* **RowStatus** - A column that specifies the status of a row (see below).

* **Name2Index** - A dictionary with the row **Name** value as the key and the row's index as the value

The per-table generated functions are:

* **DumpTable** - Generated for all tables - uses the **Name** column if an index to another table needs to be resolved.

* **AddARow / AddARowUnderLock** - Depending on whether the lock function name was specified  (and manage any **Name2Index** index).

* **CompressTableUnderLock** - Remove rows where **RowStatus** is **None** (and fix up any existing **Name2Index** index).

Now, a different view of the above:

```
There must be a Name defineColumn citation in all tables (see below for the uniqueness requirement)

If there is no lock function name specified in the defineTable citation:
  The Name column values do not need to be unique
    There must be no:
      RowStatus column defined by a defineColumn citation
      Name2Index column defined by a defineIndex citation
      An AddARow function will be generated
Else (lock function name is given in the defineTable citation)
  There must be a RowStatus defineColumn citation
    The RowStatus citatio must be the last column specified (this amplifies its atomicity to the user)
    An AddARowUnderLock function will be generated
    A CompressTableUnderLock function will be generated (if RowStatus is None the row is deleted from the table)
  There may be a defineIndex citation
    The Name column values must be unique (checked in AddARowUnderLock / duplicates cause program halt)
    The Name2Index dictionary will be managed by the AddARowUnderLock and CompressTableUnderLock functions

defineUnary - Create a list with one element (element [0] will be None unless specified otherwise)

defineList & defineDict - Create the (un-initialized) variables / types as global shared
```
