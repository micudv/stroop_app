# stroop_app - a Python project for Stroop Test using tkinter

Stroop is a psychological test created to evaluate attention span, cognitive flexibility and inhibition to automatic response and it is used to orientate a diagnosis of brain damage, stress, senile dementia or drug addiction.

The test consists of different name colours as 'Yellow', 'Red', 'Green', 'Blue', which are printed randomly on those colours and the person is asked to read the word presented. In the case of this application, the user is provided with indications assigning keys for each colour and must press the one that corresponds with the word displayed on screen. For the result, it is considered the amount of correct answers and the time elapsed. 

For this app, the user has access to three screens: the Initial, where he must register his personal information; the Test, to perform the evaluation; and finally the Results where it presents the actual score and the register from the three best results.

![image](https://user-images.githubusercontent.com/78883207/138729617-81a66b0c-9cea-4e09-9550-93db93278f7e.png)

*Example of Test screen*

## Specs

On the realization of the application, several things were considered:
- tkinter was chosen as the GIU.
- For Database, it was implemented SQlite3.
- The code was wrote respecting PEP8.
- It was made with MVC pattern, with three separate modules.

## CRUD
For *Create*, the app presents an Initial screen in which the user must register his Name, Age and Email. This data will be later saved in the database, precisely on Users table, using the name as a primary key.

![image](https://user-images.githubusercontent.com/78883207/138755837-82f4e49b-c901-4de1-a38a-defaccdaeac9.png)

*Initial screen with data entry and indications for the test*

At the same time, each entry uses regex to corroborate that the information entered is correct, as well as exceptions in case that it is not valid.

![image](https://user-images.githubusercontent.com/78883207/138757520-8512821b-0209-4c65-9a15-f6182897dd69.png)

*Regex and exceptions in controller.py module to validate data on inputs Name, Age and Email.*



For *Delete*, on Results screen we can find an 'Erase your score' button that allows to eliminate the last result of the test on tables Users and Test of the database.

![image](https://user-images.githubusercontent.com/78883207/138760337-1c03b623-37a7-42f6-9838-c5de1173ae7c.png)

*Results screen when 'Erase your score' button is pressed*

What comes for *Update*, each time a user performs a new test his score is actualized. And finally, *Read* is represented with the best three results listed on the last screen.

![image](https://user-images.githubusercontent.com/78883207/138762460-72dffd2c-be80-4c8d-b206-07541fb2b5ff.png)




