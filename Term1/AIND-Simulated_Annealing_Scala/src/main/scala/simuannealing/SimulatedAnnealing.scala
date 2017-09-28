package simuannealing

import problem.{Problem, TravelingSalesman}

import scala.annotation.tailrec
import scala.util.Random

/**
  * Created by info on 19.06.2017.
  */
class simulatedAnnealing(alpha: Double, temp: Double) {

  def schedule(time: Int) = math.pow(alpha, time) * temp

  def perform[T](current: Problem[T]): Problem[T] = {
    @tailrec
    def f(p: Problem[T], t: Int): Problem[T] = {
      val T = schedule(t)
      if (T < -1e10) return p
      val rnd = new Random
      val successors = p.successors()
      val next = successors(rnd.nextInt(successors.length))
      val deltaE = next.getValue() - p.getValue()
      if (deltaE > 0) {
        f(next, t + 1)
      } else {
        val prob = rnd.nextDouble()
        if (math.exp(deltaE / T) < prob) {
          f(next, t + 1)
        } else {
          f(p, t + 1)
        }
      }
    }
    f(current, 0)
  }
}

