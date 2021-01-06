# CS50_W Capstone Project (SwapNGameOn)

## Overview

SwapNGameOn is a platform where gamers can swap console games with another.The users just need to list out the games they own, the games they are looking for and send out swap requests to each other. The project also has added functionalities such as search function so that it is easier for users to browse for games, rating system to ensure that the users behave appropriately. The requests and swaps are also given appropriate status for easier tracking of requests sent and received by the users. Lastly, the web application is also optimised for mobile view.

## Features 

### Home page (index.html)
Home page displays all the available games that the user is allowed to swap with. Each game is listed with owner's information such as the games the owner is looking for, the prefered meetup area and also contain a hyperlink to the owner's profile. The games can be filter by name and category as well.

### Profile page (profile.html, profile.js)
Profile page displays the user's information and the games owned by the user.

**If user is the profile user:** Able to Edit information, add and delete games
 * Add Game (addGame.html) : A form with title field, dropdown category selector and a field to add in image url
 * Delete Game : User can click on delete button to delete games they own
 * Edit info: A modal with fields to input requested games and meetup area 

**If user is not the profile user:**</ins> Able to rate the profile user, request for swap on available games

### Make Request page (requestForm.html)
The user can click on 'swap!' button on the game listed to be directed to make swap request page. The page shows information on the game the user wants to swap with and a form to fill up the game the user will be offering in exchange, the meetup place to swap the game, the swap duration and the contact information of the user so that they can make arrangements once the request is accepted. There are various form validations in place such as not allowing the user to key in a past date, the end date must be after the start date and the user must provide an alternative meetup place if he indicates that he cannot meet at the prefered meetup place.

### Requests page (requests.html, requests.js)
This page displays all the requests received or send by the user and the user is able to toggle between them by clicking on the 'received' and 'sent' tabs.
* Sent requests: The requests will be labelled with accepted, declined or processing. The user also has the option to cancel the request if they change their mind.
* Received requests: The user has the option to accept or decline the received requests. If the request is accepted, the games involed in the request will be marked as on swap and the accepted request will appear in the swaps page. If the request is declined, the request will be simply be removed from the received requests.

### Swaps page (swaps.html)
This is where ongoing swaps will be displayed so that the users can keep track of the games that they have to return once the swap duration ends. Once the swap is completed the user can mark the swap as completed and the games involved in the swap will be marked as available and can be used to make new swap requests.

### NavBar (layout.html)
This is the header bar with links for the user to navigate through different pages.

### Login and Register (login.html and register.html)
New users can be registered via register page and login through the login page.

## How to run the application 

```python
python manage.py runserver
```
The database is already prefilled as shown in the demo video. You can register a new user and log into the system.
