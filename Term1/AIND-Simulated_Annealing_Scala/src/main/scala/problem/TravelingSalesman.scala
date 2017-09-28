package problem

import scala.annotation.tailrec

case class Coordinates(x: Double, y: Double)
case class Cities(cityName: String, coords: Coordinates)


abstract class Problem[T](path: List[T], distFunc: String) {
  def copy(): Problem[T]
  def successors(): List[Problem[T]]
  def getValue(): Double
}


/**
  * Created by info on 19.06.2017.
  */
class TravelingSalesman(path: List[Cities], distFunc: String) extends Problem(path, distFunc) {
  /*
  Return a copy of the current board state
   */
  def copy() = new TravelingSalesman(path, distFunc)

  /*
  Return only the city names of the current path list
   */
  def names(): List[String] = path.map(_.cityName)

  /*
  Return the xy coordinates for each city in the path
   */
  def coords(): List[Coordinates] = path.map(_.coords)

  /*
  Get all successors
   */
  def successors(): List[TravelingSalesman] = {
    val succ = for (i <- 0 until path.length) yield {
      if (i == 0) {
        val t = path.tail.dropRight(1)
        List(List(path.reverse.head), t, List(path.head)).flatten
      } else {
        val h = path.dropRight(path.length - i + 1)
        val t = path.drop(i + 1)
        if (h.length > 0 && t.length > 0) {
          List(h, List(path(i)), List(path(i -1)), t).flatten
        } else if (h.length > 0 && t.length == 0) {
          List(h, List(path(i)), List(path(i -1))).flatten
        } else if (h.length == 0 && t.length > 0) {
          List(h, List(path(i)), List(path(i -1)), t).flatten
        }
      }
    }
    succ.map{case c: List[Cities] => new TravelingSalesman(c, distFunc)}.toList
  }

  def getValue(): Double = {
    // add first city at the end of the path; not optimal
    val closedPath = path :+ path.head
    @tailrec
    def f(l: List[Cities], d: Double): Double = {
      if (l.length > 1) {
        f(l.tail, d + distance(l(0), l(1)))
      } else {
        d
      }
    }
    -1.0 * f(closedPath, 0.0)
  }

  /*
    Initialize distance function
 */
  def distance = get_distance(distFunc)

  private def get_distance(s: String): (Cities, Cities) => Double = s match {
    case s if s == "l1" => get_l1_distance
    case s if s == "l2" => get_l2_distance
  }

  private def get_l2_distance(city1: Cities, city2: Cities): Double = {
    val coord1 = city1.coords
    val coord2 = city2.coords
    return math.sqrt(math.pow(coord1.x - coord2.x, 2) + math.pow(coord1.y - coord2.y, 2))
  }

  private def get_l1_distance(city1: Cities, city2: Cities): Double = {
    val coord1 = city1.coords
    val coord2 = city2.coords
    return math.abs(coord1.x - coord2.x) + math.abs(coord1.y - coord2.y)
  }
}
