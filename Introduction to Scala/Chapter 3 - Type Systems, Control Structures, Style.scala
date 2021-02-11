/*****************Scala's static type system**********************************/

/**************Make decisions with if and else*******************************/

/*if and printing*/

// Point value of a player's hand
val hand = sevenClubs + kingDiamonds + fourSpades

// Congratulate the player if they have reached 21
if (hand == 21) {
println("Twenty-One!")
}

/*****************************************************************************/

/*if expressions result in a value*/

// Point value of a player's hand
val hand = sevenClubs + kingDiamonds + threeSpades

// Inform a player where their current hand stands
val informPlayer: String = {
  if (hand > 21)
    "Bust! :("
  else if (hand == 21)
    "Twenty-One! :)"
  else
    "Hit or stay?"
}

// Print the message
print(informPlayer)

/*****************************************************************************/

/*if and else inside of a function*/

// Find the number of points that will cause a bust
def pointsToBust(hand: Int): Int = {
  // If the hand is a bust, 0 points remain
  if (bust(hand))
    0
  // Otherwise, calculate the difference between 21 and the current hand
  else
    21 - hand
}

// Test pointsToBust with 10♠ and 5♣
val myHandPointsToBust = pointsToBust(tenSpades + fiveClubs)
println(myHandPointsToBust)

/*****************************************************************************/

/**************************while and the imperative style*********************/

/*A simple while loop*/

// Define counter variable
var i = 0

// Define the number of loop iterations
val numRepetitions = 3

// Loop to print a message for winner of the round
while (i < numRepetitions) {
  if (i < 2)
    println("winner")
  else
    println("chicken dinner")
  // Increment the counter variable

}