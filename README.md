# Gettr Post Filter 
Purpose of this script is to filter posts and comments that contain sensitive words. 

## Prerequisite
**Python > 3.8** (all 3.x should work)  
Necessary package: **requests**

## Project Structure

**Data Source ==> Script ==> Output**  

### Data source:  
It contains three txt files: **sensitive_words.txt**, **target_user.txt**, and **post_id.txt**.   
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
+ The filter_with_DB.py runs with a database required.

+ The filter_wo_DB.py runs without a database. 
   + It records IDs of filtered posts and comments in post_id.txt to avoid 
duplicate crawling.
   + Workflow:
     1. Synchronize history records and avoid duplicate downloading
      + load files in ./output/, if existing files, then get post and comment IDs
      + load post_id.txt, get IDs of posts and comments in history
      + synchronize ID record from output folder and post_id.txt, if missing IDs in output folder, filter them from gettr; 
        if missing IDs in post_id.txt, add them in post_id.txt.
     2. Load sensitive words
     3. Load user IDs and record posts and comments that contain sensitive words. 

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

