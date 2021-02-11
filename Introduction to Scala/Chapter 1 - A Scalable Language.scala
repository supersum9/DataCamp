/***************************A scalable language*******************************/

/***Define immutable variables (val)****/

// Define immutable variables for clubs 2♣ through 4♣
val twoClubs: Int = 2
val threeClubs: Int = 3
val fourClubs: Int = 4

/*****************************************************************************/

/*****Don't try to change me***/

// Define immutable variables for player names
val playerA: String = "Alex"
val playerB: String = "Chen"
val playerC: String = "Marta"

// Change playerC from Marta to Umberto
playerC = "Umberto"

/****************Mutable variables (var) and type inference*******************/

/*Define mutable variables (var)*/

// Define mutable variables for all aces
var aceClubs: Int = 1
var aceDiamonds: Int = 1
var aceHearts:  Int = 1
var aceSpades: Int = 1

/*****************************************************************************/

/*You can change me*/

// Create a mutable variable for Alex as player A
var playerA: String = "Alex"

// Change the point value of A♦ from 1 to 11
aceDiamonds = 11

// Calculate hand value for J♣ and A♦
println(jackClubs + aceDiamonds)

/*****************************************************************************/