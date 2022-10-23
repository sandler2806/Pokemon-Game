<p align = "center"> <img src = "https://user-images.githubusercontent.com/74304423/148090789-2ea77482-cc57-4b7a-8163-1720f4194233.png"> </p>


<h2>Project review </h2>
<p>
In this project, we are trying to "solve" a game that involves catching pokemon. The game is executed on a server running on our local machine.
The goal is to finish the game with the highest number of points possible, we can gain points from catching pokeomns. </p>
 
 <h3> The game </h3>
 
 <strong>Game map:</strong> 15 different levels, each has a map based on a directed weighted graph. 
 </br>

<strong> Pokemon's:</strong> randomly appear on the edges with varying values, each one has a 'type' attribute - with positive or negative value signify if the pokemon is on upward or downward edge.

<strong>Agents </strong>: the ones catching the pokemon's, each level has a different maximum number of agents, and we should dispatch them ourselves. Each has a speed that increases after they catch enough pokemon.

<h3> Restrictions</h3>
Beyond the obvious need to write a good and efficient algorithm, we cant access the server frequently, and have to keep the average number of calls - moves below 10 per second
 
 
 <h2>Design </h2>
 Our design conform to the staple OOP principles and to the MVC design pattern. <br>
 
 To match the <strong>MVC</strong> design pattern we divided our code the 3 main parts: </br>
 
 <strong>main: </strong> provide the infrastructure to communicate with the server and use it's data to issue commands for the app.
 
 <strong>GUI: </strong> serve as the "view" part, helps to user to follow the progress of the game, rely on main for communication with server and dosent perform any logical or algorithmic operations.
 
 <strong> Config: </strong> Contain and update the data we get from the server, agents locations, pokemon locations etc...
<p>
  
 </p>
 
<h2>Graphical interface </h2>
<p>
  See our Wiki page for a complete explantion of the GUI
 </p>
 
 
 
<h2>How to run the project</h2>
<p>
  To run the project you have first to download or clone the code. Then you should run the server with the following command: <strong> java -jar Ex4_Server_v0.0.jar 1 </strong>  (1 is the number of the level, choose one between 0 to 15) <br>
 After the server is running, open the main.py module in your favorite IDE and execute the main function, the game should start running and the GUI will start showing it
 </p>
 
 <h2>The algorithm </h2>
<p>
 In the begining of the game, we transform the game map to a DiGraph object (our implementation of Directed graph), with this we are able to run various graph operations and algorithms to help us make decisions. <br>
 When a new pokemon appear, we will try to pick the best agent to handle it in order to maximise our results. <br>
 The choosing process is based on several parameters.
 first, we calculate the time it takes for each agent to complete its current missions, then again for each agent we calculate how much time will it take for it to catch all its assigned pokemon's plus the new one, while taking into account all the possible catching orders.<br>
 To detrmine the travling time, we use <strong>Dijkstra's algorithm </strong> and a modified version of TSP algorithm. <br>
 After we did this calculation for every agent, we choose the agent with the least overhead generated from having to catch the new pokemon
 
 </p>
 
 
 
<h3>UML diagram </h3>

![bf84fb4c-3b5b-4621-98cc-fae07084393e](https://user-images.githubusercontent.com/91602396/148219099-62508ed1-af79-414d-b4f2-1176160617e2.jpg)


 
<h3>Reuslts</h3>
<p>
  We "played" every level of the game and wrote down the results in a single table. <br>
 notice that we never crossed the premmited number of moves per second (game 0 is 30 seconds long and all the rest are 60 seconds)
 
 <p align = "center"> <img src = "https://github.com/noamv2/PokemonGame/blob/main/pics/ccb811ba-0742-4970-a3dd-6914dc8bb59c.jpg"> </p>

 </p>
#� �P�o�k�e�m�o�n�-�G�a�m�e�
�
�
