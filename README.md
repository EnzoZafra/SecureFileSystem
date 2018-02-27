Secure File System (SFS)
ECE 422, Winter 2018
Due Date: 11:59pm Thursday, March 18, 2018.

Your goal for this project is to develop a secure file system that allows users to store data on
an untrusted machine. The machine (i.e., external users) should not be able to obtain the user's
plaintext data (i.e., your file system should encrypt the data to provide confidentiality), and the
external users should not be able to corrupt the data either (i.e., your file system should
authenticate the data it gets back from the file server to check the integrity).
Your file system should support multiple users (i.e., internal users), and allow internal users to
share files with one another. For each file, it should be possible to control the set of users who
can read, and who can write, to that file.
Your SFS should meet the following requirements:
1. SFS should allow creating of groups and users like Unix file system.
2. SFS Users (i.e., after authentication) can create, delete, read, write and rename files.
3. The file system should support directories, including home directory, like Unix file system.
4. Internal users should be able to set permissions on files and directories.
5. File names (and directory names) should be treated as confidential as well.
6. External users should not be able to modify files or directories without being detected.
7. External users should not be able to read file content, file names, or directory names.
The final result of this project should be a functional file system implementation that meets the
above requirements. You can implement your prototype in any language you want, such as
Python, Go or C++. You can decide how the file system client and server should be run. One
reasonable design would be to have the file system client provide a minimal shell environment
that allows users to perform the operations described in the above requirements.
Design Requirements
You are to submit the high level architectural view and UML class diagrams for the file system
as well as UML sequence diagrams for the requirements 1 and 3 as the “design document”.
Submission
There are 2 phases to complete your project:
1. You need to host your project on a Gitlab private project and add me (gitlab-id:
hamzeh.khazaei) and the TA Mojtaba Yeganejou (gitlab-id: mojtabayeganejou) as project
members. Your project should include source codes, design documents and a “readme”.
You may not modify or change anything after the deadline.
2. Finally, you must demo your SFS for the TA within one week after the deadline; you will
demo your project in Software Engineering Laboratory, ETLC 5-005. You must deploy
your SFS on an Ubuntu 16.04 VM on your Cybera Cloud Account for demoing. You should
arrange your demo time with the TA (yeganejo@ualberta.ca). Each demo should take no
longer than 20 minutes.
Grading
Design 40%
Correct operations 60%
