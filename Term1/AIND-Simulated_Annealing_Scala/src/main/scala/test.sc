import simuannealing.simulatedAnnealing
import problem.{Cities, Coordinates, TravelingSalesman}
val cities = List(Cities("DS", Coordinates(11, 1)), Cities("SF", Coordinates(0, 0)),
  Cities("PHX", Coordinates(2, -3)), Cities("LA", Coordinates(0, -4)))

import org.json4s._
import org.json4s.native.JsonMethods._
import org.json4s.DefaultFormats
implicit val formats = DefaultFormats


var json: String = ""
for (line <- io.Source.fromFile("D:/Programmierung/AI/term1/SAScala/data/cap.json").getLines) json += line
val data = parse(json)

val capitals = data.extract[List[Cities]].take(30)
val tsp = new TravelingSalesman(capitals, "l1")
tsp.getValue()
tsp.names()
tsp.successors().map(_.names())

val sa = new simulatedAnnealing(alpha = 0.999, temp = 100000)
val solution = sa.perform(tsp)
-1 * solution.getValue()
solution.names().foreach(println(_))
