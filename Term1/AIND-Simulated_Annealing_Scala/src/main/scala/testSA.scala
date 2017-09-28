package udacity

import org.json4s._
import org.json4s.native.JsonMethods._
import org.json4s.DefaultFormats
import simuannealing.simulatedAnnealing
import problem.{Cities, TravelingSalesman}

object testSA {
  def main(args: Array[String]) {
    implicit val formats = DefaultFormats
    var json: String = ""
    for (line <- io.Source.fromFile("data/cap.json").getLines) json += line
    val data = parse(json)

    val capitals = data.extract[List[Cities]].take(30)
    val tsp = new TravelingSalesman(capitals, "l1")
    tsp.getValue()
    tsp.names()
    tsp.successors().map(_.names())

    val sa = new simulatedAnnealing(alpha = 0.999, temp = 100000)
    val solution = sa.perform(tsp)
    println("Optimal value: " + -1 * solution.getValue())
    solution.names().foreach(println(_))
  }
}
