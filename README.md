# Gettr Post Filter 
Purpose of this script is to filter posts and comments that contain sensitive words. 

## Prerequisite
**Python > 3.8** (all 3.x should work)  
Necessary package: **requests**

## Project Structure

**Data Source ==> Script ==> Output**  

### Data source:  
It contains two txt files: **sensitive_words.txt** and **target_user.txt**.   
1. sensitive_words.txt: contains all the words to filter.
    + Format: one word one line.
    + Special symbols: "#" will be removed from words since "#" is considered for tag. Others will be saved. 
2. target_user.txt: contains all the users accounts to monitor.
    + Format: one username one line.
    + All usernames are converted to lower cases since the API cannot recognize some account names with upper cases. 
    
3. post_id.txt: contains IDs of all the post and comments that have been filtered. 
   + Format: one ID one line. 
   + No post content is saved here. This file is used to record filtered post and comment IDs. 
   + The first step for this filter program is to load this txt file. 
   
### Script
The main.py file contains all the execution code. 

### Output
The script will generate folders contains users' post with sensitive comments. 
Each folder name is the username. Within the folder, any post containing sensitive comments will be saved here. 

Folder name is the username to be monitored. 
File name is username_postID.txt. 
In the file, each content group has three lines: 
first line is the comment link and it is be pasted to browser; 
second line is the comment in JSON format;
third line is the first violated word in this comment. 

The filtered results should be manually confirmed, since the sensitive words are simply pattern matched. 
Some mismatches could happen. 
For example, a comment says "we need free speech!", 
then this comment will be picked up since this word "speech" contains a violated word "pee".  

